#!/usr/bin/env python3

# Evans YAML to PDDL converter
# Written by Igor Tikhonin in 2018

import sys, getopt
import yaml
import pprint
from boolparser import *

def usage ():
    '''This is just usage message'''
    print ('evyml2pddl.py [-h | --help] [-o <outputfile> | --output=<outputfile>] input_file.yml')

def btree_to_pddl (root):
    ''' This procedure translates logical expression supplied in a form of binary tree
            into PDDL formula.
        Input: reference to binary tree root (BooleanParser)
        Output: PDDL formula (string)
    '''
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

def operator_var_to_canonical(variable_name, class_name, context):
    ''' This procedure translates (possible complex) operator variable, into canonical form,
            e.g. (complex variable) var.attribute:
                - attribute converts to state variable
                - var converts to parameter; its class taken from context converts to parameter type
        Input:
            - variable name (string)
            - class where operator is defined (string)
            - context where complex variable is defined, e.g. operator parameters (list)
        Output: [variabe name, parameter name (or 'this'), class name (or None if variable undefined)]
    '''
    parameter = 'this'
    if '.' in variable_name:
        parameter, state_variable = variable_name.split('.', 1)
        if parameter not in context:
            class_name = None
        class_name = context[parameter]
        variable_name = state_variable
    return [variable_name, parameter, class_name]

def operator_effect_to_pddl (effect_sting, class_name, operator_name, classes_root):
    ''' This procedure converts unconditional operator assignment (effect)
            into PDDL formula.
        Input:
            - assignment from operator effect (string)
            - class where operator is defined (string)
            - operator name (string)
            - reference to classes definition (dictionary)
        Output: PDDL formulae (list)
    '''
    pddl_str = []
    tokenized_asgnmt = Tokenizer(exp = effect_sting, singleEqSign = True)
    # assignment format: state_var = value (either Boolean or inline enum item)
    if len(tokenized_asgnmt.tokens) != 3 or tokenized_asgnmt.tokens[1] != '=':
        raise Exception("SYNTAX ERROR: class " + class_name + \
            ", operator " + operator_name + " --- unsupported assignment format: " + effect_sting)
    var_nm, param_nm, class_nm = \
        operator_var_to_canonical(variable_name = tokenized_asgnmt.tokens[0], \
            class_name = class_name, context = \
                classes_root[class_name]['state']['operators'][operator_name]['parameters'])
    if class_nm == None:
        raise Exception("SYNTAX ERROR: class " + class_name + \
            ", operator " + operator_name + " --- undefined variable " + param_nm + " in operator parameters")
    if var_nm not in classes_root[class_nm]['state']['vars']:
        raise Exception("SYNTAX ERROR: class " + class_name + \
            ", operator " + operator_name + " --- undefined variable " + var_nm + " in operator effect")
    var_type = classes_root[class_nm]['state']['vars'][var_nm] # state variable type
    assignment_value = tokenized_asgnmt.tokens[2] # value to be assigned to state variable
    # state variable type is either Boolean...
    if tokenized_asgnmt.tokenTypes[2] == TokenType.VAR and \
            var_type.lower() == 'boolean' and \
            assignment_value.lower() in ['true', 'false']:
        assignment_str = '(' + class_nm + '_' + var_nm + ' ?' + param_nm + ')'
        if assignment_value.lower() == 'false':
            assignment_str = '(not ' + assignment_str + ')'
        pddl_str.append(assignment_str)
    # ...or inline enum (where all values are explisitly listed in state variable definition)
    elif tokenized_asgnmt.tokenTypes[2] == TokenType.STR and \
            isinstance(var_type, list) and assignment_value[1:-1] in var_type:
        pddl_str.append('(and')
        for st_var_val in var_type:
            assignment_str = '(' + class_nm + '_' + var_nm + '_' + st_var_val + ' ?' + param_nm + ')'
            if st_var_val != assignment_value[1:-1]:
                assignment_str = '(not ' + assignment_str + ')'
            pddl_str.append(assignment_str)
        pddl_str.append(')')
    return pddl_str


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
            if 'classes' not in code:
                raise Exception("SYNTAX ERROR: no 'classes' section found in source file.")
            domain = ['(define (domain MINE)', '(:requirements :adl)']
            types = ['(types: ']
            predicates = ['(:predicates']
            actions = []
            for cl_nm, cl_def in code['classes'].items():
                types.append(cl_nm)
                if 'state' not in cl_def:
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
                            # parse parameters
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
                                    # parse logical expressions, expand predicates;
                                    # add 'this' to the current class state variables;
                                    tokenized_expr = Tokenizer(cond_def)
                                    for index, token in enumerate(tokenized_expr.tokens):
                                        if tokenized_expr.tokenTypes[index] == TokenType.VAR:
                                            var_nm, param_nm, class_nm = operator_var_to_canonical(variable_name = token, class_name = cl_nm, context = op_def['parameters'])
                                            if class_nm == None:
                                                raise Exception("SYNTAX ERROR: class " + cl_nm + \
                                                    ", operator " + op_nm + " --- undefined variable " + param_nm + " in operator parameters")
                                            # variable is searched in 'vars' first, then in 'predicates';
                                            # when found in 'predicates', variable is substituted by the predicate
                                            if var_nm in code['classes'][class_nm]['state']['vars']:
                                                tokenized_expr.tokens[index] = param_nm + '.' + class_nm + '_' + var_nm
                                            elif var_nm in code['classes'][class_nm]['state']['predicates']:
                                                tokenized_pr = Tokenizer(code['classes'][class_nm]['state']['predicates'][var_nm])
                                                for pr_index, pr_token in enumerate(tokenized_pr.tokens):
                                                    if tokenized_pr.tokenTypes[pr_index] == TokenType.VAR:
                                                        # references from predicates to other predicates are not supported for now
                                                        # TODO: add exception when undefined variable used in predicate
                                                        if pr_token in code['classes'][class_nm]['state']['vars']:
                                                            tokenized_pr.tokens[pr_index] = param_nm + '.' + class_nm + '_' + pr_token
                                                tokenized_expr.tokens[index] = '('+ ' '.join(tokenized_pr.tokens) + ')'
                                            else:
                                                raise Exception("SYNTAX ERROR: class " + cl_nm + \
                                                    ", operator " + op_nm + " --- undefined variable " + var_nm + " in operator condition")
                                    parsed_expr = BooleanParser(' '.join(tokenized_expr.tokens))
                                    actions.append(btree_to_pddl(parsed_expr.root))
                                actions.append(')')
                            # parse operator's effect
                            if 'effect' in op_def:
                                if not isinstance(op_def['effect'], list):
                                    raise Exception("SYNTAX ERROR: class " + cl_nm + \
                                        ", operator " + op_nm + " --- effect expected to be list type")
                                actions.append(':effect (and')
                                for eff_def in op_def['effect']:
                                    if isinstance(eff_def, dict):
                                        # conditional assignment
                                        actions.append('(conditional effect -- to be done)')
                                    else:
                                        effect_in_pddl = operator_effect_to_pddl(effect_sting = eff_def, \
                                            class_name = cl_nm, operator_name = op_nm, classes_root = code['classes'])
                                        actions.extend(effect_in_pddl) # effect_in_pddl is an array of strings
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