import random
import uuid

def phn():
    n = '0000000000'
    while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
        n = str(random.randint(10**9, 10**10-1))
    #return n[:3] + '-' + n[3:6] + '-' + n[6:]
    return n[:3] + n[3:6]  + n[6:]


def unique_id():
    un_id = uuid.uuid4()
    un_id = str(un_id)
    un_id = un_id[:5]
    return un_id
