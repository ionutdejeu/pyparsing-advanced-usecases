from pyparsing import *

integer  = Word(nums)            # simple unsigned integer
variable = Char(alphas)          # single letter variable, such as x, z, m, etc.
arithOp = oneOf("+ - * /")      # arithmetic operators
string = QuotedString('"' ) | QuotedString("'")
boolean = (
        CaselessKeyword('true').setParseAction(replaceWith(True)) |
        CaselessKeyword('false').setParseAction(replaceWith(False))
)
LHS = string | integer | boolean | variable

operator = oneOf("= < > <= >= != ")

equation = variable + operator + LHS # will match "x=2+2", etc.



if __name__ == '__main__':
    equation_parser = equation.parseString("a='2'")
    print(equation_parser)

    equation_parser = equation.parseString("a=true")
    print(equation_parser)
