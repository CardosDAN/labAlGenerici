import re


def remove_comments(string):

    string = re.sub(re.compile("/\*.*?\*/", re.DOTALL), "", string)
    string = re.sub(re.compile("//.*?\n"), "", string)
    return string


string = open('Lab01_simple_instances/Lab01_simple_small_01.dat').read()

file_vars = {}

string = remove_comments(string)
values = [x.strip() for x in string.split(';')]
for value in values:
    if '=' not in value:
        continue
    pair = [x.strip() for x in value.split('=')]
    pair[1] = pair[1].replace('\\n', ' ')
    while '  ' in pair[1]:
        pair[1] = pair[1].replace('  ', ' ')
    pair[1] = pair[1].replace(' ', ', ')
    file_vars[pair[0]] = eval(pair[1])


def north_west_corner(supply, demand):
    supply_copy = supply.copy()
    demand_copy = demand.copy()
    i = 0
    j = 0
    bfs = []
    while len(bfs) < len(supply) + len(demand) - 1:
        s = supply_copy[i]
        d = demand_copy[j]
        v = min(s, d)
        supply_copy[i] -= v
        demand_copy[j] -= v
        bfs.append(((i, j), v))
        if supply_copy[i] == 0 and i < len(supply) - 1:
            i += 1
        elif demand_copy[j] == 0 and j < len(demand) - 1:
            j += 1
    return bfs


if __name__ == '__main__':
    l_SCj = file_vars['SCj']
    l_Dk = file_vars['Dk']
    supply = l_SCj
    demand = l_Dk
    bfs = north_west_corner(supply, demand)
    print(bfs)
