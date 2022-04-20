import os
low = 48
high = 80

for a in range(low, high + 1):
    for b in range(low, high + 1):
        for c in range(low, high + 1):
            seed = "\'" + chr(a) + chr(b) + chr(c) + "\'"
            os.system("./brute " + seed)


