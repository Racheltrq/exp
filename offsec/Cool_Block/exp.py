import socket
import sys
import binascii
from pwn import *


c = "f4a60fdec121df64f0dca2abcb8cb82507b20ee6da804da255714b7b588329b81597c5982b5e1a4c602c672067a4184fc59d7688c6f20ddc81be44bfa31e70fe520c7bd1cbe09f49b6576fa12c87130c9820f52dea79ac5188bdc2617e92dbc0969be076161867756b8e773ef51d6cbfbaae7b3bf0103b333248a8c2fcc833633ddcf61d54eb324a7b7ae1bf1a731c73805c78e3db842551d895d626814ee6200928ddcaa1090f5a4b916c5330b5c84d3bbb1e7defaf982ef70e585f935393e2a70ffdc0e04be13c6860518bdcdc2628747812a23541222eba2715507758e1c568c3017667e9900a4cb1481152384978a968dffe1d7b6dba967dd2e06e3cd031479ab83c71fd8c713ce5ac68c4faaf6b2a41f3479e1b5be483a02a5c74cd190521da283f034ec33f38aa22638d9b6fb6a7f485eae6fdee620901eff73b3ad5d2c44141e0baec83a3c634638aad3dec4ccf8040daa697e683aa94b0ad966fc9025f8318982686a9e0eaf7d321bdc97b21bce1153b18cc56355d98afe838d0cfc0e1651ba79e3b623d0f4b040d80db788175d056a84fe5389735159b729848afdff9335c78f2fe6b6eaaa17a87da881c2292a7c3541c7f21d67f4a28fe53eee697da35acc461597f725945d2c88c451d8deb4dfe09bfdd7974f092e19547609c690424aac10c012184c0fcc54c6f050420b6560b683e8a8ee1024a9ba1d75bb3b253917ae13e17735c15ba81b75ca8f208648dbbd8e9728f30c2fa83c6699d714599752f54322c2fe74eb80b1b07f68b884e88b0b4bb34d66d3b8475aabe12ff9c599e5a5a7b3ad532e3d705a20836685e9eaaa9a524c5d6fbb94677a9bf080f90689f52a3ddcace7cf4a2cd0253805e74ef6b82d2eeb7691b602d1c46fb1abcf63c3f45d59a5abf681168d7e04e50a3ca3bc6b40e61d573c0b34fb5d991e1812e4aa08bf48a798ddc1195dcf512bcb1992641e5ee83cdf5513acc3f4e4256ed14ec55073107b28a609735f60fa0e453ea8e8ecec6dbcae11f855a0e193a901742fa39cccf4e6d521965f81cb97170dd9af67c80f7952b70b4f469a5584f2ce016078d75c08128b6e37865d569f02e2ac26e388eb4f5935c376302fa1a82c0483d49db12801e44a0fd50dc153f8a5afaba78d1579eb24eb4c1493d796596d52eecac0860d71a0bab6d90eb422c3e55fef62d435e36261dcf128e146e286efaed292039ca284cbe36b926b7a854d2ea626f9ad9eaec6723dbfeec1a8c0ce9623e586aba3b7055d31532e887bebbf2f50397640b416728be3cb3027e2facfde92476b12eb009cd04ff1afe62ae3bda3fd773"

IV = "7dc4885cc38ef6fd0181b78f8f484873"

block_size = 32          # 16 * 2

c_blk_1 = bytes.fromhex( c[-block_size*2:-block_size] )
c_blk_2 = bytes.fromhex( c[-block_size:] )


def decrypt(blk1, blk2):
    ind = -1
    count = 1
    c_n_1 = ""
    i_n_1 = []
    c_lst = []

    IV_lst = []

    for i in range(0, len(c) - 1, 2):
        c_lst.append(c[i:i+2])

    for i in range(0, len(IV) - 1, 2):
        IV_lst.append(IV[i:i+2])

    p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1478)

    p.sendlineafter("):", b"rt1726")

    while count < 17:
        for i in range(1, 256):

            if i < 16:
                tmp = "0"+str(hex(i))[2:]
            else:
                tmp = str(hex(i))[2:]
            tmp = bytes.fromhex(tmp)
            print("tmp", tmp.hex())
            print("last ciphertext block", c_n_1)
            print("intermediate block", i_n_1)

            trailing_bytes = ""
            if count > 1:
                for i in i_n_1:
                    trailing_bytes += hex(int(i, 16) ^ count)[2:]
            print("trailing_bytes", trailing_bytes)

            send_data = blk1[:ind] + tmp + bytes.fromhex(trailing_bytes) + blk2
            print(blk1[:ind], tmp, blk2)
            #send_data = str(send_data).encode()
            p.sendline(send_data.hex())
            print(send_data.hex(), len(send_data))

            recv_data = p.recvuntil("message:")
            print(recv_data)
            print()
            if b"valid" in recv_data:
                i_n_1.insert(0, hex(int(tmp.hex(), 16) ^ count)[2:])
                c_n_1 = tmp.hex() + c_n_1
                c_lst[ind] = tmp.hex()
                ind -= 1
                count += 1
                break
            elif b"rack" in recv_data:
                print("ERROR!!!!")
                break
            


decrypt(c_blk_1, c_blk_2)



