from pathlib import Path

from UnrestrictedGrammar import UnrestrictedGrammar
from TuringMachine import TuringMachine

if __name__ == '__main__':
    tm = TuringMachine.from_json(Path('tm.json'))
    grammar = UnrestrictedGrammar(tm)
    assert grammar.accepts('11*11=1111') is True
