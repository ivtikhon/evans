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

class EvansNameTree(EvansListener):
    def enterCodeFile(self, ctx):
        ''' Create list of classess and variable context stack. '''
        self.classes = {}
        self.code_blocks = []

    def enterMainDeclaration(self, ctx):
        ''' Create main function structure.'''
        self.main = {}
        self.code_blocks.append(self.main)

    def enterClassDeclaration(self, ctx):
        ''' Create class structure, assign class context '''
        self.current_class = self.classes[ctx.ID().getText()] = {}

    def enterFunctionList(self, ctx):
        ''' Create list of functions. '''
        self.current_class['func'] = {}

    def enterFunctionDeclaration(self, ctx):
        ''' Assign function context. '''
        self.current_method = self.current_class['func'][ctx.ID().getText()] = {}
        self.code_blocks.append(self.current_method)

    def enterConstructorList(self, ctx):
        ''' Create list of constructors.'''
        self.current_class['init'] = {}

    def enterConstructorDeclaration(self, ctx):
        ''' Assign constructor context. '''
        self.current_method = self.current_class['init'][ctx.classType().getText()] = {}
        self.code_blocks.append(self.current_method)

    def enterPredicateList(self, ctx):
        ''' Create list of predicates. '''
        self.current_class['pred'] = {}

    def enterPredicateDeclaration(self, ctx):
        ''' Assign predicate context. '''
        self.current_method = self.current_class['pred'][ctx.ID().getText()] = {}
        self.code_blocks.append(self.current_method)

    def enterAttributeList(self, ctx):
        ''' Create list of attrubutes, assign variable context. '''
        self.current_attribute = self.current_class['attr'] = {}

    def enterStateList(self, ctx):
        ''' Create list of states; assign variable context. '''
        self.current_attribute = self.current_class['state'] = {}

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

    def enterDomainList(self, ctx):
        ''' Create list of domains. '''
        self.current_class['dom'] = {}

    def enterDomainDeclaration(self, ctx):
        ''' Add domain definition to the current class. '''
        self.current_domain = self.current_class['dom'][ctx.ID().getText()] = []

    def enterDomainBody(self, ctx):
        ''' Add domain items to the current domain. '''
        for item in ctx.ID():
            self.current_domain.append(item.getText())

    def enterOperatorList(self, ctx):
        ''' Create list of operators. '''
        self.current_class['oper'] = {}

    def enterOperatorDeclaration(self, ctx):
        ''' Create list of parameters; assign operator context.
            From the variable context perspective, operator doesn't differ much
            from method, so here current_method is assigned and pushed to stack.
        '''
        self.current_method = self.current_class['oper'][ctx.ID().getText()] = {}
        self.code_blocks.append(self.current_method)

    def enterGenParameters(self, ctx):
        ''' Add parameters to the list. '''
        if len(ctx.ID()) > 0:
            if 'params' not in self.current_method:
                self.current_method['params'] = {}
            for type, name in zip(ctx.genType(), ctx.ID()):
                self.current_method['params'][name.getText()] = type.getText()

    def enterGenCodeBlock(self, ctx):
        ''' Restore current variable context from stack.
            Context is supposed to be created by syntax elements using
            genCodeBlock (func, pred, if, while, etc...) and pushed to stack.
        '''
        self.current_code_block = self.code_blocks.pop()

    def enterOperatorBody(self, ctx):
        ''' Create operator context and push to stack. '''
        self.current_code_block = self.code_blocks.pop()
        if ctx.EXEC() != None:
            self.current_code_block['exec'] = exec_block = {}
            self.code_blocks.append(exec_block)
        self.current_code_block['eff'] = eff_block = {}
        self.code_blocks.append(eff_block)
        self.current_code_block = eff_block

    def exitOperatorBody(self, ctx):
        self.current_code_block = self.code_blocks.pop()

    def enterGoalList(self, ctx):
        ''' Create list of goals. '''
        self.current_class['goal'] = {}

    def enterGoalDeclaration(self, ctx):
        ''' Assign goal context. '''
        self.current_method = self.current_class['goal'][ctx.ID().getText()] = {}
        self.code_blocks.append(self.current_method)

    def enterBlockStatement(self, ctx):
        ''' Create list of statements for current code block '''
        if ctx.genStatement() != None:
            self.current_code_block['statements'] = []

    def enterIfStatement(self, ctx):
        ''' Push current variable context to stack;
            generate if-statement context and push to stack as well. '''
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
        self.current_code_block['statements'].append(if_statement)

    def exitIfStatement(self, ctx):
        ''' Restore variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

    def enterWhileStatement(self, ctx):
        ''' Push current variable context to stack;
            generate while-statement context and push to stack as well. '''
        self.code_blocks.append(self.current_code_block)
        while_statement = {'while': {}}
        self.code_blocks.append(while_statement['while'])
        self.current_code_block['statements'].append(while_statement)

    def exitWhileStatement(self, ctx):
        ''' Restore variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

    def enterForStatement(self, ctx):
        ''' Push current variable context to stack;
            generate for-statement context and push to stack as well. '''
        self.code_blocks.append(self.current_code_block)
        for_statement = {'for': {}}
        self.code_blocks.append(for_statement['for'])
        self.current_code_block['statements'].append(for_statement)

    def exitForStatement(self, ctx):
        ''' Restore variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

    def enterRetStatement(self, ctx):
        ''' Add return statement to list. '''
        self.current_code_block['statements'].append('ret')

    def enterBreakContStatement(self, ctx):
        ''' Add break/continue statement to list. '''
        statement = 'break' if ctx.BREAK() != None else 'cont'
        self.current_code_block['statements'].append(statement)

    def enterCallStatement(self, ctx):
        ''' Add method call statement to list. '''
        self.current_code_block['statements'].append('call')

def main(argv):
    input = FileStream(argv[1])
    lexer = EvansLexer(input)
    stream = CommonTokenStream(lexer)
    parser = EvansParser(stream)
    tree = parser.codeFile()
    evans_names = EvansNameTree()
    walker = ParseTreeWalker()
    # First pass: create name tree
    walker.walk(evans_names, tree)
    pprint.pprint(evans_names.classes)
    pprint.pprint(evans_names.main)


if __name__ == '__main__':
    main(sys.argv)
