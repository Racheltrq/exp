import os
import string
import base64

def isBase64(s):
    res = True
    for i in s:
        if i not in string.ascii_lowercase + string.ascii_uppercase + "0123456789+/=":
            res = False
    return res


f = open('temp.txt', 'r')

data = f.read()
f.close()

#os.system('base64 -d Base64ToBZ2.txt > bz.bz2') #base64 to bz2
#os.system('bzip2 -d bz.bz2') # bz2
#os.system('base64 -d bz > bz.hex') 
#os.system('cat bz.hex | xxd -r -p > temp.txt') #hex to ascii
count = 0
while "flag" not in data:
    count += 1

    # remove quptes
    if data[:2] =='b\'' and data[-1] == '\'':
        data = data[2:-1]
    if data[0] == '\'' and data[-1] == '\'':
        data = data[1:-1]
    if data[0] == '\"' and data[-1] == '\"':
        data = data[1:-1]
    if data[0] == '\'' and data[-1] == '\'':
        data = data[1:-1]
    #data = data.decode()
    print(data[:100])
    fwrite = open("temptemp", "w")
    fwrite.write(data)
    fwrite.close()
    os.system("rm temp.txt")
    os.system("mv temptemp temp.txt")
    # if hex
    isHex = True
    for i in data:
        if i not in "0123456789abcdef":
            isHex = False
            continue

    if isHex:
        print("-converting hex to:")
        os.system('cat bz.hex | xxd -r -p > temp')
        os.system('rm temp.txt')
        os.system('mv temp temp.txt')
        f = open('temp.txt', 'r')
        data = f.read()
        
        f.close()
        continue

    if data[:2] == "BZ":
        print("-converting bzip2 to:")
        os.system('bzip2 -d temp.txt')
        os.system('mv temp.txt.out temp.txt')
        f = open('temp.txt', 'r')
        data = f.read()
        f.close()
        continue
    
    if isBase64(data):
        print("-converting base64 to:")
        decoded_data = base64.b64decode(data)
        #print("base64 decoded:", decoded_data[0:100])
        if decoded_data[:2].decode() == "BZ":
            os.system('base64 -d temp.txt > temp') 
            os.system('rm temp.txt')
            os.system('mv temp temp.txt')
            print("-converting bzip2 to:")
            os.system('bzip2 -d temp.txt')
            os.system('mv temp.txt.out temp.txt')
            f = open('temp.txt', 'r')
            data = f.read()
            f.close()
            continue
        else:
            print("debug")
            os.system('base64 -d temp.txt > temp') 
            os.system('rm temp.txt')
            os.system('mv temp temp.txt')
            f = open('temp.txt', 'r')
            data = f.read()
            f.close()
            continue
    
    break

print(data)
        

    
    





    