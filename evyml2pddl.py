#!/usr/bin/env python3

# Evans YAML to PDDL converter
# Written by Igor Tikhonin in 2018

import sys, getopt
import yaml
import pprint
from boolparser import *

# Evans YAML parsing procedure:
# 1. Loop over classes and create list of derived predicates...
# 2. ...

def usage ():
    print ('evyml2pddl.py [-h | --help] [-o <outputfile> | --output=<outputfile>] input_file.yml')

def btree_to_pddl (root):
    left, right = None, None
    if 'left' in root:
        left = btree_to_pddl(root['left'])
    if 'right' in root:
        right = btree_to_pddl(root['right'])
    if 'left' not in root and 'right' not in root:
        return root['value']
    if left != None and right != None:
        if root['tokenType'] == TokenType.EQ:  # only simple comparisons are supported for now
            var = left
            cmp = right
            if root['left']['tokenType'] != TokenType.VAR:
                var = right
                cmp = left
            if cmp.lower() == 'true':
                cmp = None
            elif cmp.lower() == 'false':
                var = 'not (' + var + ')'
            else:
                cmp = cmp[1:-1]  # strp quotes
            if cmp != None:
                var = var + '_' + cmp
            return var
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
            # Translate derived predicates into inline logical expressions
            if not 'classes' in code:
                raise Exception("SYNTAX ERROR: no 'classes' section found in source file.")
            for cl_nm, cl_def in code['classes'].items():
                if 'state' in cl_def and 'predicates' in cl_def['state']:
                    derived_predicates = {}
                    for pr_nm, pr_def in cl_def['state']['predicates'].items():
                        tokenized_expr = Tokenizer(pr_def)
                        # here class name is added to state variables in boolean expressions,
                        # this allows boolean expressions to be translated into PDDL predicates;
                        # predicates are simple for now, i.e. no parameters, no references to other objects
                        for index, token in enumerate(tokenized_expr.tokens):
                            if tokenized_expr.tokenTypes[index] == TokenType.VAR and token in cl_def['state']['vars']:
                                tokenized_expr.tokens[index] = cl_nm + '_' + token
                        parsed_expr = BooleanParser(tokenized_expr).root
                        derived_predicates['_'.join([cl_nm, pr_nm])] = btree_to_pddl(parsed_expr)
                    cl_def['state']['derived_predicates'] = derived_predicates
            domain = ['(define (domain MINE)', '(:requirements :adl)']
            types = ['(types: ']
            predicates = ['(:predicates']
            actions = []
            for cl_nm, cl_def in code['classes'].items():
                types.append(cl_nm)
                if not 'state' in cl_def: continue
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
                                raise Exception("SYNTAX ERROR: class " + cl_nm +
                                    ", variable " + var_nm + " --- variable type is expected to be either Boolean or list")
                    # operators are translated into PDDL actions
                    elif st_nm == 'operators':
                        for op_nm, op_def in st_def.items():
                            actions.append('(:action ' + cl_nm + '_' + op_nm)
                            actions.append(':parameters (?this - ' + cl_nm)
                            op_params = {}
                            if 'parameters' in op_def:
                                if not isinstance(op_def['parameters'], dict):
                                    raise Exception("SYNTAX ERROR: class " + cl_nm +
                                        ", operator " + op_nm + " --- parameters expected to be dictionary type")
                                for par_nm, par_type in op_def['parameters'].items():
                                    actions.append('?'+ par_nm + ' - ' + par_type)
                                    op_params[par_nm] = par_type # list of params to use while parsing conditional expressions
                            actions.append(')')
                            if 'when' in op_def:
                                if not isinstance(op_def['when'], list):
                                    raise Exception("SYNTAX ERROR: class " + cl_nm +
                                        ", operator " + op_nm + " --- condition expected to be list type")
                                for cond_def in op_def['when']:
                                    parsed_expr = BooleanParser(cond_def).root
                                    pprint.pprint(parsed_expr)
                            actions.append(')')
                    # predicates are translated into inline logical expressions
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
