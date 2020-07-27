import pyparsing as pp

# JSON types are number, string, boolean, object, array, and null.
# A boolean is either the literal 'true' or the literal 'false'. Set a
# parsing action that just replaces it with the Python equivalent.
boolean = (
        pp.Keyword('true').setParseAction(pp.replaceWith(True)) |
        pp.Keyword('false').setParseAction(pp.replaceWith(False))
)
null = pp.Keyword('None').setParseAction(pp.replaceWith(None))

# pyparsing comes with a utility for parsing strings.
string = pp.QuotedString('"', escChar='\\') | pp.QuotedString("'", escChar='\\')

# All numbers in JSON are double-precision floating points, equivalent
# to the Python 'float'.
exp = pp.CaselessLiteral('e') + pp.Optional(pp.oneOf('+ -')) + pp.Word(pp.nums)
number = pp.Combine(
    pp.Optional(pp.oneOf('+ -')) +
    pp.Word(pp.nums) +
    pp.Optional('.' + pp.Optional(pp.Word(pp.nums)) + pp.Optional(exp))
)


def number_action(tok):
    return [float(tok[0])]


number.setParseAction(number_action)

# Objects and Arrays are defined in terms of expr, and expr is defined
# in terms of objects and arrays! We can get around this quandary with
# Forward(). Forward() lets us fill in the definition of a type later,
# using the << operator.
expr = pp.Forward()

# Arrays are defined as '[' (expr {',' expr}) ']'
arr = (
        pp.Suppress('[') +
        pp.Optional(pp.delimitedList(expr)('elements')) +
        pp.Suppress(']')
)

# Objects are defined as '{' (string ':' expr {',' string: expr}) '}'
keyval = string('key') + pp.Suppress(':') + expr('value')
obj = (
        pp.Suppress('{') +
        pp.Optional(pp.delimitedList(pp.Group(keyval))('elements')) +
        pp.Suppress('}')
)


# Set actions to convert them into the equivalent Python types.
def arr_action(tok):
    return [list(tok.elements)]


def obj_action(tok):
    return [{t.key: t.value for t in tok.elements}]


arr.setParseAction(arr_action)
obj.setParseAction(obj_action)

# Once we have defined obj and array in terms of expr,
# we can define expr.
expr << (boolean | null | string | number | obj | arr)

# A json document must be either an object or an array.
document = obj | arr


def loads(jsonstring):
    return document.parseString(jsonstring, parseAll=True)[0]


def load(fp):
    return loads(fp.read())

if __name__ == '__main__':
    a = loads('"dawdaw"')
    print(a)