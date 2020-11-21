import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Set, Mapping, Tuple

State = str


class Symbol(str):
    BLANK = '_'


class Direction(Enum):
    LEFT = '<'
    RIGHT = '>'


@dataclass
class TuringMachine:
    language_alphabet: Set[Symbol]
    tape_alphabet: Set[Symbol]
    start_state: State
    final_states: Set[State]
    transitions: Mapping[Tuple[State, Symbol], Tuple[State, Symbol, Direction]]

    @classmethod
    def from_json(cls, path_to_json: Path):
        with open(path_to_json) as json_file:
            data = json.load(json_file)
            start_state = data['start_state']
            final_states = data['final_states']
            language_alphabet = set(data['language_alphabet'])
            tape_alphabet = language_alphabet.copy()
            transitions = {}
            for key, value in data['transitions'].items():
                state_from, symb_from = key.split(',')
                state_to, symb_to, dir = value.split(',')
                transitions[state_from, symb_from] = state_to, symb_to, dir
                tape_alphabet.update({symb_from, symb_to})
        return cls(language_alphabet, tape_alphabet, start_state, final_states, transitions)

    def to_grammar(self):
        pass


if __name__ == '__main__':
    tm = TuringMachine.from_json(Path('./tm.json'))
    print(tm.language_alphabet)
