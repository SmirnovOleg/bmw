from pathlib import Path

from UnrestrictedGrammar import UnrestrictedGrammar

if __name__ == '__main__':
    g = UnrestrictedGrammar.from_json(Path('./t0.json'))
    print(g.accepts('1*1=1'))
