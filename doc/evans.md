# Evans Tutorial

## Classes

Classes in Evans, like in traditional object oriented languages, define new types of objects along with object attributes and methods to manage the attributes. Classes are templates, based on which new objects are created.

But here the similarity with traditional object oriented languages ends. In Evans there can be two types of attributes defined in classes: the data and state attributes, or variables, and their respective methods.

Data variables represents information about outside world, expressed in the form of objects. Set of states represents transformation of information during the life of objects.

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
