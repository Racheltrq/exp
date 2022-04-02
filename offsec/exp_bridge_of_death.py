'''
def func2(a1, a2, a3):
    v5 = int(a3-a2) / 2 + a2
    if v5 > int(a1):
        return v5 + int(func2(a1, a2, int(v5-1)))
    if v5 >= int(a1):
        return v5
    return v5 + int(func2(a1, int(v5+1), a3))

print(func2(3, 0, 20))
'''
'''
dest = int(str(6557), 16) + int("1e68", 16) + int("1a15", 16) + \
        int("1fca", 16) + int("1a51", 16) + int(str(956), 16) + \
        int("167a", 16) + int("36d", 16) + 7
'''
dest = int(str(6557), 16) + int("1e68", 16) + int("1a15", 16) + \
        int("1fca", 16) + int("1a51", 16) + int(str(956), 16) + 6

print(dest, hex(dest))
print(dest // 256, dest % 256)
#My name is Sir Lancelot of Camelot.
#3 20
#157 215
#101 88
#251 52
#17 176
#215 244
#225 75
#131 193
#189 162
#247 198
