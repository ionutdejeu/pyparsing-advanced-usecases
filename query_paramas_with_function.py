from pyparsing import *

query_function_type = oneOf("function_a function_b function_c")
LPAR, RPAR = map(Suppress, "()")
qString = QuotedString('"', escChar='\\') | QuotedString("'", escChar='\\')

c_function = (query_function_type("query_method_name")
              + LPAR + qString("query_method_param") + RPAR)


if __name__ == '__main__':
    equation_parser = c_function.parseString("function_a('dawdaw')")
    print(equation_parser.query_method_name)
    print(equation_parser.query_method_param)
    equation_parser = c_function.parseString('function_b("dawdaw")')
    print(equation_parser)


