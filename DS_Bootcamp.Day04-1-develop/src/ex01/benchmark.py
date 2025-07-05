#!/usr/bin/env python3
import timeit

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

def main():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
    'anna@live.com', 'philipp@gmail.com'] * 5
    time_usual = timeit.timeit(lambda: usual_func(emails),number=90000000)
    time_comprehension = timeit.timeit(lambda: comprehension(emails),number=90000000)
    time_map = timeit.timeit(lambda:map_func(emails),number=90000000)
    sort_time = sorted([time_usual,time_comprehension,time_map])
    if sort_time[0] ==  time_usual:
        print ("it is better to use a loop")
    elif  sort_time[0] ==  time_comprehension:
        print ("it is better to use a list comprehension")
    else:
        print ("it is better to use a map")
    print (f"{sort_time[0]} vs {sort_time[1]} vs {sort_time[2]}")

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)