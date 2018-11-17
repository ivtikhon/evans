#!/usr/bin/env python3

# Evans YAML interpreter
# Written by Igor Tikhonin in 2018

import sys, getopt
import yaml
import pprint
import os
import tempfile
import subprocess
import re
import importlib
import uuid
from boolparser import *

class Evans:
    classes = None
    builtin_classes = None
    main = None
    main_vars = None
    pddl_domain = None
    domain_file_name = None
    evymlib_module = None
    evymlib_code = None
    evymlib = None
    tempdir = None
    module_dir = None
    planner = None
    var_ref = None
    tasks_max_depth = None
    debug_opt = None

    def __init__(self, classes_root, main_root):
        self.builtin_classes = ['list', 'str', 'int', 'float', 'bool']
        self.classes = classes_root
        self.main = main_root
        self.main_vars = {}
        self.planner = {}
        self.tempdir = '/tmp'
        self.planner['path'] = '/opt/fast-downward/fast-downward.py'
        self.planner['options'] = '--evaluator "hff=ff()" --search "lazy_greedy([hff], preferred=[hff])"'
        self.planner['plan_file'] = '/tmp/sas_plan'
        self.var_ref = 'ref::'
        self.tasks_max_depth = 50
        self.evymlib_module = 'evymlib'
        self.debug_opt = []

    def parse_classes(self):
        ''' This procedure translates Evans classes into PDDL and Python
            Input: Evans classes in YAML (self.classes)
            Output: PDDL Domain (self.pddl_domain), Python code (self.evymlib_code)
        '''
        header = ['(define (domain MYDOMAIN)', '(:requirements :adl)']
        types = ['(:types ']
        predicates = ['(:predicates']
        actions = []
        python_code = []
        python_functions = []
        for cl_nm, cl_def in self.classes.items():
            python_code.append('class ' + cl_nm + ':')
            python_init = ['    def __init__(self):']
            if 'state' in cl_def:
                types.append(cl_nm) # only classes with state variables should be listed as PDDL types
                python_code.append('    class State:')
                python_init.append('        self.state = self.State()')
                for var_nm, var_def in cl_def['state'].items():
                    # only Bool and inline enum types are supported for now
                    if isinstance(var_def, str) and var_def.title() == 'Bool':
                        prd_name = '_'.join([cl_nm, var_nm])
                        predicates.append('(' + prd_name + ' ?this - ' + cl_nm + ')')
                        python_init.append('        self.state.' + var_nm + ' = False')
                    elif isinstance(var_def, list):
                        var_def.append('undef')
                        for var_state in var_def:
                            prd_name = '_'.join([cl_nm, var_nm, var_state])
                            predicates.append('(' + prd_name + ' ?this - ' + cl_nm + ')')
                        python_init.append('        self.state.' + var_nm + ' = "undef"')
                    else:
                        raise Exception("ERROR: class " + cl_nm + \
                            ", variable " + var_nm + " --- variable type is expected to be either Bool or list")
                    python_code.append('        ' + var_nm + ' = None')
            if 'operators' in cl_def:
                # operators are translated into PDDL actions
                for op_nm, op_def in cl_def['operators'].items():
                    # PDDL action
                    actions.append('(:action ' + cl_nm + '_' + op_nm)
                    # corresponding Python function
                    func_def = 'def ' + cl_nm + '_' + op_nm + '('
                    # parse operator's parameters
                    if 'parameters' in op_def:
                        actions.append(':parameters (?this - ' + cl_nm)
                        func_def += 'this'
                        if not isinstance(op_def['parameters'], dict):
                            raise Exception("ERROR: class " + cl_nm + \
                                ", operator " + op_nm + " --- parameters expected to be dictionary type")
                        # create reverse lookup list of parameters to search by number (for Python code generation)
                        param_by_number = ['this']
                        for par_nm, par_type in op_def['parameters'].items():
                            actions.append('?'+ par_nm + ' - ' + par_type)
                            func_def += ', ' + par_nm
                            param_by_number.append(par_nm)
                        actions.append(')')
                        cl_def['operators'][op_nm]['param_by_number'] = param_by_number # reverse lookup list of parameters
                    python_functions.append(func_def.lower() + '):')
                    # parse operator's condition
                    if 'when' in op_def:
                        actions.append(':precondition (and')
                        if not isinstance(op_def['when'], list):
                            raise Exception("ERROR: class " + cl_nm + \
                                ", operator " + op_nm + " --- condition expected to be list type")
                        for cond_def in op_def['when']:
                            pddl_cond = self.operator_condition_to_pddl(condition_sting = cond_def, \
                                class_name = cl_nm, operator_name = op_nm)
                            actions.append(pddl_cond)
                        actions.append(')')
                    # parse operator's effect
                    if 'effect' in op_def:
                        if not isinstance(op_def['effect'], list):
                            raise Exception("ERROR: class " + cl_nm + \
                                ", operator " + op_nm + " --- effect expected to be list type")
                        actions.append(':effect (and')
                        indent = 1
                        effect_list = op_def['effect'][:] # create a copy of effect definition
                        for index, eff_def in enumerate(effect_list):
                            # dict -> assignment
                            # int -> indent
                            # tuple -> condition in PDDL and Python
                            # str -> closing of PDDL condition body
                            if isinstance(eff_def, int):
                                indent += eff_def
                                continue
                            elif isinstance(eff_def, tuple):
                                actions.append(eff_def[0])
                                python_functions.append('    ' * indent + eff_def[1])
                                continue
                            elif isinstance (eff_def, str):
                                actions.append(eff_def)
                                continue
                            if any (cond_elem in eff_def for cond_elem in ['if', 'then', 'else']):
                                # conditional assignment
                                try:
                                    cond_context = None
                                    if 'parameters' in op_def:
                                        cond_context = op_def['parameters']
                                    parsed_condition = self.parse_conditional_statement(condition_sting = eff_def['if'],\
                                        class_name = cl_nm, context = cond_context, output_format = 'all')
                                    # unfold condition alternative
                                    if 'else' in eff_def:
                                        effect_list.insert(index + 1, -1)
                                        effect_list.insert(index + 1, '))')
                                        else_list = eff_def['else'][:]
                                        else_list.reverse()
                                        for cond_eff in else_list:
                                            effect_list.insert(index + 1, cond_eff)
                                        effect_list.insert(index + 1, 1)
                                        effect_list.insert(index + 1, ('(when (not ' + parsed_condition['pddl'] + ') (and', \
                                            'else:'))
                                    # unfold condition body
                                    then_list = eff_def['then'][:]
                                    then_list.reverse()
                                    effect_list.insert(index + 1, -1)
                                    effect_list.insert(index + 1, '))')
                                    for cond_eff in then_list:
                                        effect_list.insert(index + 1, cond_eff)
                                    effect_list.insert(index + 1, 1)
                                    effect_list.insert(index + 1, ('(when ' + parsed_condition['pddl'] + ' (and', \
                                        'if ' + parsed_condition['python'] + ':'))
                                except KeyError:
                                    raise Exception("ERROR: class " + cl_nm + \
                                        ", operator " + op_nm + " --- conditional effect is expected to be in the if-then-else format")
                            else:
                                # unconditional assignment
                                try:
                                    context = None
                                    if 'parameters' in op_def:
                                        context = op_def['parameters']
                                    assignment_code = self.parse_assignment_statement(assignment_definition = eff_def, \
                                        class_name = cl_nm, context = context, output_format = 'all')
                                    actions.extend(assignment_code['pddl'])
                                    for python_code_line in assignment_code['python']:
                                        python_functions.append('    ' * indent + python_code_line)
                                except Exception as err:
                                    raise Exception("ERROR processing operator effect: class " + cl_nm + ", operator " + op_nm + ' --- ' + str(err))
                        actions.append(')')
                    actions.append(')')
                    if 'exec' in op_def:
                        if not isinstance(op_def['exec'], list):
                            raise Exception("ERROR: class " + cl_nm + \
                                ", operator " + op_nm + " --- exec items expected to be list type")
                        for exec_def in op_def['exec']:
                            # one action at a time
                            if len(exec_def) > 1:
                                raise Exception("ERROR: class " + cl_nm + + \
                                    ", operator " + op_nm + " --- only one exec call per list item is supported")
                            method_name = list(exec_def.keys())[0]
                            method_body = "    this.attr." + method_name + '('
                            if exec_def[method_name] != None:
                                method_params = ''.join(exec_def[method_name].split()) # remove whitespaces
                                add_comma = False
                                for param in method_params.split(','):
                                    if 'parameters' in op_def and param in op_def['parameters']:
                                        method_body += param + ".attr"
                                        if add_comma:
                                            method_body += ','
                                        else:
                                            add_comma = True
                                    else:
                                        raise Exception("ERROR: class " + cl_nm + + \
                                            ", operator " + op_nm + " --- undefined variable in exec section: " + param)
                            python_functions.append(method_body + ')')
                    else:
                        python_functions.append('    pass')
            if 'attr' in cl_def or 'methods' in cl_def:
                python_code.append('    class Attr:')
                python_init.append('        self.attr = self.Attr()')
            if 'attr' in cl_def:
                for at_nm, at_def in cl_def['attr'].items():
                    if at_def not in self.builtin_classes: # only built-in types are allowed for now
                        raise Exception("ERROR: class " + cl_nm + \
                            ", attribute " + at_nm + ", attribute class " + at_def + " --- unsupported attribute class")
                    python_code.append('        ' + at_nm + ' = None')
                    if at_def == 'list':
                        python_init.append('        self.attr.' + at_nm + ' = []')
                    elif at_def == 'str':
                        python_init.append('        self.attr.' + at_nm + ' = ""')
                    elif at_def == 'int':
                        python_init.append('        self.attr.' + at_nm + ' = 0')
                    elif at_def == 'float':
                        python_init.append('        self.attr.' + at_nm + ' = 0.0')
                    elif at_def == 'bool':
                        python_init.append('        self.attr.' + at_nm + ' = False')
                    else:
                        python_init.append('        self.attr.' + at_nm + ' = None')
            if 'methods' in cl_def:
                for method_nm, method_def in cl_def['methods'].items():
                    method = '        def ' + method_nm + '(self'
                    if 'parameters' in method_def:
                        for param_nm, param_type in method_def['parameters'].items():
                            method += ', ' + param_nm
                    python_code.append(method + '):')
                    if 'body' in method_def:
                        for body_line in method_def['body'].split('\n'):
                            if body_line == '': # skip empty lines
                                continue
                            python_code.append('            ' + body_line)
                    else:
                        python_code.append('        pass')
            if ('attr' not in cl_def or len(cl_def['attr']) == 0) and \
                    ('methods' not in cl_def or len(cl_def['methods']) == 0) and \
                    ('state' not in cl_def or len(cl_def['state']) == 0):
                python_code.append('        pass')
            else:
                python_code.extend(python_init)
        predicates.append(')')
        types.append(')')
        self.pddl_domain = header + types + predicates + actions + [')']
        self.evymlib_code = python_code + python_functions
        if 'evymlib_code' in self.debug_opt:
            print('=== Evymlib code ===')
            print('\n'.join(self.evymlib_code))

    def interprete_main_tasks (self, tasks, upper_level = 'main', depth = 1):
        ''' This procedure interpretes tasks in main
            Input: list of tasks
            Output: none; the return value is used to pass the 'break' signal from the inner loop
        '''
        # Depth check is just a precaution
        if depth >= self.tasks_max_depth:
            raise Exception('FATAL: maximum depth of inner tasks has reached: ' + self.tasks_max_depth)
        for item in tasks:
            # only unconditional loop (with break) implemented for now
            if 'loop' in item:
                loop_exit = 'continue'
                while loop_exit != 'break':
                    loop_exit = self.interprete_main_tasks (item['loop'], 'loop', depth + 1)
            elif 'code' in item:
                module_name = None
                # generate code task module
                if 'module_name' not in item:
                    module_name = str(uuid.uuid1())
                    code = []
                    code_task = 'code_task'
                    fun_def = 'def ' + code_task + '('
                    for k, v in self.main_vars.items():
                        fun_def += k + ','
                    code.append(fun_def[:-1] + '):')
                    for line in item['code'].split('\n'):
                        code.append('    ' + line.rstrip())
                    return_def = '    return {'
                    for k, v in self.main_vars.items():
                        return_def += "'" + k + "': " + k + ','
                    code.append(return_def[:-1] + '}')
                    codefl = open(self.module_dir + '/' + module_name + '.py', mode='w+t')
                    codefl.write('\n'.join(code))
                    codefl.close()
                    item['module_name'] = module_name
                    if 'code_tasks' in self.debug_opt:
                        print('=== Code task ===')
                        print('\n'.join(code))
                else:
                    module_name = item['module_name']
                # import generated module
                code_mod = importlib.import_module(module_name)
                # prepare code task parameters
                code_param = {}
                for k, v in self.main_vars.items():
                    code_param[k] = v
                # execute code task
                code_retval = code_mod.code_task(**code_param)
                # sync (trivial) vars
                for k, v in code_retval.items():
                    if id(v) != id(self.main_vars[k]):
                        self.main_vars[k] = v
            elif 'auto' in item:
                self.interprete_task_auto(item['auto'])
            elif 'break' in item:
                if upper_level == 'loop':
                    return 'break'
                else:
                    raise Exception("ERROR: 'break' task in main can be used in loop context only")
        return 'continue'

    def interprete_task_auto(self, auto):
        ''' This procedure interpretes the auto task, i.e. translates it into PDDL, runs planning,
            and then executes the obtained plan.
        '''
        # generate PDDL problem code
        try:
            problem = ['(define (problem MYPROBLEM)', '(:domain MYDOMAIN)']
            objects = ['(:objects']
            init = ['(:init']
            goal = ['(:goal']
            for obj in auto['objects']:
                # generate list of object
                class_nm = self.main['vars'][obj]
                objects.append(obj + ' - ' + class_nm)
                # initialize objects
                for var_nm, var_val in self.main_vars[obj].state.__dict__.items():
                    state_var_definition = self.classes[class_nm]['state'][var_nm]
                    if isinstance(state_var_definition, list): # inline enum
                        for state_var_val in state_var_definition:
                            prefix = '('
                            postfix = ')'
                            if var_val != state_var_val:
                                prefix += 'not ('
                                postfix += ')'
                            init.append(prefix + class_nm + '_' + var_nm + '_' + state_var_val + ' ' + obj + postfix)
                    else:
                        prefix = '('
                        postfix = ')'
                        if var_val == False:
                            prefix += 'not ('
                            postfix += ')'
                        init.append(prefix + class_nm + '_' + var_nm + ' ' + obj + postfix)
            goal.append('(and')
            for goal_item in auto['goal']:
                if 'if' in goal_item:
                    goal.append('(imply ')
                    goal.append(self.goal_condition_to_pddl(goal_item['if'], auto['name']))
                    if len(goal_item['then']) > 1:
                        goal.append('(and')
                    for goal_definition in goal_item['then']:
                        goal.extend(self.goal_definition_to_pddl(goal_definition, auto['name']))
                    if len(goal_item['then']) > 1:
                        goal.append(')')
                    goal.append(')')
                else:
                    goal.extend(self.goal_definition_to_pddl(goal_item, auto['name']))
            body = problem + objects + [')'] + init +[')'] + goal + [')))']
            # create PDDL problem file
            with tempfile.NamedTemporaryFile(mode='w+t', prefix='pddl-problem-', dir=self.tempdir, delete=False) as fp:
                problem_file_name = fp.name
                fp.write('\n'.join(body))
                fp.close()
                if 'pddl_problem' in self.debug_opt:
                    print('=== PDDL problem ===')
                    print('\n'.join(body))
                # call PDDL planner
                args = self.planner['path'] + ' ' + os.path.basename(self.domain_file_name) + \
                    ' ' + os.path.basename(problem_file_name) + ' ' + self.planner['options']
                with subprocess.Popen(args, cwd=self.tempdir, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as planner:
                    planner.wait()
                    if 'planner_stdout' in self.debug_opt:
                        print('=== Planner output ===')
                        for line in planner.stdout:
                            line = line.decode().rstrip()
                            print(line)
                    if planner.returncode == 0: # planner generated a plan
                        with open(self.planner['plan_file'], 'rt') as planfile:
                            for line in planfile:
                                if line.startswith(';'):
                                    continue
                                if 'plan' in self.debug_opt:
                                    print(line.rstrip()[1:-1])
                                func_and_params = line.rstrip()[1:-1].split(' ')
                                func_name = func_and_params[0]
                                cl_name, sep, op_name = func_name.partition('_')
                                # recover class name from operator name
                                for cls in self.classes.keys():
                                    if cl_name.lower() == cls.lower():
                                        cl_name = cls
                                        break
                                func = getattr(self.evymlib, func_name)
                                func_param = {}
                                for index, param in enumerate(func_and_params[1:]):
                                    param_nm = self.classes[cl_name]['operators'][op_name]['param_by_number'][index]
                                    func_param[param_nm] = self.main_vars[param]
                                func(**func_param)
                    else:
                        raise Exception("FAILURE: PDDL planner found no solution for task auto " + auto['name'])
                # clean up
                os.remove(problem_file_name)
                subprocess.run([self.planner['path'], '--cleanup'], cwd=self.tempdir)
        except KeyError:
            raise Exception("ERROR: auto section in main tasks should contain objects and goal definitions.")

    def goal_definition_to_pddl(self, goal_definition, auto_name):
        ''' This procedure translates auto's goal into PDDL '''
        try:
            context = self.main['vars']
            pddl_arr = self.parse_assignment_statement(assignment_definition = goal_definition, \
                class_name = None, context = context)
            # no '?' symbols required in goal definition
            for index, pddl_str in enumerate(pddl_arr):
                pddl_arr[index] = pddl_arr[index].replace('?', '')
            return pddl_arr
        except Exception as err:
            raise Exception("ERROR processing goal definition: auto task " + auto_name + ' --- ' + str(err))

    def operator_effect_to_pddl(self, effect_definition, class_name, operator_name):
        ''' This procedure translate operator's effect into PDDL '''
        try:
            context = self.classes[class_name]['operators'][operator_name]['parameters']
            return self.parse_assignment_statement(assignment_definition = effect_definition, \
                class_name = class_name, context = context)
        except Exception as err:
            raise Exception("ERROR processing operator effect: class " + class_name + ", operator " + operator_name + ' --- ' + str(err))

    def parse_assignment_statement(self, assignment_definition, class_name, context, output_format = 'pddl'):
        ''' This procedure parses operator's effect
            Input:
                - assignment from operator effect or auto goal (dict)
                - class where operator is defined or None for goal (string)
                - context where variables are defined (dict)
            Output: PDDL code or Python code, or both
            Note: the calling procedure must handle exceptions
        '''
        pddl_code = []
        python_code = []
        # assignment format: state_var: value (either Bool or inline enum item)
        if len(assignment_definition) > 1:
            raise Exception("Only one variable assignment per list item is supported")
        unprocessed_var_nm = list(assignment_definition.keys())[0]
        var_nm, param_nm, class_nm = \
            var_to_canonical_form(variable_name = unprocessed_var_nm, \
                    context = context, class_name = class_name)
        if class_nm == None:
            raise Exception("Undefined variable " + param_nm + " used in assignment")
        if var_nm not in self.classes[class_nm]['state']:
            raise Exception("Undefined state variable " + var_nm + " used in assignment")
        var_type = self.classes[class_nm]['state'][var_nm] # state variable type
        assignment_value = assignment_definition[unprocessed_var_nm] # value to be assigned to state variable
        # state variable type is either Bool...
        if isinstance(var_type, str) and var_type.title() == 'Bool' and \
                (isinstance(assignment_value, bool) or assignment_value.title() in ['True', 'False']):
            if isinstance(assignment_value, bool):
                assignment_value = str(assignment_value)
            if output_format in ['pddl', 'all']:
                assignment_str = '(' + class_nm + '_' + var_nm + ' ?' + param_nm + ')'
                if assignment_value.title() == 'False':
                    assignment_str = '(not ' + assignment_str + ')'
                pddl_code.append(assignment_str)
            if output_format in ['python', 'all']:
                python_code.append(param_nm + '.state.' + var_nm + ' = ' + assignment_value)
        # ...or inline enum (where all values are explisitly listed in state variable definition)
        elif isinstance(var_type, list):
            if output_format in ['pddl', 'all']:
                if assignment_value in var_type:
                    for st_var_val in var_type:
                        assignment_str = '(' + class_nm + '_' + var_nm + '_' + st_var_val + ' ?' + param_nm + ')'
                        if st_var_val != assignment_value:
                            assignment_str = '(not ' + assignment_str + ')'
                        pddl_code.append(assignment_str)
                else:
                    raise Exception("Undefined value " + assignment_value + " is assigned on variable " + var_nm)
            if output_format in ['python', 'all']:
                python_code.append(param_nm + '.state.' + var_nm + ' = "' + assignment_value + '"')
        else:
            raise Exception("Variable " + var_nm + " is not Bool, nor list type defined")
        if output_format == 'pddl':
            return pddl_code
        elif output_format == 'python':
            return python_code
        elif output_format == 'all':
            return {'python': python_code, 'pddl': pddl_code}
        else:
            raise Exception("Unknown output format: " + output_format)

    def operator_condition_to_pddl(self, condition_sting, class_name, operator_name):
        ''' This procedure translates operator condition (when) into PDDL '''
        try:
            return self.parse_conditional_statement(condition_sting = condition_sting,\
                class_name = class_name, context = self.classes[class_name]['operators'][operator_name]['parameters'])
        except Exception as err:
            raise Exception("ERROR processing operator condition: class " + class_name + ", operator " + operator_name + " --- " + str(err))

    def effect_condition_to_pddl(self, condition_sting, class_name, operator_name):
        ''' This procedure translates operator's effect condition into PDDL '''
        try:
            return self.parse_conditional_statement(condition_sting = condition_sting,\
                class_name = class_name, context = self.classes[class_name]['operators'][operator_name]['parameters'])
        except Exception as err:
            raise Exception("ERROR processing operator effect: class " + class_name + ", operator " + operator_name + " --- " + str(err))

    def goal_condition_to_pddl(self, condition_sting, auto_name):
        ''' This procedure translates goal condition into PDDL'''
        try:
            pddl_str = self.parse_conditional_statement(condition_sting = condition_sting,\
                class_name = None, context = self.main['vars'])
            # no '?' symbols required in goal definition
            return pddl_str.replace('?', '')
        except Exception as err:
            raise Exception("ERROR processing goal condition: auto task " + auto_name + " --- " + str(err))

    def parse_conditional_statement(self, condition_sting, class_name, context, output_format = 'pddl'):
        ''' This procedure parses conditional statement (operator's when, effect condition, and auto's goal)
            and converts it into PDDL or Python, or both
            Input:
                - condition (sting)
                - class name (string): name of the class where operator is defined, or None, if this is goal's condition
                - context reference (dict): reference to operator's parameters/main's vars
            Output: PDDL formula or/and Python condition
            Note: the calling procedure must handle exceptions
        '''
        # parse logical expressions, expand predicates;
        tokenized_expr = Tokenizer(condition_sting)
        for index, token in enumerate(tokenized_expr.tokens):
            if tokenized_expr.tokenTypes[index] == TokenType.VAR:
                var_nm, param_nm, class_nm = var_to_canonical_form(variable_name = token, \
                    context = context, class_name = class_name)
                if class_nm == None:
                    raise Exception("Undefined variable " + param_nm + " used in condition")
                # variable is searched in 'state' first, then in 'predicates';
                # when found in 'predicates', variable is substituted by the predicate
                if var_nm in self.classes[class_nm]['state']:
                    tokenized_expr.tokens[index] = param_nm + '.' + class_nm + '_' + var_nm
                elif var_nm in self.classes[class_nm]['predicates']:
                    tokenized_pr = Tokenizer(self.classes[class_nm]['predicates'][var_nm])
                    for pr_index, pr_token in enumerate(tokenized_pr.tokens):
                        if tokenized_pr.tokenTypes[pr_index] == TokenType.VAR and pr_token.title() not in ['True', 'False']:
                            # TODO: references from predicates to other predicates not implemented yet
                            if pr_token in self.classes[class_nm]['state']:
                                tokenized_pr.tokens[pr_index] = param_nm + '.' + class_nm + '_' + pr_token
                            else:
                                err_str = "Undefined variable " + pr_token + " used in predicate " + var_nm
                                if class_name != class_nm:
                                    err_str += ", defined in class " + class_nm
                                raise Exception(err_str)
                    tokenized_expr.tokens[index] = '('+ ' '.join(tokenized_pr.tokens) + ')'
                else:
                    raise Exception("Undefined state variable or predicate " + var_nm + " used in condition")
        expression = ' '.join(tokenized_expr.tokens)
        expression_python = None
        expression_pddl = None
        if output_format in ['python', 'all']:
            expression_python = re.sub(r'\.[a-zA-Z]+[a-zA-Z0-9]*_', '.state.', expression) # replace class name to 'state' generating Python code
        if output_format in ['pddl', 'all']:
            expression_pddl = btree_to_pddl(BooleanParser(expression).root)
        if output_format == 'pddl':
            return expression_pddl
        elif output_format == 'python':
            return expression_python
        elif output_format == 'all':
            return {'python': expression_python, 'pddl': expression_pddl}
        else:
            raise Exception("Unknown output format: " + output_format)

# Free procedures
def usage ():
    '''This is just usage message'''
    print ('evyml2pddl.py [-h | --help] [-d <debug options> | --output=<debug options>] input_file.yml')

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
                # add state to predicate name
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
            - context where complex variable is defined, e.g. operator parameters (dict)
        Output: [state variabe name, prefix name (or 'this'), class name (or None if prefix not defined in the context)]
    '''
    prefix_name = 'this'
    if '.' in variable_name:
        if variable_name.count('.') > 1:
            raise Exception("Complex variables not supported yet: " + variable_name)
        prefix_name, state_variable = variable_name.split('.', 1)
        if prefix_name not in context:
            class_name = None
        else:
            class_name = context[prefix_name]
        variable_name = state_variable
    return [variable_name, prefix_name, class_name]


def main (argv):
# Parse main options
    try:
        opts, args = getopt.getopt(argv, "hd:", ["help", "debug="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    input = None
    debug = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-d", "--debug"):
            debug = a
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
                raise Exception("ERROR: no '" + major_section + "' section found in source file.")
            if 'tasks' not in code['main']:
                raise Exception("ERROR: no 'tasks' section found in 'main'.")
            evyml = Evans(code['classes'], code['main'])
            if debug != None:
                evyml.debug_opt = debug
            # parse classes
            evyml.parse_classes()
            # create temp directory for dynamically generated modules
            moddir = tempfile.TemporaryDirectory(prefix=evyml.evymlib_module + '-', dir=evyml.tempdir)
            evyml.module_dir = moddir.name
            # create Evymlib module
            codefl = open(evyml.module_dir + '/' + evyml.evymlib_module +'.py', mode='w+t')
            codefl.write('\n'.join(evyml.evymlib_code))
            codefl.close()
            # import Evymlib module
            sys.path.append(evyml.module_dir)
            evyml.evymlib = importlib.import_module(evyml.evymlib_module)
            # create PDDL domain file
            domainfl = tempfile.NamedTemporaryFile(mode='w+t', prefix='pddl-domain-', dir=evyml.tempdir, delete=False)
            evyml.domain_file_name = domainfl.name
            domainfl.write('\n'.join(evyml.pddl_domain))
            domainfl.close()
            if 'pddl_domain' in evyml.debug_opt:
                print('\n'.join(evyml.pddl_domain))
            # parse & execute main
            try:
                # initialize variables
                for v in evyml.main['vars']:
                    class_name = evyml.main['vars'][v]
                    if class_name in evyml.classes: # user defined class
                        evyml.main_vars[v] = getattr(evyml.evymlib, class_name)()
                    elif class_name in evyml.builtin_classes: # built-in class
                        evyml.main_vars[v] = type(class_name)()
                    else:
                        raise Exception("ERROR: main section, variable " + v + " is of unknown class " + class_name)
                # parse and execute tasks
                evyml.interprete_main_tasks(evyml.main['tasks'])
            except KeyError:
                raise Exception("ERROR: main should contain tasks and vars definitions.")
            # clean up
            os.remove(domainfl.name)
            moddir.cleanup()
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
