#!/usr/bin/env python3

import sys
import pprint
from antlr4 import *
from EvansLexer import EvansLexer
from EvansParser import EvansParser
from EvansListener import EvansListener


class EvansTree(EvansListener):
    def enterCodeFile(self, ctx):
        self.classes = {}

    def exitCodeFile(self, ctx):
        pprint.pprint(self.classes)

    def enterClassDeclaration(self, ctx):
        self.current_class = {'func': {}, 'pred': {}, 'init': {}}

    def exitClassDeclaration(self, ctx):
        self.classes[ctx.ID().getText()] = self.current_class

    def enterMethodDeclaration(self, ctx):
        self.current_class['func'][ctx.ID().getText()] = {}

    def enterConstructorDeclaration(self, ctx):
        self.current_class['init'][ctx.classType().getText()] = {}

    def enterPredicateDeclaration(self, ctx):
        self.current_class['pred'][ctx.ID().getText()] = {}

def main(argv):
    input = FileStream(argv[1])
    lexer = EvansLexer(input)
    stream = CommonTokenStream(lexer)
    parser = EvansParser(stream)
    tree = parser.codeFile()
    evans_code = EvansTree()
    walker = ParseTreeWalker()
    walker.walk(evans_code, tree)


if __name__ == '__main__':
    main(sys.argv)
