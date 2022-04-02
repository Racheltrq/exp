import codecs

nums = "97 46 23 34 4D 8A C4 7E 7C 7C 7C 73 79 97 47 22 34 F5 BB C6 83 7C 7C 7C C4 7C 7C 7C 7C 73 79 C3 7D 7C 7C 7C C6 83 7C 7C 7C C4 7D 7C 7C 7C 73 79 73 7D 7D 7D 7D C4 40 7C 7C 7C 73 79 94 BD 83 83 83 1A 10 1D 1B 52 8 4 8 7C 94 BC 83 83 83 0"

nums = nums.split(" ")
print(len(nums))

for j in range(256):
    tmp = ""
    for i in range(len(nums)):
        ttt = int(nums[i], 16) ^ j
        tmp += chr(ttt)

    if "flag" in tmp:
        print(j, tmp)