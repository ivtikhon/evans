;; Ansible domain
;; Developed by Igor Tikhonin (igor.tikhonin@gmail.com) in 2016
;;
;; (c) Igor Tikhonin

(define (domain Ansible)
  (:requirements :adl)
  
  (:types
    file
    command
    application
  )
  
  (:predicates
    ;; object states
    (file_exist ?f - file)
    (file_copied ?src ?dest - file)
    (command_executed ?cmd - command)
    
    (application_installed ?app - application)
    
    ;; directives
    (run_command ?cmd - command)
  )
  
  ;; Copy a file
  (:action ansible_copy
    :parameters (?src ?dest - file)
    :precondition (and
      (file_exist ?src)
      (not (file_copied ?src ?dest))
    )
    :effect (and
      (file_copied ?src ?dest)
      (file_exist ?dest)
    )
  )
  
  ;; Run a command
  (:action ansible_command
    :parameters (?cmd - command)
    :precondition (run_command ?cmd)
    :effect (command_executed ?cmd)
  )
)