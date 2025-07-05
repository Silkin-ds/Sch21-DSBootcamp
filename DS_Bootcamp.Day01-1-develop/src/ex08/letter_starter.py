import sys

def letter(input_email):
    with open("employers.tsv", "r", encoding='utf-8') as input:
        lines = input.readlines()
    
    flag = False
    for line in lines[1:]:
        name, surname, email = line.strip().split("\t")
        if email == input_email:
            print(f"Dear {name}, welcome to our team. We are sure that it will be a pleasure to work with you. That’s a precondition for the professionals that our company hires.")
            flag = True
            break 
    
    if not flag:
        print("Email not found")

def main():
    if len(sys.argv) != 2:
        return
    
    email = sys.argv[1]
    letter(email)

if __name__ == '__main__':
    main()