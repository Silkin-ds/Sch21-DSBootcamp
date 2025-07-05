#!/usr/bin/env python3
import sys
import resource

def read_file_to_list(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        return lines
    except FileNotFoundError:
        print(f'File not found: {file_path}')
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise ValueError("Incorrect number of arguments. Usage: ./ordinary.py file_path")
    file_path = sys.argv[1]
    start_usage = resource.getrusage(resource.RUSAGE_SELF)
    start_memory = start_usage.ru_maxrss
    lines = read_file_to_list(file_path)
    for line in lines:
        pass
    usage = resource.getrusage(resource.RUSAGE_SELF)
    end_memory = usage.ru_maxrss
    peak = (end_memory - start_memory) / (1024 ** 2)
    time_user = usage.ru_utime - start_usage.ru_utime
    system_time = usage.ru_stime - start_usage.ru_stime
    time = time_user + system_time
    print(f'Peak Memory Usage = {peak:.3f} GB')
    print(f'User Mode Time + System Mode Time = {time:.2f}s')