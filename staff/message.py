from multiprocessing.managers import BaseManager 
shared_list = [] 
class ListManager(BaseManager): pass 
ListManager.register('get_list', callable=lambda:shared_list) 
m = ListManager(address=('', 50000), authkey=123)
s = m.get_server() 
s.serve_forever() 
