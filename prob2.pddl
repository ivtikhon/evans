(define (problem EC2-test)
	(:domain EC2)
  (:objects
		inst1 inst2 inst3 - instance
		vol1_50 vol2_50 vol3_50 - volume
		fs1_vol1 fs2_vol2 fs3_vol3 - filesystem
    dir1_fs1 dir2_fs2 dir3_fs3 - directory
    url1 url2 url3 - url
		app1 app2 app3 - application
	)
	(:init
    ; Object properties
		; Dependencies
    (requires-in inst1 app1)  ; applications require instances
		(requires-in inst2 app2)
		(requires-app app2 app1)
		(requires-in inst1 vol1_50)  ; volumes require instances
		(requires-in inst1 vol2_50)
		(requires-in inst2 vol3_50)
			(requires-vol vol1_50 fs1_vol1)  ; file systems require volumes
			(requires-vol vol2_50 fs2_vol2)
			(requires-vol vol3_50 fs3_vol3)
				(requires-dir dir1_fs1 app1)  ; applications require directories
				(requires-dir dir2_fs2 app1)
				(requires-dir dir3_fs3 app2)
          (requires-fs fs1_vol1 dir1_fs1)  ; directories require file systems
          (requires-fs fs2_vol2 dir2_fs2)
          (requires-fs fs3_vol3 dir3_fs3)
		; Current state
    (created-in inst1)
    (created-in inst2)
    (running-in inst1)
    (running-in inst2)
    (created-vol vol1_50)
    (created-vol vol2_50)
    (created-vol vol3_50)
    (attached-vol vol1_50 inst1)
    (attached-vol vol2_50 inst1)
    (attached-vol vol3_50 inst2)
    (created-fs fs1_vol1 vol1_50)
    (created-fs fs2_vol2 vol2_50)
    (created-fs fs3_vol3 vol3_50)
    (mounted-fs fs1_vol1 inst1)
    (mounted-fs fs2_vol2 inst1)
    (mounted-fs fs3_vol3 inst2)
    (exists-dir dir1_fs1 fs1_vol1)
    (exists-dir dir2_fs2 fs2_vol2)
    (exists-dir dir3_fs3 fs3_vol3)
    (installed-app app1 inst1)
    (installed-app app2 inst2)
    (running-app app1 inst1)
    (running-app app2 inst2)
  )
  (:goal
    (not (attached-vol vol3_50 inst2))
  )
)
