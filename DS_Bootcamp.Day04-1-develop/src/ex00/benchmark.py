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

def main():
    emails = ['john@gmail.com', 'james@gmail.com', 'alice@yahoo.com',
    'anna@live.com', 'philipp@gmail.com'] * 5
    time_usual = timeit.timeit(lambda: usual_func(emails),number=90000000)
    time_comprehension = timeit.timeit(lambda: comprehension(emails),number=90000000)
    if time_comprehension <= time_usual:
        print(f"it is better to use a list comprehension\n{time_comprehension} vs {time_usual}")
    else:
        print(f"it is better to use a loop\n{time_usual} vs {time_comprehension}")

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)