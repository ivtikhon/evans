#!/usr/bin/env python3
#
# Evans interpreter
# Copyright (c) 2019 Igor Tikhonin

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
        self.current_class = {
            'func': {},
            'pred': {},
            'init': {},
            'attr': {},
            'state': {},
            'oper': {}
        }

    def exitClassDeclaration(self, ctx):
        self.classes[ctx.ID().getText()] = self.current_class

    def enterFunctionDeclaration(self, ctx):
        self.current_method = self.current_class['func'][ctx.ID().getText()] = {'parameters': {}}

    def enterConstructorDeclaration(self, ctx):
        self.current_method = self.current_class['init'][ctx.classType().getText()] = {'parameters': {}}

    def enterPredicateDeclaration(self, ctx):
        self.current_method = self.current_class['pred'][ctx.ID().getText()] = {'parameters': {}}

    def enterAttributeList(self, ctx):
        self.current_var = {}

    def exitAttributeList(self, ctx):
        self.current_class['attr'].update(self.current_var)

    def enterStateList(self, ctx):
        self.current_var = {}

    def exitStateList(self, ctx):
        self.current_class['state'].update(self.current_var)

    def enterVarDeclarator(self, ctx):
        self.current_var[ctx.ID().getText()] = {}

    def enterOperatorDeclaration(self, ctx):
        self.current_method = self.current_class['oper'][ctx.ID().getText()] = {'parameters': {}}

    def enterGenParameters(self, ctx):
        for type, name in zip(ctx.genType(), ctx.ID()):
            self.current_method['parameters'][name.getText()] = type.getText()

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
