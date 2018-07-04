# Evans Tutorial

## Classes

Classes in Evans, like in traditional object oriented languages, define new types of objects along with object attributes and procedures, or methods, to manage the attributes. Classes can be seen as templates, based on which new objects are created.

But here the similarity with traditional object oriented languages ends. In Evans, there can be two types of attributes defined in classes: the data and state attributes, also called variables, and their respective methods.

Data variables represents information about outside world, expressed in the form of objects. Set of object states represents how information transforms during the life of objects.

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
        <state variable name>: <Boolean|inline enum>
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
            <state variable name>: <Boolean|inline enum>
            ...
            # conditional effect
            if: <logical formula>
            then:
              <state variable name>: <Boolean|inline enum>
              ...
            else:
              <state variable name>: <Boolean|inline enum>
              ...
          exec:
            # data methods are called here
            - <data method name>: parameter1, parameter2, ...
            ...
  ...
```

### Embedded classes

#### Data
* String
* Int
* Long
* Float
* Double

#### State
* Boolean
