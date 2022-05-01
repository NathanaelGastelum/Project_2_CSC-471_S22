import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_file")
args = parser.parse_args()

def get_input():
    rules = {}
    with open(args.input_file) as file:
        for line in file:
            line = line.split("-", maxsplit=1)

            rules[line[0]] = set(line[1].strip().split("|"))

    return rules


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

    for key, value in rules.items():
        if len(rules[key]) == 1:
            if '0' in rules[key]:
                removed.add(key)
    
    # remove null Variables
    for key in removed:
        del rules[key]

    # removes null units from rules
    for key, value in rules.items():
        for subrule in value:
            rules[key].remove(subrule)
            rules[key].add("".join([x for x in subrule if x not in removed]))

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
        temp = set()
        
        for i, rule in enumerate(value):
            index_set = {j for j in range(len(rule)) if rule[j] in V}
            index_combinations = get_powerset(index_set)

            if rule != '0':
                if any(x in V for x in rule):
                    for combo in index_combinations:
                        new_rule = "".join([rule[j] for j in range(len(rule)) if j not in combo])
                        if new_rule and new_rule != key: 
                            temp.add(new_rule)
        
        # remove '0' rules
        rules[key] = {x for x in rules[key] if x != '0'}
        if temp:
            rules[key].update(temp)


    return rules

 
def remove_useless_rules(rules):
    # handle non terminating variables
    terminal_set = set()

    for key, value in rules.items():
       for rule in value:
           if len(get_nonterminals(rule)) == 0:
             terminal_set.add(key)

    for key, value in rules.items():
        for rule in value:
            if set(get_nonterminals(rule)).issubset(terminal_set):
               terminal_set.add(key)

    removed_keys = []

    for key, value in rules.items():
        removed_rule = []
        for rule in value: 
           for variable in get_nonterminals(rule):
               if variable not in terminal_set:
                   removed_rule.append(rule)
                   break

        for r in removed_rule:
            value.remove(r)
        if len(value) == 0:
            removed_keys.append(key)
    
    for key in removed_keys:
        del rules[key]

    # handle unreachable variables
    reachable = {'S'}
    current_len = 0

    for rule in rules['S']:
        reachable.update(get_nonterminals(rule))

    while current_len != len(reachable):
        current_len = len(reachable)
        
        for key in reachable:
            for rule in rules[key]:
                reachable.update(get_nonterminals(rule))
    
    rules = {key: rules[key] for key in rules.keys() if key in reachable}
                     
    return rules


def print_output(cfg):
    cfg = remove_e_rules(cfg)
    cfg = remove_useless_rules(cfg)
    
    for key, value in cfg.items():
        string_builder = []
        string_builder.append(f"{key}-")

        for i, rule in enumerate(value):
            if i > 0:
                string_builder.append("|")
            string_builder.append(f"{rule}")

        print("".join(string_builder))


print_output(get_input())
