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
        ''' Create class structure '''
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
        ''' Create list of parameters, assign function context '''
        self.current_method = self.current_class['func'][ctx.ID().getText()] = {
            'params': {},
            'body': {}
        }

    def enterConstructorDeclaration(self, ctx):
        ''' Create list of parameters, assign function context '''
        self.current_method = self.current_class['init'][ctx.classType().getText()] = {
            'params': {},
            'body': {}
        }

    def enterPredicateDeclaration(self, ctx):
        ''' Create list of parameters; assign predicate context. '''
        self.current_method = self.current_class['pred'][ctx.ID().getText()] = {'params': {}}

    def enterAttributeList(self, ctx):
        ''' Create list of attributes; assign variable context. '''
        self.current_var = self.current_class['attr'] = {}

    def enterStateList(self, ctx):
        ''' Create list of states; assign variable context. '''
        self.current_var = self.current_class['state'] = {'dom': {}}

    def enterGenVarDeclaration(self, ctx):
        ''' Add new variables to the current list. '''
        parentContextRuleIndex = ctx.parentCtx.getRuleIndex() # get parent context
        if parentContextRuleIndex not in [EvansParser.RULE_attributeList, EvansParser.RULE_stateList]:
            print('### varDeclaration,', EvansParser.ruleNames[parentContextRuleIndex])
            return
        type = ctx.genType().getText()
        # TODO: implement variable initialization (variableInitializer)
        for item in ctx.varDeclarator():
            name = item.ID().getText()
            self.current_var[name] = {'type': type, 'val': None}

    def enterDomainDeclaration(self, ctx):
        ''' Add domain definition to the current class. '''
        domain_list = self.current_class['state']['dom'][ctx.ID().getText()] = []
        for item in ctx.domainList().ID():
            domain_list.append(item.getText())

    def enterOperatorDeclaration(self, ctx):
        ''' Create list of parameters; assign operator context. '''
        self.current_method = self.current_class['oper'][ctx.ID().getText()] = {'params': {}}

    def enterGenParameters(self, ctx):
        ''' Add parameters to the list. '''
        for type, name in zip(ctx.genType(), ctx.ID()):
            self.current_method['params'][name.getText()] = type.getText()

    def enterOperatorBody(self, ctx):
        if ctx.WHEN():
            pass

    def enterGenCodeBlock(self, ctx):
        parentContextRuleIndex = ctx.parentCtx.getRuleIndex() # get parent context
        if parentContextRuleIndex == RULE_functionDeclaration:
            self.current_code_block = self.current_method['body']
            self.current_code_block['vars'] = {}

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
