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
            self.variable_context[item.getText()] = {'type': type}

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
        ''' Assign operator context.
            From the variable context perspective, operator doesn't differ much
            from method, so here current_method is assigned and pushed to stack.
        '''
        self.current_method = self.current_class['oper'][ctx.ID().getText()] = {}
        self.code_blocks.append(self.current_method)

    def enterGenParameters(self, ctx):
        ''' Add parameters to the current method context. '''
        if len(ctx.ID()) > 0:
            if 'vars' not in self.current_method:
                self.current_method['vars'] = {}
            for type, name in zip(ctx.genType(), ctx.ID()):
                self.current_method['vars'][name.getText()] = {'type': type.getText()}

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
        ''' Create environment '''
        self.current_class = None
        self.current_method = None
        self.current_code_block = None
        self.expr_stack = []
        self.code_blocks = []
        self.process_expressions = False

    def enterMainDeclaration(self, ctx):
        ''' Create main function structure.'''
        self.code_blocks.append(self.main)
        self.current_method = self.main
        self.current_class = None
        print('Main function')

    def enterClassDeclaration(self, ctx):
        ''' Assign class context '''
        self.current_class = self.classes[ctx.ID().getText()]
        self.current_method = None
        self.current_code_block = None
        print('Class: ' + ctx.ID().getText())

    def enterFunctionDeclaration(self, ctx):
        ''' Assign function context. '''
        self.current_method = self.current_class['func'][ctx.ID().getText()]
        self.code_blocks.append(self.current_method)
        print('Function: ' + ctx.ID().getText())

    def enterConstructorDeclaration(self, ctx):
        ''' Assign constructor context. '''
        self.current_method = self.current_class['init'][ctx.classType().getText()]
        self.code_blocks.append(self.current_method)
        print('Constructor: ' + ctx.classType().getText())

    def enterPredicateDeclaration(self, ctx):
        ''' Assign predicate context. '''
        self.current_method = self.current_class['pred'][ctx.ID().getText()]
        self.code_blocks.append(self.current_method)
        print('Predicate: ' + ctx.ID().getText())

    def enterOperatorDeclaration(self, ctx):
        ''' Assign operator context. '''
        self.current_method = self.current_class['oper'][ctx.ID().getText()]
        self.code_blocks.append(self.current_method)
        print('Operator: ' + ctx.ID().getText())

    def enterGenCodeBlock(self, ctx):
        ''' Restore current variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()
        if 'statements' in self.current_code_block:
            self.statement_index = 0

    def enterOperatorBody(self, ctx):
        ''' Create operator context and push to stack. '''
        self.current_code_block = self.code_blocks.pop()
        if ctx.EXEC() != None:
            exec_block = self.current_code_block['exec']
            self.code_blocks.append(exec_block)
            exec_block['backref'] = self.current_code_block
        eff_block = self.current_code_block['eff']
        self.code_blocks.append(eff_block)
        eff_block['backref'] = self.current_code_block

    def enterOperatorCodeBlock(self, ctx):
        ''' Restore operator variable context from stack'''
        self.current_code_block = self.code_blocks.pop()
        if 'statements' in self.current_code_block:
            self.statement_index = 0

    def enterGoalDeclaration(self, ctx):
        ''' Assign goal context. '''
        self.current_method = self.current_class['goal'][ctx.ID().getText()]
        self.code_blocks.append(self.current_method)

    def enterIfStatement(self, ctx):
        ''' Push current variable context to stack;
            generate if-statement context and push to stack as well. '''
        self.code_blocks.append(self.current_code_block)
        statement = self.current_code_block['statements'][self.statement_index]
        self.statement_index += 1
        # sanity check
        if 'if' not in statement:
            raise Exception("Internal error: if-statement expected, but got this: " + str(statement))
        statement['if']['backref'] = self.current_code_block
        if ctx.ELSE() != None:
            self.code_blocks.append(statement['else'])
            statement['else']['backref'] = self.current_code_block
        if ctx.ELIF() != None and len(ctx.ELIF()) > 0:
            elif_len = len(ctx.ELIF())
            for i in range(elif_len - 1, -1, -1):
                self.code_blocks.append(statement['elif'][i])
                statement['elif'][i]['backref'] = self.current_code_block
        self.code_blocks.append(statement['if'])

    def exitIfStatement(self, ctx):
        ''' Restore variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

    def enterWhileStatement(self, ctx):
        ''' Push current variable context to stack;
            generate while-statement context and push to stack as well. '''
        self.code_blocks.append(self.current_code_block)
        statement = self.current_code_block['statements'][self.statement_index]
        self.statement_index += 1
        # sanity check
        if 'while' not in statement:
            raise Exception("Internal error: while-statement expected, but got this: " + str(statement))
        self.code_blocks.append(statement['while'])
        statement['while']['backref'] = self.current_code_block

    def exitWhileStatement(self, ctx):
        ''' Restore variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

    def enterForStatement(self, ctx):
        ''' Push current variable context to stack;
            generate for-statement context and push to stack as well. '''
        self.code_blocks.append(self.current_code_block)
        statement = self.current_code_block['statements'][self.statement_index]
        self.statement_index += 1
        # sanity check
        if 'for' not in statement:
            raise Exception("Internal error: for-statement expected, but got this: " + str(statement))
        self.code_blocks.append(statement['for'])
        statement['for']['backref'] = self.current_code_block

    def exitForStatement(self, ctx):
        ''' Restore variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

    def enterRetStatement(self, ctx):
        statement = self.current_code_block['statements'][self.statement_index]
        self.statement_index += 1
        # sanity check
        if 'ret' not in statement:
            raise Exception("Internal error: ret-statement expected, but got this: " + str(statement))

    def enterBreakContStatement(self, ctx):
        statement = self.current_code_block['statements'][self.statement_index]
        self.statement_index += 1
        # sanity check
        statement = 'break' if ctx.BREAK() != None else 'cont'
        if statement not in statement:
            raise Exception("Internal error: " + statement + "-statement expected, but got this: " + str(statement))

    def enterExpressionStatement(self, ctx):
        statement = self.current_code_block['statements'][self.statement_index]
        self.statement_index += 1
        # sanity check
        if 'expr' not in statement:
            raise Exception("Internal error: expr-statement expected, but got this: " + str(statement))

    def enterVarDeclarationStatement(self, ctx):
        ''' For DEBUG purposes only: trigger expression processing'''
        self.process_expressions = True

    def exitVarDeclarationStatement(self, ctx):
        ''' Initialize declared variable(s)
            type var = expression
            type var1, var2, ... = (expression1, expression2, ...)     // assignement unpacking
        '''
        self.process_expressions = False
        if ctx.variableInitializer() == None:
            return
        print("Variable declaration statement: " + ctx.genVarDeclaration().genType().getText() + \
            ' ' + ctx.genVarDeclaration().nameList().getText())
        var_context = None
        parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
        if parentContextRuleIndex == EvansParser.RULE_blockStatement:
            var_context = self.current_code_block['vars']
        elif parentContextRuleIndex == EvansParser.RULE_attributeList:
            var_context = self.current_class['attr']
        elif parentContextRuleIndex == EvansParser.RULE_stateList:
            var_context = self.current_class['state']
        else:
            raise Exception("Internal error: variable declaration statement: " + \
                ctx.genVarDeclaration().nameList().getText() + " - unexpected parent context: " + \
                EvansParser.ruleNames[parentContextRuleIndex])
        init_list = []
        counter = 1
        while counter > 0:
            expr_stack_item = self.expr_stack.pop()
            counter -= 1
            if expr_stack_item[0] == 'VariableInitializer':
                counter = expr_stack_item[1]
                continue
            elif expr_stack_item[0] in ['VarExpression', 'LiteralExpression']:
                init_list.insert(0, expr_stack_item)
            else:
                raise Exception("Internal error: " + expr_stack_item[0] + " not implemented yet in variable declaration")
        var_list = []
        for item in ctx.genVarDeclaration().nameList().ID():
            var_name = item.getText()
            var_list.append(var_context[var_name])
        var_list_len = len(var_list)
        init_list_len = len(init_list)
        if var_list_len == init_list_len: # unpacking
            for variable, initializer in zip(var_list, init_list):
                variable['value'] = initializer
        elif var_list_len == 1 and init_list_len > 1:  # List assignment
            var_list[0]['value'] = init_list
        elif init_list_len == 1: # assign single value to multiple variables
            for variable in var_list:
                variable['value'] = init_list[0]
        elif init_list_len == 0:
            for variable in var_list:
                variable['value'] = None
        else:
            raise Exception("Error, unexpected assignment: " + ctx.genVarDeclaration().getText())
        print("Variable declaration and initialization:")
        for variable in var_list:
            pprint.pprint(variable)

