/*
 * Evans grammar
 * Developed by Igor Tikhonin in 2019
 * (c) All rights reserved
 */

grammar Evans;

file
    : (classDeclaration | mainDeclaration)+
    ;

classDeclaration
    : CLASS ID '{' classBody? '}'
    ;

classBody
    : ( attributeDeclaration
    | stateDeclaration
    | constructorDeclaration
    | functionDeclaration
    | predicateDeclaration
    | operatorDeclaration )
    ;

attributeDeclaration
    : ATTR ':' varDeclaration+
    ;

stateDeclaration
    : STATE ':' varDeclaration+
    ;

varDeclaration
    : genType ID ('=' genExpression)? (',' ID ('=' genExpression)? )* ';'
    ;

constructorDeclaration
    : INIT ':' methodDeclaration+
    ;

functionDeclaration
    : FUNC ':' methodDeclaration+
    ;

methodDeclaration
    : ID '(' methodParameters ')' (':' returnType )? genCodeBlock
    ;

genCodeBlock
    : '{' blockStatement* '}'
    ;

blockStatement
    : varDeclaration
    | genStatement
    | genAssignment
    ;

genStatement
    : IF '(' genCondition ')' genCodeBlock ('else' genCodeBlock)?
    | FOR '(' forControl ')' genCodeBlock
    | WHILE '(' whileControl ')' genCodeBlock
    | RET genExpression? ';'
    | (BREAK | CONT) ';'
    ;

genAssignment
    : ID ('.' ID)* '=' genExpression ';'
    ;

genExpression
    : '(' genExpression ')'
    | genLiteral
    | ID
    | genExpression '.' (ID | methodCall)
    | methodCall
    | '(' genType ')' genExpression
    | genExpression ('++' | '--')
    | ('+'|'-'|'++'|'--') genExpression
    | genExpression ('*'|'/'|'%') genExpression
    | genExpression ('+'|'-') genExpression
    ;

methodCall
    : ID '(' expressionList? ')'
    ;

expressionList
    : genExpression (',' genExpression)*
    ;

returnType
    : genType
    ;

genType
    : embeddedType
    | classType
    ;

genLiteral
    : DECIMAL_LITERAL
    | FLOAT_LITERAL
    | CHAR_LITERAL
    | STRING_LITERAL
    | BOOL_LITERAL
    | NULL_LITERAL
    ;


classType
    : ID
    ;

// Embedded types
embeddedType
    : LIST
    | BOOL
    | STR
    ;

// Identifier
ID  : LETTER (LETTER | '_' | [0-9])* ;

fragment LETTER : [a-zA-Z] ;

// Key words
CLASS : 'class' ;
ATTR  : 'attr' ;
STATE : 'state' ;
INIT  : 'init' ;
FUNC  : 'func' ;
IF    : 'if' ;
ELSE  : 'else' ;
FOR   : 'for' ;
WHILE : 'while' ;
RET   : 'ret' ;
BREAK : 'break' ;
CONT  : 'cont' ;

// Embedded types
LIST : 'list' ;
BOOL : 'bool' ;
STR : 'str' ;

// Whitespaces
WS: [ \t\r\n]+ -> skip ;
