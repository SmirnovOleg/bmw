from collections import deque
from itertools import product
from math import log2

from Grammar import Production, Grammar
from TuringMachine import Symbol, Direction, TuringMachine


class TMBasedUnrestrictedGrammar(Grammar):
    BLANKS_AT_THE_END_LIMIT = 100

    def __init__(self, tm: TuringMachine):
        productions = set()

        # Add generative productions with additional variables A1, A2 and A3
        productions.add(Production(['A1'], [tm.start_state, 'A2']))
        for a in tm.language_alphabet:
            productions.add(Production(['A2'], [f'[{a},{a}]', 'A2']))
        productions.add(Production(['A2'], ['A3']))
        productions.add(Production(['A3'], [f'[{Symbol.EPS}, {Symbol.BLANK}]', 'A3']))
        productions.add(Production(['A3'], [Symbol.EPS]))

        # Add checking productions which emulate the TM behaviour
        language_alphabet_with_eps = tm.language_alphabet.union({Symbol.EPS})
        for a in language_alphabet_with_eps:
            for (q, c), (p, e, d) in tm.transitions.items():
                if d == Direction.RIGHT:
                    productions.add(Production([q, f'[{a},{c}]'], [f'[{a},{e}]', p]))
        for a, b in product(language_alphabet_with_eps, language_alphabet_with_eps):  # with EPS or not?
            for i in tm.tape_alphabet:
                for (q, c), (p, j, d) in tm.transitions.items():
                    if d == Direction.LEFT:
                        productions.add(Production([f'[{b},{i}]', q, f'[{a},{c}]'], [p, f'[{b},{i}]', f'[{a},{j}]']))

        # Add checking productions which transform a virtual "tape" to a terminal string
        for a in language_alphabet_with_eps:
            for c in tm.tape_alphabet:
                for q in tm.final_states:
                    productions.add(Production([f'[{a},{c}]', q], [q, a, q]))
                    productions.add(Production([q, f'[{a},{c}]'], [q, a, q]))
        for q in tm.final_states:
            productions.add(Production([q], [Symbol.EPS]))

        new_variables = set(f'[{v1},{v2}]' for v1, v2 in product(language_alphabet_with_eps, tm.tape_alphabet))
        self._tm = tm
        super().__init__(
            variables=new_variables.union(tm.states).union({'A1', 'A2', 'A3'}),
            terminals=tm.language_alphabet,
            productions=productions,
            start_variable='A1'
        )

    def accepts(self, word: str) -> bool:
        # Scale up the amount of "[EPS,BLANK]" at the end of a virtual "tape" exponentially
        for blanks_amount in [2 ** p for p in range(int(log2(self.BLANKS_AT_THE_END_LIMIT)))]:
            sentences = deque([['q0']
                               + [f'[{x},{x}]' for x in word]
                               + [f'[{Symbol.EPS},{Symbol.BLANK}]'] * blanks_amount])

            # Leave only "checking" productions
            non_generative_productions = {p for p in self.productions
                                          if p.head != ['A1'] and p.head != ['A2'] and p.head != ['A3']}
            max_head_size = max([len(p.head) for p in non_generative_productions])

            # Optimization: do not traverse sentences which were already visited
            visited_sentences = set()

            while len(sentences) > 0:
                sent = sentences.popleft()

                # If current sentence consist of only terminals or epsilons, check for the given word
                if (all([x in self._tm.language_alphabet or x == Symbol.EPS for x in sent])
                        and ''.join([x for x in sent if x != Symbol.EPS]) == word):
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
                visited_sentences.add(tuple(sent))

        return False
