#!/usr/bin/env Python
# coding=utf-8

import socket
import  ssl

def parsed_url(url):
    """
    解析url
    :return: protocol, host, port, path 
    """
    # 检查protocol
    protocol = 'http'
    if url[:7] == 'http://':
        u = url.split('://')[1]
    elif url[:8] == 'https://':
        protocol = 'https'
        u = url.split('://')[1]
    else:
        u = url

    # 检查默认path
    i = u.find('/')
    if i == -1:
        host = u
        path = '/'
    else:
        host = u[:i]
        path = u[i:]

    # 检查port
    port_dict = {
        'http': 80,
        'https': 443,
    }
    # 默认端口
    port = port_dict[protocol]
    if ':' in host:
        h = host.split(':')
        host = h[0]
        port = int(h[1])

    return protocol, host, port, path


def socket_by_protocol(protocol):
    """
    根据协议返回一个socket实例
    :return: s
    """
    if protocol == 'http':
        s = socket.socket()
    else:
        s = ssl.wrap_socket(socket.socket())

    return s

def response_by_socket(s):
    """
    参数是一个socket实例
    返回这个socket读取的所有数据
    :param s: socket
    :return: response
    """
    response = b''
    buffer_size = 1024
    while True:
        r = s.recv(buffer_size)
        if len(r) == 0:
            break
        response += r

    return response

def parsed_response(r):
    """
    用于处理返回得到的response
    状态码是int
    headers是dict
    body是str
    :param r: response
    :return: status_code, headers, body
    """

    # 1.通过\r\n\r\n分解header和body
    header, body = r.split('\r\n\r\n',1)
    # 2.通过截取第一个\r\n分解响应首行和headers
    h = header.split('\r\n')
    # 3.获得状态码,响应行格式类似HTTP/1.1 200 OK
    status_code = h[0].split()[1]
    status_code = int(status_code)

    # 4.构造headers字典,添加键值对
    headers = {}
    for line in h[1:]:
        # 键值对中间有一个空格一定要记得
        k, v = line.split(': ')
        headers[k] = v

    return status_code, headers, body


def get(url):

    # 1.解析url, 得出protocol, host, port, path
    protocol, host, port, path = parsed_url(url)

    # 2.需要判定Protocol属于http还是https
    s = socket_by_protocol(protocol)

    # 3.构造socket对象连接host和port
    s.connect((host, port))

    # 4.连接后将path作为request的一部分send给服务器
    request = 'GET {} HTTP/1.1\r\nhost:{}\r\nConnection: close\r\n\r\n'.format(path, host)
    encoding = 'utf-8'
    s.send(request.encode(encoding))

    # 5.服务器返回响应
    response = response_by_socket(s)
    r = response.decode(encoding)

    # 6.处理解析后获得返回的status_code, headers, body
    status_code, headers, body = parsed_response(r)
    # 判断如果出现301则跳转转移后的网址
    if status_code == 301:
        url = headers['Location']
        return get(url)
    return status_code, headers, body

def main():

    url = "http://movie.douban.com/top250"
    status_code, headers, body = get(url)
    print(status_code, headers, body)


def test_parsed_url():
    """
    测试parsed_url是否出错
    :return: 
    """
    http = 'http'
    https = 'https'
    host = 'g.cn'
    path= '/'
    test_items = [
        ('http://g.cn', (http, host, 80, path)),
        ('http://g.cn/', (http, host, 80, path)),
        ('http://g.cn:90', (http, host, 90, path)),
        ('http://g.cn:90/', (http, host, 90, path)),
        #
        ('https://g.cn', (https, host, 443, path)),
        ('https://g.cn:233/', (https, host, 233, path)),
    ]

    for t in test_items:
        url, expected = t
        u = parsed_url(url)
        e = "parsed_url ERROR, ({}) ({}) ({})".format(url, u, expected)
        assert u == expected, e

def test_get():
    """
    测试是否能正确处理http和https
    :return: 
    """
    urls = [
        'http://movie.douban.com/top250',
        'https://movie.douban.com/top250',
    ]

    for u in urls:
        get(u)

def test_parsed_response():
    """
    测试能否正确响应解析
    :return: 
    """
    response = 'HTTP/1.1 301 Moved Permanently\r\n' \
        'Content-Type: text/html\r\n' \
        'Location: https://movie.douban.com/top250\r\n' \
        'Content-Length: 178\r\n\r\n' \
        'test body'
    status_code, header, body = parsed_response(response)
    assert status_code == 301
    assert len(list(header.keys())) == 3
    assert body == 'test body'

def test():
    """
    用于测试的主函数
    :return: none
    """
    test_parsed_url()
    test_get()
    test_parsed_response()

if __name__ == '__main__':
    test()
    main()