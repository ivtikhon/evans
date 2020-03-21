#!/usr/bin/env python3
#
# Evans interpreter
# Copyright (c) 2020 Igor Tikhonin

import sys
import pprint
import os.path
from antlr4 import *
from EvansLexer import EvansLexer
from EvansParser import EvansParser
from EvansListener import EvansListener

class EvansNameTree(EvansListener):
    def enterCodeFile(self, ctx):
        ''' Create list of classess and variable context stack.
            State labels form the labels namespace at the global level
            to be visible everywhere.
        '''
        self.classes = {}
        self.global_names = {'labels': {}, 'vars': {}}
        self.code_blocks = []  # stack of blocks of code

    def enterMainDeclaration(self, ctx):
        ''' Create main function structure.'''
        self.main = {}
        self.code_blocks.append(self.main)

    def enterClassDeclaration(self, ctx):
        ''' Create class structure, assign class context.
            Attributes and states form the properties namespace.
            Constuctors, functions, predicates and operators
            form the namespace of methods.
        '''
        name = ctx.ID().getText()
        self.current_class = self.classes[name] = {
            'name': name,
            'who': 'class',
        }
        class_body = ctx.classBody()
        attr_list = ['attributeList', 'stateList']
        if any(getattr(class_body, attr)() for attr in attr_list):
            self.current_class['prop_names'] = {}
        method_list = [
            'constructorList', 'functionList',
            'predicateList', 'operatorList'
        ]
        if any(getattr(class_body, method)() for method in method_list):
            self.current_class['method_names'] = {}

    def enterFunctionList(self, ctx):
        ''' Create list of functions. '''
        self.current_class['func'] = {}

    def enterFunctionDeclaration(self, ctx):
        ''' Assign function context. '''
        name = ctx.ID().getText()
        self.current_method = self.current_class['func'][name] = \
            {'name': name, 'who': 'func'}
        # TODO: check if name already registered and print error
        self.current_class['method_names'][name] = 'func'
        self.code_blocks.append(self.current_method)

    def enterConstructorList(self, ctx):
        ''' Create list of constructors.'''
        self.current_class['init'] = {}

    def enterConstructorDeclaration(self, ctx):
        ''' Assign constructor context. '''
        name = ctx.classType().getText()
        self.current_method = self.current_class['init'][name] = \
            {'name': name, 'who': 'init'}
        # TODO: check if name already registered and print error
        self.current_class['method_names'][name] = 'init'
        self.code_blocks.append(self.current_method)

    def enterPredicateList(self, ctx):
        ''' Create list of predicates. '''
        self.current_class['pred'] = {}

    def enterPredicateDeclaration(self, ctx):
        ''' Assign predicate context. '''
        name = ctx.ID().getText()
        self.current_method = self.current_class['pred'][name] = \
            {'name': name, 'who': 'pred'}
        # TODO: check if name already registered and print error
        self.current_class['method_names'][name] = 'pred'
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
            self.current_code_block['statements'].append({'vardec': {}})

    def enterGenVarDeclaration(self, ctx):
        ''' Add new variables to the current context. '''
        genName = True if ctx.genType() else False
        type = ctx.genType().getText() if genName else ctx.primType.text
        nameList = ctx.nameList().ID() if genName else ctx.nameWithAttrList().nameWithAttr()
        for item in nameList:
            name = item.getText() if genName else item.ID().getText()
            self.variable_context[name] = \
                    {'name': name, 'who': 'var', 'type': type}
            # TODO: attributes and states loose their identity here;
            # implement context propagation to keep them different
            # TODO: check if name already registered and print error
            self.current_class['prop_names'][name] = 'prop'

    def enterOperatorList(self, ctx):
        ''' Create list of operators. '''
        self.current_class['oper'] = {}

    def enterOperatorDeclaration(self, ctx):
        ''' Assign operator context.
            From the variable context perspective, operator doesn't differ much
            from method, so here current_method is assigned and pushed to stack.
        '''
        name = ctx.ID().getText()
        self.current_method = self.current_class['oper'][name] = \
            {'name': name, 'who': 'oper'}
        # TODO: check if name already registered and print error
        self.current_class['method_names'][name] = 'oper'
        self.code_blocks.append(self.current_method)

    def enterGenParameters(self, ctx):
        ''' Add parameters to the current method context. '''
        if len(ctx.ID()) > 0:
            if 'vars' not in self.current_method:
                self.current_method['vars'] = {}
            for type, name in zip(ctx.genType(), ctx.ID()):
                self.current_method['vars'][name.getText()] = \
                    {'name': name.getText(), 'type': type.getText(), 'who': 'param'}

    def enterGenCodeBlock(self, ctx):
        ''' Restore current variable context from stack.
            Context is supposed to be created by syntax elements which use
            genCodeBlock (func, pred, if, while, etc...) and pushed to stack.
        '''
        self.current_code_block = self.code_blocks.pop()
        if ctx.blockStatement() != None:
            self.current_code_block['statements'] = []

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
            self.current_code_block['statements'] = []

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

    def enterAssignmentStatement(self, ctx):
        ''' Add assignment statement to list. '''
        self.current_code_block['statements'].append('assign')

