import json
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Set, List, Union, Tuple

from machines.TuringMachine import Symbol, State

Variable = str
Terminal = str
Sentence = List[str]


@dataclass
class Production:
    head: List[Union[Terminal, Variable]]
    body: List[Union[Terminal, Variable]]

    def __hash__(self):
        return hash(tuple(self.head)) * 31 + hash(tuple(self.body))

    def __repr__(self):
        return f'{";".join(self.head)}->{";".join(self.body)}'


@dataclass
class TMBasedGrammar:
    variables: Set[Variable]
    terminals: Set[Terminal]
    gen_productions: Set[Production]
    check_productions: Set[Production]
    term_productions: Set[Production]
    start_variable: Variable
    start_state: State
    blank: Variable = '_'

    def __repr__(self):
        all_prods = self.gen_productions.union(self.check_productions).union(self.term_productions)
        return '\n'.join([str(prod) for prod in all_prods])

    @classmethod
    def from_json(cls, path_to_json: Path):
        with open(path_to_json) as json_file:
            data = json.load(json_file)
            start_variable = data['start_variable']
            start_state = data['start_state']
            terminals = set(data['terminals'])
            blank = data['blank']
            variables = set()
            gen_prods = set()
            for production in data['gen_productions']:
                head, body = production.split("->")
                head, body = head.split(";"), body.split(";")
                variables.update(set(head).union(set(body)))
                gen_prods.add(Production(head, body))
            check_prods = set()
            for production in data['check_productions']:
                head, body = production.split("->")
                head, body = head.split(";"), body.split(";")
                variables.update(set(head).union(set(body)))
                check_prods.add(Production(head, body))
            term_prods = set()
            for production in data['term_productions']:
                head, body = production.split("->")
                head, body = head.split(";"), body.split(";")
                variables.update(set(head).union(set(body)))
                term_prods.add(Production(head, body))
            variables = variables.difference(terminals)
            return cls(variables, terminals, gen_prods, check_prods, term_prods, start_variable, start_state, blank)

    def _inference(self, word_on_tape: List[Variable]) -> Tuple[bool, List[Tuple[Sentence, Production]]]:
        sentences = deque([word_on_tape])
        max_head_size = max([len(p.head) for p in self.check_productions])
        visited_sentences = set()
        derivation = []

        while len(sentences) > 0:
            sent = sentences.popleft()
            if all([x in self.terminals.union([Symbol.EPS]) for x in sent]):
                return True, derivation
            if tuple(sent) in visited_sentences:
                continue
            for substr_size in range(1, max_head_size + 1):
                for pos in range(len(sent) - substr_size + 1):
                    prefix, substr, suffix = sent[:pos], sent[pos:pos + substr_size], sent[pos + substr_size:]
                    for prod in self.check_productions.union(self.term_productions):
                        if prod.head == substr:
                            sentences.append(prefix + prod.body + suffix)
                            derivation.append((sent, prod))
            visited_sentences.add(tuple(sent))

        return False, derivation

    def export(self, filename: Path):
        with open(filename, 'w') as file:
            with open('gen_prods.txt', 'w') as f:
                for prod in self.gen_productions:
                    head = ';'.join([elem for elem in prod.head])
                    body = ''.join([elem for elem in prod.body])
                    f.write(f"\"{head}->{body}\",\n")

            for prod in self.check_productions:
                head = ';'.join([elem for elem in prod.head])
                body = ';'.join([elem for elem in prod.body])
                file.write(f"\"{head}->{body}\",\n")
            
            with open('term_prods.txt', 'w') as f:
                for prod in self.term_productions:
                    head = ';'.join([elem for elem in prod.head])
                    body = ''.join([elem for elem in prod.body])
                    f.write(f"\"{head}->{body}\",\n")

    def export_to_json(self, filename: Path):
        # WIP
        #
        # with open(filename, 'w') as file:
        #     file.write('{\n')
        #     tabs_amount = 1
        #     file.write(tabs_amount * '  ' + '"start_variable": "A1",\n')
        #     file.write(tabs_amount * '  ' + '"final_state": "S",\n')
        #     var_to_name = {var: f'V{counter}' for counter, var in enumerate(self.variables) if var.startswith('[')}
        #     var_to_name[self.start_variable] = 'S'
        #     for prod in self.productions:
        #         head = ' '.join([(elem if elem not in var_to_name else var_to_name[elem]) for elem in prod.head])
        #         body = ' '.join([(elem if elem not in var_to_name else var_to_name[elem]) for elem in prod.body])
        #         file.write(f'{head} -> {body}\n')
        pass