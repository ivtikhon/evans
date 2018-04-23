(define (problem CALC-test)
  (:domain CALC)
  (:objects
    stack1 - stack
    key1 - key
    display1 - display
    alu1 - alu
  )
  (:init
;    (key_isdigit key1)
    (key_isop key1)
    (alu_op_stored alu1)
    (alu_reg_stored alu1)
  )
  (:goal
    (and
      (key_processed key1)
      (display_updated display1)
    )
  )
)
