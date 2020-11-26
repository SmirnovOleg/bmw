from typing import Tuple, List
from collections import deque
from itertools import product

from LBA import BoundSymbol
from TMBasedGrammar import Production, TMBasedGrammar, Sentence
from TuringMachine import Directions, TuringMachine


class ContextSensitiveGrammar(TMBasedGrammar):
    def __init__(self, *args, **kwargs):
        super(ContextSensitiveGrammar, self).__init__(*args, **kwargs)

    @classmethod
    def from_turing_machine(cls, turing_machine: TuringMachine):
        terminals = turing_machine.language_alphabet.copy()
        terminals.discard(BoundSymbol.LEFT)
        terminals.discard(BoundSymbol.RIGHT)

        tape_symbols = turing_machine.tape_alphabet.copy()
        tape_symbols.discard(BoundSymbol.LEFT)
        tape_symbols.discard(BoundSymbol.RIGHT)

        productions = set()

        # Add generative productions with additional variables A1 and A2
        for a in terminals:
            # 1
            productions.add(
                Production(
                    ['A1'],
                    [f'[{turing_machine.start_state},{BoundSymbol.LEFT},{a},{a},{BoundSymbol.RIGHT}]'],
                ))
            # 4.1
            productions.add(
                Production(
                    ['A1'],
                    [f'[{turing_machine.start_state},{BoundSymbol.LEFT},{a},{a}]', 'A2'],
                ))
            # 4.2
            productions.add(
                Production(
                    ['A2'],
                    [f'[{a},{a}]', 'A2'],
                ))
            # 4.3
            productions.add(
                Production(
                    ['A2'],
                    [f'[{a},{a},{BoundSymbol.RIGHT}]'],
                ))

        # not_final_states = turing_machine.states.difference(turing_machine.final_states)
        for (q, x), (p, y, d) in turing_machine.transitions.items():
            for a in terminals:
                if p in turing_machine.final_states:
                    for c in tape_symbols:
                        # 3.1
                        productions.add(
                            Production(
                                [f'[{p},{BoundSymbol.LEFT},{c},{a},{BoundSymbol.RIGHT}]'],
                                [f'{a}']
                            ))
                        # 3.2
                        productions.add(
                            Production(
                                [f'[{BoundSymbol.LEFT},{p},{c},{a},{BoundSymbol.RIGHT}]'],
                                [f'{a}']
                            ))
                        # 3.3
                        productions.add(
                            Production(
                                [f'[{BoundSymbol.LEFT},{c},{a},{p},{BoundSymbol.RIGHT}]'],
                                [f'{a}']
                            ))

                        # 8.1
                        productions.add(
                            Production(
                                [f'[{p},{BoundSymbol.LEFT},{c},{a}]'],
                                [f'{a}']
                            ))
                        # 8.2
                        productions.add(
                            Production(
                                [f'[{BoundSymbol.LEFT},{p},{c},{a}]'],
                                [f'{a}']
                            ))
                        # 8.3
                        productions.add(
                            Production(
                                [f'[{p},{c},{a}]'],
                                [f'{a}']
                            ))
                        # 8.4
                        productions.add(
                            Production(
                                [f'[{p},{c},{a},{BoundSymbol.RIGHT}]'],
                                [f'{a}']
                            ))
                        # 8.5
                        productions.add(
                            Production(
                                [f'[{c},{a},{p},{BoundSymbol.RIGHT}]'],
                                [f'{a}']
                            ))

                        for b in terminals:
                            # 9.1
                            productions.add(
                                Production(
                                    [f'{a}', f'[{c},{b}]'],
                                    [f'{a}', f'{b}']
                                ))
                            # 9.2
                            productions.add(
                                Production(
                                    [f'{a}', f'[{c},{b},{BoundSymbol.RIGHT}]'],
                                    [f'{a}', f'{b}']
                                ))
                            # 9.3
                            productions.add(
                                Production(
                                    [f'[{c},{a}]', f'{b}'],
                                    [f'{a}', f'{b}']
                                ))
                            # 9.4
                            productions.add(
                                Production(
                                    [f'[{BoundSymbol.LEFT},{c},{a}]', f'{b}'],
                                    [f'{a}', f'{b}']
                                ))
                if x == BoundSymbol.LEFT:
                    if d == Directions.RIGHT:
                        for X in tape_symbols:
                            # 2.1
                            productions.add(
                                Production(
                                    [f'[{q},{BoundSymbol.LEFT},{X},{a},{BoundSymbol.RIGHT}]'],
                                    [f'[{BoundSymbol.LEFT},{p},{X},{a},{BoundSymbol.RIGHT}]']
                                ))
                            # 5.1
                            productions.add(
                                Production(
                                    [f'[{q},{BoundSymbol.LEFT},{X},{a}]'],
                                    [f'[{BoundSymbol.LEFT},{p},{X},{a}]']
                                ))
                elif x == BoundSymbol.RIGHT:
                    if d == Directions.LEFT:
                        for X in tape_symbols:
                            # 2.4
                            productions.add(
                                Production(
                                    [f'[{BoundSymbol.LEFT},{X},{a},{q},{BoundSymbol.RIGHT}]'],
                                    [f'[{BoundSymbol.LEFT},{p},{X},{a},{BoundSymbol.RIGHT}]']
                                ))
                            # 7.2
                            productions.add(
                                Production(
                                    [f'[{X},{a},{q},{BoundSymbol.RIGHT}]'],
                                    [f'[{p},{X},{a},{BoundSymbol.RIGHT}]']
                                ))
                if d == Directions.RIGHT:
                    # 2.3
                    productions.add(
                        Production(
                            [f'[{BoundSymbol.LEFT},{q},{x},{a},{BoundSymbol.RIGHT}]'],
                            [f'[{BoundSymbol.LEFT},{y},{a},{p},{BoundSymbol.RIGHT}]']
                        ))
                    # 7.1
                    productions.add(
                        Production(
                            [f'[{q},{x},{a},{BoundSymbol.RIGHT}]'],
                            [f'[{y},{a},{p},{BoundSymbol.RIGHT}]']
                        ))
                else:
                    # 2.2
                    productions.add(
                        Production(
                            [f'[{BoundSymbol.LEFT},{q},{x},{a},{BoundSymbol.RIGHT}]'],
                            [f'[{p},{BoundSymbol.LEFT},{y},{a},{BoundSymbol.RIGHT}]']
                        ))
                    # 5.2
                    productions.add(
                        Production(
                            [f'[{BoundSymbol.LEFT},{q},{x},{a}]'],
                            [f'[{p},{BoundSymbol.LEFT},{y},{a}]']
                        ))

                for Z in tape_symbols:
                    for b in terminals:
                        if d == Directions.RIGHT:
                            # 5.3 
                            productions.add(
                                Production(
                                    [f'[{BoundSymbol.LEFT},{q},{x},{a}]', f'[{Z},{b}]'],
                                    [f'[{BoundSymbol.LEFT},{y},{a}]', f'[{p},{Z},{b}]']
                                ))
                            # 6.1 
                            productions.add(
                                Production(
                                    [f'[{q},{x},{a}]', f'[{Z},{b}]'],
                                    [f'[{y},{a}]', f'[{p},{Z},{b}]']
                                ))
                            # 6.3 
                            productions.add(
                                Production(
                                    [f'[{q},{x},{a}]', f'[{Z},{b},{BoundSymbol.RIGHT}]'],
                                    [f'[{y},{a}]', f'[{p},{Z},{b},{BoundSymbol.RIGHT}]']
                                ))
                        else:
                            # 6.2 
                            productions.add(
                                Production(
                                    [f'[{Z},{b}]', f'[{q},{x},{a}]'],
                                    [f'[{p},{Z},{b}]', f'[{y},{a}]']
                                ))
                            # 6.4 
                            productions.add(
                                Production(
                                    [f'[{BoundSymbol.LEFT},{Z},{b}]', f'[{q},{x},{a}]'],
                                    [f'[{BoundSymbol.LEFT},{p},{Z},{b}]', f'[{y},{a}]']
                                ))
                            # 7.3 
                            productions.add(
                                Production(
                                    [f'[{Z},{b}]', f'[{q},{x},{a},{BoundSymbol.RIGHT}]'],
                                    [f'[{p},{Z},{b}]', f'[{y},{a},{BoundSymbol.RIGHT}]']
                                ))

        new_variables = \
            set(f'[{q},{BoundSymbol.LEFT},{ts},{term},{BoundSymbol.RIGHT}]' for q, term, ts in
                product(turing_machine.states, terminals, tape_symbols))
        new_variables.union(
            set(f'[{BoundSymbol.LEFT},{q},{ts},{term},{BoundSymbol.RIGHT}]' for q, term, ts in
                product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables.union(
            set(f'[{BoundSymbol.LEFT},{ts},{term},{q},{BoundSymbol.RIGHT}]' for q, term, ts in
                product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables = new_variables.union(
            set(f'[{q},{ts},{term}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables = new_variables.union(
            set(f'[{q},{ts},{term},{BoundSymbol.RIGHT}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables = new_variables.union(
            set(f'[{ts},{term},{q},{BoundSymbol.RIGHT}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables = new_variables.union(
            set(f'[{BoundSymbol.LEFT},{ts},{term}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables = new_variables.union(
            set(f'[{ts},{term}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables = new_variables.union(
            set(f'[{ts},{term},{BoundSymbol.RIGHT}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables = new_variables.union(
            set(f'[{BoundSymbol.LEFT},{q},{ts},{term}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables = new_variables.union(
            set(f'[{q},{BoundSymbol.LEFT},{ts},{term}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )

        gen_prods = set()
        check_prods = set()
        term_prods = set()
        for prod in productions:
            if prod.head[0].startswith('A'):
                gen_prods.add(prod)
            elif not prod.body[0].startswith('['):
                term_prods.add(prod)
            else:
                check_prods.add(prod)

        return cls(
            variables=new_variables.union({'A1', 'A2'}),
            terminals=turing_machine.language_alphabet,
            gen_productions=gen_prods,
            check_productions=check_prods,
            term_productions=term_prods,
            start_variable='A1',
            start_state=turing_machine.start_state,
            blank=turing_machine.blank
        )

    def inference(self, word: str) -> Tuple[bool, List[Tuple[Sentence, Production]]]:
        word_on_tape = (
            [f'[{self.start_state},{BoundSymbol.LEFT},{word[0]},{word[0]}]']
            + [f'[{x},{x}]' for x in word[1:-1]]
            + [f'[{word[-1]},{word[-1]},{BoundSymbol.RIGHT}]']
        )
        derivation = [([self.start_variable], Production(['A1'], [f'[qS,{BoundSymbol.LEFT},1,1]','A2']))]
        current_sent = [f'[qS,{BoundSymbol.LEFT},1,1]','A2']
        for x in word[:-1]:
            derivation.append((current_sent, Production(['A2'], [f'[{x},{x}]', 'A2'])))
            current_sent = current_sent[:-1] + [f'[{x},{x}]', 'A2']
        derivation.append((current_sent, Production(['A2'], [f'[1,1,{BoundSymbol.RIGHT}]'])))
        ans, tail_derivation = self._inference(word_on_tape)
        return ans, derivation + tail_derivation