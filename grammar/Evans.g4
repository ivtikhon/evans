/*
 * Evans grammar
 * Copyright (c) 2019 Igor Tikhonin
 */

grammar Evans;

codeFile
    : classDeclaration+ mainDeclaration?
    ;

classDeclaration
    : CLASS ID '{' classBody '}'
    ;

classBody
    : attributeList? stateList? constructorList? functionList? predicateList? operatorList? goalList?
    ;

attributeList
    : ATTR ':' genVarDeclaration+
    ;

stateList
    : STATE ':' (genVarDeclaration | domainDeclaration)+
    ;

domainDeclaration
    : DOM ID '{' domainList '}'
    ;

domainList
    : ID (',' ID)*
    ;

genVarDeclaration
    : genType varDeclarator (',' varDeclarator)* ';'
    ;

varDeclarator
    : ID ('=' variableInitializer)?
    ;

variableInitializer
    : listInitializer
    | genExpression
    ;

listInitializer
    : '(' (variableInitializer (',' variableInitializer)* )? ')'
    ;

constructorList
    : INIT ':' constructorDeclaration+
    ;

constructorDeclaration
    : classType '(' genParameters? ')' genCodeBlock
    ;

functionList
    : FUNC ':' functionDeclaration+
    ;

goalList
    : GOAL ':' goalDeclaration+
    ;

functionDeclaration
    : ID '(' genParameters? ')' (':' returnType )? genCodeBlock
    ;

goalDeclaration
    : ID '(' genParameters? ')' '{' genExpression '}'
    ;

mainDeclaration
    : MAIN '(' genParameters? ')' genCodeBlock
    ;


genParameters
    : genType ID (',' genType ID)*
    ;

predicateList
    : PRED ':' predicateDeclaration+
    ;

predicateDeclaration
    : ID '(' genParameters? ')' genCodeBlock
    ;

operatorList
    : OPER ':' operatorDeclaration+
    ;

operatorDeclaration
    : ID '(' genParameters? ')' '{' operatorBody '}'
    ;

operatorBody
    : (WHEN ':' genExpression)? EFF ':' operatorCodeBlock (EXEC ':' operatorCodeBlock)?
    ;

operatorCodeBlock
    : blockStatement+
    ;

genCodeBlock
    : '{' blockStatement* '}'
    ;

blockStatement
    : genVarDeclaration
    | genStatement
    | genAssignment
    ;

genStatement
    : IF '(' genExpression ')' genCodeBlock
      (ELIF '(' genExpression ')' genCodeBlock)*
      (ELSE genCodeBlock)?                          # IfStatement
    | WHILE '(' genExpression ')' genCodeBlock      # WhileStatement
    | RET genExpression? ';'                        # RetStatement
    | (BREAK | CONT) ';'                            # BreakContStatement
    | (genExpression '.')? methodCall ';'           # CallStatement
    ;

genAssignment
    : ID ('.' ID)* ('=' | '+=' | '-=' | '*=' | '/=' | '%=') genExpression ';'
    ;

genExpression
    : '(' genExpression ')'                                     # ParensExpression
    | genLiteral                                                # LiteralExpression
    | ID                                                        # VarExpression
    | genExpression '[' genExpression ']'                       # IndexExpression
    | createNew                                                 # NewExpression
    | methodCall                                                # CallExpression
    | typeConversion                                            # TypeConvExpression
    | genExpression '.' (ID | methodCall )                      # AttrExpression
    | '!' genExpression                                         # NotExpression
    | ('+'|'-') genExpression                                   # PrefixExpression
    | genExpression ('*'|'/'|'%') genExpression                 # MulDivExpression
    | genExpression ('+'|'-') genExpression                     # AddSubExpression
    | genExpression ('<'|'>'|'<='|'>='|'!='|'==') genExpression # CompareExpression
    | genExpression '&&' genExpression                          # AndExpression
    | genExpression '||' genExpression                          # OrExpression
    | genExpression '?' genExpression ':' genExpression         # TernaryExpression
    ;

createNew
    : genType '(' expressionList? ')'
    ;

methodCall
    : ID '(' expressionList? ')'
    ;

typeConversion
    : genType '(' genExpression ')'
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
    | FLOAT
    | INT
    | DOM
    | NUM
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
INIT : 'init' ;
GOAL : 'goal' ;
MAIN : 'main' ;

// Embedded types
LIST : 'list' ;
BOOL : 'bool' ;
STR : 'str' ;
FLOAT : 'float' ;
INT : 'int' ;
DOM : 'dom' ;
NUM: 'num' ;

// Identifier
ID  : LETTER (LETTER | '_' | DIGIT)* ;

fragment LETTER : [a-zA-Z] ;
fragment DIGIT : [0-9] ;

// Whitespaces & comments
COMMENT : '#' ~[\r\n\f]* -> skip ;
WS: [ \t\r\n]+ -> skip ;
