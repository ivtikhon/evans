#!/usr/bin/env python3

import sys
import pprint
from antlr4 import *
from EvansLexer import EvansLexer
from EvansParser import EvansParser
from EvansListener import EvansListener


class PDDLConverter(EvansListener):
    def exitClassDeclaration(self, ctx):
        print('class: ' + ctx.ID().getText())

    def exitMethodDeclaration(self, ctx):
        print('method: ' + ctx.ID().getText())

    def exitPredicateDeclaration(self, ctx):
        print('pred: ' + ctx.ID().getText())

def main(argv):
    input = FileStream(argv[1])
    lexer = EvansLexer(input)
    stream = CommonTokenStream(lexer)
    parser = EvansParser(stream)
    tree = parser.codeFile()
    pddl_code = PDDLConverter()
    walker = ParseTreeWalker()
    walker.walk(pddl_code, tree)


if __name__ == '__main__':
    main(sys.argv)
