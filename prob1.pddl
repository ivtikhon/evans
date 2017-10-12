(define (problem EC2-test)
	(:domain EC2)
	(:objects
		inst1 inst2 inst3 - instance
		vol1_50 vol2_50 vol3_50 - volume
		fs1_vol1 - filesystem
	)
	(:init
		(requires-in inst1 vol1_50)
		(requires-vol vol1_50 fs1_vol1)
		(created-in inst1)
;		(attached-vol vol1_50 inst1)
	)
	(:goal
		(created-fs fs1_vol1 vol1_50)
	)
)
