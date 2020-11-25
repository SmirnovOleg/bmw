from ContextSensitiveGrammar import ContextSensitiveGrammar
from LBA import LBA, BoundSymbol

lba = LBA.from_json('lba.json')
print(lba)

csg = ContextSensitiveGrammar(lba)

csg.export('csg.txt')
print(csg.accepts('1111*1111=1111111111111111'))