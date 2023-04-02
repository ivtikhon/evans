import inspect
import beniget
import gast
import pprint
import json
import astpretty

DEBUG = True

class PddlObject:
    def __init__(self, name: str, type: str = "object"):
        self.name = name
        self.type = type

    def __str__(self):
        return f'?{self.name} - {self.type}'

class PddlPredicate:
    pass

class PddlPredicateIsTrue(PddlPredicate):
    def __init__(self, pddlobject: PddlObject):
        self.object = pddlobject

    def __str__(self):
        return f'(is_true ?{self.object.name})'

class PddlPredicateIsAttr(PddlPredicate):
    def __init__(self, pddlobject: PddlObject, attributeobject: PddlObject):
        self.object = pddlobject
        self.attribute = attributeobject
    
    def __str__(self):
        return f'(is_attr ?{self.object.name} ?{self.attribute.name})'

class PddlPredicateIsEq(PddlPredicate):
    def __init__(self, leftpddlobject: PddlObject, rightpddlobject: PddlObject):
        self.leftobject = leftpddlobject
        self.rightobject = rightpddlobject
    
    def __str__(self):
        return f'(is_eq ?{self.leftobject.name} ?{self.rightobject.name})'

class PddlPredicateIsMember(PddlPredicate):
    def __init__(self, pddlobject: PddlObject, memberobject: PddlObject):
        self.object = pddlobject
        self.member = memberobject
    
    def __str__(self):
        return f'(is_member ?{self.object.name} ?{self.member.name})'

class PddlExists:
    def __init__(self, pddlobject: PddlObject, expression):
        self.object = pddlobject
        if type(expression) != list:
            self.expression = [expression]
        else:
            self.expression = expression 

    def __str__(self):
        expr = ' '.join([str(p) for p in self.expression])
        if len(self.expression) > 1:
            expr = f'(and {expr})'
        return f'(exists ({str(self.object)}) {expr})'

class PddlForAll:
    def __init__(self, pddlobject: PddlObject, expression):
        self.object = pddlobject
        if type(expression) != list:
            self.expression = [expression]
        else:
            self.expression = expression 

    def __str__(self):
        expr = ' '.join([str(p) for p in self.expression])
        if len(self.expression) > 1:
            expr = f'(and {expr})'
        return f'(forall ({str(self.object)}) {expr})'

class PddlNot:
    def __init__(self, pddlpredicate):
        self.predicate = pddlpredicate
    
    def __str__(self):
        return f'(not {self.predicate})'

class PddlConstant:
    def __init__(self, name: str, value: str):
        self.name = name
        self.value = value
    
    def __str__(self):
        return f'?{self.name}'

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
                    v = self.variables[var]
                    v.attributes[node.attr] = PddlObject(f'{v.name}_{node.attr}', f'attr_{v.type}')
                    break
            else:
                # Not found: it must be a global name
                raise Exception(f"Global variables in action functions are not supported: {node.value.id}")
        else:
            raise Exception("Parsing of complex attributes is not implemented")
        self.generic_visit(node)

