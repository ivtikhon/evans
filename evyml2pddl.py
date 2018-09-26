#!/usr/bin/env python3

# Evans YAML to PDDL converter
# Written by Igor Tikhonin in 2018

import sys, getopt
import yaml
import pprint
from boolparser import *

class Evans:
    classes = None
    main = None
    main_vars = None
    pddl_domain = None

    def __init__(self, classes_root, main_root):
        embedded_classes = {
            'Char': {
                'attr': {}
            },
            'String': {
                'attr': {}
            },
            'Number': {
                'attr': {}
            },
            'List': {
                'attr': {}
            }
        }
        self.classes = classes_root
        self.main = main_root
        self.classes.update(embedded_classes)
        self.main_vars = {}

    def parse_classes(self):
        ''' This procedure translates Evans classes into PDDL
            Input: Evans classes in YAML (self.classes)
            Output: PDDL Domain (self.pddl_domain)
        '''
        header = ['(define (domain MYDOMAIN)', '(:requirements :adl)']
        types = ['(types: ']
        predicates = ['(:predicates']
        actions = []
        for cl_nm, cl_def in self.classes.items():
            types.append(cl_nm)
            if 'state' in cl_def:
                for var_nm, var_def in cl_def['state'].items():
                    # only Boolean and inline enum types are supported for now
                    if isinstance(var_def, str) and var_def.title() == 'Boolean':
                        prd_name = '_'.join([cl_nm, var_nm])
                        predicates.append('(' + prd_name + ' ?this - ' + cl_nm + ')')
                    elif isinstance(var_def, list):
                        for var_state in var_def:
                            prd_name = '_'.join([cl_nm, var_nm, var_state])
                            predicates.append('(' + prd_name + ' ?this - ' + cl_nm + ')')
                    else:
                        raise Exception("SYNTAX ERROR: class " + cl_nm + \
                            ", variable " + var_nm + " --- variable type is expected to be either Boolean or list")
            if 'operators' in cl_def:
                # operators are translated into PDDL actions
                for op_nm, op_def in cl_def['operators'].items():
                    actions.append('(:action ' + cl_nm + '_' + op_nm)
                    # parse operator's parameters
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
                            pddl_cond = self.operator_condition_to_pddl(condition_sting = cond_def, \
                                class_name = cl_nm, operator_name = op_nm)
                            actions.append(pddl_cond)
                        actions.append(')')
                    # parse operator's effect
                    if 'effect' in op_def:
                        if not isinstance(op_def['effect'], list):
                            raise Exception("SYNTAX ERROR: class " + cl_nm + \
                                ", operator " + op_nm + " --- effect expected to be list type")
                        actions.append(':effect (and')
                        for eff_def in op_def['effect']:
                            if any (cond_elem in eff_def for cond_elem in ['if', 'then', 'else']):
                                # conditional assignment
                                try:
                                    pddl_cond = self.operator_condition_to_pddl(condition_sting = eff_def['if'], \
                                        class_name = cl_nm, operator_name = op_nm)
                                    actions.append('(when')
                                    actions.append(pddl_cond)
                                    # multi-level conditional expressions are not supported for now
                                    if 'if' in eff_def['then']:
                                        raise Exception("SYNTAX ERROR: class " + cl_nm + \
                                            ", operator " + op_nm + " --- multilevel conditional statements not supported yet.")
                                    if len(eff_def['then']) > 1:
                                        actions.append('(and')
                                    for cond_eff in eff_def['then']:
                                        pddl_effect = self.operator_effect_to_pddl(effect_definition = cond_eff, \
                                            class_name = cl_nm, operator_name = op_nm)
                                        actions.extend(pddl_effect) # pddl_effect is an array of strings
                                    if len(eff_def['then']) > 1:
                                        actions.append(')')
                                    actions.append(')')
                                    if 'else' in eff_def:
                                        actions.append('(when (not ')
                                        actions.append(pddl_cond)
                                        actions.append(')')
                                        if len(eff_def['else']) > 1:
                                            actions.append('(and')
                                        for cond_eff in eff_def['else']:
                                            pddl_effect = self.operator_effect_to_pddl(effect_definition = cond_eff, \
                                                class_name = cl_nm, operator_name = op_nm)
                                            actions.extend(pddl_effect)
                                        if len(eff_def['else']) > 1:
                                            actions.append(')')
                                        actions.append(')')
                                except KeyError:
                                    raise Exception("SYNTAX ERROR: class " + cl_nm + \
                                        ", operator " + op_nm + " --- conditional effect is expected to be in the if: ... then: ... else: format")
                            else:
                                # unconditional assignment
                                effect_in_pddl = self.operator_effect_to_pddl(effect_definition = eff_def, \
                                    class_name = cl_nm, operator_name = op_nm)
                                actions.extend(effect_in_pddl)
                        actions.append(')')
                    actions.append(')')
            if 'attr' in cl_def:
                for at_nm, at_def in cl_def['attr'].items():
                    if at_def not in self.classes:
                        raise Exception("SYNTAX ERROR: class " + cl_nm + \
                            ", attribute " + at_nm + ", attribute class " + at_def + " --- attribute class is not defined.")
        predicates.append(')')
        types.append(')')
        self.pddl_domain = header + types + predicates + actions + [')']

    def parse_main(self):
        ''' This procedure interpretes the main section of Evan YAML
        '''
        try:
            # initialize variables
            for v in self.main['exec']['vars']:
                class_name = self.main['exec']['vars'][v]
                self.main_vars[v] = {'class': class_name}
                if class_name in self.classes:
                    if 'state' in self.classes[class_name]:
                        self.main_vars[v]['state'] = {}
                        for var_nm, var_def in self.classes[class_name]['state'].items():
                            # Boolean state variables are initialized with 'False';
                            # all other state variables are set to 'undef'
                            # TODO: initialize Number type with 0 (zero)
                            if isinstance(var_def, str) and var_def.title() == 'Boolean':
                                self.main_vars[v]['state'][var_nm] = False
                            else:
                                self.main_vars[v]['state'][var_nm] = 'undef'
                    # attributes are initialized with 'None' for now
                    if 'attr' in self.classes[class_name]:
                        self.main_vars[v]['attr'] = {}
                        for var_nm, var_def in self.classes[class_name]['attr'].items():
                            self.main_vars[v]['attr'][var_nm] = None
                else:
                    raise Exception("SYNTAX ERROR: main section, variable " + v + " is of unknown class " + class_name)
            # parse tasks
            self.exec_tasks_to_pddl(self.main['exec']['tasks'])
        except KeyError:
            raise Exception("SYNTAX ERROR: exec section in main should contain tasks and vars definitions.")

    def exec_tasks_to_pddl (self, tasks):
        ''' This procedure translates the exec tasks in main into PDDL
            Input: list of exec tasks
            Output: none; the return value is used to pass the 'break' signal from the inner loop
        '''
        for item in tasks:
            # only unconditional loop (with break) implemented for now
            if 'loop' in item:
                loop_exit = 'continue'
                while loop_exit != 'break':
                    loop_exit = self.exec_tasks_to_pddl (item['loop'])
            elif 'auto' in item:
                if 'init' in item['auto']:
                    # state variables initialization
                    for assignment in item['auto']['init']:
                        # one assignment per list item
                        if len(assignment) > 1:
                            raise Exception("SYNTAX ERROR: main section, task auto '" + item['auto']['name'] + \
                                "', init section --- only one variable assignment per list item is currently supported")
                        full_var_nm = list(assignment.keys())[0]
                        main_var_nm, state_var_nm = full_var_nm.split('.', 1)
                        self.main_vars[main_var_nm]['state'][state_var_nm] = assignment[full_var_nm]
                try:
                    problem = ['(define (problem MYPROBLEM)', '(:domain MYDOMAIN)']
                    objects = ['(:objects']
                    init = ['(:init']
                    goal = ['(:goal']
                    for obj in item['auto']['objects']:
                        # generate list of object
                        objects.append(obj + ' - ' + self.main_vars[obj]['class'])
                        # initialize objects
                        for var_nm, var_val in self.main_vars[obj]['state'].items():
                            prefix = '('
                            postfix = ')'
                            if isinstance(var_val, bool):
                                if var_val == False:
                                    prefix = '(not ('
                                    postfix = '))'
                                var_val = ''
                            else:
                                var_val = '_' + var_val
                            init.append(prefix + self.main_vars[obj]['class'] + '_' + var_nm + var_val + ' ' + obj + postfix)
                    objects.append(')')
                    init.append(')')
                    goal.append(')')
                    body = problem + objects + init + goal
                    body.append(')')
                    print('\n'.join(body))
                except KeyError:
                    raise Exception("SYNTAX ERROR: auto section in main tasks should contain objects and goal definitions.")
            elif 'break' in item:
                return 'break'
        return 'continue'

    def operator_effect_to_pddl (self, effect_definition, class_name, operator_name):
        ''' This procedure converts operator assignment (effect) into PDDL formula.
            Input:
                - assignment from operator effect (dictionary)
                - class where operator is defined (string)
                - operator name (string)
            Output: PDDL formulae (list of strings)
        '''
        pddl_str = []
        # assignment format: state_var: value (either Boolean or inline enum item)
        if len(effect_definition) > 1:
            raise Exception("SYNTAX ERROR: class " + class_name + \
                ", operator " + operator_name + " --- only one variable assignment per list item is currently supported in operator effect")
        unprocessed_var_nm = list(effect_definition.keys())[0]
        var_nm, param_nm, class_nm = \
            var_to_canonical_form(variable_name = unprocessed_var_nm, \
                    context = self.classes[class_name]['operators'][operator_name]['parameters'], \
                    class_name = class_name)
        if class_nm == None:
            raise Exception("SYNTAX ERROR: class " + class_name + \
                ", operator " + operator_name + " --- undefined variable " + param_nm + " in operator parameters")
        if var_nm not in self.classes[class_nm]['state']:
            raise Exception("SYNTAX ERROR: class " + class_name + \
                ", operator " + operator_name + " --- undefined variable " + var_nm + " in operator effect")
        var_type = self.classes[class_nm]['state'][var_nm] # state variable type
        assignment_value = effect_definition[unprocessed_var_nm] # value to be assigned to state variable
        # state variable type is either Boolean...
        if isinstance(var_type, str) and var_type.title() == 'Boolean' and \
                (isinstance(assignment_value, bool) or assignment_value.title() in ['True', 'False']):
            if isinstance(assignment_value, bool):
                assignment_value = str(assignment_value)
            assignment_str = '(' + class_nm + '_' + var_nm + ' ?' + param_nm + ')'
            if assignment_value.title() == 'False':
                assignment_str = '(not ' + assignment_str + ')'
            pddl_str.append(assignment_str)
        # ...or inline enum (where all values are explisitly listed in state variable definition)
        elif isinstance(var_type, list) and assignment_value in var_type:
            pddl_str.append('(and')
            for st_var_val in var_type:
                assignment_str = '(' + class_nm + '_' + var_nm + '_' + st_var_val + ' ?' + param_nm + ')'
                if st_var_val != assignment_value[1:-1]:
                    assignment_str = '(not ' + assignment_str + ')'
                pddl_str.append(assignment_str)
            pddl_str.append(')')
        else:
            raise Exception("SYNTAX ERROR: class " + class_name + \
                ", operator " + operator_name + ", variable " + var_nm + " --- unsupported variable type in operator effect")
        return pddl_str

    def operator_condition_to_pddl(self, condition_sting, class_name, operator_name):
        ''' This procedure parses Evans YAML conditional statement and
            converts it to PDDL
        '''
        # parse logical expressions, expand predicates;
        # add 'this' to the current class state variables;
        tokenized_expr = Tokenizer(condition_sting)
        for index, token in enumerate(tokenized_expr.tokens):
            if tokenized_expr.tokenTypes[index] == TokenType.VAR:
                var_nm, param_nm, class_nm = var_to_canonical_form(variable_name = token, \
                    context = self.classes[class_name]['operators'][operator_name]['parameters'], \
                    class_name = class_name)
                if class_nm == None:
                    raise Exception("SYNTAX ERROR: class " + class_name + \
                        ", operator " + operator_name + " --- undefined variable " + param_nm + " in operator parameters")
                # variable is searched in 'state' first, then in 'predicates';
                # when found in 'predicates', variable is substituted by the predicate
                if var_nm in self.classes[class_nm]['state']:
                    tokenized_expr.tokens[index] = param_nm + '.' + class_nm + '_' + var_nm
                elif var_nm in self.classes[class_nm]['predicates']:
                    tokenized_pr = Tokenizer(self.classes[class_nm]['predicates'][var_nm])
                    for pr_index, pr_token in enumerate(tokenized_pr.tokens):
                        if tokenized_pr.tokenTypes[pr_index] == TokenType.VAR:
                            # references from predicates to other predicates are not supported for now
                            # TODO: add exception when undefined variable used in predicate
                            if pr_token in self.classes[class_nm]['state']:
                                tokenized_pr.tokens[pr_index] = param_nm + '.' + class_nm + '_' + pr_token
                    tokenized_expr.tokens[index] = '('+ ' '.join(tokenized_pr.tokens) + ')'
                else:
                    raise Exception("SYNTAX ERROR: class " + class_nm + \
                        ", operator " + operator_name + " --- undefined variable " + var_nm + " in operator condition")
        return btree_to_pddl(BooleanParser(' '.join(tokenized_expr.tokens)).root)

