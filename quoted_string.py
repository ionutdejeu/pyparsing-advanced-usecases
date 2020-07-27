import pyparsing as pp


# pyparsing comes with a utility for parsing strings.
string = pp.QuotedString('"', escChar='\\') | pp.QuotedString("'", escChar='\\')


if __name__ == '__main__':
    equation_parser = string.parseString("'dawdaw'")
    print(equation_parser)
    equation_parser = string.parseString('"dawdaw"')
    print(equation_parser)