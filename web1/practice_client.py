import socket, ssl

# socket.AF_INET代表的是ipv4协议, socket.SOCK_STREAM代表的是tcp协议
# 1. socket.socket()用来解析http
# s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# 2. ssl是专门用来处理https的模块, 通过warp_socket生成一个SSLsocket对象
s = ssl.wrap_socket(socket.socket())

host = 'movie.douban.com'
port = 443

# 用connect连接上主机,参数是个tuple
s.connect((host, port))

ip, port = s.getsockname()
print('本机ip和port {} {}'.format(ip, port))

http_request = 'GET / HTTP/1.1\r\nhost:{}\r\n\r\n'.format(host)
request = http_request.encode('utf-8')
print('请求', request)
# 发送请求需要用bytes格式发送
s.send(request)

# 接收服务器响应数据, 1023表示的是接受1023个字节
response = s.recv(1023)

print('响应数据', response)
print('响应的str格式:', response.decode('utf-8'))