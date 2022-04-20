a = "656769670000000034427b6d5f433153616c5f43000000004175476e525f45670000000078305f4553414c4700007d53"

ind = 0
res = []
while ind + 1 < len(a):
    res.append(chr(int(a[ind:ind+2], 16)))
    ind += 2
res_new = []
for i in range(len(res)):
    if i % 4 == 0:
        sub_list = res[i:i+4]
        sub_list.reverse()
        res_new.extend(sub_list)

lst = []
for i in range(34):
    idx = i
    if (i >= 4 and i <= 15):
        idx += 4
    if (i >= 16 and i <= 23):
        idx += 8
    if (i > 23):
        idx += 12
    #print(res_new[idx])
    lst.append(res_new[idx])

print("".join(lst))
