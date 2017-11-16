(define (problem EC2-test)
  (:domain EC2)
  (:objects
    inst1 inst2 inst3 - instance
    vol1_50 vol2_50 vol3_50 - volume
    fs1_vol1 fs2_vol2 fs3_vol3 - filesystem
    dir1_fs1 dir2_fs2 dir3_fs3 - directory
    url1 url2 url3 - url
    app1 app2 app3 - application
    fl1 fl2 fl3 - file
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
;        (requires-dir dir1_fs1 app1)  ; applications require directories
        (requires-dir dir2_fs2 app1)
        (requires-dir dir3_fs3 app2)
          (requires-fs fs1_vol1 dir1_fs1)  ; directories require file systems
          (requires-fs fs2_vol2 dir2_fs2)
          (requires-fs fs3_vol3 dir3_fs3)
            (requires-dir dir1_fs1 fl1)  ; files require directories
        (requires-fl fl1 app1)
    ; Current state
;    (created-in inst1)
;    (created-in inst2)
;      (attached-vol vol1_50 inst1)
    (exists-file fl1 url1)
  )
  (:goal
    (and
      (running-app app1 inst1)
      (exists-file fl1 dir1_fs1)
    )
  )
)
