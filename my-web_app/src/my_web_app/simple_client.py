from http import client


h1 = client.HTTPConnection('localhost', 8001)
h1.request("GET", "/")

res = h1.getresponse()
print(res.status, res.reason)

data = res.read()
print(data)