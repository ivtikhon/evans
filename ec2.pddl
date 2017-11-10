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
    instance volume filesystem application directory url file - object
  )
  (:predicates
    ;; instance states
    (running-in ?inst1 - instance)  ;; 'not running' is equal to 'stopped'
    (created-in ?inst1 - instance)
    (terminated-in ?inst1 - instance) ;; terminated instance can't be re-created, so 'not created' is not equal to 'terminated'
    ;; application states
    (running-app ?app1 - application ?inst1 - instance) ;; 'not running' is equal to 'stopped'
    (installed-app ?app1 - application ?inst1 - instance)
    ;; volume states
    (attached-vol ?vol1 - volume ?inst1 - instance) ;; 'not attached' is equal to 'detached'
    (created-vol ?vol1 - volume)
    ;; file system states
    (created-fs ?fs1 - filesystem ?vol1 - volume)
    (mounted-fs ?fs1 - filesystem ?inst1 - instance) ;; 'not mounted' id equal to 'unmounted'
    ;; file states
    (exists-file ?fl1 - file ?path - (either directory url))
    ;; directory states
    (exists-dir ?dir1 - directory ?fs1 - filesystem)
    ;; dependencies
    (requirement-satisfied ?obj1 ?obj2 - object)  ;; depependency resolved fpr the pair of objects, when obj2 depends on obj1
;    (requires-in ?inst1 - instance ?obj1 - object) ;; instance is required by object, i.e. object depends on running instance
    (requires-in-running ?inst1 - instance ?obj1 - object)
    (requires-in-created ?inst1 - instance ?obj1 - object)
    (requires-vol ?vol1 - volume ?obj1 - object)  ;; volume is required by object
    (requires-fs ?fs1 - filesystem ?obj1 - object)  ;; file system is required by object
    (requires-app ?app1 - application ?obj1 - object)  ;; application is required by object
    (requires-dir ?dir1 - directory ?obj1 - object)  ;; directory is required by object
    (requires-fl ?fl1 - file ?obj1 - object) ;; file is required by object
  )

  ;; create and start an instance
  ;; instance is created if there is an object that requires it
  ;; terminated instance can't be re-created
  (:action launch-in
    :parameters (?inst1 - instance)
    :precondition (and
      (and
        (not (running-in ?inst1))
        (not (created-in ?inst1))
        (not (terminated-in ?inst1))
      )
      (exists (?obj1 - object)
        (and
          (or (requires-in-created ?inst1 ?obj1)(requires-in-running ?inst1 ?obj1))
          (not (requirement-satisfied ?inst1 ?obj1))
        )
      )
    )
    :effect (and
      (created-in ?inst1)
      (running-in ?inst1)
      (forall (?objn - object)
        (when (or (requires-in-created ?inst1 ?objn)(requires-in-running ?inst1 ?objn))
          (requirement-satisfied ?inst1 ?objn)
        )
      )
    )
  )

  ;; start an instance
  ;; instance is started if there is an object that requires it
  (:action start-in
    :parameters (?inst1 - instance)
    :precondition (and
      (created-in ?inst1)
      (not (running-in ?inst1))
      (exists (?obj1 - object)
        (and
          (requires-in-running ?inst1 ?obj1)
          (not (requirement-satisfied ?inst1 ?obj1))
        )
      )
    )
    :effect (and
      (running-in ?inst1)
      (forall (?objn - object)
        (when (requires-in-running ?inst1 ?objn)
          (requirement-satisfied ?inst1 ?objn)
        )
      )
    )
  )

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
      (not (created-vol ?vol1))
      (exists (?obj1 - object) (requires-vol ?vol1 ?obj1))
    )
    :effect (created-vol ?vol1)
  )

  ;; attach storage volume to instance
  ;; storage volume can be attached to one instance only
  ;; the instance can be either running or stopped
  (:action attach-vol
    :parameters (?vol1 - volume ?inst1 - instance)
    :precondition (and
      (created-in ?inst1)
      (created-vol ?vol1)
      (requires-in-running ?inst1 ?vol1)
      (not (exists (?instn - instance) (attached-vol ?vol1 ?instn)))
    )
    :effect (attached-vol ?vol1 ?inst1)
  )

  ;; detach volume
  ;; all file systems dependent on volume are to be unmounted
  ;; and all applications dependent on file systems are to be stopped
  (:action detach-vol
    :parameters (?vol1 - volume ?inst1 - instance)
    :precondition (and
      (running-in ?inst1)
      (attached-vol ?vol1 ?inst1)
      (forall (?fsn - filesystem)
        (imply (requires-vol ?vol1 ?fsn)(not (mounted-fs ?fsn ?inst1)))
      )
    )
    :effect (not (attached-vol ?vol1 ?inst1))
  )

  ;; create file system
  ;; file system requires a running instance with a volume attached
  (:action create-fs
    :parameters (?fs1 - filesystem ?vol1 - volume ?inst1 - instance)
    :precondition (and
      (not (created-fs ?fs1 ?vol1))
      (requires-vol ?vol1 ?fs1)
      (requires-in-running ?inst1 ?vol1)
      (running-in ?inst1)
      (attached-vol ?vol1 ?inst1)
    )
    :effect (created-fs ?fs1 ?vol1)
  )

  ;; mount file system
  ;; file system requires a running instance with a volume attached
  ;; file system is supposed to be created in order to be mounted
  (:action mount-fs
    :parameters (?fs1 - filesystem ?inst1 - instance)
    :precondition (and
      (exists (?vol1 - volume) (and (created-fs ?fs1 ?vol1) (attached-vol ?vol1 ?inst1)))
      (running-in ?inst1)
    )
    :effect (mounted-fs ?fs1 ?inst1)
  )

  ;; unmount file system
  ;; all applications require this file system are to be stopped
  (:action unmount-fs
    :parameters (?fs1 - filesystem ?inst1 - instance)
    :precondition (and
      (mounted-fs ?fs1 ?inst1)
      (running-in ?inst1)
      (exists (?vol1 - volume) (and (requires-vol ?vol1 ?fs1) (attached-vol ?vol1 ?inst1)))
      (forall (?appn - application)
        (forall (?dir1 - directory)
          (imply (and (requires-fs ?fs1 ?dir1)(requires-dir ?dir1 ?appn)(requires-in-running ?inst1 ?appn))(not (running-app ?appn ?inst1)))
        )
      )
    )
    :effect (not (mounted-fs ?fs1 ?inst1))
  )

  ;; install application
  ;; application requires an instance and directory(ies)
  ;; all required file systems and directories are to be created first
  (:action install-app
    :parameters (?app1 - application ?inst1 - instance)
    :precondition (and
      (not (installed-app ?app1 ?inst1))
      (requires-in-running ?inst1 ?app1)
      (running-in ?inst1)
      (forall (?dir1 - directory)
        (forall (?fs1 - filesystem)
          (imply (and (requires-fs ?fs1 ?dir1)(requires-dir ?dir1 ?app1))
            (and (mounted-fs ?fs1 ?inst1)(exists-dir ?dir1 ?fs1))
          )
        )
      )
    )
    :effect (installed-app ?app1 ?inst1)
  )

  ;; start application
  ;; application requires an instance, file system(s), and directory(ies)
  ;; all required applications start first
  (:action start-app
    :parameters (?app1 - application ?inst1 - instance)
    :precondition (and
      (running-in ?inst1)
      (requires-in-running ?inst1 ?app1)
      (installed-app ?app1 ?inst1)
      (not (running-app ?app1 ?inst1))
      (forall (?appn - application)
        (forall (?instn - instance)
          (imply (and (requires-in-running ?instn ?appn) (requires-app ?appn ?app1))
            (running-app ?appn ?instn)
          )
        )
      )
      (forall (?dir1 - directory)
        (forall (?fs1 - filesystem)
          (imply (and (requires-fs ?fs1 ?dir1)(requires-dir ?dir1 ?app1))
            (and (mounted-fs ?fs1 ?inst1)(exists-dir ?dir1 ?fs1))
          )
        )
      )
      (forall (?fl1 - file)
        (forall (?dir1 - directory)
          (imply (and (requires-dir ?dir1 ?fl1)(requires-fl ?fl1 ?app1))
            (exists-file ?fl1 ?dir1)
          )
        )
      )
    )
    :effect (running-app ?app1 ?inst1)
  )

  ;; stop application
  ;; all dependent applications stop first
  (:action stop-app
    :parameters (?app1 - application ?inst1 - instance)
    :precondition (and
      (running-in ?inst1)
      (running-app ?app1 ?inst1)
      (forall (?appn - application)
        (forall (?instn - instance)
          (imply (and (running-app ?appn ?instn) (requires-app ?app1 ?appn))
            (not (running-app ?appn ?instn))
          )
        )
      )
    )
    :effect (not (running-app ?app1 ?inst1))
  )

  (:action create-dir
    :parameters (?dir1 - directory ?fs1 - filesystem ?inst1 - instance)
    :precondition (and
      (requires-fs ?fs1 ?dir1)
      (running-in ?inst1)
      (mounted-fs ?fs1 ?inst1)
    )
    :effect (exists-dir ?dir1 ?fs1)
  )

  (:action copy-file
    :parameters (?fl1 - file ?src - (either directory url) ?dest - directory ?inst1 - instance)
    :precondition (and
      (exists (?obj1 - object) (requires-fl ?fl1 ?obj1))
      (running-in ?inst1)
      (exists-file ?fl1 ?src)
      (exists (?fs1 - filesystem)
        (exists (?vol1 - volume)
          (and
            (requires-fs ?fs1 ?dest)
            (requires-in-running ?inst1 ?vol1)
            (mounted-fs ?fs1 ?inst1)
            (exists-dir ?dest ?fs1)
          )
        )
      )
    )
    :effect (exists-file ?fl1 ?dest)
  )
)
