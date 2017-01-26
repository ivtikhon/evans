(define (problem AN1)
  (:domain Ansible)
  (:objects
    test1 test2 test3 - file
 ;;   vagrant - userid
 ;;   users - groupid
  )
  (:init
    (file_exist test1)
    (file_exist test2)
 	)
	(:goal
		(file_exist test3)
	)
)
