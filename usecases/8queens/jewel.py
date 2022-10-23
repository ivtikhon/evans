import inspect
import beniget
import gast
import pprint

class Action(gast.NodeVisitor):
    def __init__(self, function_node, decorator_function, chains):
        self.name = decorator_function
        self.local_vars = {}
        self.chains = chains
        self.node = function_node
        print(decorator_function)

        for var in chains.locals[function_node]:
            self.local_vars[var] = {'name': var.name}

    def visit_Attribute(self, node):
        print(f'{node.value.id} . {node.attr}')
        for var in self.local_vars:
            if node.value != var.node:
                for use in var.users():
                    if node.value == use.node:
                        print(f'Use of {node.value.id}')
        self.generic_visit(node)

    
    def visit_ListComp(self, node):
        for var in self.chains.locals[node]:
            self.local_vars[var] = {'name': var.name}
        self.generic_visit(node)

class Class:
    def __init__(self, name):
        self.actions = {}
        self.attributes = {}
        
        source_code = inspect.getsource(name)
        module = gast.parse(source_code)
        chains = beniget.DefUseChains()
        chains.visit(module)

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
                                action = Action(function, decorator_function.name, chains)
                                self.actions[decorator_function.name] = action
                                action.visit(function)

class Plan:
    def __init__(self, objects, goal):
        self.objects = objects
        self.classes = {}
        self.goal = goal

        for class_name in set([type(obj) for obj in self.objects]):
            self.classes[class_name] = Class(class_name)

    def generate_plan(self):
        pass

