/*
 * Evans grammar
 * Developed by Igor Tikhonin in 2019
 * (c) All rights reserved
 */

grammar Evans;

file
    : (classDefinition | mainDefinition)+
    ;
