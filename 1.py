import redis

# class Redis(object):
#     def __init__(self, host='localhost', port=6379, db=1, password=None, socket_timeout=None):
#         return 
capitals = {}
capitals["Bahamas"] = "Nassau"
capitals["Croatia"] = "Zagreb"
POOL = redis.ConnectionPool(host='10.0.0.1', port=6379, db=0)
r = redis.Redis()
r.mset(capitals)

print(r.get("Bahamas"))

