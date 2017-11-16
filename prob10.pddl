(define (problem EC2-test)
  (:domain EC2)
  (:objects
    vpc1 - vpc
    inst1 inst2 inst3 - instance
    vol1_50 vol2_50 vol3_50 - volume
    fs1_vol1 fs2_vol2 fs3_vol3 - filesystem
    dir1_fs1 dir2_fs2 dir3_fs3 - directory
    url1 url2 url3 - url
    app1_inst1 app2_inst2 app3_inst3 - application
    fl1_url1 fl2_dir1 fl3_dir2 - file
  )
  (:init
    (requires vol1_50 attached inst1 created)
    (requires fs1_vol1 created vol1_50 attached)
    (requires fs1_vol1 created inst1 running)
  )
  (:goal
    (and
      (has-state fs1_vol1 attached)
    )
  )
)
