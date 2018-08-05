# Evans Tutorial

## Introduction

Programming essentially is an information processing exercise. Software developers write programs that take some data as input, modify the data according to program algorithms, and then present the results as output. In other words, it is a three-stage process, with 1) the _initial state_, where some data is considered to work with; then 2) a _course of actions_ is applied to transform data into its 3) desired, or _goal_ state.

Selecting the best course of actions is what constitutes programming. Algorithms encoded in programs define the data transformation procedure. Coding is difficult and prone to errors. And so far the evolution of programming languages has been going toward designing better language syntax to ease the process of coding.

By introducing the Evans programming language, we suggest to shift attention of the programming community from developing code, which describes the data transformation _procedure_, toward designing the data transformation _model_, and utilize capability of automated (classical) planning for selecting the appropriate course of actions, i.e. generating the actual code.

Evans extends the well known PDDL (Planning Domain Definition Language) with _classes_ and _state variables_, and also adds _execution_ capacity to PDDL actions, called _operators_ in Evans.

The language syntax is not designed yet, so we model syntax elements using YAML for now.

## Classes

Classes in Evans, like in traditional object oriented languages, define new types of objects along with object attributes and procedures, or methods, to manage the attributes. Classes can be seen as templates, based on which new objects are created.

What differs Evans from traditional object oriented languages is that in Evans, we distinguish between object _attributes_ and object _states_. Attributes represents information about objects, i.e. attributes are object characteristics. Set of object states represents how information transforms during the object lifetime, i.e. object states, expressed in the form of state variables, are procedural checkpoints.

In the following example we use postal service to show attributes and state variables in use. So, if you would like to send a letter to someone, the actual information is the letter content and the sender and recipient addresses (these are the letter attributes). The content is written on a sheet of paper, which is enclosed into an envelope, which, in its turn, is sealed, stamped, addressed and dropped into the nearest postal box (these are the state variables).

```
classes:
  letter:
    state:
      location: [sender_home, postal_box, in_transit, recipient_mailbox]
      status: [written, addressed, sealed, stamped, sent, received]
    attr:
      content: List
      source_address: String
      destination_address: String
  ...
```

### Attributes

Attributes are object _characteristics_, such as size, shape, weight, length, color, etc. In attributes we encode information about object, describing what the object is.
```
classes:
  cirle:
    attr:
      radius: Number
      color: String
      coordinates: List
  ...
```

### Methods

Methods in Evans have the same semantic as in any other object oriented languages, i.e. methods allow to manage object attributes. Methods do not have access to state variables.

### State Variables

State variables hold _states_ in which object of a certain class can be. For example, typical location of a hockey mom's car can be either home, work, school, ice rink, or shopping mall:

```
classes:
  car:
    state:
      location: [home, work, school, ice_rink, shopping_mall]
  ...
```

State variables can also be the Boolean type, i.e. has either True or False value, or Number type, i.e. assume any numeric value. Say, to specify if the hockey mom's car needs maintenance, we can define a Boolean variable **maintenance_required**, and a Number variable **next_maintenance_in_days**:

```
classes:
  car:
    state:
      maintenance_required: Boolean
      next_maintenance_in_days: Number
    operators:
      maintenance_signal:
        when:
          - not maintenance_required
          - next_maintenance_in_days < 15
        effect:
          - maintenance_required = True
  ...
```

State variables can be accessed directly in the same class operators, like it is shown in the previous example, where we read the value of the variable **maintenance_required** in the **maintenance_signal** operator precondition, and assigned its value in the operator effect. To access other classes' state variables, they have to be prefixed by the relevant object name. In the example below, we define two classes: **stack** and **address**, and we access the state variable **processed** which belongs to the **address** class from the operator **push**:

```
classes:
  stack:
    state:
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
      processed: Boolean
  ...
```

State variables can also be accessed by predicates, described below.

### Predicates

Predicates are facts about objects, which are either True or False. Predicates can simply return the value of a state variable, if it is Boolean, or calculate the value using a logical formula. For example, a smart fridge can figure out the fact that a bottle of milk has to be added to an online order by checking the amount of bottles of milk in:
```
classes:
  fridge:
    state:
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

Operators are actions that can manipulate the objects' states. Say, a pizza, when cooked, is to be delivered, so **deliver** can be one of the operators of the **pizza** class:

```
classes:
  pizza:
    state:
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

Operators have (optional) parameters, the list of objects supplied as arguments. Operators are executed when their preconditions are satisfied. If no precondition specified, then operator is always applicable. Operators have effect if they modify any state variables. And operators can trigger method(s) execution. (Remember, methods belong to attributes.) Operators do not have direct access to attributes.

In the example above, the operator **deliver** has parameters **from** and **to** in the **parameters:** section. The operator is executed when its precondition, described in the section **when:**, is satisfied (when pizza is cooked). And the operator effect, described in the section **effect:** is what the pizza delivered.

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
    attr:
      <attribute name>: <class name>
      ...
    methods:
      <method name>:
        [parameters:]
          <parameter name>: <class name>
          ...
        body: |
          <code in Python>
      ...
    state:
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
          # methods are called here
          - <method name>: parameter1, parameter2, ...
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
