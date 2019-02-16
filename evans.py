#!/usr/bin/env python3

import sys
from antlr4 import *
from EvansLexer import EvansLexer
from EvansParser import EvansParser

def main(argv):
    input = FileStream(argv[1])
    lexer = EvansLexer(input)
    stream = CommonTokenStream(lexer)
    parser = EvansParser(stream)
    tree = parser.codeFile()

if __name__ == '__main__':
    main(sys.argv)
