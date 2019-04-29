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


    # Enter a parse tree produced by EvansParser#domainList.
    def enterDomainList(self, ctx:EvansParser.DomainListContext):
        pass

    # Exit a parse tree produced by EvansParser#domainList.
    def exitDomainList(self, ctx:EvansParser.DomainListContext):
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


    # Enter a parse tree produced by EvansParser#goalList.
    def enterGoalList(self, ctx:EvansParser.GoalListContext):
        pass

    # Exit a parse tree produced by EvansParser#goalList.
    def exitGoalList(self, ctx:EvansParser.GoalListContext):
        pass


    # Enter a parse tree produced by EvansParser#predicateList.
    def enterPredicateList(self, ctx:EvansParser.PredicateListContext):
        pass

    # Exit a parse tree produced by EvansParser#predicateList.
    def exitPredicateList(self, ctx:EvansParser.PredicateListContext):
        pass


    # Enter a parse tree produced by EvansParser#operatorList.
    def enterOperatorList(self, ctx:EvansParser.OperatorListContext):
        pass

    # Exit a parse tree produced by EvansParser#operatorList.
    def exitOperatorList(self, ctx:EvansParser.OperatorListContext):
        pass


    # Enter a parse tree produced by EvansParser#domainDeclaration.
    def enterDomainDeclaration(self, ctx:EvansParser.DomainDeclarationContext):
        pass

    # Exit a parse tree produced by EvansParser#domainDeclaration.
    def exitDomainDeclaration(self, ctx:EvansParser.DomainDeclarationContext):
        pass


    # Enter a parse tree produced by EvansParser#functionDeclaration.
    def enterFunctionDeclaration(self, ctx:EvansParser.FunctionDeclarationContext):
        pass

    # Exit a parse tree produced by EvansParser#functionDeclaration.
    def exitFunctionDeclaration(self, ctx:EvansParser.FunctionDeclarationContext):
        pass


    # Enter a parse tree produced by EvansParser#goalDeclaration.
    def enterGoalDeclaration(self, ctx:EvansParser.GoalDeclarationContext):
        pass

    # Exit a parse tree produced by EvansParser#goalDeclaration.
    def exitGoalDeclaration(self, ctx:EvansParser.GoalDeclarationContext):
        pass


    # Enter a parse tree produced by EvansParser#mainDeclaration.
    def enterMainDeclaration(self, ctx:EvansParser.MainDeclarationContext):
        pass

    # Exit a parse tree produced by EvansParser#mainDeclaration.
    def exitMainDeclaration(self, ctx:EvansParser.MainDeclarationContext):
        pass


    # Enter a parse tree produced by EvansParser#nameList.
    def enterNameList(self, ctx:EvansParser.NameListContext):
        pass

    # Exit a parse tree produced by EvansParser#nameList.
    def exitNameList(self, ctx:EvansParser.NameListContext):
        pass


    # Enter a parse tree produced by EvansParser#constructorDeclaration.
    def enterConstructorDeclaration(self, ctx:EvansParser.ConstructorDeclarationContext):
        pass

    # Exit a parse tree produced by EvansParser#constructorDeclaration.
    def exitConstructorDeclaration(self, ctx:EvansParser.ConstructorDeclarationContext):
        pass


    # Enter a parse tree produced by EvansParser#genVarDeclaration.
    def enterGenVarDeclaration(self, ctx:EvansParser.GenVarDeclarationContext):
        pass

    # Exit a parse tree produced by EvansParser#genVarDeclaration.
    def exitGenVarDeclaration(self, ctx:EvansParser.GenVarDeclarationContext):
        pass


    # Enter a parse tree produced by EvansParser#variableInitializer.
    def enterVariableInitializer(self, ctx:EvansParser.VariableInitializerContext):
        pass

    # Exit a parse tree produced by EvansParser#variableInitializer.
    def exitVariableInitializer(self, ctx:EvansParser.VariableInitializerContext):
        pass


    # Enter a parse tree produced by EvansParser#listInitializer.
    def enterListInitializer(self, ctx:EvansParser.ListInitializerContext):
        pass

    # Exit a parse tree produced by EvansParser#listInitializer.
    def exitListInitializer(self, ctx:EvansParser.ListInitializerContext):
        pass


    # Enter a parse tree produced by EvansParser#genParameters.
    def enterGenParameters(self, ctx:EvansParser.GenParametersContext):
        pass

    # Exit a parse tree produced by EvansParser#genParameters.
    def exitGenParameters(self, ctx:EvansParser.GenParametersContext):
        pass


    # Enter a parse tree produced by EvansParser#predicateDeclaration.
    def enterPredicateDeclaration(self, ctx:EvansParser.PredicateDeclarationContext):
        pass

    # Exit a parse tree produced by EvansParser#predicateDeclaration.
    def exitPredicateDeclaration(self, ctx:EvansParser.PredicateDeclarationContext):
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


    # Enter a parse tree produced by EvansParser#operatorCodeBlock.
    def enterOperatorCodeBlock(self, ctx:EvansParser.OperatorCodeBlockContext):
        pass

    # Exit a parse tree produced by EvansParser#operatorCodeBlock.
    def exitOperatorCodeBlock(self, ctx:EvansParser.OperatorCodeBlockContext):
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


    # Enter a parse tree produced by EvansParser#varDeclarationStatement.
    def enterVarDeclarationStatement(self, ctx:EvansParser.VarDeclarationStatementContext):
        pass

    # Exit a parse tree produced by EvansParser#varDeclarationStatement.
    def exitVarDeclarationStatement(self, ctx:EvansParser.VarDeclarationStatementContext):
        pass


    # Enter a parse tree produced by EvansParser#IfStatement.
    def enterIfStatement(self, ctx:EvansParser.IfStatementContext):
        pass

    # Exit a parse tree produced by EvansParser#IfStatement.
    def exitIfStatement(self, ctx:EvansParser.IfStatementContext):
        pass


    # Enter a parse tree produced by EvansParser#WhileStatement.
    def enterWhileStatement(self, ctx:EvansParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by EvansParser#WhileStatement.
    def exitWhileStatement(self, ctx:EvansParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by EvansParser#ForStatement.
    def enterForStatement(self, ctx:EvansParser.ForStatementContext):
        pass

    # Exit a parse tree produced by EvansParser#ForStatement.
    def exitForStatement(self, ctx:EvansParser.ForStatementContext):
        pass


    # Enter a parse tree produced by EvansParser#RetStatement.
    def enterRetStatement(self, ctx:EvansParser.RetStatementContext):
        pass

    # Exit a parse tree produced by EvansParser#RetStatement.
    def exitRetStatement(self, ctx:EvansParser.RetStatementContext):
        pass


    # Enter a parse tree produced by EvansParser#BreakContStatement.
    def enterBreakContStatement(self, ctx:EvansParser.BreakContStatementContext):
        pass

    # Exit a parse tree produced by EvansParser#BreakContStatement.
    def exitBreakContStatement(self, ctx:EvansParser.BreakContStatementContext):
        pass


    # Enter a parse tree produced by EvansParser#ExpressionStatement.
    def enterExpressionStatement(self, ctx:EvansParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by EvansParser#ExpressionStatement.
    def exitExpressionStatement(self, ctx:EvansParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by EvansParser#assignmentStatement.
    def enterAssignmentStatement(self, ctx:EvansParser.AssignmentStatementContext):
        pass

    # Exit a parse tree produced by EvansParser#assignmentStatement.
    def exitAssignmentStatement(self, ctx:EvansParser.AssignmentStatementContext):
        pass


    # Enter a parse tree produced by EvansParser#TernaryExpression.
    def enterTernaryExpression(self, ctx:EvansParser.TernaryExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#TernaryExpression.
    def exitTernaryExpression(self, ctx:EvansParser.TernaryExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#LiteralExpression.
    def enterLiteralExpression(self, ctx:EvansParser.LiteralExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#LiteralExpression.
    def exitLiteralExpression(self, ctx:EvansParser.LiteralExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#VarExpression.
    def enterVarExpression(self, ctx:EvansParser.VarExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#VarExpression.
    def exitVarExpression(self, ctx:EvansParser.VarExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#EqualExpression.
    def enterEqualExpression(self, ctx:EvansParser.EqualExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#EqualExpression.
    def exitEqualExpression(self, ctx:EvansParser.EqualExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#IndexExpression.
    def enterIndexExpression(self, ctx:EvansParser.IndexExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#IndexExpression.
    def exitIndexExpression(self, ctx:EvansParser.IndexExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#NotExpression.
    def enterNotExpression(self, ctx:EvansParser.NotExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#NotExpression.
    def exitNotExpression(self, ctx:EvansParser.NotExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#CompareExpression.
    def enterCompareExpression(self, ctx:EvansParser.CompareExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#CompareExpression.
    def exitCompareExpression(self, ctx:EvansParser.CompareExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#OrExpression.
    def enterOrExpression(self, ctx:EvansParser.OrExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#OrExpression.
    def exitOrExpression(self, ctx:EvansParser.OrExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#ParensExpression.
    def enterParensExpression(self, ctx:EvansParser.ParensExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#ParensExpression.
    def exitParensExpression(self, ctx:EvansParser.ParensExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#AddSubExpression.
    def enterAddSubExpression(self, ctx:EvansParser.AddSubExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#AddSubExpression.
    def exitAddSubExpression(self, ctx:EvansParser.AddSubExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#AndExpression.
    def enterAndExpression(self, ctx:EvansParser.AndExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#AndExpression.
    def exitAndExpression(self, ctx:EvansParser.AndExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#PrefixExpression.
    def enterPrefixExpression(self, ctx:EvansParser.PrefixExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#PrefixExpression.
    def exitPrefixExpression(self, ctx:EvansParser.PrefixExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#AttrExpression.
    def enterAttrExpression(self, ctx:EvansParser.AttrExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#AttrExpression.
    def exitAttrExpression(self, ctx:EvansParser.AttrExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#CallExpression.
    def enterCallExpression(self, ctx:EvansParser.CallExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#CallExpression.
    def exitCallExpression(self, ctx:EvansParser.CallExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#MulDivExpression.
    def enterMulDivExpression(self, ctx:EvansParser.MulDivExpressionContext):
        pass

    # Exit a parse tree produced by EvansParser#MulDivExpression.
    def exitMulDivExpression(self, ctx:EvansParser.MulDivExpressionContext):
        pass


    # Enter a parse tree produced by EvansParser#methodCall.
    def enterMethodCall(self, ctx:EvansParser.MethodCallContext):
        pass

    # Exit a parse tree produced by EvansParser#methodCall.
    def exitMethodCall(self, ctx:EvansParser.MethodCallContext):
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


