with open('test', 'r') as f:
    l = f.readlines()
    f.close()

ll = l[0].split('title="')

lt = []
for x in ll:
    buffer = ''
    cc = 0
    while x[cc] != '"':
        buffer += x[cc]
        cc += 1
    lt.append(buffer)

lt.remove('<div class=')
[print(x) for x in lt]
print(len(lt))
