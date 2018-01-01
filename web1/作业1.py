# coding: utf-8

import socket

# 1
# 补全函数
def protocol_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表协议的字符串, 'http' 或者 'https'
    '''
    str = url.find('://')
    if str > 0:
        return url.split('://')[0]
    else:
        return None


# 2
# 补全函数
def host_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表主机的字符串, 比如 'g.cn'
    '''
    str = url.find('://')
    if str > 0:
        url2 = url.split('://')[1]
    else:
        url2 = url

    str2 = url2.find('/')
    if str2 == -1:
        host = url2
    else:
        host = url2[:str2]

    return host


# 3
# 补全函数
def port_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表端口的字符串, 比如 '80' 或者 '3000'
    注意, 如上课资料所述, 80 是默认端口
    '''
    host = host_of_url(url)
    str3 = host.find(':')
    if str3 > 0:
        port = host[str3 + 1:]
    else:
        port = 80

    return port


# 4
# 补全函数


def path_of_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'

    返回代表路径的字符串, 比如 '/' 或者 '/search'
    注意, 如上课资料所述, 当没有给出路径的时候, 默认路径是 '/'
    '''
    str = url.find('://')
    if str > 0:
        url2 = url.split('://')[1]
    else:
        url2 = url

    str2 = url2.find('/')
    if str2 == -1:
        path = '/'
    else:
        path = url2[str2:]

    return path


# 4
# 补全函数
def parsed_url(url):
    '''
    url 是字符串, 可能的值如下
    'g.cn'
    'g.cn/'
    'g.cn:3000'
    'g.cn:3000/search'
    'http://g.cn'
    'https://g.cn'
    'http://g.cn/'
    返回一个 tuple, 内容如下 (protocol, host, port, path)
    '''
    # proto = protocol_of_url(url)
    # host = host_of_url(url)
    # port = port_of_url(url)
    # path = path_of_url(url)
    # tuple_url = (proto, host, port, path)
    # return tuple_url

    # 判断协议
    str = url.find('://')
    if str > 0:
        proto = url.split('://')[0]
        url2 = url.split('://')[1]
    else:
        proto = 'None'
        url2 = url

    # 判断主机名和路径
    str2 = url2.find('/')
    if str2 == -1:
        host = url2
        path = '/'
    else:
        host = url2[:str2]
        path = url2[str2:]

    # 判断端口
    str3 = host.find(':')
    if str3 > 0:
        port = host[:str3 + 1]
    else:
        port = 80

    tuple_url = (proto, host, port, path)
    return tuple_url


# 5
# 把向服务器发送 HTTP 请求并且获得数据这个过程封装成函数
# 定义如下
def get(url):
    '''
    本函数使用上课代码 client.py 中的方式使用 socket 连接服务器
    获取服务器返回的数据并返回
    注意, 返回的数据类型为 bytes
    '''
    s = socket.socket()

    # 获取主机和端口
    host = host_of_url(url)
    port = port_of_url(url)

    # 连接上主机
    s.connect((host, port))

    ip, port = s.getsockname()
    print('本机的ip, port是 {} {}'.format(ip, port))

    http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)

    request = http_request.encode('utf-8')
    print('请求 ', request)
    s.send(request)

    response = s.recv(1000)

    print('响应', response, '/n')

    print('响应的 str 格式', response.decode('utf-8'))


# 使用
def main():
    url = 'http://movie.douban.com/top250'
    # print(parsed_url(url))
    r = get(url)
    print(r)


if __name__ == '__main__':
    main()
