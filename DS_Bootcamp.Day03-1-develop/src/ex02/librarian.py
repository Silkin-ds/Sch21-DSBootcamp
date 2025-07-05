#!/usr/bin/env python3
import os
import subprocess
import sys
import shutil

def check_envm():
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and (sys.base_prefix != sys.prefix)):
        raise EnvironmentError("This script must be run inside a virtual environment.")

def install_libraries():
    libraries = ['beautifulsoup4', 'pytest']
    subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + libraries)

def get_installed_libraries():
    return subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8')

def save_requirements(installed_packages):
    with open('requirements.txt', 'w') as f:
        f.write(installed_packages)

def archive_envm():
    env_folder = os.path.dirname(sys.prefix)
    shutil.make_archive('dionedre', 'zip', env_folder)

def main():
    try:
        check_envm()
        install_libraries()
        installed_packages = get_installed_libraries()
        print("Installed libraries:")
        print(installed_packages)
        save_requirements(installed_packages)
        archive_envm()
    except ValueError:
        print(f"Error: {ValueError}")

if __name__ == '__main__':
    main()