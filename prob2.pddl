(define (problem EC2-test)
	(:domain EC2)
	(:objects
		inst1 inst2 inst3 - instance
		vol1_50 vol2_50 vol3_50 - volume
		fs1_vol1 fs2_vol2 fs3_vol3 - filesystem
		app1 app2 app3 - application
	)
	(:init
		; Dependencies
		(requires-in inst1 vol1_50)  ; volumes require instances
		(requires-in inst1 vol2_50)
		(requires-in inst2 vol3_50)
			(requires-vol vol1_50 fs1_vol1)  ; file systems require volumes
			(requires-vol vol2_50 fs2_vol2)
			(requires-vol vol3_50 fs3_vol3)
				(requires-fs fs1_vol1 app1)  ; applications require file systems
				(requires-fs fs2_vol2 app1)
				(requires-fs fs3_vol3 app2)
		(requires-in inst1 app1)  ; applications require instances
		(requires-in inst2 app2)
		(requires-app app2 app1)
		; Current state
    (created-in inst1)
	  (attached-vol vol1_50 inst1)
    (running-in inst2)
    (created-vol vol3_50)
    (created-vol vol2_50)
    (attached-vol vol3_50 inst2)
    (created-fs fs3_vol3 vol3_50)
    (attached-vol vol2_50 inst1)
    (mounted-fs fs3_vol3 inst2)
    (installed-app app2 inst2)
    (running-app app2 inst2)
    (running-in inst1)
    (created-fs fs1_vol1 vol1_50)
    (created-fs fs2_vol2 vol2_50)
    (mounted-fs fs1_vol1 inst1)
    (mounted-fs fs2_vol2 inst1)
    (installed-app app1 inst1)
    (running-app app1 inst1)
  )
  (:goal
    (not (attached-vol vol3_50 inst2))
  )
)
