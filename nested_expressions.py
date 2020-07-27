from pyparsing import *

data_type = oneOf("void int short long char float double")
decl_data_type = Combine(data_type + Optional(Word('*')))
ident = Word(alphas+'_', alphanums+'_')
number = pyparsing_common.number
arg = Group(decl_data_type + ident)
LPAR, RPAR = map(Suppress, "()")

code_body = nestedExpr('{', '}', ignoreExpr=(quotedString | cStyleComment))

c_function = (decl_data_type("type")
              + ident("name")
              + LPAR + Optional(delimitedList(arg), [])("args") + RPAR
              + code_body("body"))
c_function.ignore(cStyleComment)

source_code = '''
    int is_odd(int x) {
        return (x%2);
    }

    int dec_to_hex(char hchar) {
        if (hchar >= '0' && hchar <= '9') {
            return (ord(hchar)-ord('0'));
        } else {
            return (10+ord(hchar)-ord('A'));
        }
    }
'''

if __name__ == '__main__':
    for func in c_function.searchString(source_code):
        print("%(name)s (%(type)s) args: %(args)s" % func)