#!/usr/bin/env python3

# Evans YAML to PDDL converter
# Written by Igor Tikhonin in 2018

import sys, getopt
import yaml

def usage ():
    print ('evyml2pddl.py [-h | --help] [-o <outputfile> | --output=<outputfile>] input_file.yml')

def error_exit(msg):
    print(msg)
    sys.exit()


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
            struct = yaml.load(stream)
            if 'classes' in struct:
                for cl_nm, cl_def in struct['classes'].items():
                    if 'state' in cl_def:
                        for st_nm, st_def in cl_def['state'].items():
                            if st_nm == 'vars':
                                for var_nm, var_def in st_def.items():
                                    print (var_def)
                                    print ('(' + '_'.join([cl_nm.lower(), var_nm]) + ' ?p - ' + cl_nm + ')')
            else:
                error_exit("No 'classes' section found in source file.")
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(2)

if __name__ == "__main__":
    main(sys.argv[1:])
