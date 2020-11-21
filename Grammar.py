from dataclasses import dataclass
from typing import Set, List, Union

Variable = str
Terminal = str


@dataclass
class Production:
    head: List[Union[Terminal, Variable]]
    body: List[Union[Terminal, Variable]]


@dataclass
class Grammar:
    variables: Set[Variable]
    terminals: Set[Terminal]
    productions: Set[Production]
    start_variable: Variable
