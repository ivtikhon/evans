;; Ansible domain
;; Developed by Igor Tikhonin (igor.tikhonin@gmail.com) in 2016
;;
;; (c) Igor Tikhonin

(define (domain Ansible)
  (:requirements :adl)
  
  (:types file userid groupid string - object
  )
  
  (:predicates
    (file_exist ?f - file)
 ;   (file_ownership ?f - file ?u - userid ?g - groupid)
  )
  
  ;; Copy a file
  (:action ansible_copy
    :parameters (?src ?dest - file)
    :precondition (and
      (file_exist ?src)
      (not (file_exist ?dest))
    )
    :effect (file_exist ?dest)
  )
)