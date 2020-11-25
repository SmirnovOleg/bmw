from itertools import product

from TMBasedGrammar import Production, TMBasedGrammar
from TuringMachine import Symbol, Directions, TuringMachine


class UnrestrictedGrammar(TMBasedGrammar):
    def __init__(self, *args, **kwargs):
        super(UnrestrictedGrammar, self).__init__(*args, **kwargs)

    @classmethod
    def from_turing_machine(cls, turing_machine: TuringMachine):
        gen_prods = set()

        # Add generative productions with additional variables A1, A2 and A3
        gen_prods.add(Production(['A1'], [turing_machine.start_state, 'A2']))
        for a in turing_machine.language_alphabet:
            gen_prods.add(Production(['A2'], [f'[{a},{a}]', 'A2']))
        gen_prods.add(Production(['A2'], ['A3']))
        gen_prods.add(Production(['A3'], [f'[{Symbol.EPS}, {turing_machine.blank}]', 'A3']))
        gen_prods.add(Production(['A3'], [Symbol.EPS]))

        # Add checking productions which emulate the TM behaviour
        check_prods = set()
        language_alphabet_with_eps = turing_machine.language_alphabet.union({Symbol.EPS})
        for a in language_alphabet_with_eps:
            for (q, c), (p, e, d) in turing_machine.transitions.items():
                if d == Directions.RIGHT:
                    check_prods.add(Production([q, f'[{a},{c}]'], [f'[{a},{e}]', p]))
        for a, b in product(language_alphabet_with_eps, language_alphabet_with_eps):
            for i in turing_machine.tape_alphabet:
                for (q, c), (p, j, d) in turing_machine.transitions.items():
                    if d == Directions.LEFT:
                        check_prods.add(Production([f'[{b},{i}]', q, f'[{a},{c}]'], [p, f'[{b},{i}]', f'[{a},{j}]']))

        # Add terminal productions which transform a virtual "tape" to a terminal string
        term_prods = set()
        for a in language_alphabet_with_eps:
            for c in turing_machine.tape_alphabet:
                for q in turing_machine.final_states:
                    term_prods.add(Production([f'[{a},{c}]', q], [q, a, q]))
                    term_prods.add(Production([q, f'[{a},{c}]'], [q, a, q]))
        for q in turing_machine.final_states:
            term_prods.add(Production([q], [Symbol.EPS]))

        new_variables = \
            set(f'[{v1},{v2}]' for v1, v2 in product(language_alphabet_with_eps, turing_machine.tape_alphabet))
        return cls(
            variables=new_variables.union(turing_machine.states).union({'A1', 'A2', 'A3'}),
            terminals=turing_machine.language_alphabet,
            gen_productions=gen_prods,
            check_productions=check_prods,
            term_productions=term_prods,
            start_variable='A1',
            blank=turing_machine.blank
        )

    def accepts(self, word: str) -> bool:
        word_on_tape = (
                [f'[{Symbol.EPS},{self.blank}]']
                + ['q0']
                + [f'[{x},{x}]' for x in word]
                + [f'[{Symbol.EPS},{self.blank}]']
        )
        return self._accepts(word_on_tape)
