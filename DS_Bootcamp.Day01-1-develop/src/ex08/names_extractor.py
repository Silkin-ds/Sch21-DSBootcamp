import sys

def read_file(path):
    with open(rf'{path}',"r",encoding='utf-8') as input:
        emails = input.read().strip().split('\n')
    
    employers=[]

    for email in emails:
        if "@corp.com" in email:
            body = email.split("@")[0]
            name,surname = body.split(".")
            name = name.capitalize()
            surname = surname.capitalize()
            employers.append(f"{name}\t{surname}\t{email}\n")
    return employers

def write_tsv(lines):
    with open("employers.tsv","w",encoding='utf-8') as output:
        output.write("Name\tSurname\tE-mail\n")
        return output.writelines(lines)

def main():
    if len(sys.argv) != 2:
        return
    
    path=sys.argv[1]
    lines=read_file(path)
    write_tsv(lines)

if __name__ == '__main__':
    main()