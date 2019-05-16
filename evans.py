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
        self.variable_context = self.current_class['attr'] = {}

    def enterStateList(self, ctx):
        ''' Create list of states, assign variable context. '''
        self.variable_context = self.current_class['state'] = {}

    def enterVarDeclarationStatement(self, ctx):
        ''' Assign variable context for code block '''
        parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
        if parentContextRuleIndex == EvansParser.RULE_blockStatement:
            if 'vars' not in self.current_code_block:
                self.current_code_block['vars'] = {}
            self.variable_context = self.current_code_block['vars']

    def enterGenVarDeclaration(self, ctx):
        ''' Add new variables to the current context. '''
        type = ctx.genType().getText()
        for item in ctx.nameList().ID():
            self.variable_context[item.getText()] = {'type': type, 'val': None}

    def enterDomainList(self, ctx):
        ''' Create list of domains. '''
        self.current_class['dom'] = {}

    def enterDomainDeclaration(self, ctx):
        ''' Add domain definition to the current class. '''
        self.current_domain = self.current_class['dom'][ctx.ID().getText()] = []
        for item in ctx.nameList().ID():
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
        if ctx.blockStatement() != None:
            for item in ctx.blockStatement():
                if item.genStatement() != None:
                    self.current_code_block['statements'] = []
                    break

    def enterOperatorBody(self, ctx):
        ''' Create operator context and push to stack. '''
        self.current_code_block = self.code_blocks.pop()
        if ctx.EXEC() != None:
            self.current_code_block['exec'] = exec_block = {}
            self.code_blocks.append(exec_block)
        self.current_code_block['eff'] = eff_block = {}
        self.code_blocks.append(eff_block)
        self.current_code_block = eff_block

    def enterOperatorCodeBlock(self, ctx):
        ''' Restore operator variable context from stack'''
        self.current_code_block = self.code_blocks.pop()
        if ctx.blockStatement() != None:
            for item in ctx.blockStatement():
                if item.genStatement() != None:
                    self.current_code_block['statements'] = []
                    break

    def enterGoalList(self, ctx):
        ''' Create list of goals. '''
        self.current_class['goal'] = {}

    def enterGoalDeclaration(self, ctx):
        ''' Assign goal context. '''
        self.current_method = self.current_class['goal'][ctx.ID().getText()] = {}
        self.code_blocks.append(self.current_method)

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
        if ctx.genVarDeclaration() != None:
            self.variable_context = for_statement['for']['vars'] = {}
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

    def enterExpressionStatement(self, ctx):
        ''' Add expression statement to list. '''
        self.current_code_block['statements'].append('expr')

