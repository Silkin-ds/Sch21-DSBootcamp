#!/usr/bin/env python3
import timeit
import random
from collections import Counter

def my_count(numbers):
    count_dict = {i:0 for i in range(101)}
    for number in numbers:
        count_dict[number] +=1
    return count_dict

def my_top(numbers):
    count_dict = my_count(numbers)
    return sorted(count_dict.items(), key = lambda x:x[1], reverse=True)[:10]

def count_counter(numbers):
    return Counter(numbers)

def counter_top(numbers):
    return Counter(numbers).most_common(10)

def main():
    my_list = [random.randint(0,100) for i in range (0,1000000)]
    my_time = timeit.timeit(lambda:my_count(my_list),number=1)
    print(f"my function: {my_time}")
    counter_time = timeit.timeit(lambda: count_counter(my_list), number=1)
    print(f"Counter: {counter_time}")
    manual_top_time = timeit.timeit(lambda: my_top(my_list), number=1)
    print(f"my top: {manual_top_time}")
    counter_top_time = timeit.timeit(lambda: counter_top(my_list), number=1)
    print(f"Counter`s top: {counter_top_time}")

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)