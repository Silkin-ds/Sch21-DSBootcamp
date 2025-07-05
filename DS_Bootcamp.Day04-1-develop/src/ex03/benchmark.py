#!/usr/bin/env python3
import timeit
import sys
from functools import reduce

def sum_loop(number):
    sum = 0
    for i in range(1,number + 1):
        sum += i
    return sum

def sum_reduce(number):
    return reduce(lambda sum,n: sum + n* n, range(1,number + 1), 0)

def main():
    if len(sys.argv) != 4:
        print("Must be func_name,attempts,number")
        return
    
    function_name = sys.argv[1]
    try:
        attempts = int(sys.argv[2])
        number = int(sys.argv[3])
    except ValueError:
        print("Arguments must be integer")
    
    if function_name == 'loop':
        name = sum_loop
    elif function_name == 'reduce':
        name = sum_reduce
    else:
        raise ValueError("Function name must be loop/reduce")
    
    time_spent = timeit.timeit(lambda:name(number), number=attempts)
    print(time_spent)
    
if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)