class EvansCodeTree(EvansListener):
    def enterCodeFile(self, ctx):
        ''' Create operational stacks '''
        # self.expr_stack = []
        self.code_blocks = []

    def enterMainDeclaration(self, ctx):
        ''' Create main function structure.'''
        self.code_blocks.append(self.main)

    def enterClassDeclaration(self, ctx):
        ''' Assign class context '''
        self.current_class = self.classes[ctx.ID().getText()]

    def enterFunctionDeclaration(self, ctx):
        ''' Assign function context. '''
        self.current_method = self.current_class['func'][ctx.ID().getText()]
        self.code_blocks.append(self.current_method)

    def enterConstructorDeclaration(self, ctx):
        ''' Assign constructor context. '''
        self.current_method = self.current_class['init'][ctx.classType().getText()]
        self.code_blocks.append(self.current_method)

    def enterPredicateDeclaration(self, ctx):
        ''' Assign predicate context. '''
        self.current_method = self.current_class['pred'][ctx.ID().getText()]
        self.code_blocks.append(self.current_method)

    def enterOperatorDeclaration(self, ctx):
        ''' Assign operator context. '''
        self.current_method = self.current_class['oper'][ctx.ID().getText()]
        self.code_blocks.append(self.current_method)

    def enterGenCodeBlock(self, ctx):
        ''' Restore current variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()
        if 'statements' in self.current_code_block:
            self.stat_counter = 0

    def enterOperatorBody(self, ctx):
        ''' Create operator context and push to stack. '''
        self.current_code_block = self.code_blocks.pop()
        if ctx.EXEC() != None:
            self.code_blocks.append(self.current_code_block['exec'])
        eff_block = self.current_code_block['eff']
        self.code_blocks.append(eff_block)
        self.current_code_block = eff_block

    def enterOperatorCodeBlock(self, ctx):
        ''' Restore operator variable context from stack'''
        self.current_code_block = self.code_blocks.pop()
        if 'statements' in self.current_code_block:
            self.stat_counter = 0

    def enterGoalDeclaration(self, ctx):
        ''' Assign goal context. '''
        self.current_method = self.current_class['goal'][ctx.ID().getText()]
        self.code_blocks.append(self.current_method)

    def enterIfStatement(self, ctx):
        ''' Push current variable context to stack;
            generate if-statement context and push to stack as well. '''
        self.code_blocks.append(self.current_code_block)
        statement = self.current_code_block['statements'][self.stat_counter]
        self.stat_counter += 1
        # sanity check
        if 'if' not in statement:
            raise Exception("Internal error: if-statement expected, but got this: " + str(statement))
        if ctx.ELSE() != None:
            self.code_blocks.append(statement['else'])
        if ctx.ELIF() != None and len(ctx.ELIF()) > 0:
            elif_len = len(ctx.ELIF())
            for i in range(elif_len - 1, -1, -1):
                self.code_blocks.append(statement['elif'][i])
        self.code_blocks.append(statement['if'])

    def exitIfStatement(self, ctx):
        ''' Restore variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

    def enterWhileStatement(self, ctx):
        ''' Push current variable context to stack;
            generate while-statement context and push to stack as well. '''
        self.code_blocks.append(self.current_code_block)
        statement = self.current_code_block['statements'][self.stat_counter]
        self.stat_counter += 1
        # sanity check
        if 'while' not in statement:
            raise Exception("Internal error: while-statement expected, but got this: " + str(statement))
        self.code_blocks.append(statement['while'])

    def exitWhileStatement(self, ctx):
        ''' Restore variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

    def enterForStatement(self, ctx):
        ''' Push current variable context to stack;
            generate for-statement context and push to stack as well. '''
        self.code_blocks.append(self.current_code_block)
        statement = self.current_code_block['statements'][self.stat_counter]
        self.stat_counter += 1
        # sanity check
        if 'for' not in statement:
            raise Exception("Internal error: for-statement expected, but got this: " + str(statement))
        self.code_blocks.append(statement['for'])

    def exitForStatement(self, ctx):
        ''' Restore variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

    def enterRetStatement(self, ctx):
        statement = self.current_code_block['statements'][self.stat_counter]
        self.stat_counter += 1
        # sanity check
        if 'ret' not in statement:
            raise Exception("Internal error: ret-statement expected, but got this: " + str(statement))

    def enterBreakContStatement(self, ctx):
        statement = self.current_code_block['statements'][self.stat_counter]
        self.stat_counter += 1
        # sanity check
        statement = 'break' if ctx.BREAK() != None else 'cont'
        if statement not in statement:
            raise Exception("Internal error: " + statement + "-statement expected, but got this: " + str(statement))

    def enterExpressionStatement(self, ctx):
        statement = self.current_code_block['statements'][self.stat_counter]
        self.stat_counter += 1
        # sanity check
        if 'expr' not in statement:
            raise Exception("Internal error: expr-statement expected, but got this: " + str(statement))

