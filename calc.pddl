;;
;; Simple calculator in PDDL
;; Develped by Igor Tikhonin (ivtikhon@gmail.com) in 2018
;;
(define (domain CALC)
  (:requirements :adl)
  (:types
    stack key display alu
  )
  (:predicates
    ;; stack
    (stack_changed ?s - stack)
    (stack_point ?s - stack)
    (stack_lastkey_point ?s - stack)

    ;; key
    (key_isdigit ?k - key)
    (key_ispoint ?k - key)
    (key_isop ?k - key)
    (key_iseq ?k - key)
    (key_isclear ?k - key)
    (key_iserase ?k - key)
    (key_processed ?k - key)

    ;; display
    (display_updated ?d - display)

    ;; alu keeps last operation and register
    (alu_op_stored ?a - alu)
    (alu_reg_stored ?a - alu)
  )

  (:action stack_push
    :parameters (?s - stack ?k - key)
    :precondition (and
      (not (stack_changed ?s))
      (not (key_processed ?k))
      (or (key_isdigit ?k) (key_ispoint ?k))
    )
    :effect (and
      (stack_changed ?s)
      (key_processed ?k)
      (when (key_ispoint ?k) (stack_lastkey_point ?s))
      (when (not (key_ispoint ?k)) (not (stack_lastkey_point ?s)))
    )
  )

  (:action stack_pop
    :parameters (?s - stack ?k - key)
    :precondition (and
      (not (stack_changed ?s))
      (not (key_processed ?k))
      (key_iserase ?k)
    )
    :effect (and
      (stack_changed ?s)
      (key_processed ?k)
      (when (stack_lastkey_point ?s) (not (stack_lastkey_point ?s)))
    )
  )

  ;; copy stack to register and empty stack
  (:action stack_to_register
    :parameters (?s - stack ?k - key ?a - alu)
    :precondition (and
      (not (key_processed ?k))
      (key_isop ?k)
      (not (alu_reg_stored ?a))
      (alu_op_stored ?a)
    )
    :effect (and
      (alu_reg_stored ?a)
      (stack_changed ?s)
      (not (stack_point ?s))
      (not (stack_lastkey_point ?s))
      (key_processed ?k)
    )
  )

  (:action alu_store_op
    :parameters (?a - alu ?k - key)
    :precondition (and
      (not (alu_op_stored ?a))
      (key_isop ?k)
    )
    :effect (and
      (alu_op_stored ?a)
    )
  )


;  (:action alu_exec_op
;    :parameters (?a - alu ?s - stack ?k - key)
;    :precondition (and
;      (not (alu_op_stored ?a))
;      (key_isop ?k)
;    )
;    :effect (and ()))

  (:action display_stack
    :parameters (?d - display ?s - stack ?k - key)
    :precondition (and
      (not (display_updated ?d))
      (key_processed ?k)
    )
    :effect (and
      (display_updated ?d)
      (when (stack_changed ?s)(not (stack_changed ?s)))
    )
  )
)
