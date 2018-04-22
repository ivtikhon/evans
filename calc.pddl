;;
;;
(define (domain CALC)
  (:requirements :adl)
  (:types
    stack key
    ;; alu display
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
