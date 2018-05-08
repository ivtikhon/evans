;;
;; Simple calculator in PDDL
;; Developed by Igor Tikhonin (ivtikhon@gmail.com) in 2018
;;
(define (domain CALC)
  (:requirements :adl)
  (:types
    stack key display alu
  )
  (:predicates
    ;; stack
    (stack_changed ?s - stack)
    (stack_dec_point ?s - stack)  ;; there is a decimal point in the stack
    (stack_lastkey_point ?s - stack)  ;; if 'erase' comes, we need to know whether the previous key was a decimal point
    (stack_tobe_cleaned ?s - stack)  ;; clean stack next cycle

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
    (alu_op_executed ?a - alu)
    (alu_reg_stored ?a - alu)
  )

  ;; clean stack after operation was stored
  (:action stack_clean
    :parameters (?s - stack ?k - key)
    :precondition (and
      (not (key_processed ?k))
      (or (key_isdigit ?k) (key_ispoint ?k))
      (stack_tobe_cleaned ?s)
    )
    :effect (and
      (not (stack_tobe_cleaned ?s))
      (not (stack_dec_point ?s))
      (not (stack_lastkey_point ?s))
;      (stack_changed ?s)
    )
  )

  ;; push digit or decimal point to stack
  ;; ignore extra decimal points
  ;; TODO write ignore extra point action
  (:action stack_push
    :parameters (?s - stack ?k - key)
    :precondition (and
      (not (stack_changed ?s))
      (not (key_processed ?k))
      (or (key_isdigit ?k) (key_ispoint ?k))
      (not (stack_tobe_cleaned ?s))
    )
    :effect (and
      (stack_changed ?s)
      (key_processed ?k)
      (when (key_ispoint ?k) (and (stack_dec_point ?s) (stack_lastkey_point ?s)))
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
      (when (stack_lastkey_point ?s) (and
          (not (stack_lastkey_point ?s))
          (not (stack_dec_point ?s))
        )
      )
    )
  )

  ;; copy stack to register and mark stack to be cleaned next cycle
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
  ;    (stack_changed ?s)
      (key_processed ?k)
      (stack_tobe_cleaned ?s)
    )
  )

  ;; copy value from register to stack and mark stack to be cleaned next cycle
  (:action stack_from_register
    :parameters (?s - stack ?k - key ?a - alu)
    :precondition (and
      (alu_op_executed ?a)
      (or (key_isop ?k) (key_iseq ?k))
      (not (key_processed ?k))
    )
    :effect (and
      (key_processed ?k)
      (stack_changed ?s)
      (not (alu_reg_stored ?a))
      (stack_tobe_cleaned ?s)
    )
  )

  ;; store current operation to alu for later execution
  (:action alu_store_op
    :parameters (?a - alu ?k - key)
    :precondition (and
      (not (alu_op_stored ?a))
      (key_isop ?k)
      (not (alu_reg_stored ?a))
      (not (key_processed ?k))
    )
    :effect (and
      (alu_op_stored ?a)
    )
  )

  ; execute stored operation with register and stack
  ; and store result to register
  ; if key is an operation, store it to alu
  (:action alu_exec_op
    :parameters (?a - alu ?s - stack ?k - key)
    :precondition (and
      (or (key_isop ?k) (key_iseq ?k))
      (alu_op_stored ?a)
      (alu_reg_stored ?a)
      (not (alu_op_executed ?a))
    )
    :effect (and
      (alu_op_executed ?a)
      (when (key_iseq ?k) (not (alu_op_stored ?a)))
    )
  )

  (:action display_stack
    :parameters (?d - display ?s - stack ?k - key)
    :precondition (and
      (not (display_updated ?d))
      (key_processed ?k)
      (stack_changed ?s)
    )
    :effect (and
      (display_updated ?d)
      (not (stack_changed ?s))
    )
  )
)
