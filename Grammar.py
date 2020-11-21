from dataclasses import dataclass
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
