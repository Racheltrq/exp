import string

f = open("ciphertext.txt", "r")
str1 = f.read()
lst = []
for i in range(0, len(str1), 2):
    if i % 2 == 0:
        lst.append(str1[i:i+2])
print(lst)

ind = 0

while ind < 256:
    res = ""
    for i in lst:
        res += chr(int(i, 16) ^ ind)
    print(res)
    ind += 1