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
    : CLASS ID '{' classBody? '}'
    ;

classBody
    : ( attributeDefinition
    | stateDefinition
    | constructorDefinition
    | functionDefinition
    | predicateDefinition
    | operatorDefiniton )
    ;

ID  : LETTER (LETTER | [0-9])* ;

fragment LETTER : [a-zA-Z] ;

CLASS : 'class';

WS: [ \t\r\n]+ -> skip ;
