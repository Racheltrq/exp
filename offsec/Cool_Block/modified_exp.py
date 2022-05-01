from pwn import *
import argparse
import http.client
import re
import sys
import time
from itertools import cycle
from urllib.parse import urlencode

""" This file is from https://github.com/mpgn/Padding-oracle-attack/blob/master/exploit.py """
#######################################
# CUSTOMIZE YOUR RESPONSE ORACLE HERE #
#######################################
""" The function you want change to adapt the result to your problem """

p = remote("offsec-chalbroker.osiris.cyber.nyu.edu", 1478)
p.sendlineafter("):", b"rt1726")
p.recvuntil("message:")
cipher = "f4a60fdec121df64f0dca2abcb8cb82507b20ee6da804da255714b7b588329b81597c5982b5e1a4c602c672067a4184fc59d7688c6f20ddc81be44bfa31e70fe520c7bd1cbe09f49b6576fa12c87130c9820f52dea79ac5188bdc2617e92dbc0969be076161867756b8e773ef51d6cbfbaae7b3bf0103b333248a8c2fcc833633ddcf61d54eb324a7b7ae1bf1a731c73805c78e3db842551d895d626814ee6200928ddcaa1090f5a4b916c5330b5c84d3bbb1e7defaf982ef70e585f935393e2a70ffdc0e04be13c6860518bdcdc2628747812a23541222eba2715507758e1c568c3017667e9900a4cb1481152384978a968dffe1d7b6dba967dd2e06e3cd031479ab83c71fd8c713ce5ac68c4faaf6b2a41f3479e1b5be483a02a5c74cd190521da283f034ec33f38aa22638d9b6fb6a7f485eae6fdee620901eff73b3ad5d2c44141e0baec83a3c634638aad3dec4ccf8040daa697e683aa94b0ad966fc9025f8318982686a9e0eaf7d321bdc97b21bce1153b18cc56355d98afe838d0cfc0e1651ba79e3b623d0f4b040d80db788175d056a84fe5389735159b729848afdff9335c78f2fe6b6eaaa17a87da881c2292a7c3541c7f21d67f4a28fe53eee697da35acc461597f725945d2c88c451d8deb4dfe09bfdd7974f092e19547609c690424aac10c012184c0fcc54c6f050420b6560b683e8a8ee1024a9ba1d75bb3b253917ae13e17735c15ba81b75ca8f208648dbbd8e9728f30c2fa83c6699d714599752f54322c2fe74eb80b1b07f68b884e88b0b4bb34d66d3b8475aabe12ff9c599e5a5a7b3ad532e3d705a20836685e9eaaa9a524c5d6fbb94677a9bf080f90689f52a3ddcace7cf4a2cd0253805e74ef6b82d2eeb7691b602d1c46fb1abcf63c3f45d59a5abf681168d7e04e50a3ca3bc6b40e61d573c0b34fb5d991e1812e4aa08bf48a798ddc1195dcf512bcb1992641e5ee83cdf5513acc3f4e4256ed14ec55073107b28a609735f60fa0e453ea8e8ecec6dbcae11f855a0e193a901742fa39cccf4e6d521965f81cb97170dd9af67c80f7952b70b4f469a5584f2ce016078d75c08128b6e37865d569f02e2ac26e388eb4f5935c376302fa1a82c0483d49db12801e44a0fd50dc153f8a5afaba78d1579eb24eb4c1493d796596d52eecac0860d71a0bab6d90eb422c3e55fef62d435e36261dcf128e146e286efaed292039ca284cbe36b926b7a854d2ea626f9ad9eaec6723dbfeec1a8c0ce9623e586aba3b7055d31532e887bebbf2f50397640b416728be3cb3027e2facfde92476b12eb009cd04ff1afe62ae3bda3fd773"
IV = "7dc4885cc38ef6fd0181b78f8f484873"


def test_validity(response):

    if b"valid" in response:
        return True
    else:
        return False


###################################
# CUSTOMIZE YOUR ORACLE HTTP HERE #
###################################
def call_oracle(up_cipher):
    p.sendline(up_cipher)
    response = p.recvuntil("message:")
    return response


def split_len(seq, length):
    return [seq[i : i + length] for i in range(0, len(seq), length)]


""" Create custom block for the byte we search"""


def block_search_byte(size_block, i, pos, l):
    hex_char = hex(pos).split("0x")[1]
    return (
        "00" * (size_block - (i + 1))
        + ("0" if len(hex_char) % 2 != 0 else "")
        + hex_char
        + "".join(l)
    )


""" Create custom block for the padding"""


def block_padding(size_block, i):
    l = []
    for t in range(0, i + 1):
        l.append(
            ("0" if len(hex(i + 1).split("0x")[1]) % 2 != 0 else "")
            + (hex(i + 1).split("0x")[1])
        )
    return "00" * (size_block - (i + 1)) + "".join(l)


