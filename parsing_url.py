
'''
Custom parser to extract information from a similar url structure https://api_root/v1/module/entity/<id>
based on example url parser presented here https://www.accelebrate.com/blog/pyparseltongue-parsing-text-with-pyparsing
'''
from pyparsing import *
url_chars = alphanums + '-_.~%+'
scheme = oneOf('http https')('scheme')
host = Combine(delimitedList(Word(url_chars), '.'))('host')
port = Suppress(':') + Word(nums)('port')

version = Combine(
    Suppress('/')
    +CaselessKeyword('v1')
)('version')
module = Combine(
    Suppress('/')
    +Word(url_chars)
)('module')
entity_type = Combine(
    Suppress('/')
    +Word(url_chars)
)('entity')
entity_id = Combine(
    Suppress('/')
    +Word(url_chars)
)

query_pair = Group(Word(url_chars) + Suppress('=') + Word(url_chars))
query = Group(Suppress('?') + delimitedList(query_pair, '&'))('query')


path = Combine(
  Suppress('/')
  + OneOrMore(~query + Word(url_chars + '/'))
)('path')

url_parser = (
  scheme
  + Suppress('://')
  + host
  + Optional(port)
  + version
  + module
  + entity_type
  + entity_id
  + Optional(query)
)

test_urls = [
  'https://api2.host.com:929/v1/module/entity/test1?q=12231&order=desc&pagination=10&isValid=true'
]
fmt = '{0:10s} {1}'


if __name__ == '__main__':
    for test_url in test_urls:

        print("URL:", test_url)

        tokens = url_parser.parseString(test_url)

        print(tokens, '\n')
        print(fmt.format("Scheme:", tokens.scheme))
        print(fmt.format("Host:", tokens.host))
        print(fmt.format("Port:", tokens.port))
        print(fmt.format("V:", tokens.version))
        print(fmt.format("M:", tokens.module))
        print(fmt.format("E:", tokens.entity))
        #print(fmt.format("Path:", tokens.path))
        print("Query:")
        for key, value in tokens.query:
            print("\t{} ==> {}".format(key, value))
        #print(fmt.format('Fragment:', tokens.fragment))
        print('-' * 60, '\n')