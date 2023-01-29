import inspect
import beniget
import gast
import pprint
import json
import astpretty

DEBUG = True

class ActionVariables(gast.NodeVisitor):
    def __init__(self, variables, chains, ancestors):
        self.variables = variables
        self.chains = chains
        self.ancestors = ancestors

    def visit_ListComp(self, node):
        for v in self.chains.locals[node]:
            self.variables[v] = Variable(v.name(), node, self.ancestors.parents(v.node))
        self.generic_visit(node)

class VariableAttributes(gast.NodeVisitor):
    def __init__(self, variables):
        self.variables = variables

    def visit_Attribute(self, node):
        if isinstance(node.value, gast.Name):
            # Direct attribute
            for var in self.variables:
                # Find the variable, the attibute belongs to
                if node.value in [use.node for use in var.users()]:
                    self.variables[var].attributes.add(node.attr)
                    break
            else:
                # Not found: it must be a global name
                raise Exception(f"Global variables in action functions are not supported: {node.value.id}")
        else:
            raise Exception("Parsing of complex attributes is not implemented yet")
        self.generic_visit(node)

class Var:
    pass

class Variable:
    def __init__(self, name, node, parents):
        self.name = name
        self.node = node
        self.type = None
        self.attributes = set()
        if isinstance(node, gast.ListComp):
            self.type = f'{Var.__module__}.{Var.__name__}'
        elif isinstance(node, gast.Name):
            annotation = None
            # Function arguments
            if isinstance(parents[-1], gast.arguments) and isinstance(parents[-2], gast.FunctionDef):
                # are supposed to have type annotations
                if node.annotation:
                    annotation = node.annotation
            # Assignment
            elif isinstance(parents[-1], gast.AnnAssign):
                # with a type annotation
                annotation = parents[-1].annotation

            if annotation:
                # Type annotation is either a string
                if isinstance(annotation, gast.Constant):
                    self.type = annotation.value
                # or a class name
                else:
                    self.type = annotation.id

class Action:
    def __init__(self, function_node, decorator_function, chains, ancestors):
        self.name = decorator_function
        self.variables = {}
        self.chains = chains
        self.ancestors = ancestors
        self.node = function_node
        action_vars = ActionVariables(self.variables, chains, ancestors)
        action_vars.visit(function_node)

        for v in chains.locals[function_node]:
            self.variables[v] = Variable(v.name(), v.node, ancestors.parents(v.node))

        var_attributes = VariableAttributes(self.variables)
        var_attributes.visit(function_node)

        if DEBUG:
            print(f'Function: {decorator_function}')
            for v in self.variables.values():
                print(f'{v.name}: {v.type}')
                for a in v.attributes:
                    print(f"  {a}")


class Class:
    def __init__(self, name):
        self.actions = {}
        self.attributes = {}
        
        source_code = inspect.getsource(name)
        module = gast.parse(source_code)
        # astpretty.pprint(module)
        chains = beniget.DefUseChains()
        chains.visit(module)
        ancestors = beniget.Ancestors()
        ancestors.visit(module)

        class_tree = module.body[0]
        # Get the Actions class
        action_class = [node for node in class_tree.body if isinstance(node, gast.ClassDef) and node.name == 'Actions']
        if action_class:
            for class_node in action_class[0].body:
                if isinstance(class_node, gast.FunctionDef):
                    # Action class contains functions decorated with the classmethod decorator
                    if any(decorator.id == 'classmethod' for decorator in class_node.decorator_list):
                        decorator_function = class_node
                        # Decorator function is expected to return a function
                        return_node = [
                            function_node for function_node in decorator_function.body
                                if isinstance(function_node, gast.Return) and isinstance(function_node.value, gast.Name)
                        ]
                        if return_node:
                            action_function = [
                                function_node for function_node in decorator_function.body 
                                    if isinstance(function_node, gast.FunctionDef) and function_node.name == return_node[0].value.id
                            ]
                            if action_function:
                                function = action_function[0]
                                self.actions[decorator_function.name] = Action(function, decorator_function.name, chains, ancestors)
                                

class Plan:
    def __init__(self, objects, goal):
        self.objects = objects
        self.classes = {}
        self.goal = goal

        for class_name in set([type(obj) for obj in self.objects]):
            self.classes[class_name] = Class(class_name)

    def generate_plan(self):
        pass