def hex_xor(s1, s2):
    b = bytearray()
    for c1, c2 in zip(bytes.fromhex(s1), cycle(bytes.fromhex(s2))):
        b.append(c1 ^ c2)
    return b.hex()


def run(cipher, size_block):
    cipher = cipher.upper()
    found = False
    valide_value = []
    result = []
    len_block = size_block * 2
    cipher_block = split_len(cipher, len_block)

    if len(cipher_block) == 1:
        print("[-] Abort there is only one block")
        sys.exit()
    # for each cipher_block
    for block in reversed(range(1, len(cipher_block))):
        if len(cipher_block[block]) != len_block:
            print("[-] Abort length block doesn't match the size_block")
            break
        print("[+] Search value block : ", block, "\n")
        # for each byte of the block
        for i in range(0, size_block):
            # test each byte max 255
            for ct_pos in range(0, 256):
                # 1 xor 1 = 0 or valide padding need to be checked
                if ct_pos != i + 1 or (
                    len(valide_value) > 0 and int(valide_value[-1], 16) == ct_pos
                ):

                    bk = block_search_byte(size_block, i, ct_pos, valide_value)
                    bp = cipher_block[block - 1]
                    bc = block_padding(size_block, i)

                    tmp = hex_xor(bk, bp)
                    cb = hex_xor(tmp, bc).upper()

                    up_cipher = cb + cipher_block[block]
                    # time.sleep(0.5)

                    # we call the oracle, our god
                    response = call_oracle(up_cipher)

                    if args.verbose == True:
                        exe = re.findall("..", cb)
                        discover = ("").join(exe[size_block - i : size_block])
                        current = ("").join(exe[size_block - i - 1 : size_block - i])
                        find_me = ("").join(exe[: -i - 1])

                        sys.stdout.write(
                            "\r[+] Test [Byte %03i/256 - Block %d ]: \033[31m%s\033[33m%s\033[36m%s\033[0m"
                            % (ct_pos, block, find_me, current, discover)
                        )
                        sys.stdout.flush()

                    if test_validity(response):

                        found = True

                        # data analyse and insert in right order
                        value = re.findall("..", bk)
                        valide_value.insert(0, value[size_block - (i + 1)])

                        if args.verbose == True:
                            print("")
                            print("[+] HTTP ", response.status, response.reason)
                            print("[+] Block M_Byte : %s" % bk)
                            print("[+] Block C_{i-1}: %s" % bp)
                            print("[+] Block Padding: %s" % bc)
                            print("")

                        bytes_found = "".join(valide_value)
                        if (
                            i == 0
                            and int(bytes_found, 16) > size_block
                            and block == len(cipher_block) - 1
                        ):
                            print(
                                "[-] Error decryption failed the padding is > "
                                + str(size_block)
                            )
                            sys.exit()

                        print(
                            "\033[36m" + "\033[1m" + "[+]" + "\033[0m" + " Found",
                            i + 1,
                            "bytes :",
                            bytes_found,
                        )
                        print("")

                        break
            if found == False:
                # lets say padding is 01 for the last byte of the last block (the padding block)
                if len(cipher_block) - 1 == block and i == 0:
                    value = re.findall("..", bk)
                    valide_value.insert(0, "01")
                    if args.verbose == True:
                        print("")
                        print(
                            "[-] No padding found, but maybe the padding is length 01 :)"
                        )
                        print("[+] Block M_Byte : %s" % bk)
                        print("[+] Block C_{i-1}: %s" % bp)
                        print("[+] Block Padding: %s" % bc)
                        print("")
                        bytes_found = "".join(valide_value)
                else:
                    print("\n[-] Error decryption failed")
                    result.insert(0, "".join(valide_value))
                    hex_r = "".join(result)
                    print("[+] Partial Decrypted value (HEX):", hex_r.upper())
                    padding = int(hex_r[len(hex_r) - 2 : len(hex_r)], 16)
                    print(
                        "[+] Partial Decrypted value (ASCII):",
                        bytes.fromhex(hex_r[0 : -(padding * 2)]).decode(),
                    )
                    sys.exit()
            found = False

        result.insert(0, "".join(valide_value))
        valide_value = []

    print("")
    hex_r = "".join(result)
    print("[+] Decrypted value (HEX):", hex_r.upper())
    padding = int(hex_r[len(hex_r) - 2 : len(hex_r)], 16)
    print(
        "[+] Decrypted value (ASCII):",
        bytes.fromhex(hex_r[0 : -(padding * 2)]).decode(),
    )


if __name__ == "__main__":
    
    run(IV+cipher, 16)