class ActionAssert(gast.NodeVisitor):
    def __init__(self, variables, ancestors):
        self.variables = variables
        self.ancestors = ancestors
        self.pddl = []
    
    def generic_visit(self, node):
        raise Exception(f'Not supported node type: {type(node).__name__} in asserts')
    
    def visit_Assert(self, node):
        super().generic_visit(node)

    def visit_UnaryOp(self, node):
        if isinstance(node.op, gast.Not):
            super().generic_visit(node)
            predicate = self.pddl.pop()
            self.pddl.append(PddlNot(predicate))
        else:
            # We're not supposed to be here
            raise Exception('Internal error')

    def visit_Compare(self, node):
        '''
            Compare(left, ops, comparators)
            one comparison operation is supported;
            left is either gast.Name or gast.Attribute;
            comparator[0] is either gast.Name, gast.Attribute, or gast.Constant;
            ops[0] is either gast.Eq, or gast.NotEq;
        '''
        if len(node.ops) > 1:
            raise Exception('Only one comparison operation is supported for now')
        if type(node.left) not in [gast.Name, gast.Attribute]:
            raise Exception(f'Not supported node type {type(node.left).__name__} in comparisons')
        if type(node.comparators[0]) not in [gast.Name, gast.Attribute, gast.Constant]:
            raise Exception(f'Not supported node type {type(node.comparators[0]).__name__} in comparisons')
        super().generic_visit(node)
        comparator = self.pddl.pop()
        left = self.pddl.pop()
        
        # remove PddlPredicateIsTrue
        if isinstance(node.left, gast.Attribute):
            left.expression.pop() 
        if isinstance(node.comparators[0], gast.Attribute):
            comparator.expression.pop()

        if isinstance(node.left, gast.Name) and (isinstance(node.comparators[0], gast.Name) or isinstance(node.comparators[0], gast.Constant)): # two PddlPredicateIsTrue
            pddl_predicate = PddlPredicateIsEq(left.object, comparator.object)
        elif isinstance(node.left, gast.Name) and isinstance(node.comparators[0], gast.Attribute): # PddlPredicateIsEq and PddlExists
            pddl_predicate = comparator
            pddl_predicate.expression.append(PddlPredicateIsEq(left.object, comparator.object))
        elif isinstance(node.left, gast.Attribute) and (isinstance(node.comparators[0], gast.Name) or isinstance(node.comparators[0], gast.Constant)): # PddlExists and PddlPredicateIsTrue
            pddl_predicate = left
            pddl_predicate.expression.append(PddlPredicateIsEq(left.object, comparator.object))
        elif isinstance(node.left, gast.Attribute) and isinstance(node.comparators[0], gast.Attribute): # two PddlExists
            pddl_predicate = left
            pddl_predicate.expression.append(comparator)
            comparator.expression.append(PddlPredicateIsEq(left.object, comparator.object))
        else:
            # We're not supposed to be here
            raise Exception('Internal error')

        if isinstance(node.ops[0], gast.Eq):
            self.pddl.append(pddl_predicate)
        elif isinstance(node.ops[0], gast.NotEq):
            self.pddl.append(PddlNot(pddl_predicate))
        else:
            # We're not supposed to be here
            raise Exception('Internal error')

    def visit_Attribute(self, node):
        if not isinstance(node.ctx, gast.Load):
            raise Exception(f'Attribute context {node.ctx} is not supported in asserts')
        if isinstance(node.value, gast.Name):
            super().generic_visit(node)
            for var in self.variables:
                if node.value in [use.node for use in var.users()]:
                    v = self.variables[var]
                    self.pddl.pop() # Remove the attribute name
                    attr_pddl_obj = v.attributes[node.attr]
                    exists_obj = PddlExists(attr_pddl_obj, [PddlPredicateIsAttr(v.pddlobject, attr_pddl_obj), PddlPredicateIsTrue(attr_pddl_obj)])
                    self.pddl.append(exists_obj)
                    break
            else:
                # We're not supposed to be here
                raise Exception('Internal error')

        else:
            raise Exception("Parsing of complex attributes is not implemented")

    def visit_Name(self, node):
        '''
            name is a variable or an attribute;
            function names are ignored
        '''
        if isinstance(self.ancestors.parents(node)[-1], gast.Call):
            return
        for var in [v for v in self.variables if v.name() == node.id]:
            if node is var.node or node in [use.node for use in var.users()]:
                v = self.variables[var]
                self.pddl.append(PddlPredicateIsTrue(v.pddlobject))
                break
        else:
            # We're not supposed to be here
            raise Exception(f'Internal error in visit_Name: {node.id}')

    def visit_Constant(self, node):
        self.pddl.append(PddlPredicateIsTrue(PddlObject(f'const_{node.value}')))    # TODO: revisit constant parsing

    def visit_Call(self, node):
        '''Only any() or all() are supported with list comprehension as a single argument'''
        if isinstance(node.func, gast.Name) and len(node.args) == 1 and isinstance(node.args[0], gast.ListComp):
            if node.func.id == 'any':
                pass 
            elif node.func.id == 'all': # Replace PddlExists with PddlForAll;   NOTE: forall requires pddl impliation; not implemented yet
                raise Exception('PddlForAll is not implemented yet')
            else:
                raise Exception(f'Not supported function {node.func.id} in asserts')
        else:
            raise Exception(f'Only any() or all() are supported with list comprehension as an argument in asserts')
        super().generic_visit(node)

    def visit_ListComp(self, node):
        '''
            ListComp(elt, generators[comprehension])
            elt can be gast.Name, gast.Attribute, or gast.Compare
            Only one iterator is supported
        '''
        if len(node.generators) > 1:
            raise Exception('Only one iterator is supported in asserts')
        if type(node.elt) not in [gast.Name, gast.Attribute, gast.Compare]:
            raise Exception(f'Not supported element type {type(node.elt).__name__} in list comprehensions')
        super().generic_visit(node)
        comprehension = self.pddl.pop()
        elt = self.pddl.pop()
        comprehension.expression.append(elt)
        self.pddl.append(comprehension)
        
    def visit_comprehension(self, node):
        '''
            comprehension(target, iter, ifs)
            target is gast.Name;
            iter is gast.Name or gast.Attribute;
            only one ifs is supported;
        '''
        if len(node.ifs) > 1:
            raise Exception('Only one if is supported in list comprehensions')
        if type(node.iter) not in [gast.Name, gast.Attribute]:
            raise Exception(f'Not supported iterator type {type(node.iter).__name__} in list comprehensions')
        if not isinstance(node.target, gast.Name):
            raise Exception(f'Not supported target type {type(node.target).__name__} in list comprehensions')
        super().generic_visit(node)
        ifs = None
        if node.ifs:
            ifs = self.pddl.pop()
        iter = self.pddl.pop()
        target = self.pddl.pop()
        if isinstance(node.iter, gast.Name):
            pddl_predicate = PddlPredicateIsMember(iter.object, target.object)
        elif isinstance(node.iter, gast.Attribute):
            iter.expression.pop() # Remove PddlPredicateIsTrue from PddlExists
            pddl_predicate = iter
            pddl_predicate.expression.append(PddlPredicateIsMember(iter.object, target.object))
        else:
            # We're not supposed to be here
            raise Exception('Internal error')
        if ifs:
            pddl_predicate.expression.append(ifs)
        self.pddl.append(PddlExists(target.object, [pddl_predicate]))

    def visit_Eq(self, node):
        pass

    def visit_NotEq(self, node):
        pass

    def visit_Not(self, node):
        pass

    def visit_Load(self, node):
        pass

