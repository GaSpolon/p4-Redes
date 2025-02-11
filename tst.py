from re import U


a = b''
b = b'aiojsioah\x00'
for i in b:
    print(i)
    # print(bytes(i))
    a += i.to_bytes(1,byteorder='big')
print(a)