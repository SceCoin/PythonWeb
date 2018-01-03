import json
from utils import log


def save(data, path):
    """
    本函数是把一个dict或者list写入文件
    :param data: dict or list
    :param path: 文件保存路径
    """
    # ensure_ascii=False 用户保存中文
    # indent用于缩进
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('models--save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个json文件中载入数据并转化为dict或者list
    :param path:  文件路径
    :return: dict or list
    """
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('models--load', s)
        return json.loads(s)


class Model(object):
    # @classmethod说明是一个类方法
    # 类方法的调用方式是 类名.类方法()

    @classmethod
    def db_path(cls):
        # classmethod有一个参数是class
        # 所有可以得到class的名字
        classname = cls.__name__
        path = 'db/{}.txt'.format(classname)
        return path

    @classmethod
    def new(cls, form):
        # 下面一句相当于 User(form) 或者 Msg(form)
        m = cls(form)
        return m

    @classmethod
    def all(cls):
        """
        得到一个类的所有存储的实例
        """
        path = cls.db_path()
        models = load(path)
        ms = [cls.new(m) for m in models]
        return ms
        # return models

    # 作业 3.5
    #
    # 对每一个 Model 添加一个 id 属性, 初始值为 None
    # 每一个 Model 的 id 是独一无二并且增长的数字
    # save 的时候, 如果 id 属性为 None 就给它赋值并添加/保存
    # 如果 id 属性不为 None 就在所有数据中修改并保存
    #
    # 用法例子如下
    """
    # 假设有这个用户
    u = User.find_by(username='gua')
    u.password = 'pwd'
    u.save()
    # 直接保存


    form = dict(
    	username= 'newgua',
        password= '123',
    )
    u = User(form)
    u.save()
    # 因为这是一个新用户, 并没有 id
    # 所以 save 的时候被赋予了一个 id
    """
    def save(self):
        """
        save函数用于把一个model的实例保存到文件中
        """
        models = self.all()
        log('models', models)
        models.append(self)
        # __dict__是包含了对象所有属性和值的字典
        l = [m.__dict__ for m in models]
        for i in range(len(l)):
            l[i]['id'] = i
        path = self.db_path()
        save(l, path)

    # 作业 3.3
    #
    # 为 Model 添加一个类方法 find_by
    # 用法和例子如下
    """
    u = User.find_by(username='gua')

    上面这句可以返回一个 username 属性为 'gua' 的 User 实例
    如果有多条这样的数据, 返回第一个
    如果没这样的数据, 返回 None

    注意, 这里参数的名字是可以变化的, 所以应该使用 **kwargs 功能
    """
    def find_by(self, **kwargs):
        path = self.db_path()
        models = load(path)
        for up in models:
            if dict(up, **kwargs) == up:
                return up
        return None

    # 作业 3.4
    #
    # 为 Model 添加一个类方法 find_all
    # 用法和例子如下
    """
    us = User.find_all(password='123')
    上面这句可以以 list 的形式返回所有 password 属性为 '123' 的 User 实例
    如果没这样的数据, 返回 []

    注意, 这里参数的名字是可以变化的, 所以应该使用 **kwargs 功能
    """
    def find_all(self, **kwargs):
        path = self.db_path()
        models = load(path)
        findall = []
        for up in models:
            if dict(up, **kwargs) == up:
                findall.append(up)
        return findall

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)