# genExpression is used in:
# - variableInitializer
# - operatorBody
# - genStatement
#   - ifStatement
#   - whileStatement
#   - forStatement
#   - retStatement
#   - expressionStatement
# - assignmentStatement
# - genExpression
#   - ParensExpression
#   - AttrExpression
#   - IndexExpression
#   - NotExpression
#   - PrefixExpression
#   - MulDivExpression
#   - AddSubExpression
#   - CompareExpression
#   - EqualExpression
#   - AndExpression
#   - OrExpression
#   - TernaryExpression
# - expressionList

    # def enterParensExpression(self, ctx):
    #     print("Expression with parens: " + ctx.genExpression().getText(), end='')
    #     parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
    #     print("; parent: " + EvansParser.ruleNames[parentContextRuleIndex])
    #
    def exitVariableInitializer(self, ctx):
        ''' If listInitializer is defined, push its length to the expression stack'''
        if not self.process_expressions:
            return
        if ctx.listInitializer() != None:
            self.expr_stack.append(('VariableInitializer', len(ctx.listInitializer().variableInitializer())))

    def exitLiteralExpression(self, ctx):
        if not self.process_expressions:
            return
        parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
        self.expr_stack.append(('LiteralExpression', ctx.getText()))

    def exitVarExpression(self, ctx):
        ''' Variable can be defined in following contexts:
                - code_blocks belong to the current_method (vars)
                - current_class (attrs & states)
                - global (not implemented yet)
        '''
        if not self.process_expressions:
            return
        var_name = ctx.ID().getText()
        # print("Var expression: " + var_name, end='')
        parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
        # print("; parent: " + EvansParser.ruleNames[parentContextRuleIndex])
        context_list = []
        # current method
        if self.current_code_block != None:
            code_block = self.current_code_block
            while True:
                if 'vars' in code_block:
                    context_list.append(code_block['vars'])
                if 'backref' in code_block:
                    code_block = code_block['backref']
                else:
                    break
        # current class
        if self.current_class != None:
            if 'attr' in self.current_class:
                context_list.append(self.current_class['attr'])
            if 'state' in self.current_class:
                context_list.append(self.current_class['state'])
        var_context = None
        for context_item in context_list:
            if var_name in context_item:
                var_context = context_item
                break
        self.expr_stack.append(('VarExpression', var_name, var_context))

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
    #
    # def enterMethodCall(self, ctx):
    #     print('Method call: ', end='')
    #     if(ctx.ID() != None):
    #         print(ctx.ID().getText(), end='')
    #     else:
    #         print(ctx.genType().getText(), end='')
    #     parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
    #     print("; parent: " + EvansParser.ruleNames[parentContextRuleIndex])

    def exitAddSubExpression(self, ctx):
        if not self.process_expressions:
            return
        parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
        right = self.expr_stack.pop()
        left = self.expr_stack.pop()
        op = '+' if ctx.op.type == EvansParser.ADD else '-'
        self.expr_stack.append(('AddSubExpression', left[1] + op + right[1]))

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
