(define (problem CALC-test)
  (:domain CALC)
  (:objects
    stack1 - stack
    key1 - key
  )
  (:init
    (key_isdigit key1)
  )
  (:goal
    (and
      (key_processed key1)
    )
  )
)
