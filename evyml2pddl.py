#!/usr/bin/env python3

# Evans YAML to PDDL converter
# Written by Igor Tikhonin in 2018

import sys, getopt
import yaml

def usage ():
    print ('evyml2pddl.py [-o <outputfile>] input_file.yml')

def main (argv):
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "output="])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    output = None
    for o, a in opts:
        if o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
    if output == None:
        print ('Output: stdout')
    else:
        print ('Output: ' + output)
    print ('Input: ' + args)

if __name__ == "__main__":
    main()

# with open("example.yaml", 'r') as stream:
#     try:
#         print(yaml.load(stream))
#     except yaml.YAMLError as exc:
#         print(exc)
