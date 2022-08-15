import os
import json

f=open("1.txt","w")
f.write("{\"a\":1}")
f.close()


f=open("1.txt","r")
s=f.read()
f.close()
print(s)
b=json.loads(s)
print(b)

