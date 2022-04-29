import argparse
import enum
from multiprocessing.sharedctypes import Value
from traceback import print_tb

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

def get_nonterminals(rule):
    nonterminals = []
    rule.split()
    for char in rule:
        if char.isupper():
            nonterminals.append(char)
            
    return nonterminals

def get_powerset(V):
    node_set = list(V)
    powerset = []

    for i in range(1 << len(node_set)):
        powerset.append([])
        for j in range(len(node_set)):
            if i & (1 << j):
                powerset[i].append(node_set[j])

    return powerset

def remove_e_rules(rules):
    removed = set()

    for rule in rules.items():
        if len(rule[1]) == 1:
            if rule[1][0] == '0':
                removed.add(rule[0])
    
    for key in removed:
        rules.pop(key)

    for key, value in rules.items():
        for i, subrule in enumerate(value):
            rules[key][i] = "".join([x for x in subrule if x not in removed])

    V = set()
    for key, value in rules.items():
        for rule in value:
            if rule == '0':
                V.add(key)

    # Check for nullable unit rules
    for key, value in rules.items():
        for rule in value:
            if len(rule) == 1 and rule in V:
                V.add(key)

    for key, value in rules.items():
        temp = []
        
        for i, rule in enumerate(value):
            index_set = {j for j in range(len(rule)) if rule[j] in V}
            index_combinations = get_powerset(index_set)

            if rule != '0':
                if any(x in V for x in rule):
                    for combo in index_combinations:
                        temp.append("".join([rule[j] for j in range(len(rule)) if j not in combo]))
        
        rules[key] = [x for x in rules[key] if x != '0']
        if temp:
            rules[key] += temp # TODO: handle duplicates/rules that don't need multiple combinations


    return rules

rules = get_input()
print(remove_e_rules(rules))