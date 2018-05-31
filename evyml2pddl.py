#!/usr/bin/env python3

# Evans YAML to PDDL converter
# Written by Igor Tikhonin in 2018

import sys, getopt
import yaml

def usage ():
    print ('evyml2pddl.py [-h | --help] [-o <outputfile> | --output=<outputfile>] input_file.yml')

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
            domain = ['(define (domain MINE)', '(:requirements :adl)']
            types = ['(types: ']
            predicates = ['(:predicates']
            actions = []
            if not 'classes' in code:
                raise Exception("SYNTAX ERROR: no 'classes' section found in source file.")
            for cl_nm, cl_def in code['classes'].items():
                types.append(cl_nm)
                if not 'state' in cl_def:
                    continue
                for st_nm, st_def in cl_def['state'].items():
                    # state variables are translated into PDDL predicates
                    if st_nm == 'vars':
                        for var_nm, var_def in st_def.items():
                            if isinstance(var_def, str) and var_def == 'Boolean':
                                predicates.append('(' + '_'.join([cl_nm, var_nm]) + ' ?p - ' + cl_nm + ')')
                            elif isinstance(var_def, list):
                                for var_state in var_def:
                                    predicates.append('(' + '_'.join([cl_nm, var_nm, var_state]) + ' ?p - ' + cl_nm + ')')
                            else:
                                raise Exception("SYNTAX ERROR: class " + cl_nm +
                                    ", variable " + var_nm + " --- variable type is expected to be either Boolean or list")
                    # operators are translated into PDDL actions
                    elif st_nm == 'operators':
                        for op_nm, op_def in st_def.items():
                            actions.append('(:action ' + cl_nm + '_' + op_nm)
                            actions.append(':parameters (?this - ' + cl_nm)
                            if 'parameters' in op_def:
                                if not isinstance(op_def['parameters'], dict):
                                    raise Exception("SYNTAX ERROR: class " + cl_nm +
                                        ", operator " + op_nm + " --- parameters expected to be dictionary type")
                                for par_nm, par_type in op_def['parameters'].items():
                                    actions.append('?'+ par_nm + ' - ' + par_type)
                            actions.append(')')
                            if 'when' in op_def:
                                pass
                            actions.append(')')
            predicates.append(')')
            types.append(')')
            body = domain + types + predicates + actions
            body.append(')')
            print('\n'.join(body))
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
