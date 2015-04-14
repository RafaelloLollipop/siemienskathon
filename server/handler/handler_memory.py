from multiprocessing.managers import BaseManager 
shared_client_list = []
class ListManager(BaseManager): pass 
ListManager.register('get_client_list', callable=lambda:shared_client_list)
m = ListManager(address=('', 50000), authkey=123)
s = m.get_server() 
s.serve_forever() 
