import inspect
import beniget
import gast
import pprint

class Plan:
    def __init__(self, objects, goal):
        self.objects = objects
        self.goal = goal

    def generate_plan(self):
        for class_name in set([type(obj) for obj in self.objects]):
            source_code = inspect.getsource(class_name)
            module = gast.parse(source_code)
            chains = beniget.DefUseChains()
            chains.visit(module)
            class_tree = module.body[0]
            # Get the Actions class
            actions_class = None
            for node in class_tree.body:
                if isinstance(node, gast.ClassDef) and node.name == 'Actions':
                    actions_class = node
                    break
            # Parse actions functions
            if actions_class:
                for class_node in actions_class.body:
                    if isinstance(class_node, gast.FunctionDef):
                        # Action class contains functions decorated with the classmethod decorator
                        if any(decorator.id == 'classmethod' for decorator in class_node.decorator_list):
                            decorator_function = class_node
                            # Decorator function is expected to return a function
                            return_node = None
                            action_function = None
                            for function_node in decorator_function.body:
                                if isinstance(function_node, gast.Return) and isinstance(function_node.value, gast.Name):
                                    return_node = function_node
                                    break
                            if return_node:
                                for function_node in decorator_function.body:
                                    if isinstance(function_node, gast.FunctionDef) and function_node.name == return_node.value.id:
                                        action_function = function_node
                                        break
                            if action_function:
                                for local_var in chains.locals[action_function]:
                                    print(local_var.name())

