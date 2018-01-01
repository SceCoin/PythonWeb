import socket

# host为空字符串,表示为接受任意ip地址的连接
host = ''
port = 2000

s = socket.socket()
# bind用于绑定服务器
s.bind((host, port))


while True:

    # 1.第一步listen(5)
    s.listen(5)

    # 当有客户端过来连接时, s.accept函数就会有两个返回值,
    # 一个是连接 和 客户端的 ip地址
    # 2.第二步accept()获得两个值
    connection, address = s.accept()

    #recv既可以是接收客户端发来的数据, 在客户端时也是接受服务端发来的数据
    # 3.第三步connection.recv()接受数据
    request = connection.recv(1024)

    print('ip and request, {}\n{}'.format(address, request.decode('utf-8')))

    response = b'<h1>Hello World!</h1><h2>oh my god!</h2>'
    # 4.第四步sendall()发送响应消息
    connection.sendall(response)
    connection.close()



