#!/usr/bin/env python3
import os

def main():
    venv = os.environ.get('VIRTUAL_ENV')
    if venv:
        print(f"Your current virtual env is {venv}")
    else:
        print("You are not in a virtual environment.")

if __name__ == '__main__':
    main()