# genExpression is used in:
# - variableInitializer
# - operatorBody
# - ifStatement
# - whileStatement
# - forStatement
# - retStatement
# - expressionStatement
# - assignmentStatement
# - expressionList

    # def enterParensExpression(self, ctx):
    #     print("Expression with parens: " + ctx.genExpression().getText(), end='')
    #     parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
    #     print("; parent: " + EvansParser.ruleNames[parentContextRuleIndex])
    #
    # def enterLiteralExpression(self, ctx):
    #     print("Literal expression: " + ctx.genLiteral().getText(), end='')
    #     parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
    #     print("; parent: " + EvansParser.ruleNames[parentContextRuleIndex])

    def enterVarExpression(self, ctx):
        ''' Variable can be defined in following contexts:
                - current_code_block (vars)
                - current_method (parameters and vars)
                - current_class (attributes)
                - global (not implemented yet)
        '''
        var_name = ctx.ID().getText()
        # print("Var expression: " + var_name, end='')
        # parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
        # print("; parent: " + EvansParser.ruleNames[parentContextRuleIndex])
        context_list = []
        context_names = ['current code block', 'method params', 'method vars', 'class attrs', 'class states']
        if hasattr(self, 'current_code_block') and 'var' in self.current_code_block:
            context_list.append(self.current_code_block['vars'])
        if hasattr(self, 'current_method') and 'params' in self.current_method:
            context_list.append(self.current_method['params'])
        if hasattr(self, 'current_method') and 'vars' in self.current_method:
            context_list.append(self.current_method['vars'])
        if 'attrs' in self.current_class:
            context_list.append(self.current_class['attr'])
        if 'state' in self.current_class:
            context_list.append(self.current_class['state'])
        var_context = None
        for index, context_item in enumerate(context_list):
            if var_name in context_item:
                var_context = context_item
                break
        if var_context != None:
            print('Var: ' + var_name + ' found in ' + context_names[index])
        else:
            print ('Var: ' + var_name + ' not found')

    # def enterNotExpression(self, ctx):
    #     print("Not expression: " + ctx.genExpression().getText(), end='')
    #     parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
    #     print("; parent: " + EvansParser.ruleNames[parentContextRuleIndex])
    #
    # def enterAndExpression(self, ctx):
    #     print("And expression: " + ctx.genExpression()[0].getText() + ' AND ' + ctx.genExpression()[1].getText(), end='')
    #     parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
    #     print("; parent: " + EvansParser.ruleNames[parentContextRuleIndex])
    #
    # def enterOrExpression(self, ctx):
    #     print("Or expression: " + ctx.genExpression()[0].getText() + ' OR ' + ctx.genExpression()[1].getText(), end='')
    #     parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
    #     print("; parent: " + EvansParser.ruleNames[parentContextRuleIndex])
    #
    # def enterIndexExpression(self, ctx):
    #     print("Index expression: " + ctx.genExpression()[0].getText() + ' -> ' + ctx.genExpression()[1].getText())
    #
    # def enterCallExpression(self, ctx):
    #     print("Method call expression: " + ctx.methodCall().getText(), end='')
    #     parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
    #     print("; parent: " + EvansParser.ruleNames[parentContextRuleIndex])
    #
    # def enterAttrExpression(self, ctx):
    #     ''' Attribute expression
    #         - starts with:
    #             * literal
    #             * ID
    #             * index expression
    #             * method call
    #             * expresson surrounded by parens (not supported);
    #         - continues with:
    #             * ID
    #             * index expression
    #             * method call;
    #         - ends with:
    #             * ID
    #             * method call;
    #     '''
    #     print("Attribute access expression: " + ctx.genExpression().getText(), end=' -> ')
    #     if ctx.ID() != None:
    #         print('ID: ' + ctx.ID().getText(), end='')
    #     elif ctx.methodCall() != None:
    #         print('method: ' + ctx.methodCall().getText(), end='')
    #     parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
    #     print("; parent: " + EvansParser.ruleNames[parentContextRuleIndex])
    #     # self.expr_stack.append(ctx.genExpression())
    #
    # def enterMethodCall(self, ctx):
    #     print('Method call: ', end='')
    #     if(ctx.ID() != None):
    #         print(ctx.ID().getText(), end='')
    #     else:
    #         print(ctx.genType().getText(), end='')
    #     parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
    #     print("; parent: " + EvansParser.ruleNames[parentContextRuleIndex])

def main(argv):
    input = FileStream(argv[1])
    lexer = EvansLexer(input)
    stream = CommonTokenStream(lexer)
    parser = EvansParser(stream)
    tree = parser.codeFile()
    evans_names = EvansNameTree()
    name_walker = ParseTreeWalker()
    # First pass: create name tree
    name_walker.walk(evans_names, tree)
    # pprint.pprint(evans_names.classes)
    # pprint.pprint(evans_names.main)
    # Second pass: generate code
    code_walker = ParseTreeWalker()
    evans_code = EvansCodeTree()
    evans_code.classes = evans_names.classes
    evans_code.main = evans_names.main
    code_walker.walk(evans_code, tree)

if __name__ == '__main__':
    main(sys.argv)
