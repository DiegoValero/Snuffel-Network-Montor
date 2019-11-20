import hashlib, datetime, db

"""
Function to increase the complexity of the password
by adding a salt that changes every minute
"""

# Admin pass: DAY+HOUR+MINUTE, flip digits.
# First digit +2 and add before first digit, second digit +1 and add to last digit
#
# Example:
# DAY = 21
# HOUR = 7
# MINUTE = 19
# 21 + 7 + 19 = 47
# Add 10 = 57
# Flip digits = 75
# First digit +2 and add = 275
# Second digit +1 and subtract = 2756
def pwdSalt(pwd):
    x = datetime.datetime.now()
    base = x.day + x.hour + x.minute
    base += 10
    # flip
    fl = str(base)[::-1]

    # 1st part
    fd = str(fl)[1]
    f1 = int(fd) + 2
    p1 = str(f1) + fd

    # 2nd part
    sd = str(fl)[0]
    s2 = int(sd) + 1
    p2 = sd + str(s2)

    salt = p1 + p2
    xxx = pwd + salt
    return pwd + salt

def getHashFromString(value):
    return hashlib.md5(value.encode()).hexdigest()

def compareHash(value):
    a = getHashFromString(pwdSalt(value))

    x = datetime.datetime.now()
    admin = "admin" + str(int(x.day + x.hour + x.minute))
    b = db.hashQuery(admin)

    if a == b:
        return 1
    return 0
