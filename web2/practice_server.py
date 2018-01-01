import socket


def log(*args, **kwargs):
    print('log', *args, **kwargs)


def route_index():
    """
    主页处理函数, 返回主页的响应
    :return: 
    """
    header = 'HTTP/1.x 200 OK\r\nContent-Type: text/html\r\n'
    body = '<h1>Hello World</h1><img src="/doge.gif"/>'
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_image():
    """
    图片处理函数,读取图片并生成响应返回
    :return: 
    """
    with open('doge.gif', 'rb') as f:
        header = b'HTTP/1.x 200 OK\r\nContent-Type: image/gif\r\n\r\n'
        img = header + f.read()
        return img


def error(code=404):
    """
    根据错误code返回不同的错误响应
    :return: 
    """
    e = {
        404: b'HTTP/1.x 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>',
    }
    return e.get(code, b'')


def response_for_path(path):
    """
    根据path调用响应的处理函数
    没有处理的返回404
    :param path: 
    :return: 
    """
    r = {
        '/': route_index,
        '/doge.gif': route_image,
    }

    response = r.get(path, error)
    return response()


def run(host='', port=3000):
    """
    启动服务器
    :param host: 
    :param port: 
    :return: 
    """

    # 1.初始化socket, 使用with可以保证程序中断时正确关闭socket
    with socket.socket() as s:
        # 2.使用bind绑定host,port
        s.bind((host, port))

        # 3.开始无限循环处理请求
        while True:

            # 4.开始监听,通过accept获得客户端的连接和ip地址两个值
            s.listen(5)
            connection, address = s.accept()
            # 5.通过connection.recv()获得客户端收的到的请求
            request = connection.recv(1024)
            request = request.decode('utf-8')
            log('ip and request, {}\n{}'.format(address, request))

            # 因为chrome会发送空请求导致split得到空List,所以用try防止崩溃
            try:
                # 6. 获取path, 并获得响应的内容
                path = request.split()[1]
                response = response_for_path(path)
                # 7. 把响应发送给客户端
                connection.sendall(response)
            except Exception as e:
                log('error', e)

            # 8.关闭连接
            connection.close()


if __name__ == '__main__':
    # 生成配置并且运行程序
    config = dict(
        host='',
        port=3000,
    )
    # 如果不了解 **kwargs 的用法, 群里问或者看书/搜索 关键字参数
    run(**config)
