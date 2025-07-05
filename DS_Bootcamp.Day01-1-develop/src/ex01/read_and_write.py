def read():
    with open(r'ds.csv', 'r', encoding='utf-8') as output:
        return output.readlines()

def replace(line):
    result = []
    flag = False
    for char in line:
        if char == '"':
            flag = not flag 
        elif char == ',' and not flag:
            result.append('\t')
        else:
            result.append(char)
    return ''.join(result)

def write(lines):
    with open(r"ds.tsv", 'w', encoding='utf-8') as output:
        output.writelines(lines)

def main():
    lines = read()
    replaced_lines = [replace(line) for line in lines]
    write(replaced_lines)

if __name__ == "__main__":
    main()