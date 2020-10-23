class Redis(object):
    def __init__(self, host='localhost', port=6379,
                 db=1, password=None, socket_timeout=None)