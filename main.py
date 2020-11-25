from pathlib import Path

from UnrestrictedGrammar import UnrestrictedGrammar

if __name__ == '__main__':
    g = UnrestrictedGrammar.from_json(Path('./t0.json'))
    word = '1*1=1'
    ans, derivation = g.inference(word)
    if ans:
        for sent, prod in derivation:
            print(' '.join(sent))
            print(f'Applying: {prod}')
        print(' '.join([x for x in word]))
    else:
        print(ans)
