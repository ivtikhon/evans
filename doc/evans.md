# Evans Tutorial

## Classes

There are three types of classes in Evans: *data*, *state*, and *hybrid*.

### Hybrid classes

```
classes:
  <class name>:
    data:
      vars:
        <data variable name>: <data/hybrid type>
        ...
      methods:
        <data method name>:
          [parameters:]
            <parameter name>: <data/hybrid type>
            ...
          body: |
            <code in Python or JS>
        ...
    state:
      vars:
        <state variable name>: <state type/inline enum>
        ...
      predicates:
        <predicate name>: <logical formula>
        ...
      operators:
        <operator name>:
          parameters:
            <parameter name>: <state/hybrid type>
            ...
          when:
            - <logical formula>
            ...
          effect:
            - <state variable name> = <boolean/logical formula>
          exec: |
            <code in Python or JS>
```

### Embedded classes

#### Data
* String
* Int

#### State
* Boolean

##### Hybrid
* List
