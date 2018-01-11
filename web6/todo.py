from models import Model
import time


# 继承自 Model 的 Todo 类
class Todo(Model):
    def __init__(self, form):
        self.id = form.get('id', None)
        self.title = form.get('title', '')
        self.user_id = int(form.get('user_id', -1))
        # 还应该增加 时间 等数据

        # 5.2, 给Todo 类增加一个 created_time 属性
        # 它保存的是创建数据的 unix 时间, int 类型
        # 简单说来就是 int(time.time())
        # self.created_time = time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(int(time.time())))
        self.created_time = form.get('created_time', 0)

        # 5.3, 给Todo 类增加一个 updated_time 属性
        # 它保存的是修改数据的时间
        self.updated_time = form.get('updated_time', 0)

