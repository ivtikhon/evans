#!/usr/bin/env python3

# Evans YAML to PDDL converter
# Written by Igor Tikhonin in 2018

import sys, getopt
import yaml

def usage ():
    print ('evyml2pddl.py [-h | --help] [-o <outputfile> | --output=<outputfile>] input_file.yml')

def main (argv):
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
    print ('Input: ' + input)
    if output == None:
        print ('Output: stdout')
    else:
        print ('Output: ' + output)

if __name__ == "__main__":
    main(sys.argv[1:])

# with open("example.yaml", 'r') as stream:
#     try:
#         print(yaml.load(stream))
#     except yaml.YAMLError as exc:
#         print(exc)
