# Evans Tutorial

## Classes

Classes in Evans, like in traditional object oriented languages, define new types of objects along with their attributes and methods to modify the attributes.  

Classes are templates, based on which new objects are created.

But here the similarity ends. In Evans, in contrary to traditional object oriented languages, there can be two types of attributes defined in classes: the data and state attributes, and their respective methods.

Data represents information. Set of states represents transformation of information.
```
classes:
  <class name>:
    data:
      vars:
        <data variable name>: <type>
        ...
      methods:
        <data method name>:
          [parameters:]
            <parameter name>: <type>
            ...
          body: |
            <code in Python>
        ...
    state:
      vars:
        <state variable name>: <boolean type|inline enum>
        ...
      predicates:
        <predicate name>: <logical formula>
        ...
      operators:
        <operator name>:
          parameters:
            <parameter name>: <type>
            ...
          when:
            - <logical formula>
            ...
          effect:
            <state variable name>: <boolean type|inline enum>
            ...
          exec:
            - <data method name>: parameter1, parameter2, ...
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
