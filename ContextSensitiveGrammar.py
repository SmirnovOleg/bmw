from collections import deque
from itertools import product

from Grammar import Production, Grammar
from TuringMachine import Symbol, Directions, TuringMachine
from LBA import LBA, BoundSymbol


class ContextSensitiveGrammar(Grammar):
    def __init__(self, turing_machine: TuringMachine):
        self.turing_machine = turing_machine
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
                if q in turing_machine.final_states:
                    # 3.1
                    productions.add(
                        Production(
                            [f'[{q},{BoundSymbol.LEFT},{x},{a},{BoundSymbol.RIGHT}]'],
                            [f'{a}']
                    ))
                    # 3.2
                    productions.add(
                        Production(
                            [f'[{BoundSymbol.LEFT},{q},{x},{a},{BoundSymbol.RIGHT}]'],
                            [f'{a}']
                    ))
                    # 3.3
                    productions.add(
                        Production(
                            [f'[{BoundSymbol.LEFT},{x},{a},{q},{BoundSymbol.RIGHT}]'],
                            [f'{a}']
                    ))

                    # 8.1
                    productions.add(
                        Production(
                            [f'[{q},{BoundSymbol.LEFT},{x},{a}]'],
                            [f'{a}']
                    ))
                    # 8.2
                    productions.add(
                        Production(
                            [f'[{BoundSymbol.LEFT},{q},{x},{a}]'],
                            [f'{a}']
                    ))
                    # 8.3
                    productions.add(
                        Production(
                            [f'[{q},{x},{a}]'],
                            [f'{a}']
                    ))
                    # 8.4
                    productions.add(
                        Production(
                            [f'[{q},{x},{a},{BoundSymbol.RIGHT}]'],
                            [f'{a}']
                    ))
                    # 8.5
                    productions.add(
                        Production(
                            [f'[{x},{a},{q},{BoundSymbol.RIGHT}]'],
                            [f'{a}']
                    ))

                    for b in terminals:
                        # 9.1
                        productions.add(
                            Production(
                                [f'{a}', f'[{x},{b}]'],
                                [f'{a}', f'{b}']
                        ))
                        # 9.2
                        productions.add(
                            Production(
                                [f'{a}', f'[{x},{b},{BoundSymbol.RIGHT}]'],
                                [f'{a}', f'{b}']
                        ))
                        # 9.3
                        productions.add(
                            Production(
                                [f'[{x},{a}]', f'{b}'],
                                [f'{a}', f'{b}']
                        ))
                        # 9.4
                        productions.add(
                            Production(
                                [f'[{BoundSymbol.LEFT},{x},{a}]', f'{b}'],
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
                if x == BoundSymbol.RIGHT:
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
            set(f'[{q},{BoundSymbol.LEFT},{ts},{term},{BoundSymbol.RIGHT}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        new_variables.union(
            set(f'[{BoundSymbol.LEFT},{q},{ts},{term},{BoundSymbol.RIGHT}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables.union(
            set(f'[{BoundSymbol.LEFT},{ts},{term},{q},{BoundSymbol.RIGHT}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables.union(
            set(f'[{q},{ts},{term}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables.union(
            set(f'[{q},{ts},{term},{BoundSymbol.RIGHT}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables.union(
            set(f'[{ts},{term},{q},{BoundSymbol.RIGHT}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables.union(
            set(f'[{BoundSymbol.LEFT},{ts},{term}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables.union(
            set(f'[{ts},{term}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )
        new_variables.union(
            set(f'[{ts},{term},{BoundSymbol.RIGHT}]' for q, term, ts in product(turing_machine.states, terminals, tape_symbols))
        )

        super().__init__(
            variables=new_variables.union({'A1', 'A2'}),
            terminals=turing_machine.language_alphabet,
            productions=productions,
            start_variable='A1'
        )

    def accepts(self, word: str) -> bool:
        sentences = deque([[f'[qS,{BoundSymbol.LEFT},{word[0]},{word[0]}]']
                           + [f'[{x},{x}]' for x in word[1:-1]]
                           + [f'[{word[-1]},{word[-1]},{BoundSymbol.RIGHT}]']])

        # Leave only "checking" productions
        non_generative_productions = {p for p in self.productions
                                      if p.head != ['A1'] and p.head != ['A2'] and p.head != ['A3']}
        max_head_size = max([len(p.head) for p in non_generative_productions])

        # Optimization: do not traverse sentences which were already visited
        visited_sentences = set()

        prods = set()
        while len(sentences) > 0:
            sent = sentences.popleft()
            
            # Optimization: if there is already a final state on the tape, accept it without producing all terminals
            if any([any([f in x for f in self.turing_machine.final_states]) for x in sent]):
                print(len(prods))
                return True

            if tuple(sent) in visited_sentences:
                continue

            # Extending sentences
            for substr_size in range(1, max_head_size + 1):
                for pos in range(len(sent) - substr_size + 1):
                    prefix, substr, suffix = sent[:pos], sent[pos:pos + substr_size], sent[pos + substr_size:]
                    for prod in non_generative_productions:
                        if prod.head == substr:
                            sentences.append(prefix + prod.body + suffix)
                            prods.add(prod)
            visited_sentences.add(tuple(sent))
        print(len(prods))

        return False
