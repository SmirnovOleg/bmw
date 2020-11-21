import json
from enum import Enum
from pathlib import Path
from typing import Set, Mapping, Tuple

State = str
Symbol = str


class Direction(Enum):
    LEFT = '<'
    RIGHT = '>'


class TuringMachine:
    def __init__(self, start_state: State, final_states: Set[State],
                 transitions: Mapping[Tuple[State, Symbol], Tuple[State, Symbol, Direction]]):
        self.start_state = start_state
        self.final_states = final_states
        self.transitions = transitions

    @classmethod
    def from_json(cls, path_to_json: Path):
        with open(path_to_json) as json_file:
            data = json.load(json_file)
            start_state = data['start_state']
            final_states = data['final_states']
            transitions = {}
            for key, value in data['transitions'].items():
                state_from, symb_from = key.split(',')
                state_to, symb_to, dir = value.split(',')
                transitions[state_from, symb_from] = state_to, symb_to, dir
        return cls(start_state, final_states, transitions)


if __name__ == '__main__':
    tm = TuringMachine.from_json(Path('./tm.json'))