class EvansCodeElement:
    CLASS, ATTR, STATE, FUNC, INIT, PRED, OPER, GOAL, MAIN = range(9)
    elementNames = ['CLASS', 'ATTR', 'STATE', 'FUNC', 'INIT', 'PRED',
                    'OPER', 'GOAL', 'MAIN']

class EvansPythonCode:
    def __init__(self):
        self.codeClasses = []
        self.currentIndent = 0 
        self.codeMain = []
    
    def printCode(self):
        print('\n'.join(self.codeClasses + self.codeMain))
        self.currentIndent = 0

    def addClass(self, name):
        self.codeClasses.append('class ' + name + ':')
        self.currentIndent = 1

    def addFunction(self, name):
        self.codeClasses.append(' ' * 4 + 'def ' + name + ':')
        self.currentIndent = 2

    def addMain(self):
        self.codeMain.append('def main:')
        self.currentIndent = 1

    def addLineToClasses(self, line, indent = 0):
        self.codeClasses.append(' ' * (self.currentIndent * 4) + line)
        self.currentIndent += indent

    def addLineToMain(self, line, indent = 0):
        self.codeMain.append(' ' * (self.currentIndent * 4) + line)
        self.currentIndent += indent

class EvansCodeTree(EvansListener):
    def __init__(self, classes, main, global_names):
        self.classes = classes
        self.main = main
        self.globalNames = global_names
        self.debug = False
        self.pythonCode = EvansPythonCode()

    def internalError(self, msg):
        ''' Print internal error and exit '''
        raise Exception(
            'Internal error: ' + msg + '\n' +
            '  Class: ' + self.current_class['name'] + '\n' +
            '  Method: ' + self.current_method['name']
        )

    def runTimeError(self, ctx, msg):
        ''' Print runtime error and exit '''
        startToken = ctx.start
        lineNumber = startToken.line
        inputStream = startToken.getInputStream()
        fileName = os.path.normpath(inputStream.fileName)
        line = inputStream.strdata.split('\n')[lineNumber - 1].strip()
        raise Exception(
            "Runtime error: " + msg + "\n File: " + fileName + "\n Line: " + line
        )

    def getCurrentStatement(self):
        index = self.current_code_block['statement_index']
        return self.current_code_block['statements'][index]

    def getCurrentStatementIncrementIndex(self):
        statement = self.getCurrentStatement()
        self.current_code_block['statement_index'] += 1
        return statement

    def setCurrentStatementIndex(self, index):
        self.current_code_block['statement_index'] = index

    def enterCodeFile(self, ctx):
        ''' Create environment '''
        self.exprStack = []
        self.code_blocks = []
        self.processExpressions = False
        self.currentCodeElement = None

    def enterMainDeclaration(self, ctx):
        ''' Create main function structure.'''
        self.code_blocks.append(self.main)
        self.current_method = self.main
        self.current_class = None
        self.currentCodeElement = EvansCodeElement.MAIN
        if self.debug:
            print('Main function')

    def enterClassDeclaration(self, ctx):
        ''' Assign class context '''
        name = ctx.ID().getText()
        self.current_class = self.classes[name]
        self.current_method = None
        self.current_code_block = None
        self.currentCodeElement = EvansCodeElement.CLASS
        self.pythonCode.addClass(name)
        if self.debug:
            print('Class: ' + name)

    def enterFunctionDeclaration(self, ctx):
        ''' Assign function context. '''
        name = ctx.ID().getText()
        self.current_method = self.current_class['func'][name]
        self.code_blocks.append(self.current_method)
        self.currentCodeElement = EvansCodeElement.FUNC
        self.pythonCode.addFunction(name)
        if self.debug:
            print('Function: ' + name)

    def enterConstructorDeclaration(self, ctx):
        ''' Assign constructor context. '''
        name = ctx.classType().getText()
        self.current_method = self.current_class['init'][name]
        self.code_blocks.append(self.current_method)
        self.currentCodeElement = EvansCodeElement.INIT
        self.pythonCode.addFunction(name)
        if self.debug:
            print('Constructor: ' + name)

    def enterPredicateDeclaration(self, ctx):
        ''' Assign predicate context. '''
        name = ctx.ID().getText()
        self.current_method = self.current_class['pred'][name]
        self.code_blocks.append(self.current_method)
        self.currentCodeElement = EvansCodeElement.PRED
        self.pythonCode.addFunction(name)
        if self.debug:
            print('Predicate: ' + name)

    def enterOperatorDeclaration(self, ctx):
        ''' Assign operator context. '''
        name = ctx.ID().getText()
        self.current_method = self.current_class['oper'][name]
        self.code_blocks.append(self.current_method)
        self.currentCodeElement = EvansCodeElement.OPER
        self.pythonCode.addFunction(name)
        if self.debug:
            print('Operator: ' + name)

    def enterGenCodeBlock(self, ctx):
        ''' Restore current variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()
        if 'statements' in self.current_code_block:
            self.setCurrentStatementIndex(0)

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
            self.setCurrentStatementIndex(0)

    def enterGoalDeclaration(self, ctx):
        ''' Assign goal context. '''
        name = ctx.ID().getText()
        self.current_method = self.current_class['goal'][name]
        self.code_blocks.append(self.current_method)
        self.currentCodeElement = EvansCodeElement.GOAL
        if self.debug:
            print('Goal: ' + name)

    def enterIfStatement(self, ctx):
        ''' Push current variable context to stack;
            generate if-statement context and push to stack as well. '''
        self.code_blocks.append(self.current_code_block)
        statement = self.getCurrentStatementIncrementIndex()
        # sanity check
        if 'if' not in statement:
            self.internalError("if-statement expected, but got this: " + str(statement))
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
        statement = self.getCurrentStatementIncrementIndex()
        # sanity check
        if 'while' not in statement:
            self.internalError("while-statement expected, but got this: " + str(statement))
        self.code_blocks.append(statement['while'])
        statement['while']['backref'] = self.current_code_block

    def exitWhileStatement(self, ctx):
        ''' Restore variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

    def enterForStatement(self, ctx):
        ''' Push current variable context to stack;
            generate for-statement context and push to stack as well. '''
        self.code_blocks.append(self.current_code_block)
        statement = self.getCurrentStatementIncrementIndex()
        # sanity check
        if 'for' not in statement:
            self.internalError("for-statement expected, but got this: " + str(statement))
        self.code_blocks.append(statement['for'])
        statement['for']['backref'] = self.current_code_block

    def exitForStatement(self, ctx):
        ''' Restore variable context from stack. '''
        self.current_code_block = self.code_blocks.pop()

    def enterRetStatement(self, ctx):
        ''' Process ret-statement '''
        statement = self.getCurrentStatementIncrementIndex()
        # sanity check
        if 'ret' not in statement:
            self.internalError("ret-statement expected, but got this: " + str(statement))

    def enterBreakContStatement(self, ctx):
        ''' Process break/cont-statement '''
        statement = self.getCurrentStatementIncrementIndex()
        # sanity check
        control = 'break' if ctx.BREAK() != None else 'cont'
        if control not in statement:
            self.internalError(control + "-statement expected, but got this: " + str(statement))

    def enterExpressionStatement(self, ctx):
        ''' Process expression statement '''
        statement = self.getCurrentStatementIncrementIndex()
        if self.debug:
            print("Expression statement: " + ctx.getText())
        # sanity check
        if 'expr' not in statement:
            self.internalError("expr-statement expected, but got this: " + str(statement))

    def enterAssignmentStatement(self, ctx):
        ''' Process assignment statement '''
        statement = self.getCurrentStatementIncrementIndex()
        if self.debug:
            print("Assignment statement: " + ctx.getText())
        # sanity check
        if 'assign' not in statement:
            self.internalError("assign-statement expected, but got this: " + str(statement))

    # Going down, I declare attributes of classes
    # and local variables

    def enterVarDeclarationStatement(self, ctx):
        ''' Process variable declaration statement'''
        parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
        varDeclarationRef = ctx.genVarDeclaration()
        varTypeRef = varDeclarationRef.genType()
        varNameRef = varDeclarationRef.nameList()
        varTypeNameText = None
        # General type variable or variable with controlled set of values
        if varTypeRef:
            varTypeNameText = varTypeRef.getText()
        else:
            varTypeRef = varDeclarationRef.primType
            varTypeNameText = varTypeRef.text
            varNameRef = varDeclarationRef.nameWithAttrList()
        varNameText = varNameRef.getText()
        if self.debug:
            print("Variable declaration statement: " + varTypeNameText + ' ' + varNameText, end='')
            if ctx.variableInitializer():
                print(' = ' + ctx.variableInitializer().getText(), end='')
            print('')
        self.pythonCode.addLineToClasses(varNameText + ' = None')
        if parentContextRuleIndex == EvansParser.RULE_blockStatement:
            statement = self.getCurrentStatementIncrementIndex()
            # sanity check
            if 'vardec' not in statement:
                self.internalError("var declaration statement expected, but got this: " + str(statement))
            # DEVELOPMENT IN PROGRESS - Expression processing trigger - ON
            self.processExpressions = True

    # Going up, I assign values to attributes and local variables

    def exitVarDeclarationStatement(self, ctx):
        ''' Initialize declared variable(s)
            type var = expression
            type var1, var2, ... = (expression1, expression2, ...)     // assignement unpacking
            e.g. str [set('s1', 's2')] a, [set('s10', 's20')] b = ('s1', 's10')
        '''
        # DEVELOPMENT IN PROGRESS - Expression processing trigger - OFF
        self.processExpressions = False
        if not ctx.variableInitializer():
            return

        if ctx.variableInitializer().listInitializer():
            self.internalError("List initializer is not implemented yet")

        # codeRef = self.current_class['code']
        # # The context is a code block, or a class
        # parentContextRuleIndex = ctx.parentCtx.getRuleIndex()
        # if parentContextRuleIndex == EvansParser.RULE_blockStatement:
        #     codeRef = self.current_code_block['code']
        # # Convert declarations into assignments
        # if codeRef:
        #     codeRef.append()

    #     init_list = []
    #     counter = 1
    #     while counter > 0:
    #         exprStack_item = self.exprStack.pop()
    #         counter -= 1
    #         if exprStack_item[0] == 'VariableInitializer':
    #             counter = exprStack_item[1]
    #             continue
    #         elif exprStack_item[0] in ['VarExpression', 'LiteralExpression']:
    #             init_list.insert(0, exprStack_item)
    #         else:
    #             raise Exception("Internal error: " + exprStack_item[0] + " not implemented yet in variable declaration")
    #     var_list = []
    #     for item in ctx.genVarDeclaration().nameList().ID():
    #         var_name = item.getText()
    #         var_list.append(code[var_name])
    #     var_list_len = len(var_list)
    #     init_list_len = len(init_list)
    #     if var_list_len == init_list_len: # unpacking
    #         for variable, initializer in zip(var_list, init_list):
    #             variable['value'] = initializer
    #     elif var_list_len == 1 and init_list_len > 1:  # List assignment
    #         var_list[0]['value'] = init_list
    #     elif init_list_len == 1: # assign single value to multiple variables
    #         for variable in var_list:
    #             variable['value'] = init_list[0]
    #     elif init_list_len == 0:
    #         for variable in var_list:
    #             variable['value'] = None
    #     else:
    #         raise Exception("Error, unexpected assignment: " + ctx.genVarDeclaration().getText())
    #     print("Variable declaration and initialization:")
    #     for variable in var_list:
    #         pprint.pprint(variable)

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
    # def exitVariableInitializer(self, ctx):
    #     ''' If listInitializer is defined, push its length to the expression stack'''
    #     if not self.processExpressions:
    #         return
    #     if ctx.listInitializer() != None:
    #         self.exprStack.append(('VariableInitializer', len(ctx.listInitializer().variableInitializer())))

    def exitLiteralExpression(self, ctx):
        ''' Process literals '''
        literal = ctx.genLiteral().getText()
        if self.debug:
            print("LiteralExpression: " + literal)
        if not self.processExpressions:
            return
        self.exprStack.append(('LiteralExpression', literal))

    def exitVarExpression(self, ctx):
        ''' Variable can be defined in following contexts:
                - code_blocks belong to the current_method (vars);
                - current_class (attrs & states);
                - global.
        '''
        varName = ctx.ID().getText()
        if self.debug:
            print("VarExpression: " + varName)
        if not self.processExpressions:
            return

        methodCodeElements = [EvansCodeElement.FUNC, EvansCodeElement.INIT,
                            EvansCodeElement.PRED, EvansCodeElement.OPER,
                            EvansCodeElement.MAIN]
        varContext = None
        # Search in method variables
        if self.currentCodeElement in methodCodeElements:
            codeBlock = self.current_code_block
            while True:
                if 'vars' in codeBlock and varName in codeBlock['vars']:
                    varContext = 'method'
                    break
                if 'backref' in codeBlock:
                    codeBlock = codeBlock['backref']
                else:
                    break
        # Search in class properties
        if not varContext and varName in self.current_class['prop_names']:
            varContext = 'class'
        # Search globally
        if not varContext and varName in self.globalNames['vars']:
            varContext = 'global'

        if not varContext:
            self.runTimeError(ctx, "Variable is not defined: " + varName)

        self.exprStack.append(('VarExpression', varName, varContext))

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
    def exitAttrExpression(self, ctx):
        ''' Member access expression
            - starts with:
                * literal
                * ID
                * index expression
                * method call
                * expresson surrounded by parens (not supported);
            - continues with:
                * ID
                * index expression
                * method call;
            - ends with:
                * ID
                * method call;
        '''
        if self.debug:
            print("Attribute access expression: " + ctx.genExpression().getText(), end=' -> ')
            if ctx.ID() != None:
                print('ID: ' + ctx.ID().getText(), end='')
            elif ctx.methodCall() != None:
                print('method: ' + ctx.methodCall().getText(), end='')
            print("")

    def exitCallExpression(self, ctx):
        ''' Process local method call '''
        method = ctx.methodCall()
        if self.debug:
            print('Local method call: ', end='')
            if(method.ID()):
                print(method.ID().getText(), end='')
            else:
                print(method.genType().getText(), end='')
            print("")

    # def exitAddSubExpression(self, ctx):
    #     if not self.processExpressions:
    #         return
    #     self.exprStack.append(('AddSubExpression', ctx.op.type))

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
    # pprint.pprint(evans_names.global_names)
    # pprint.pprint(evans_names.main)
    # Second pass: generate code
    code_walker = ParseTreeWalker()
    evans_code = EvansCodeTree(
        classes = evans_names.classes,
        main = evans_names.main,
        global_names = evans_names.global_names
    )
    # evans_code.debug = True
    code_walker.walk(evans_code, tree)
    evans_code.pythonCode.printCode()
    # pprint.pprint(evans_code.classes)
    # # # for cl_name, cl_def in evans_code.classes.items():
    # # #     print('\n'.join(cl_def['code']))

if __name__ == '__main__':
    main(sys.argv)
