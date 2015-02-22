import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)
mc.set("some_key", "Some value")
value = mc.get("some_key")
mc.set("another_key", 3)
mc.delete("another_key")
value = mc.get("another_key")
mc.set("key", "1")   # note that the key used for incr/decr must be a string.
mc.incr("key")
mc.decr("key")

print(value)

mc.set_multi({ "USA_98105": "raining",
                     "USA_94105": "foggy",
                     "USA_94043": "sunny" },
			)
			
class Server(object):
  def __init__(self):
    self.rooms = []

  def run(self):
    print("R")

			