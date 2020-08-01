import pyparsing as pp

class ParsinActionTest(object):
    def __init__(self, tokens):
        self.term = tokens[0]

    def __repr__(self):
        'instead of just the  term, we represent it as TAGS[term]'
        return 'Keyword-{0}'.format(self.term)

# pyparsing comes with a utility for parsing strings.
string = pp.QuotedString('"', escChar='\\') | pp.QuotedString("'", escChar='\\')
string.setParseAction(ParsinActionTest)

if __name__ == '__main__':
    equation_parser = string.parseString("'dawdaw'")
    print(equation_parser)
    equation_parser = string.parseString('"dawdaw"')
    print(equation_parser)