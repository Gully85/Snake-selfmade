# play around with the guideline-checker pycodestyle

from csv import reader
from lib2to3.pgen2 import token
from tabnanny import check
from unittest.main import MAIN_EXAMPLES
import pycodestyle
import tokenize
import re


# a made-up guideline: Do not compare if 3 == x, always if x == 3.
# in other words: Directly after if, there must not be a constant
# (could be extended to: directly after the keywords and/or/not)
@pycodestyle.register_check
def yoda_condition(logical_line, tokens):
    """Avoid checking constant == variable instead of
    variable == constant.
    
    Okay: if count == 3:
    E715: if 3 == count: 
    """

    directly_behind_if = False
    for token in tokens:
        if token.string == "if":
            directly_behind_if = True
            # print("detected ifcond. Printing token: ", token)
        elif directly_behind_if:
            # print(token)
            if token.type == 2:
                # print("Yoda condition detected")
                yield token.start[1], "E715 in an if-statement, first op can't be a constant"
            directly_behind_if = False
        else:
            directly_behind_if = False



# another made-up guideline to play with regex. Comments must be longer 
# than one word. (zero words are ok)

# Regex explaination: any amount of non-#, then comment sign (1 or more), 
# optional space, a word, any amount of whitespace, end of line
# (\w+ is one or more letter/digit)
ONEWORDCOMMENT_REGEX = re.compile(r"[^#]*#+\s*\w+\s*$")
@pycodestyle.register_check
def one_word_comment(physical_line):
    """Comments should be at least two words long.
    
    Okay: # Hello World
    Okay: x = 3  # this sets x
    E716: pass #kthxbye
    """
    match = ONEWORDCOMMENT_REGEX.match(physical_line)

    if match:
        #print(match)
        return match.end(), "Error: comments should be at least two words long"



# another made-up guideline to play with checkerstate. Any definition (def keyword)
# must be followed by a docstring in the next logical line, i.e. """ or '''
@pycodestyle.register_check
def def_without_docstring(logical_line: str, checker_state: dict):
    if checker_state.get('right_behind_def'):
        if (logical_line.startswith("'''") or
            logical_line.startswith('"""')):
            checker_state["right_behind_def"] = False
        else:
            checker_state["right_behind_def"] = False
            yield 0, "Error: Definition without docstring"
        
    if logical_line.startswith("def"):
        checker_state['right_behind_def'] = True

# moved "all vars must be appear in the docstring" check to the poison stash. 
# If at all, use AST for that.

# run all checks
style = pycodestyle.StyleGuide(config_file="setup.cfg")
result = style.check_files(["codefile_to_check.py"])

print(result)