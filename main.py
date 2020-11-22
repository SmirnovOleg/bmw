from pathlib import Path

from TMBasedUnrestrictedGrammar import TMBasedUnrestrictedGrammar
from TuringMachine import TuringMachine

if __name__ == '__main__':
    tm = TuringMachine.from_json(Path('./tm.json'))
    t0_grammar = TMBasedUnrestrictedGrammar(tm)
    print(t0_grammar.accepts('110'))
