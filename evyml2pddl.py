#!/usr/bin/env python3

# Evans YAML to PDDL converter
# Written by Igor Tikhonin in 2018

import sys, getopt
import yaml
import pprint
from boolparser import *

def usage ():
    print ('evyml2pddl.py [-h | --help] [-o <outputfile> | --output=<outputfile>] input_file.yml')

def btree_to_pddl (root):
    left, right = None, None
    if 'left' in root:
        left = btree_to_pddl(root['left'])
    if 'right' in root:
        right = btree_to_pddl(root['right'])
    if 'left' not in root and 'right' not in root:
        if root['tokenType'] == TokenType.VAR and root['value'].lower() not in ['true', 'false']:
            var = root['value']
            # translate Evans variable_name.predicate_name into PDDL (predicate_name ?variable_name)
            if '.' in var:
                key, attr = var.split('.', 1)
                var = attr + ' ?' + key
            return '(' + var + ')'
        else:
            return root['value']
    if left != None and right != None:
        if root['tokenType'] == TokenType.EQ:  # only simple comparisons are supported for now, e.g. state_variable == 'state'
            var = left
            cmp = right
            if root['left']['tokenType'] != TokenType.VAR:
                var = right
                cmp = left
            if cmp.lower() == 'true':
                cmp = None
            elif cmp.lower() == 'false':
                var = '(not ' + var + ')'
            else:
                cmp = cmp[1:-1]  # strp quotes from strings
            if cmp != None:
                # add state variable name to predicate name
                if ' ?' in var:
                    predic, param = var.split(' ?', 1)
                    var = predic + '_' + cmp + ' ?' + param
                else:
                    var = var[:-1] + '_' + cmp + ')'
            return var
        elif root['tokenType'] == TokenType.OR:
            return '(or ' + left + ' ' + right + ')'
        elif root['tokenType'] == TokenType.AND:
            return '(and ' + left + ' ' + right + ')'
        else:
            raise Exception("Only '==', 'and', 'or', 'not' are supported in logical expressions for now.")
    elif right != None and root['tokenType'] == TokenType.NOT:
        return '(not ' + right + ')'
    else:
        raise Exception("Complex logical expressions not implemented yet.")

def main (argv):
# Parse options
    try:
        opts, args = getopt.getopt(argv, "ho:", ["help", "output="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    output = None
    input = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
    if len(args) == 1:
        input = args[0]
    else:
        usage()
        sys.exit()
# Read YAML file
    with open(input, 'r') as stream:
        try:
            code = yaml.load(stream)
            if not 'classes' in code:
                raise Exception("SYNTAX ERROR: no 'classes' section found in source file.")
            domain = ['(define (domain MINE)', '(:requirements :adl)']
            types = ['(types: ']
            predicates = ['(:predicates']
            actions = []
            for cl_nm, cl_def in code['classes'].items():
                types.append(cl_nm)
                if not 'state' in cl_def:
                    continue
                for st_nm, st_def in cl_def['state'].items():
                    # state variables are translated into PDDL predicates
                    if st_nm == 'vars':
                        for var_nm, var_def in st_def.items():
                            # only Boolean and inline enum types are supported for now
                            if isinstance(var_def, str) and var_def == 'Boolean':
                                prd_name = '_'.join([cl_nm, var_nm])
                                predicates.append('(' + prd_name + ' ?this - ' + cl_nm + ')')
                            elif isinstance(var_def, list):
                                for var_state in var_def:
                                    prd_name = '_'.join([cl_nm, var_nm, var_state])
                                    predicates.append('(' + prd_name + ' ?this - ' + cl_nm + ')')
                            else:
                                raise Exception("SYNTAX ERROR: class " + cl_nm + \
                                    ", variable " + var_nm + " --- variable type is expected to be either Boolean or list")
                    # operators are translated into PDDL actions
                    elif st_nm == 'operators':
                        for op_nm, op_def in st_def.items():
                            actions.append('(:action ' + cl_nm + '_' + op_nm)
                            if 'parameters' in op_def:
                                actions.append(':parameters (?this - ' + cl_nm)
                                if not isinstance(op_def['parameters'], dict):
                                    raise Exception("SYNTAX ERROR: class " + cl_nm + \
                                        ", operator " + op_nm + " --- parameters expected to be dictionary type")
                                for par_nm, par_type in op_def['parameters'].items():
                                    actions.append('?'+ par_nm + ' - ' + par_type)
                                actions.append(')')
                            # parse operator's condition
                            if 'when' in op_def:
                                actions.append(':precondition (and')
                                if not isinstance(op_def['when'], list):
                                    raise Exception("SYNTAX ERROR: class " + cl_nm + \
                                        ", operator " + op_nm + " --- condition expected to be list type")
                                for cond_def in op_def['when']:
                                    # parse logical expressions; expand predicates; add 'this' to local state variables;
                                    tokenized_expr = Tokenizer(cond_def)
                                    for index, token in enumerate(tokenized_expr.tokens):
                                        if tokenized_expr.tokenTypes[index] == TokenType.VAR:
                                            # variable is searched in 'vars' first, then in 'predicates';
                                            # when found in 'predicates', variable is substituted by the predicate
                                            class_nm = cl_nm
                                            var_nm = token
                                            param_nm = 'this'
                                            if '.' in token:
                                                param_nm, var_nm = token.split('.', 1)
                                                if not param_nm in op_def['parameters']:
                                                    raise Exception("SYNTAX ERROR: class " + cl_nm + \
                                                        ", operator " + op_nm + " --- undefined variable " + param_nm + " in condition")
                                                class_nm = op_def['parameters'][param_nm]
                                            if var_nm in code['classes'][class_nm]['state']['vars']:
                                                tokenized_expr.tokens[index] = param_nm + '.' + class_nm + '_' + var_nm
                                            elif var_nm in code['classes'][class_nm]['state']['predicates']:
                                                tokenized_pr = Tokenizer(code['classes'][class_nm]['state']['predicates'][var_nm])
                                                for pr_index, pr_token in enumerate(tokenized_pr.tokens):
                                                    if tokenized_pr.tokenTypes[pr_index] == TokenType.VAR:
                                                        # references from predicates to other predicates are not supported for now
                                                        if pr_token in code['classes'][class_nm]['state']['vars']:
                                                            tokenized_pr.tokens[pr_index] = param_nm + '.' + class_nm + '_' + pr_token
                                                tokenized_expr.tokens[index] = '('+ ' '.join(tokenized_pr.tokens) + ')'
                                            else:
                                                raise Exception("SYNTAX ERROR: class " + cl_nm + \
                                                    ", operator " + op_nm + " --- undefined variable " + var_nm + " in condition")
                                    parsed_expr = BooleanParser(' '.join(tokenized_expr.tokens))
                                    actions.append(btree_to_pddl(parsed_expr.root))
                                actions.append(')')
                            actions.append(')')
            predicates.append(')')
            types.append(')')
            body = domain + types + predicates + actions
            body.append(')')
            print('\n'.join(body))
            # pprint.pprint(code)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
