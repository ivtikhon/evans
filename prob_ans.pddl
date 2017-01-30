(define (problem AN1)
  (:domain Ansible)
  (:objects
    ibm_im_pkg temp_file - file
    ibm_im - application
  )
  (:init
    (file_exist ibm_im_pkg)
 	)
	(:goal
		(file_copied ibm_im_pkg temp_file)
	)
)
