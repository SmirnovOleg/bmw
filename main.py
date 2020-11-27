import sys
from pathlib import Path

from grammars.ContextSensitiveGrammar import ContextSensitiveGrammar
from grammars.UnrestrictedGrammar import UnrestrictedGrammar

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Wrong number of arguments. Usage example: python main.py t0 1*111=111')
        sys.exit(1)
    if sys.argv[1] == 't0':
        grammar = UnrestrictedGrammar.from_json(Path('resources/t0.json'))
    elif sys.argv[1] == 't1':
        grammar = ContextSensitiveGrammar.from_json(Path('resources/t1.json'))
    else:
        print('Wrong grammar type. Choose `t0` or `t1`')
        sys.exit(1)
    word = sys.argv[2]
    ans, derivation = grammar.inference(word)
    if ans:
        print('Accepted! Inference:')
        for sent, prod in derivation:
            print(' '.join(sent))
            prod_repr = f'{" ".join(prod.head)} -> {" ".join(prod.body)}'
            print(f'    Applying: {prod_repr}')
        print(' '.join([x for x in word]))
    else:
        print('Wrong answer')
