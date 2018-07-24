# Evans Tutorial

## Intoduction

Programming essentially is an information processing exercise. Software developers write programs that take some data as input, modify the data according to program algorithms, and then present the results as output. In other words, it is a three-stage process, with 1) the _initial state_, where some data is considered to work with; then 2) a _course of actions_ is applied to transform data into its 3) desired state, or _goal_.

Selecting the best course of actions is what constitutes programming. Algorithms encoded in programs define the data transformation procedure. Coding is difficult and prone to errors. And so far the evolution of programming languages has been going toward designing better language syntax to ease the process of coding.

By introducing the Evans programming language, we suggest to shift attention of the programming community from developing code, which describes the data transformation _procedure_, toward designing the data transformation _model_, and utilize capability of automated (classical) planning for selecting the appropriate course of actions, i.e. generating the actual code.

Evans extends the well known PDDL (Planning Domain Definition Language) with _classes_ and _state variables_, and also adds _execution_ capacity to PDDL actions, called _operators_ in Evans.

The language syntax is not designed yet, so we model syntax elements using YAML for now.

## Classes

Classes in Evans, like in traditional object oriented languages, define new types of objects along with object attributes and procedures, or methods, to manage the attributes. Classes can be seen as templates, based on which new objects are created.

But here the similarity with traditional object oriented languages ends. In Evans, there can be two types of attributes defined in classes: the data and state attributes, also called variables, and their respective methods.

Data variables represents information about objects in outside world, expressed in the form of object attributes. Set of object states represents how information transforms during the life of objects.

Let's use postal service as an example to show the data and state variables in use. If you would like to send a letter to someone, the actual information is the letter content and the sender and recipient addresses (these are the data variables). The content is written on a sheet of paper, which is enclosed into an envelope, which, in its turn, is sealed, stamped, addressed and dropped into the nearest postal box (these are the state variables).

```
classes:
  letter:
    state:
      vars:
        location: [sender_home, postal_box, in_transit, recipient_mailbox]
        status: [written, addressed, sealed, stamped, sent, received]
    data:
      vars:
        content: List
        source_address: String
        destination_address: String
  ...
```

### State Variables

State variables describe _states_ in which object of a certain class can be. For example, typical location of a hockey mom's car can be either home, work, school, ice rink, or shopping mall:

```
classes:
  car:
    state:
      vars:
        location: [home, work, school, ice_rink, shopping_mall]
  ...
```

State variables can also be the Boolean type, i.e. has either True or False value, or Number type, i.e. assume any numeric value. Say, to specify if the hockey mom's car needs maintenance, we can define a Boolean variable 'maintenance_required', and a Number variable 'next_maintenance_in_days':

```
classes:
  car:
    state:
      vars:
        maintenance_required: Boolean
        next_maintenance_in_days: Number
      operators:
        maintenance_signal:
          when:
            - not maintenance_required
            - next_maintenance_in_days <= 15
          effect:
            - maintenance_required = True
  ...
```

State variables can be accessed directly in the same class operators, like it is shown in the previous example, where we read the value of the variable 'maintenance_required' in the 'maintenance_signal' operator precondition, and assigned its value in the operator effect. To access other classes' state variables, they have to be prefixed by the relevant object name. In the example below, we define two classes: stack and address, and we access the address state variable 'processed' from the stack operator 'push':

```
classes:
  stack:
    state:
      vars:
        pointer:
          - incremented
          - decremented
      operators:
        push:
          parameters:
            val: address
          when:
            - not val.processed
          effect:
            - pointer = incremented
            - val.processed = True

  address:
    state:
      vars:
        processed: Boolean
  ...
```

Predicates also have read-only access to state variables.

### Predicates

Predicates are facts about objects, which are either True or False. Predicates can simply return the value of a state variable, if it is Boolean, or calculate the value using a logical formula. For example, a smart fridge can figure out the fact that a bottle of milk has to be added to an online order by checking the amount of bottles of milk in:
```
classes:
  fridge:
    vars:
      milk_bottles: Number
    predicates:
      is_milk_requred: milk_bottles < 1
    operators:
      place_order:
        when:
          - is_milk_requred
  ...
```

### Operators

Operators are actions that can manipulate the objects' states. Say, a pizza, when cooked, is to be delivered, so 'deliver' can be one of the operators of the pizza class:

```
classes:
  pizza:
    state:
      vars:
        order: [received, cooked, delivered]
      operators:
        deliver:
          parameters:
            from: Location
            to: Location
          when:
            - order == cooked
          effect:
           - order = delivered
        cook:
          when:
            - order == received
          effect:
            - order = cooked
  ...
```

## Main
_To Be Done_

### Initial state
_To Be Done_

### Goal
_To Be Done_

## Formal YAML description
```
classes:
  <class name>:
    data:
      vars:
        <data variable name>: <class name>
        ...
      methods:
        <data method name>:
          [parameters:]
            <parameter name>: <class name>
            ...
          body: |
            <code in Python>
        ...
    state:
      vars:
        <state variable name>: <Boolean|Number|list>
        ...
      predicates:
        <predicate name>: <logical formula>
        ...
      operators:
        <operator name>:
          parameters:
            <parameter name>: <class name>
            ...
          when:
            - <logical formula>
            ...
          effect:
            - <state variable name> = <Boolean|Number|list>
              ...
            # conditional effect
            - if: <logical formula>
              then:
                - <state variable name> = <Boolean|value from list>
                ...
              else:
                <state variable name> = <Boolean|value from list>
                ...
          exec:
            # data methods are called here
            - <data method name>: parameter1, parameter2, ...
            ...
  ...
```
### Embedded classes
* Boolean
* Number
* Char
* String
* List
* Dict
