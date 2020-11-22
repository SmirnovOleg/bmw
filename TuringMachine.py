import json
from dataclasses import dataclass
from pathlib import Path
from typing import Set, Mapping, Tuple

State = str


class Symbol(str):
    EPS = 'eps'


class Directions:
    LEFT = '<'
    RIGHT = '>'


@dataclass
class TuringMachine:
    # Assume that machine's "head" position is at the beginning of a word on the "tape"
    language_alphabet: Set[Symbol]
    tape_alphabet: Set[Symbol]
    blank: Symbol
    directions: Directions
    states: Set[State]
    start_state: State
    final_states: Set[State]
    transitions: Mapping[Tuple[State, Symbol], Tuple[State, Symbol, Directions]]

    @classmethod
    def from_json(cls, path_to_json: Path):
        with open(path_to_json) as json_file:
            data = json.load(json_file)
            start_state = data['start_state']
            final_states = data['final_states']
            blank = data['blank']
            directions = Directions()
            directions.LEFT = data['directions']['left']
            directions.RIGHT = data['directions']['right']
            language_alphabet = set(data['language_alphabet'])
            tape_alphabet = language_alphabet.copy()
            tape_alphabet.add(blank)
            transitions = {}
            states = set()
            for key, value in data['transitions'].items():
                state_from, symb_from = key.split(',')
                state_to, symb_to, dir = value.split(',')
                transitions[state_from, symb_from] = state_to, symb_to, dir
                tape_alphabet.update({symb_from, symb_to})
                states.update({state_from, state_to})
        return cls(language_alphabet, tape_alphabet, blank, directions, states, start_state, final_states, transitions)
