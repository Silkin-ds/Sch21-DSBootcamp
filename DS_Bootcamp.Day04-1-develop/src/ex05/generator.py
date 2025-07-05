#!/usr/bin/env python3
import sys
import resource

def generator_file(path):
    try:
        with open(path,'r', encoding= 'utf-8') as file:
            for line in file:
                yield line
    except FileNotFoundError:
        print(f'File not found: {path}')
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("Incorrect number of arguments Usage: ./generator.py file_path")
    file_path = sys.argv[1]
    for _ in generator_file(file_path):
        pass
    usage = resource.getrusage(resource.RUSAGE_SELF)
    peak = usage.ru_maxrss / 1024**2
    time = usage.ru_utime + usage.ru_stime
    print(f'Peak Memory Usage = {peak:.3f} GB')
    print(f'User Mode Time + System Mode Time = {time:.2f}s')