import socket
import urllib.parse

from utils import log

from routes import route_static
from routes import route_dict


class Request(object):
    def __init__(self):
        self.method = 'GET'
        self.path = ''
        self.query = {}
        self.body = ''
        self.headers = {}
        self.cookies = {}

    def add_cookies(self):
        """
        获得cookie, 返回一个字典的形式
        :return: 
        """
        cookies = self.headers.get('Cookie', '')
        cks = cookies.split('; ')
        log('server-cookie', cks)
        for ck in cks:
            if '=' in ck:
                k, v = ck.split('=')
                self.cookies[k] = v

    def add_headers(self, header):
        head = header.split('\r\n')
        for h in head:
            k, v = h.split(': ', 1)
            self.headers[k] = v
        self.cookie = {}
        self.add_cookies()

    def form(self):
        """
        form 函数用于把 body 解析为一个字典并返回
        body 的格式如下 a=b&c=d&e=1
        """
        body = urllib.parse.unquote(self.body)
        args = body.split('&')
        f = {}
        for arg in args:
            k, v = arg.split('=')
            f[k] = v
        return f


request = Request()


def parsed_path(path):
    """
    分割path和query
    :param path: 
    :return: 
    """
    if path.find('?') == -1:
        return path, {}
    else:
        path, query_str = path.split('?', 1)
        args = query_str.split('&')
        query = {}
        for arg in args:
            k, v = arg.split('=')
            query[k] = v
        return path, query


def error(request, code=404):
    """
    未查找到路由返回404
    :return: 
    """
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_path(path):
    # 先分割paht和query
    path, query = parsed_path(path)
    request.path = path
    request.query = query
    log('server--path and query: ', path, query)
    # 获得了path 后就可以跳转路由
    r = {
        '/static': route_static,
    }
    r.update(route_dict)
    response = r.get(path, error)
    return response(request)


def run(host='', port=2000):

    # 建立host和端口
    with socket.socket() as s:
        s.bind((host, port))

        while True:
            # 开始监听
            s.listen(5)

            # 建立连接, 接受请求
            connection, address = s.accept()

            # 得到请求信息
            res = connection.recv(1000)
            res = res.decode('utf-8')
            log('原始请求\n', res)
            # 分解请求信息
            if len(res.split()) < 2:
                continue
            # 获得path之后在response_for_path中进一步分解path和query
            path = res.split()[1]
            # 获得method
            request.method = res.split()[0]
            # 获得body
            request.body = res.split('\r\n\r\n', 1)[1]
            # 获得headers
            request.add_headers(res.split('\r\n\r\n', 1)[0].split('\r\n', 1)[1])
            # 处理请求
            response = response_for_path(path)
            # 返回响应
            connection.sendall(response)
            # 关闭连接
            connection.close()


if __name__ == '__main__':
    config = dict(
        host='',
        port=2000
    )

    run(**config)