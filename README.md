## Arithmetic Expressions Language Checker

A tool for checking correctness of arithmetic expressions
(**multiplications**) using Type-0 and Type-1 grammars. 
Currently implemented with **unary** numeral system. 

### Usage

You will need only Python 3.8 to run the tool from command line:

`python main.py grammar word`

 - `grammar`: could be `t0` (to use Recursively enumerable grammar) or `t1` 
(to use Context-sensitive grammar), required argument
 - `word`: a word to check for correctness, use symbols `1`, `*`, and `=` 
 without spaces, required argument
 
 #### Examples

 - `python main.py t0 1*11=1`
 - `python main.py t1 111*11=111111`


