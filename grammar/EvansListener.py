# Generated from grammar/Evans.g4 by ANTLR 4.7.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .EvansParser import EvansParser
else:
    from EvansParser import EvansParser

# This class defines a complete listener for a parse tree produced by EvansParser.
class EvansListener(ParseTreeListener):

    # Enter a parse tree produced by EvansParser#codeFile.
    def enterCodeFile(self, ctx:EvansParser.CodeFileContext):
        pass

    # Exit a parse tree produced by EvansParser#codeFile.
    def exitCodeFile(self, ctx:EvansParser.CodeFileContext):
        pass


    # Enter a parse tree produced by EvansParser#classDeclaration.
    def enterClassDeclaration(self, ctx:EvansParser.ClassDeclarationContext):
        pass

    # Exit a parse tree produced by EvansParser#classDeclaration.
    def exitClassDeclaration(self, ctx:EvansParser.ClassDeclarationContext):
        pass


    # Enter a parse tree produced by EvansParser#classBody.
    def enterClassBody(self, ctx:EvansParser.ClassBodyContext):
        pass

    # Exit a parse tree produced by EvansParser#classBody.
    def exitClassBody(self, ctx:EvansParser.ClassBodyContext):
        pass


    # Enter a parse tree produced by EvansParser#attributeList.
    def enterAttributeList(self, ctx:EvansParser.AttributeListContext):
        pass

    # Exit a parse tree produced by EvansParser#attributeList.
    def exitAttributeList(self, ctx:EvansParser.AttributeListContext):
        pass


    # Enter a parse tree produced by EvansParser#stateList.
    def enterStateList(self, ctx:EvansParser.StateListContext):
        pass

    # Exit a parse tree produced by EvansParser#stateList.
    def exitStateList(self, ctx:EvansParser.StateListContext):
        pass


    # Enter a parse tree produced by EvansParser#varDeclaration.
    def enterVarDeclaration(self, ctx:EvansParser.VarDeclarationContext):
        pass

    # Exit a parse tree produced by EvansParser#varDeclaration.
    def exitVarDeclaration(self, ctx:EvansParser.VarDeclarationContext):
        pass


    # Enter a parse tree produced by EvansParser#varDeclarator.
    def enterVarDeclarator(self, ctx:EvansParser.VarDeclaratorContext):
        pass

    # Exit a parse tree produced by EvansParser#varDeclarator.
    def exitVarDeclarator(self, ctx:EvansParser.VarDeclaratorContext):
        pass


    # Enter a parse tree produced by EvansParser#variableInitializer.
    def enterVariableInitializer(self, ctx:EvansParser.VariableInitializerContext):
        pass

    # Exit a parse tree produced by EvansParser#variableInitializer.
    def exitVariableInitializer(self, ctx:EvansParser.VariableInitializerContext):
        pass


    # Enter a parse tree produced by EvansParser#arrayInitializer.
    def enterArrayInitializer(self, ctx:EvansParser.ArrayInitializerContext):
        pass

    # Exit a parse tree produced by EvansParser#arrayInitializer.
    def exitArrayInitializer(self, ctx:EvansParser.ArrayInitializerContext):
        pass


    # Enter a parse tree produced by EvansParser#constructorList.
    def enterConstructorList(self, ctx:EvansParser.ConstructorListContext):
        pass

    # Exit a parse tree produced by EvansParser#constructorList.
    def exitConstructorList(self, ctx:EvansParser.ConstructorListContext):
        pass


    # Enter a parse tree produced by EvansParser#functionList.
    def enterFunctionList(self, ctx:EvansParser.FunctionListContext):
        pass

    # Exit a parse tree produced by EvansParser#functionList.
    def exitFunctionList(self, ctx:EvansParser.FunctionListContext):
        pass


    # Enter a parse tree produced by EvansParser#methodDeclaration.
    def enterMethodDeclaration(self, ctx:EvansParser.MethodDeclarationContext):
        pass

    # Exit a parse tree produced by EvansParser#methodDeclaration.
    def exitMethodDeclaration(self, ctx:EvansParser.MethodDeclarationContext):
        pass


    # Enter a parse tree produced by EvansParser#methodParameters.
    def enterMethodParameters(self, ctx:EvansParser.MethodParametersContext):
        pass

    # Exit a parse tree produced by EvansParser#methodParameters.
    def exitMethodParameters(self, ctx:EvansParser.MethodParametersContext):
        pass


    # Enter a parse tree produced by EvansParser#predicateList.
    def enterPredicateList(self, ctx:EvansParser.PredicateListContext):
        pass

    # Exit a parse tree produced by EvansParser#predicateList.
    def exitPredicateList(self, ctx:EvansParser.PredicateListContext):
        pass


    # Enter a parse tree produced by EvansParser#predicateDeclaration.
    def enterPredicateDeclaration(self, ctx:EvansParser.PredicateDeclarationContext):
        pass

    # Exit a parse tree produced by EvansParser#predicateDeclaration.
    def exitPredicateDeclaration(self, ctx:EvansParser.PredicateDeclarationContext):
        pass


    # Enter a parse tree produced by EvansParser#operatorList.
    def enterOperatorList(self, ctx:EvansParser.OperatorListContext):
        pass

    # Exit a parse tree produced by EvansParser#operatorList.
    def exitOperatorList(self, ctx:EvansParser.OperatorListContext):
        pass


    # Enter a parse tree produced by EvansParser#operatorDeclaration.
    def enterOperatorDeclaration(self, ctx:EvansParser.OperatorDeclarationContext):
        pass

    # Exit a parse tree produced by EvansParser#operatorDeclaration.
    def exitOperatorDeclaration(self, ctx:EvansParser.OperatorDeclarationContext):
        pass


    # Enter a parse tree produced by EvansParser#operatorBody.
    def enterOperatorBody(self, ctx:EvansParser.OperatorBodyContext):
        pass

    # Exit a parse tree produced by EvansParser#operatorBody.
    def exitOperatorBody(self, ctx:EvansParser.OperatorBodyContext):
        pass


    # Enter a parse tree produced by EvansParser#genCodeBlock.
    def enterGenCodeBlock(self, ctx:EvansParser.GenCodeBlockContext):
        pass

    # Exit a parse tree produced by EvansParser#genCodeBlock.
    def exitGenCodeBlock(self, ctx:EvansParser.GenCodeBlockContext):
        pass


    # Enter a parse tree produced by EvansParser#blockStatement.
    def enterBlockStatement(self, ctx:EvansParser.BlockStatementContext):
        pass

    # Exit a parse tree produced by EvansParser#blockStatement.
    def exitBlockStatement(self, ctx:EvansParser.BlockStatementContext):
        pass


    # Enter a parse tree produced by EvansParser#genStatement.
    def enterGenStatement(self, ctx:EvansParser.GenStatementContext):
        pass

    # Exit a parse tree produced by EvansParser#genStatement.
    def exitGenStatement(self, ctx:EvansParser.GenStatementContext):
        pass


    # Enter a parse tree produced by EvansParser#genAssignment.
    def enterGenAssignment(self, ctx:EvansParser.GenAssignmentContext):
        pass

    # Exit a parse tree produced by EvansParser#genAssignment.
    def exitGenAssignment(self, ctx:EvansParser.GenAssignmentContext):
        pass


    # Enter a parse tree produced by EvansParser#genExpression.
    def enterGenExpression(self, ctx:EvansParser.GenExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#genExpression.
    def exitGenExpression(self, ctx:EvansParser.GenExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#methodCall.
    def enterMethodCall(self, ctx:EvansParser.MethodCallContext):
        pass

    # Exit a parse tree produced by EvansParser#methodCall.
    def exitMethodCall(self, ctx:EvansParser.MethodCallContext):
        pass


    # Enter a parse tree produced by EvansParser#typeConversion.
    def enterTypeConversion(self, ctx:EvansParser.TypeConversionContext):
        pass

    # Exit a parse tree produced by EvansParser#typeConversion.
    def exitTypeConversion(self, ctx:EvansParser.TypeConversionContext):
        pass


    # Enter a parse tree produced by EvansParser#expressionList.
    def enterExpressionList(self, ctx:EvansParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by EvansParser#expressionList.
    def exitExpressionList(self, ctx:EvansParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by EvansParser#returnType.
    def enterReturnType(self, ctx:EvansParser.ReturnTypeContext):
        pass

    # Exit a parse tree produced by EvansParser#returnType.
    def exitReturnType(self, ctx:EvansParser.ReturnTypeContext):
        pass


    # Enter a parse tree produced by EvansParser#genType.
    def enterGenType(self, ctx:EvansParser.GenTypeContext):
        pass

    # Exit a parse tree produced by EvansParser#genType.
    def exitGenType(self, ctx:EvansParser.GenTypeContext):
        pass


    # Enter a parse tree produced by EvansParser#genLiteral.
    def enterGenLiteral(self, ctx:EvansParser.GenLiteralContext):
        pass

    # Exit a parse tree produced by EvansParser#genLiteral.
    def exitGenLiteral(self, ctx:EvansParser.GenLiteralContext):
        pass


    # Enter a parse tree produced by EvansParser#classType.
    def enterClassType(self, ctx:EvansParser.ClassTypeContext):
        pass

    # Exit a parse tree produced by EvansParser#classType.
    def exitClassType(self, ctx:EvansParser.ClassTypeContext):
        pass


    # Enter a parse tree produced by EvansParser#embeddedType.
    def enterEmbeddedType(self, ctx:EvansParser.EmbeddedTypeContext):
        pass

    # Exit a parse tree produced by EvansParser#embeddedType.
    def exitEmbeddedType(self, ctx:EvansParser.EmbeddedTypeContext):
        pass


