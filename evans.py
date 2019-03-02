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
        ''' Create list of parameters; assign function context. '''
        self.current_method = self.current_class['func'][ctx.ID().getText()] = {'params': {}}

    def enterConstructorDeclaration(self, ctx):
        ''' Create list of parameters; assign constructor context. '''
        self.current_method = self.current_class['init'][ctx.classType().getText()] = {'params': {}}

    def enterPredicateDeclaration(self, ctx):
        ''' Create list of parameters; assign predicate context. '''
        self.current_method = self.current_class['pred'][ctx.ID().getText()] = {'params': {}}

    def enterAttributeList(self, ctx):
        ''' Create list of attributes; assign variable context. '''
        self.current_var = self.current_class['attr'] = {}

    def enterStateList(self, ctx):
        ''' Create list of states; assign variable context. '''
        self.current_var = self.current_class['state'] = {}

    def enterGenVarDeclaration(self, ctx):
        ''' Add new variables to the current list.'''
        contextRuleIndex = ctx.parentCtx.getRuleIndex() # parent context
        if contextRuleIndex != EvansParser.RULE_attributeList:
            print('### varDeclaration,', EvansParser.ruleNames[contextRuleIndex])
            return
        type = ctx.genType().getText()
        for name in ctx.varDeclarator():
            self.current_var[name.ID().getText()] = type

    def enterStateDom(self, ctx):
        name = ctx.ID().getText()
        val = ctx.domainItem().STRING_LITERAL().getText() if ctx.domainItem() != None else "'undef'"
        dom = []
        for item in ctx.domainList().domainItem():
            dom.append(item.STRING_LITERAL().getText())
        self.current_var[name] = {'dom': dom, 'val': val}

    def enterOperatorDeclaration(self, ctx):
        ''' Create list of parameters; assign operator context. '''
        self.current_method = self.current_class['oper'][ctx.ID().getText()] = {'params': {}}

    def enterGenParameters(self, ctx):
        ''' Add parameters to the list. '''
        for type, name in zip(ctx.genType(), ctx.ID()):
            self.current_method['params'][name.getText()] = type.getText()

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
