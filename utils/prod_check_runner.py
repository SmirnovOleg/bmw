from pathlib import Path

from grammars.ContextSensitiveGrammar import ContextSensitiveGrammar
from machines.LBA import LBA

lba = LBA.from_json(Path('../resources/lba.json'))

csg = ContextSensitiveGrammar.from_turing_machine(lba)
csg.export('t1.txt')

words = [
    '11*11=1111',
    '1*11=11',
    '11*1=11',
    '1*1=1',
    '111*11=111111',
    '111*111=111111111',
]
for word in words:
    ans, derivation = csg.inference(word)
    if ans:
        for sent, prod in derivation:
            print(' '.join(sent))
            print(f'Applying: {prod}')
        print(' '.join([x for x in word]))
    else:
        print(ans)