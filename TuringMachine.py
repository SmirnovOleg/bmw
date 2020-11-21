import json
from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import Set, Mapping, Tuple

from Grammar import Grammar, Production

State = str


class Symbol(str):
    BLANK = '_'
    EPS = 'eps'


class Direction:
    LEFT = '<'
    RIGHT = '>'


@dataclass
class TuringMachine:
    # Assume that machine's "head" position is at the beginning of a word on the "tape"
    language_alphabet: Set[Symbol]
    tape_alphabet: Set[Symbol]
    states: Set[State]
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
            states = set()
            for key, value in data['transitions'].items():
                state_from, symb_from = key.split(',')
                state_to, symb_to, dir = value.split(',')
                transitions[state_from, symb_from] = state_to, symb_to, dir
                tape_alphabet.update({symb_from, symb_to})
                states.update({state_from, state_to})
        return cls(language_alphabet, tape_alphabet, states, start_state, final_states, transitions)

    def to_grammar(self) -> Grammar:
        productions = set()
        productions.add(Production(['A1'], [self.start_state, 'A2']))
        for a in self.language_alphabet:
            productions.add(Production(['A2'], [f'[{a},{a}]', 'A2']))
        productions.add(Production(['A2'], ['A3']))
        productions.add(Production(['A3'], [f'[{Symbol.EPS}, {Symbol.BLANK}]', 'A3']))
        productions.add(Production(['A3'], [Symbol.EPS]))
        language_alphabet_with_eps = self.language_alphabet.union({Symbol.EPS})
        for a in language_alphabet_with_eps:
            for (q, c), (p, e, d) in self.transitions.items():
                if d == Direction.RIGHT:
                    productions.add(Production([q, f'[{a},{c}]'], [f'[{a},{e}]', p]))
        for a, b in product(language_alphabet_with_eps, language_alphabet_with_eps):  # with EPS or not?
            for i in self.tape_alphabet:
                for (q, c), (p, j, d) in self.transitions.items():
                    if d == Direction.LEFT:
                        productions.add(Production([f'[{b},{i}]', q, f'[{a},{c}]'], [p, f'[{b},{i}]', f'[{a},{j}]']))
        for a in language_alphabet_with_eps:
            for c in self.tape_alphabet:
                for q in self.final_states:
                    productions.add(Production([f'[{a},{c}]', q], [q, a, q]))
                    productions.add(Production([q, f'[{a},{c}]'], [q, a, q]))
        for q in self.final_states:
            productions.add(Production([q], [Symbol.EPS]))
        new_variables = set(f'[{v1},{v2}]' for v1, v2 in product(language_alphabet_with_eps, self.tape_alphabet))
        return Grammar(
            variables=new_variables.union(self.states).union({'A1', 'A2', 'A3'}),
            terminals=self.language_alphabet,
            productions=productions,
            start_variable='A1'
        )


if __name__ == '__main__':
    tm = TuringMachine.from_json(Path('./tm.json'))
    print(tm.to_grammar())
