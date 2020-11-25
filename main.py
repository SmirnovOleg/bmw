from pathlib import Path

from TuringMachine import TuringMachine
from UnrestrictedGrammar import UnrestrictedGrammar

if __name__ == '__main__':
    tm = TuringMachine.from_json(Path('tm.json'))
    g = UnrestrictedGrammar.from_turing_machine(tm)
    print(g.accepts('1*11=11'))
