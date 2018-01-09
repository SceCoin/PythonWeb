from utils import log
from models.message import Message
from models.user import User

import random

session = {}

def random_str():
    """
    生成一个随机字符串
    :return: 
    """
    seed = 'sadlfjwerwerjwf1249723wl234djfwoejiltndslbfnjfdherjtwqlj'
    s = ''
    for i in  range(16):
        random_index = random.randint(0, len(seed) - 2)
        s += seed[random_index]
    return s


def current_user(request):
    session_id = request.cookies.get('user', '')
    username = session.get(session_id, '<游客>')
    return username


def templates(name):
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def route_index(request):
    """
    主页信息
    :param request: 
    :return: 
    """
    header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
    body = templates('index.html')
    response = header + '\r\n' + body
    return response.encode(encoding='utf-8')


def response_with_headers(headers):
    header = "HTTP/1.1 200 OK\r\n"
    header +=  ''.join(['{}: {}\r\n'.format(k,v) for k,v in headers.items()])
    return header


def route_login(request):
    """
    登录页面函数
    :param request: 
    :return: 
    """
    headers = {
        'Content-Type': 'text/html',
    }
    log('routes-login-cookies',request.cookies)
    username = current_user(request)
    if request.method == 'POST':
        form = request.form()
        log('routes--form的信息', form)
        u = User.new(form)
        if u.validate_login():
            session_id = random_str()
            log('session_id:', session_id)
            session[session_id] = u.username
            headers['Set-Cookie'] = 'user={}'.format(session_id)
            result = '登录成功'
        else:
            result = '用户名密码错误'
    else:
        result = ''
    body = templates('login.html')
    body = body.replace('{{result}}', result)
    body = body.replace('{{username}}', username)
    header = response_with_headers(headers)
    response = header + '\r\n' + body
    return response.encode(encoding='utf-8')

def route_register(request):
    """
        POST请求的body里面含有query
        例如: username=1234&password=4321
        所以需要用request.form解析成字典
        然后传入User.new方法中
    """
    header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
    if request.method == 'POST':
        # HTTP BODY 如下
        # username=gw123&password=123
        # 经过 request.form() 函数之后会变成一个字典
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            result = '注册成功<br> <pre>{}</pre>'.format(User.all())
        else:
            result = '已被注册或用户名或者密码长度必须大于2'
    else:
        result = ''
    body = templates('register.html')
    body = body.replace('{{result}}', result)
    response = header + '\r\n' + body
    return response.encode(encoding='utf-8')


message_list = []


def route_message(request):
    """
    主页的处理函数, 返回主页的响应
    """
    log('本次请求的 method', request.method)
    if request.method == 'POST':
        form = request.form()
        msg = Message.new(form)
        log('routes--post', form)
        message_list.append(msg)
        # 应该在这里保存 message_list
    header = 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n'
    # body = '<h1>消息版</h1>'
    body = templates('html_basic.html')
    msgs = '<br>'.join([str(m) for m in message_list])
    body = body.replace('{{messages}}', msgs)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def route_static(request):
    """
    处理静态资源, 读取图片并生成响应返回
    request.query是一个字典
    """
    filename = request.query.get('file', 'doge.gif')
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 0K\r\nContent-Type: image/gif\r\n'
        img = header + b'\r\n' + f.read()
        return img


# 作业 4.2
#
# 添加一个新的路由 /profile (在 routes.py 文件中)
# 如果登录了, 则返回一个页面显示用户的三项资料(id, username, note)
# 如果没登录, 返回 302 为状态码来 重定向到登录界面
# 当返回 302 响应的时候, 必须在 HTTP 头部加一个 Location 字段并且设置值为你想要定向的页面
# 如果不理解这个格式, 请查看之前作业中豆瓣电影页面返回的 301 响应的格式

def route_profile(request):
    """
    登录后的详情页, 显示user,id,note
    :param request: 
    :return: 
    """
    header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
    body = templates('profile.html')
    username = current_user(request)
    log('reoutes-username:', username)
    if username == '<游客>':
        header = "HTTP/1.1 302 Found\r\nLocation: http://localhost:2000/login\r\n"
    else:
        u = User.find_by(username=username)
        userid = u['id']
        usernote = u['note'].replace('+', ' ')
        body = body.replace('{{username}}', username)
        body = body.replace('{{id}}', str(userid))
        body = body.replace('{{note}}', usernote)
    response = header + '\r\n' + body
    return response.encode(encoding='utf-8')

route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
    '/profile': route_profile,
}
