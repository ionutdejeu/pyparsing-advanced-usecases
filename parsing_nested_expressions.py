from pyparsing import *

class UnaryOperation(object):
    def __init__(self, tokens):
        self.op, self.operands = tokens[0]


class BinaryOperation(object):
    def __init__(self, tokens):
        self.op = tokens[0][1]
        self.operands = tokens[0][0::2]


class SearchAnd(BinaryOperation):
    def __repr__(self):
        return '(' + ' & '.join(['{}'.format(oper) for oper in self.operands]) + ')'


class SearchOr(BinaryOperation):
    def __repr__(self):
        return '(' + ' | '.join(['{}'.format(oper) for oper in self.operands]) + ')'


class SearchXor(BinaryOperation):
    def __repr__(self):
        return '(' + ' ^ '.join(['{}'.format(oper) for oper in self.operands]) + ')'


class SearchNot(UnaryOperation):
    def __repr__(self):
        return 'TAGS[\'all\'] - {}'.format(self.operands)


class SearchTerm(object):
    def __init__(self, tokens):
        self.term = tokens[0]

    def __repr__(self):
        'instead of just the  term, we represent it as TAGS[term]'
        return 'TAGS[\'{0}\']'.format(self.term)


# the grammar
and_ = CaselessLiteral("and")
or_ = CaselessLiteral("or")
xor_ = CaselessLiteral("xor")
not_ = CaselessLiteral("not")

searchTerm = Word(alphanums) | quotedString.setParseAction(removeQuotes)
searchTerm.setParseAction(SearchTerm)

searchExpr = operatorPrecedence(searchTerm,
                                [(not_, 1, opAssoc.RIGHT, SearchNot),
                                 (and_, 2, opAssoc.LEFT, SearchAnd),
                                 (xor_, 2, opAssoc.LEFT, SearchXor),
                                 (or_, 2, opAssoc.LEFT, SearchOr)])

if __name__ == '__main__':
    print(searchExpr.parseString('not kpt')[0])
    print(searchExpr.parseString('not (kpt and eos)')[0])
    print(searchExpr.parseString('kpt or not eos)')[0])
    print(searchExpr.parseString('wood and blue or red')[0])
    print(searchExpr.parseString('wood and blue xor red')[0])


