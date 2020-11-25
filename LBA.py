from pathlib import Path

from dataclasses import dataclass

from TuringMachine import TuringMachine


class BoundSymbol:
    LEFT = '#'
    RIGHT = '$'

@dataclass
class LBA(TuringMachine):

    @classmethod
    def from_json(cls, path_to_json: Path):
        lba = super(LBA, cls).from_json(path_to_json)
        assert BoundSymbol.LEFT in lba.language_alphabet
        assert BoundSymbol.RIGHT in lba.language_alphabet
        return lba