from utils import log
from models.message import Message
from models.user import User

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

def route_login(request):
    header = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n"
    if request.method == 'POST':
        form = request.form()
        log('routes--form的信息', form)
        u = User.new(form)
        if u.validate_login():
            result = '登录成功'
        else:
            result = '用户名密码错误'
    else:
        result = ''
    body = templates('login.html')
    body = body.replace('{{result}}', result)
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


route_dict = {
    '/': route_index,
    '/login': route_login,
    '/register': route_register,
    '/messages': route_message,
}
