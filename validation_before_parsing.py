'''
Based on tutorial https://noahgilmore.com/blog/pyparsing-trees/
'''
from pyparsing import *

class FunctionParseToken(object):

    def __repr__(self):
        'instead of just the  term, we represent it as TAGS[term]'
        return 'Tokens'.format(self.tokens)

def action(string, location, tokens):
    print(string,location,tokens)
    return tokens

class Item:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return "{Item: %s}" % self.value

def transform(string, location, tokens):
    return [Item(token) for token in tokens]

def test_condition(tokens,**kwargs):
    print('condition check on'+str(tokens))
    return True


query_function_type = oneOf("function_a function_b function_c")
LPAR, RPAR = map(Suppress, "()")
qString = QuotedString('"', escChar='\\') | QuotedString("'", escChar='\\')

c_function = (query_function_type("query_method_name")
              + LPAR + qString("query_method_param") + RPAR)

c_function.addParseAction(action)
c_function.addParseAction(transform)
c_function.addCondition(test_condition)
c_function.addCondition(lambda toks: len(toks[0].value)>202, message="Only support years 2000 and later")

if __name__ == '__main__':
    equation_parser = c_function.parseString("function_b(\"dawdaw\")")
    equation_parser = c_function.parseString('function_a("dawdaw")')
    print(equation_parser)




