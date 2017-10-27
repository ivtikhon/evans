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
	)
	(:goal
		(running-app app1 inst1)
	)
)
