from utils import log
from utils import template
from utils import redirect
from utils import http_response

from todo import Todo

def index(request):
    todo_list = Todo.all()
    body = template('simple_todo_index.html', todos=todo_list)
    return http_response(body)

def add(request):
    form = request.form()
    t = Todo.new(form)
    t.save()
    return redirect('/jinja/index')

route_dict = {
    '/jinja/index': index,
    '/jinja/add': add,
}