class ActionEffect(gast.NodeVisitor):
    def __init__(self, variables, ancestors):
        self.variables = variables
        self.ancestors = ancestors
        self.pddl = []

    def visit_Assign(self, node):
        '''
            Assign(targets, value)
            only one target is supported;
            target is gast.Name or gast.Attribute;
            value is gast.Name, gast.Attribute, gast.Constant
        '''
        if len(node.targets) > 1:
            raise Exception('Only one target is supported in action effects')
        super().generic_visit(node)

        value = self.pddl.pop()
        target = self.pddl.pop()
        raise Exception(f'Not implemented yet')

    def visit_Name(self, node):
        '''
            name is a variable or an attribute;
        '''
        for var in [v for v in self.variables if v.name() == node.id]:
            if node is var.node or node in [use.node for use in var.users()]:
                v = self.variables[var]
                self.pddl.append(PddlPredicateIsTrue(v.pddlobject))
                break
        else:
            # We're not supposed to be here
            raise Exception(f'Internal error in visit_Name: {node.id}')

class ListCompVar:
    pass

class Variable:
    def __init__(self, name, node, parents):
        self.name = name
        self.node = node
        self.type = None
        self.function_agrument = False
        self.attributes = {}
        if isinstance(node, gast.ListComp):
            self.type = f'{ListCompVar.__module__}.{ListCompVar.__name__}'
        elif isinstance(node, gast.Name):
            annotation = None
            # Function arguments
            if isinstance(parents[-1], gast.arguments) and isinstance(parents[-2], gast.FunctionDef):
                # are supposed to have type annotations
                if node.annotation:
                    annotation = node.annotation
                self.function_agrument = True
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
        self.pddlobject = PddlObject(self.name, self.type)

class Action:
    def __init__(self, function_node, decorator_function, classname, chains, ancestors):
        self.name = decorator_function
        self.variables = {}
        self.chains = chains
        self.ancestors = ancestors
        self.node = function_node

        # Extract local vars from list comprehensions
        action_vars = ActionVariables(self.variables, chains, ancestors)
        action_vars.visit(function_node)

        # Collect local variables
        for v in chains.locals[function_node]:
            self.variables[v] = Variable(v.name(), v.node, ancestors.parents(v.node))

        # Collect attributes
        var_attributes = VariableAttributes(self.variables)
        var_attributes.visit(function_node)

        # Generate PDDL code
        self.pddl_code = [
            f'(:action {classname}-{decorator_function}',
            ':parameters ('
        ]
        for v in self.variables.values():
            if v.function_agrument:
                self.pddl_code.append(f'?{v.name} - {v.type}')
        self.pddl_code.append(')')

        precondition_body = [':precondition (and']
        effect_body = [':effect (and']

        # Parse asserts
        for function_node in function_node.body:
            if isinstance(function_node, gast.Assert):
                assert_node = ActionAssert(self.variables, self.ancestors)
                assert_node.visit(function_node)
                precondition_body.append(str(assert_node.pddl[0]))
            else:
                effect_body.append('(effect)')
        
        if len(precondition_body) > 1:
            precondition_body.append(')')
            self.pddl_code += precondition_body

        if len(effect_body) > 1:
            effect_body.append(')')
            self.pddl_code += effect_body

        self.pddl_code.append(')')

        if DEBUG:
            print(f'Function: {decorator_function}')
            for v in self.variables.values():
                print(f'{v.name}: {v.type}')
                for a in v.attributes:
                    print(f"  {a}")
            
            print("\n".join(self.pddl_code))

class Class:
    def __init__(self, name):
        self.classname = f'{name.__module__}-{name.__name__}'
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
                                self.actions[decorator_function.name] = Action(function, decorator_function.name, self.classname, chains, ancestors)
                                

class Plan:
    def __init__(self, objects, goal):
        self.objects = objects
        self.classes = {}
        self.goal = goal

        for class_name in set([type(obj) for obj in self.objects]):
            self.classes[class_name] = Class(class_name)

    def generate_plan(self):
        pass