def usage ():
    '''This is just usage message'''
    print ('evyml2pddl.py [-h | --help] [-o <outputfile> | --output=<outputfile>] input_file.yml')

def btree_to_pddl (root):
    ''' This procedure translates logical expression, supplied in a form of binary tree,
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
        if root['tokenType'] == TokenType.VAR and root['value'].title() not in ['True', 'False']:
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
            if cmp.title() == 'True':
                cmp = None
            elif cmp.title() == 'False':
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
        raise Exception("Complex logical expressions not supported yet.")

def var_to_canonical_form(variable_name, context, class_name = None):
    ''' This procedure translates (possible complex) operator variable, into canonical form,
            e.g. (complex variable) prefix.state_varibale -> state_variable, prefix, prefix class
        Input:
            - variable name (string)
            - class where operator is defined (string)
            - context where complex variable is defined, e.g. operator parameters (list)
        Output: [state variabe name, prefix name (or 'this'), class name (or None if prefix not defined in the context)]
    '''
    prefix_name = 'this'
    if '.' in variable_name:
        if variable_name.count('.') > 1:
            raise Exception("Complex variables not supported yet: " + variable_name)
        prefix_name, state_variable = variable_name.split('.', 1)
        if prefix_name not in context:
            class_name = None
        class_name = context[prefix_name]
        variable_name = state_variable
    return [variable_name, prefix_name, class_name]

def main (argv):
# Parse main options
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
            # load evyml code
            code = yaml.load(stream)
            # perform sanity check
            if any (major_section not in code for major_section in ['classes', 'main']):
                raise Exception("SYNTAX ERROR: no '" + major_section + "' section found in source file.")
            if 'exec' not in code['main']:
                raise Exception("SYNTAX ERROR: no 'exec' section found in 'main'.")
            evyml = Evans(code['classes'], code['main'])
            # parse classes
            evyml.parse_classes()
            print('\n'.join(evyml.pddl_domain))
            # parse main
            evyml.parse_main()
            # pprint.pprint(code['main'])
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
