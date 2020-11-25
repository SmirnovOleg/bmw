# res = ''

# with open('tm.txt', 'r') as f:
#     for line in f.readlines():
#         l, r = line.split(':')
#         l = l[1:-1]
#         r = r[2:-3]
#         res += l + '\n'
#         res += r + '\n'

from ContextSensitiveGrammar import ContextSensitiveGrammar
from LBA import LBA, BoundSymbol

lba = LBA.from_json('lba.json')
print(lba)

csg = ContextSensitiveGrammar(lba)

csg.export('csg.txt')
print(csg.accepts('¢1*1=1$'))