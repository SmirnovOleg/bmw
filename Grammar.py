from dataclasses import dataclass
from pathlib import Path
from typing import Set, List, Union

Variable = str
Terminal = str


@dataclass
class Production:
    head: List[Union[Terminal, Variable]]
    body: List[Union[Terminal, Variable]]

    def __hash__(self):
        return hash(tuple(self.head)) * 31 + hash(tuple(self.body))

    def __repr__(self):
        return f'{"".join(self.head)} -> {"".join(self.body)}'


@dataclass
class Grammar:
    variables: Set[Variable]
    terminals: Set[Terminal]
    productions: Set[Production]
    start_variable: Variable

    def __repr__(self):
        return '\n'.join([str(prod) for prod in self.productions])

    def export(self, filename: Path):
        with open(filename, 'w') as file:
            var_to_name = {var: f'V{counter}' for counter, var in enumerate(self.variables) if var.startswith('[')}
            var_to_name[self.start_variable] = 'S'
            for prod in self.productions:
                head = ' '.join([(elem if elem not in var_to_name else var_to_name[elem]) for elem in prod.head])
                body = ' '.join([(elem if elem not in var_to_name else var_to_name[elem]) for elem in prod.body])
                file.write(f'{head} -> {body}\n')

