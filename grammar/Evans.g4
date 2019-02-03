/*
 * Evans grammar
 * Developed by Igor Tikhonin in 2019
 * (c) All rights reserved
 */

grammar Evans;

file
    : (classDefinition | mainDefinition)+
    ;

classDefinition
    : CLASS NL* ID NL* '{' NL* classBody? NL* '}' NL*
    ;

classBody
    : attributeDefinition
    | constructorDefinition
    | functionDefinition
    | predicateDefinition
    | operatorDefiniton
    ;

ID  : LETTER (LETTER | [0-9])* ;

fragment
LETTER : [a-zA-Z] ;

CLASS: 'class';

NL: '\n' | '\r' '\n'? ;

WS: [ \t]+ -> skip ;
