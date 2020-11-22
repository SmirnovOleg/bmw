from pathlib import Path

from TMBasedUnrestrictedGrammar import TMBasedUnrestrictedGrammar
from TuringMachine import TuringMachine

if __name__ == '__main__':
    tm = TuringMachine.from_json(Path('tm.json'))
    grammar = TMBasedUnrestrictedGrammar(tm)
    assert grammar.accepts('11*11=1111') is True
    assert grammar.accepts('111*1=111') is True
    assert grammar.accepts('1*11=1') is False
    assert grammar.accepts('=241*') is False
    grammar.export(Path('./grammar.txt'))
