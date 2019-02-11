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
    : 'if' '(' genCondition ')' genCodeBlock ('else' genCodeBlock)?
    | 'for' '(' forControl ')' genCodeBlock
    | 'while' '(' whileControl ')' genCodeBlock
    | 'ret' (genExpression)? ';'
    | ('break' | 'cont') ';'
    ;

genAssignment
    : ID ('.' ID)* '=' genExpression ';'
    ;

genExpression
    : '(' genExpression ')'
    | genLiteral
    | ID ('.' ID)*
    | methodCall
    | '(' genType ')' genExpression
    | genExpression ('++' | '--')
    | ('+'|'-'|'++'|'--') genExpression
    | genExpression ('*'|'/'|'%') genExpression
    | genExpression ('+'|'-') genExpression

    ;

returnType
    : genType
    ;

genType
    : embeddedType
    | classType
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

// Embedded types
LIST : 'list' ;
BOOL : 'bool' ;
STR : 'str' ;

// Whitespaces
WS: [ \t\r\n]+ -> skip ;
