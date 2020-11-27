prods = set()
with open('real_check_prods.txt', 'r') as f:
    for line in f.readlines():
        prods.add(line)
with open('real_check_prods.txt', 'w') as f:
    for prod in prods:
        f.write(prod)