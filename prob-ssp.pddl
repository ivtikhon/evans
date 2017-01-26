(define (problem SSP)
	(:domain EC2)
	(:objects
		apweb42 apweb43 apweb44 apweb45
			aptrans44 aptrans45
			wltrans38 wltrans39 wltrans40 wltrans41 wltrans42 wltrans43
			dbblack39 dbblack50 - instance
		volweb42_50 volweb43_50 volweb44 - volume
		app1 app2 app3 - application
	)
	(:init
		(attach-to-in inst1 vol1_50)
		(attach-to-in inst2 vol2_50)
		(run-on-in inst1 app1)
		(run-on-in inst2 app2)
		(run-on-in inst2 app3)
		(startup-order-app app2 app1)
	)
	(:goal
		(and
			(running-app app1 inst1)
			(running-app app3 inst2)
		)
	)
)
