/*
 * Evans grammar
 * Developed by Igor Tikhonin in 2019
 * (c) All rights reserved
 */

grammar Evans;

codeFile
    : (classDeclaration)+
//    : (classDeclaration | mainDeclaration)+
    ;

classDeclaration
    : CLASS ID '{' classBody '}'
    ;

classBody
    : attributeList? stateList? functionList? predicateList? operatorList?
    ;

attributeList
    : ATTR ':' varDeclaration+
    ;

stateList
    : STATE ':' varDeclaration+
    ;

varDeclaration
    : genType varDeclarator (',' varDeclarator)* ';'
    ;

varDeclarator
    : ID ('=' variableInitializer)?
    ;

variableInitializer
    : arrayInitializer
    | genExpression
    ;

arrayInitializer
    : '(' (variableInitializer (',' variableInitializer)* )? ')'
    ;

functionList
    : FUNC ':' methodDeclaration+
    ;

methodDeclaration
    : ID '(' methodParameters? ')' (':' returnType )? genCodeBlock
    ;

methodParameters
    : genType ID (',' genType ID)*
    ;

predicateList
    : PRED ':' predicateDeclaration+
    ;

predicateDeclaration
    : ID '(' methodParameters? ')' genCodeBlock
    ;

operatorList
    : OPER ':' operatorDeclaration+
    ;

operatorDeclaration
    : ID '(' methodParameters? ')' '{' operatorBody '}'
    ;

operatorBody
    : (WHEN ':' genExpression)? EFF ':' blockStatement+ (EXEC ':' blockStatement+)?
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
    : IF '(' genExpression ')' genCodeBlock (ELIF '(' genExpression ')' genCodeBlock)* (ELSE genCodeBlock)?
//    | FOR '(' forControl ')' genCodeBlock
    | WHILE '(' genExpression ')' genCodeBlock
    | RET genExpression? ';'
    | (BREAK | CONT) ';'
    | (genExpression '.')? methodCall ';'
    ;

genAssignment
    : ID ('.' ID)* ('=' | '+=' | '-=' | '*=' | '/=' | '%=') genExpression ';'
    ;

genExpression
    : '(' genExpression ')'
    | genLiteral
    | ID
    | methodCall
    | typeConversion
    | genExpression '.' (ID | methodCall | typeConversion)
    | genExpression ('++' | '--')
    | 'not' genExpression
    | ('+'|'-'|'++'|'--') genExpression
    | genExpression ('*'|'/'|'%') genExpression
    | genExpression ('+'|'-') genExpression
    | genExpression ('<'|'>'|'<='|'>='|'!='|'==') genExpression
    | genExpression 'and' genExpression
    | genExpression 'or' genExpression
    ;

methodCall
    : ID '(' expressionList? ')'
    ;

typeConversion
    : genType '(' expressionList? ')'
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
    | STRING_LITERAL
    | BOOL_LITERAL
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

// Literals
STRING_LITERAL
    : '"' ( STRING_ESCAPE | ~('\\'|'"') )* '"'
    | '\'' ( STRING_ESCAPE | ~('\''|'\\') )* '\''
    ;

fragment STRING_ESCAPE
    : '\\' [btnfr"'\\]
    ;

DECIMAL_LITERAL
    : DIGIT+
    ;

FLOAT_LITERAL
    : DIGIT+ '.' DIGIT+ EXPONENT?
    | '.' DIGIT+ EXPONENT?
    | DIGIT+ EXPONENT
    ;

BOOL_LITERAL
    : 'true'
    | 'false'
    ;

fragment EXPONENT : [eE] [+-]? DIGIT+ ;

// Key words
CLASS : 'class' ;
ATTR : 'attr' ;
STATE : 'state' ;
FUNC : 'func' ;
PRED : 'pred' ;
OPER : 'oper' ;
IF : 'if' ;
ELSE : 'else' ;
ELIF : 'elif' ;
FOR : 'for' ;
WHILE : 'while' ;
RET : 'ret' ;
BREAK : 'break' ;
CONT : 'cont' ;
WHEN : 'when' ;
EFF : 'eff' ;
EXEC : 'exec' ;

// Embedded types
LIST : 'list' ;
BOOL : 'bool' ;
STR : 'str' ;

// Identifier
ID  : LETTER (LETTER | '_' | DIGIT)* ;

fragment LETTER : [a-zA-Z] ;
fragment DIGIT : [0-9] ;

// Whitespaces & comments
COMMENT : '#' ~[\r\n\f]* -> skip ;
WS: [ \t\r\n]+ -> skip ;
