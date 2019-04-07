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
        self.code_blocks = []

    def exitClassDeclaration(self, ctx):
        self.classes[ctx.ID().getText()] = self.current_class

    def enterFunctionDeclaration(self, ctx):
        ''' Create list of parameters, assign function context '''
        self.current_method = self.current_class['func'][ctx.ID().getText()] = {}
        self.code_blocks.append(self.current_method)

    def enterConstructorDeclaration(self, ctx):
        ''' Create list of parameters, assign function context '''
        self.current_method = self.current_class['init'][ctx.classType().getText()] = {}
        self.code_blocks.append(self.current_method)

    def enterPredicateDeclaration(self, ctx):
        ''' Create list of parameters; assign predicate context. '''
        self.current_method = self.current_class['pred'][ctx.ID().getText()] = {}
        self.code_blocks.append(self.current_method)

    def enterAttributeList(self, ctx):
        ''' Create list of attributes; assign variable context. '''
        self.current_attribute = self.current_class['attr'] = {}

    def enterStateList(self, ctx):
        ''' Create list of states; assign variable context. '''
        self.current_attribute = self.current_class['state'] = {'dom': {}}

    def enterGenVarDeclaration(self, ctx):
        ''' Add new variables to the current context. '''
        parentContextRuleIndex = ctx.parentCtx.getRuleIndex() # get parent context
        variable_context = None
        if parentContextRuleIndex in [EvansParser.RULE_attributeList, EvansParser.RULE_stateList]:
            variable_context = self.current_attribute
        elif parentContextRuleIndex == EvansParser.RULE_blockStatement:
            if 'vars' not in self.current_code_block:
                self.current_code_block['vars'] = {}
            variable_context = self.current_code_block['vars']
        # TODO: add error code here if the parent context is unknown
        if variable_context != None:
            type = ctx.genType().getText()
            for item in ctx.varDeclarator():
                name = item.ID().getText()
                variable_context[name] = {'type': type, 'val': None}

    def enterDomainDeclaration(self, ctx):
        ''' Add domain definition to the current class. '''
        domain_list = self.current_class['state']['dom'][ctx.ID().getText()] = []
        for item in ctx.domainList().ID():
            domain_list.append(item.getText())

    def enterOperatorDeclaration(self, ctx):
        ''' Create list of parameters; assign operator context. '''
        self.current_method = self.current_class['oper'][ctx.ID().getText()] = {}

    def enterGenParameters(self, ctx):
        ''' Add parameters to the list. '''
        if len(ctx.ID()) > 0:
            if 'params' not in self.current_method:
                self.current_method['params'] = {}
            for type, name in zip(ctx.genType(), ctx.ID()):
                self.current_method['params'][name.getText()] = type.getText()

    def enterGenCodeBlock(self, ctx):
        ''' Restore current variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

    def enterIfStatement(self, ctx):
        ''' Push current variable context to stack;
            generate conditional statement context and push to stack as well. '''
        self.code_blocks.append(self.current_code_block)
        if_statement = {'if': {}}
        if ctx.ELSE() != None:
            if_statement['else'] = {}
            self.code_blocks.append(if_statement['else'])
        if ctx.ELIF() != None and len(ctx.ELIF()) > 0:
            elif_len = len(ctx.ELIF())
            if_statement['elif'] = [{}] * elif_len
            for i in range(elif_len - 1, -1, -1):
                self.code_blocks.append(if_statement['elif'][i])
        self.code_blocks.append(if_statement['if'])
        if 'statements' not in self.current_code_block:
            self.current_code_block['statements'] = []
        self.current_code_block['statements'].append(if_statement)

    def exitIfStatement(self, ctx):
        ''' Restore variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

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
