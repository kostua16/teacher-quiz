# coding: utf8
__author__ = 'kole0114'


class WorkFlow(object):
    def __init__(self, todo=[], completed=[], current=None,params=dict()):
        self.todo_items = todo
        self.completed_items = completed
        self.current = current
        self.params=params

    def set_param(self,name,val):
        self.params[name]=val
    def has_param(self,name):
        return name in self.params.keys()

    def get_param(self,name):
        if self.has_param(name):
            return self.params[name]
        return None

    def start(self):
        self.get_task()

    def add_task_to_end(self, name):
        print "len before:%s[%s]" % (len(self.todo_items),self.todo_items)
        self.todo_items.append(name)
        print "len after:%s[%s]" % (len(self.todo_items),self.todo_items)

    def add_task_to_start(self, name):
        print "len before:%s[%s]" % (len(self.todo_items),self.todo_items)
        self.todo_items.insert(-1, name)
        print "len after:%s[%s]" % (len(self.todo_items),self.todo_items)

    def has_task(self,name):
        return name in self.todo_items or name in self.completed_items

    def get_task(self):
        if self.current == None:
            try:
                task = self.todo_items.pop(0)
                self.current = task
            except IndexError:
                return None
        return self.current

    def change_task(self,name):
        if not name in self.todo_items:
            print('change_task[new]:%s' % name)
            self.add_task_to_start(name)
            self.current=name
        else:
            print('change_task[exists]:%s' % name)
            self.current=name

    def complete_task(self):
        if self.current == None:
            print('complete:current is none')
            self.start()
            return False
        else:
            self.completed_items.append(self.current)
            print('complete:add')
            self.current = None
            self.start()
            return True
