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
    (requires vol1_50 running vol1_50 created)
    (requires vol1_50 attached inst1 created)
    (requires fs1_vol1 created vol1_50 attached)
    (requires fs1_vol1 created inst1 running)
  )
  (:goal
    (and
      (has-state vol1_50 attached)
    )
  )
)
