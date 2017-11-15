;; This code was developed by Igor Tikhonin (ivtikhon@gmail.com) in 2014-2017.
;; Amazon's EC2 is used as the infrastructure model.

;; Instances:
;;  - launched in a non-default VPC
;;  - getting access to the internet through a NAT instance
;; Each instance has:
;;  - a default network interface with a private IP;
;;  - an internal DNS hostname that resolves to the private IP address of the instance;
;;  - an internal (root) volume used by operating system only
;; Dependencies:
;; volume requires an instance to be attached to
;; application requires:
;;  - instance to run on
;;  - directory to be installed to
;; application may depend on another application, i.e. it might require another application
;; directory requires a filesystem to be created at
;; file requires a directory to be stored in
;;
;; (c) Igor Tikhonin

(define (domain EC2)
  (:requirements :adl)
  (:types
    instance volume filesystem application directory url file state
  )
  (:constants
    created running terminated exits installed - state
  )
  (:predicates
    (has-state ?obj1 - object ?st1 - state)
    (requires ?obj1 - object ?st1 - state ?obj2 - object ?st2 - state) ;; for obj1 to get to state st1, obj2 requies to be in st2
  )

  ;; create and start an instance
  ;; instance is created if there is an object that requires it
  ;; terminated instance can't be re-created
  (:action launch-in
    :parameters (?inst1 - instance)
    :precondition (and
      (not (has-state ?inst1 running))
      (not (has-state ?inst1 created))
      (not (has-state ?inst1 terminated))
      (exists (?obj1 - object)
        (exists (?st1 - state)
          (or (requires ?obj1 ?st1 ?inst1 created)(requires ?obj1 ?st1 ?inst1 running))
        )
      )
      (forall (?objn - object)
        (forall (?stn - state)
          (imply
            (requires ?inst1 running ?objn ?stn) (has-state ?objn ?stn)
          )
        )
      )
    )
    :effect (and
      (has-state ?inst1 created)
      (has-state ?inst1 running)
    )
  )

  ;; start an instance
  ;; instance is started if there is an object that requires it
;  (:action start-in
;    :parameters (?inst1 - instance)
;    :precondition (and
;      (has-state ?inst1 created)
;      (not (has-state ?inst1 running))
;      (not (has-state ?inst1 terminated))
;      (exists (?obj1 - object)
;        (exist (?st1 - state)
;          (requires ?obj1 ?st1 ?inst1 running)
;        )
;      )
;      (forall (?objn - object)
;        (forall (?stn - state)
;          (imply
;            (requires ?inst1 running ?objn ?stn) (has-state ?objn ?stn)
;          )
;        )
;      )
;    )
;    :effect (has-state ?inst1 running)
;  )

;  ;; stop instance
;  ;; all running applications are to be stopped
;  (:action stop-in
;    :parameters (?inst1 - instance)
;    :precondition (and
;      (running-in ?inst1)
;      (forall (?appn - application)
;        (imply (requires-in ?inst1 ?appn)
;          (not (running-app ?appn ?inst1))
;        )
;      )
;    )
;    :effect (not (running-in ?inst1))
;  )

  ;; create volume
  ;; volume is created if there is an object that requires it
  (:action create-vol
    :parameters (?vol1 - volume)
    :precondition (and
      (not (has-state ?vol1 created))
      (exists (?obj1 - object)
        (exists (?st1 - state)
          (requires ?obj1 ?st1 ?vol1 created)
        )
      )
      (forall (?objn - object)
        (forall (?stn - state)
          (imply
            (requires ?vol1 created ?objn ?stn) (has-state ?objn ?stn)
          )
        )
      )
    )
    :effect (has-state ?vol1 created)
  )

  ;; attach storage volume to instance
  ;; storage volume can be attached to one instance only
  ;; the instance can be either running or stopped
  (:action attach-vol
    :parameters (?vol1 - volume ?inst1 - instance)
    :precondition (and
      (has-state ?inst1 created)
      (has-state ?vol1 created)
      (requires ?vol1 attached ?inst1 running)
      (requires ?vol1 attached ?vol1 created)
      (not (exists (?instn - instance) (attached-vol ?vol1 ?instn)))
    )
    :effect (attached-vol ?vol1 ?inst1)
  )

;  ;; detach volume
;  ;; all file systems dependent on volume are to be unmounted
;  ;; and all applications dependent on file systems are to be stopped
;  (:action detach-vol
;    :parameters (?vol1 - volume ?inst1 - instance)
;    :precondition (and
;      (running-in ?inst1)
;      (attached-vol ?vol1 ?inst1)
;      (forall (?fsn - filesystem)
;        (imply (requires-vol ?vol1 ?fsn)(not (mounted-fs ?fsn ?inst1)))
;      )
;    )
;    :effect (not (attached-vol ?vol1 ?inst1))
;  )
;
;  ;; create file system
;  ;; file system requires a running instance with a volume attached
;  (:action create-fs
;    :parameters (?fs1 - filesystem ?vol1 - volume ?inst1 - instance)
;    :precondition (and
;      (not (created-fs ?fs1 ?vol1))
;      (requires-vol ?vol1 ?fs1)
;      (requires-in-running ?inst1 ?vol1)
;      (running-in ?inst1)
;      (attached-vol ?vol1 ?inst1)
;    )
;    :effect (created-fs ?fs1 ?vol1)
;  )
;
;  ;; mount file system
;  ;; file system requires a running instance with a volume attached
;  ;; file system is supposed to be created in order to be mounted
;  (:action mount-fs
;    :parameters (?fs1 - filesystem ?inst1 - instance)
;    :precondition (and
;      (exists (?vol1 - volume) (and (created-fs ?fs1 ?vol1) (attached-vol ?vol1 ?inst1)))
;      (running-in ?inst1)
;    )
;    :effect (mounted-fs ?fs1 ?inst1)
;  )
;
;  ;; unmount file system
;  ;; all applications require this file system are to be stopped
;  (:action unmount-fs
;    :parameters (?fs1 - filesystem ?inst1 - instance)
;    :precondition (and
;      (mounted-fs ?fs1 ?inst1)
;      (running-in ?inst1)
;      (exists (?vol1 - volume) (and (requires-vol ?vol1 ?fs1) (attached-vol ?vol1 ?inst1)))
;      (forall (?appn - application)
;        (forall (?dir1 - directory)
;          (imply (and (requires-fs ?fs1 ?dir1)(requires-dir ?dir1 ?appn)(requires-in-running ?inst1 ?appn))(not (running-app ?appn ?inst1)))
;        )
;      )
;    )
;    :effect (not (mounted-fs ?fs1 ?inst1))
;  )
;
;  ;; install application
;  ;; application requires an instance and directory(ies)
;  ;; all required file systems and directories are to be created first
;  (:action install-app
;    :parameters (?app1 - application ?inst1 - instance)
;    :precondition (and
;      (not (installed-app ?app1 ?inst1))
;      (requires-in-running ?inst1 ?app1)
;      (running-in ?inst1)
;      (forall (?dir1 - directory)
;        (forall (?fs1 - filesystem)
;          (imply (and (requires-fs ?fs1 ?dir1)(requires-dir ?dir1 ?app1))
;            (and (mounted-fs ?fs1 ?inst1)(exists-dir ?dir1 ?fs1))*/
;          )
;        )
;      )
;    )
;    :effect (installed-app ?app1 ?inst1)
;  )
;
;  ;; start application
;  ;; application requires an instance, file system(s), and directory(ies)
;  ;; all required applications start first
;  (:action start-app
;    :parameters (?app1 - application ?inst1 - instance)
;    :precondition (and
;      (running-in ?inst1)
;      (requires-in-running ?inst1 ?app1)
;      (installed-app ?app1 ?inst1)
;      (not (running-app ?app1 ?inst1))
;      (forall (?appn - application)
;        (forall (?instn - instance)
;          (imply (and (requires-in-running ?instn ?appn) (requires-app ?appn ?app1))
;            (running-app ?appn ?instn)
;          )
;        )
;      )
;      (forall (?dir1 - directory)
;        (forall (?fs1 - filesystem)
;          (imply (and (requires-fs ?fs1 ?dir1)(requires-dir ?dir1 ?app1))
;            (and (mounted-fs ?fs1 ?inst1)(exists-dir ?dir1 ?fs1))
;          )
;        )
;      )
;      (forall (?fl1 - file)
;        (forall (?dir1 - directory)
;          (imply (and (requires-dir ?dir1 ?fl1)(requires-fl ?fl1 ?app1))
;            (exists-file ?fl1 ?dir1)
;          )
;        )
;      )
;    )
;    :effect (running-app ?app1 ?inst1)
;  )
;
;  ;; stop application
;  ;; all dependent applications stop first
;  (:action stop-app
;    :parameters (?app1 - application ?inst1 - instance)
;    :precondition (and
;      (running-in ?inst1)
;      (running-app ?app1 ?inst1)
;      (forall (?appn - application)
;        (forall (?instn - instance)
;          (imply (and (running-app ?appn ?instn) (requires-app ?app1 ?appn))
;            (not (running-app ?appn ?instn))
;          )
;        )
;      )
;    )
;    :effect (not (running-app ?app1 ?inst1))
;  )
;
;  (:action create-dir
;    :parameters (?dir1 - directory ?fs1 - filesystem ?inst1 - instance)
;    :precondition (and
;      (requires-fs ?fs1 ?dir1)
;      (running-in ?inst1)
;      (mounted-fs ?fs1 ?inst1)
;    )
;    :effect (exists-dir ?dir1 ?fs1)
;  )
;
;  (:action copy-file
;    :parameters (?fl1 - file ?src - (either directory url) ?dest - directory ?inst1 - instance)
;    :precondition (and
;      (exists (?obj1 - object) (requires-fl ?fl1 ?obj1))
;      (running-in ?inst1)
;      (exists-file ?fl1 ?src)
;      (exists (?fs1 - filesystem)
;        (exists (?vol1 - volume)
;          (and
;            (requires-fs ?fs1 ?dest)
;            (requires-in-running ?inst1 ?vol1)
;            (mounted-fs ?fs1 ?inst1)
;            (exists-dir ?dest ?fs1)
;          )
;        )
;      )
;    )
;    :effect (exists-file ?fl1 ?dest)
;  )
)
