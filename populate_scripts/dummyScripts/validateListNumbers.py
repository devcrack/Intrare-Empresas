import re
data = "1,2,3"
if re.compile("^[0-9,]+$").match(data):
    print('match')
else:
    print('no match')