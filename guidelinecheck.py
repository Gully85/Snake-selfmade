# play around with the guideline-checker pycodestyle

from csv import reader
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


# another made-up guideline that uses state and tokenizing. 
# If a function is defined with "def", it remembers the 
# name of all variables. They must all appear somewhere in the 
# docstring. Since the logical_line mechanism replaces all strings 
# with "xxxx", this must operate on physical lines

# Explaination of regex: Line that starts with "def", capture the word
# between def and (, ignoring all whitespace

# The reader is a finite-state automaton. Allowing TypeHints and 
# Linebreaks (not more than one, only after a comma or after start
# of parameter list) makes several states necessary.

FUNCTION_DEFINITION_REGEX = re.compile(r"\s*def\s+(\w+)\s*\(.*")

import enum
class PAR_READER_STATES(enum.Enum):
    SEARCHING_DEF_KEYWORD = enum.auto()
    METHOD_NAME = enum.auto()
    PROBABLY_VARNAME = enum.auto()
    VARNAME = enum.auto()
    FOUND_VARNAME = enum.auto()
    ONE_MORE_PAR = enum.auto()
    TYPEHINT = enum.auto()
    FOUND_TYPEHINT = enum.auto()
    DOCSTRING = enum.auto()

@pycodestyle.register_check
def undocumented_parameters(physical_line: str, 
                            tokens,
                            checker_state: dict):
    reader_state = checker_state.get('reader_state')
    if reader_state is None:
        if not physical_line.lstrip().startswith("def"):
            return
        reader_state = PAR_READER_STATES.SEARCHING_DEF_KEYWORD
        checker_state['reader_state'] = reader_state
        checker_state['var_names'] = []
        checker_state['vars_mentioned'] = []
        print("entering DEF mode, line = ", physical_line)
        
    for token_type, text, start, end, line in tokens:
        if reader_state == PAR_READER_STATES.SEARCHING_DEF_KEYWORD:
            print("in DEF mode, processing token ", text)
            if token_type == tokenize.NAME and text == "def":
                reader_state = PAR_READER_STATES.METHOD_NAME
                checker_state['reader_state'] = reader_state
                print("found DEF, entering Methodname mode")
            continue
        elif reader_state == PAR_READER_STATES.METHOD_NAME:
            print("in Methodname mode, processing token ", text)
            if token_type == tokenize.NAME:
                checker_state['method_name'] = text
                print("found method name: ", text)
                reader_state = PAR_READER_STATES.PROBABLY_VARNAME
                checker_state["reader_state"] = reader_state
                continue
            else:
                raise SyntaxError("expected Method Name")
        elif reader_state == PAR_READER_STATES.PROBABLY_VARNAME:
            print(start, text)
            if token_type == tokenize.OP and text == "(":
                continue
            elif token_type == tokenize.NAME:
                print("found var name: ", text)
                checker_state['var_names'].append(text)
                checker_state['vars_mentioned'].append(False)
                reader_state = PAR_READER_STATES.FOUND_VARNAME
                checker_state['reader_state'] = reader_state
                continue
            elif token_type == tokenize.OP and text == ")":
                print("found end of par list")
                print("varname summary:", checker_state.get('var_names'))
                checker_state["reader_state"] = PAR_READER_STATES.DOCSTRING
                checker_state.clear()
                return  # could verify that the line ends with ":", but that
                        # would be a SyntaxError anyway
            else:
                raise SyntaxError("expected var name or (, line ="+line)
        elif reader_state == PAR_READER_STATES.FOUND_VARNAME:
            if token_type == tokenize.OP and text == ")":
                print("found end of par list")
                print("varname summary: ", checker_state.get("var_names"))
                checker_state["reader_state"] = PAR_READER_STATES.DOCSTRING
                checker_state.clear()
                return
            elif token_type == tokenize.OP and text == ":":
                print("found TypeHint indicator")
                reader_state = PAR_READER_STATES.TYPEHINT
                checker_state["reader_state"] = reader_state
            elif token_type == tokenize.OP and text == ",":
                print("entering ONEMOREPAR mode")
                reader_state = PAR_READER_STATES.ONE_MORE_PAR
                checker_state["reader_state"] = reader_state
            else:
                print(token_type, text)


    

# run all checks
style = pycodestyle.StyleGuide(config_file="setup.cfg")
result = style.check_files(["codefile_to_check.py"])

