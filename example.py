import tarantool
server = tarantool.connect("localhost", 33013)

demo = server.space(0)

print(demo.select('AAAA'))
