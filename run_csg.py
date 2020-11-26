from ContextSensitiveGrammar import ContextSensitiveGrammar
from LBA import LBA, BoundSymbol

lba = LBA.from_json('lba.json')

csg = ContextSensitiveGrammar(lba)
csg.export('t1.txt')
print(csg.accepts('111*111=111111111'))