import random
from multiprocessing.managers import BaseManager
class ListManager(BaseManager): pass
ListManager.register('get_list')
m = ListManager(address=('localhost', 50000), authkey=123)
m.connect()
l = m.get_list()
l.append(random.random())