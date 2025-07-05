#!/usr/bin/env python3
import timeit
import sys

def usual_func(emails):
    new_mail = []
    for email in emails:
        if email.endswith('gmail.com'):
            new_mail.append(email)
    return new_mail

def comprehension(emails):
    return [email for email in emails if email.endswith('@gmail.com')]

def map_func(emails):
    return(list(map(lambda email: email if email.endswith('@gmail.com') else None,emails)))

def filter_func(emails):
    return (list(map(lambda email: email if email.endswith('@gmail.com') else None,emails)))

def main():
    function_name = sys.argv[1]
    if len(sys.argv)!= 3:
        print("Must be function_name and attempts")
        return
    
    try:
        attempts = int(sys.argv[2])
    except: 
        raise ValueError("argument must be integer")
    
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
    'anna@live.com', 'philipp@gmail.com'] * 5

    if function_name == 'loop':
        name = usual_func
    elif function_name == 'list_comprehension':
        name = comprehension
    elif function_name == 'map':
        name = map_func
    elif function_name == 'filter':
        name = filter_func
    else:
        raise ValueError("Invalid function name")
    
    time_spent = timeit.timeit(lambda:name(emails), number=attempts)
    print(f"{time_spent}")
if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)