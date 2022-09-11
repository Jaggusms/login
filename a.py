i=input()
print(type(i))
try:
    i=int(i)
except :
    pass
finally:
    print(type(i))