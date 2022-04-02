


dict = {"A": [int("E3", 16), "C", "G"],
        "B": [int("1F9", 16), "E", "D"],
        "C": [int("468", 16), "D", "G"],
        "D": [int("213", 16), "I", "D"],
        "E": [int("121", 16), "F", "H"],
        "F": [int("3A9", 16), "A", "F"],
        "G": [int("19A", 16), "J", "A"],
        "H": [int("13A", 16), "A", "J"],
        "I": [int("362", 16), "J", "B"],
        "J": [int("2C6", 16), "J", "D"]
}


tot = 9595 - int("E3", 16)

def recurse(lst, res, tot, cur):
    if tot == 0:
        print(res)
        print(lst)
        return
    if tot < 0:
        return


    choices = [dict[cur][1], dict[cur][2]] # "C" or "G"
    #print(dict[choices[0]])
    recurse(lst + choices[0], res + "L", tot - dict[choices[0]][0], choices[0])
    recurse(lst + choices[1], res + "R", tot - dict[choices[1]][0], choices[1])

    return
    
recurse("", "", tot, "A")