import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
args = parser.parse_args()

def get_input():
    rules = {}
    with open(args.input_file) as file:
        for line in file:
            line = line.split("-", maxsplit=1)

            rules[line[0]] = line[1].strip().split("|")

    return rules

print(get_input())