;; This code was developed by Igor Tikhonin (ivtikhon@gmail.com) in 2014-2017.
;; Amazon's EC2 is used as the infrastructure model.

;; Instances:
;; Instances are launched in a non-default VPC.
;; Instances are getting access to the internet through a NAT instance.
;; Each instance has:
;;   - a default network interface eth0 and an associated with it private IP;
;;   - an internal DNS hostname that resolves to the private IP address of the instance;
;;
;; Applications:
;;   - require file systems, located either on system disks, or attached volumes
;;
;; File systems
;;   - file system requires a logical volume (in terms of LVM), so file systems do not
;;     exist separately of logical volumes
;;
;; (c) Igor Tikhonin

(define (domain EC2)
  (:requirements :adl)
  (:types instance volume filesystem application)
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
    ;; dependencies
    (requires-in ?inst1 - instance ?obj1 - object) ;; instance is required by object, i.e. object depends on running instance
    (requires-vol ?vol1 - volume ?obj1 - object)  ;; volume is required by object
    (requires-fs ?fs1 - filesystem ?obj1 - object)  ;; file system is required by object
    (requires-app ?app1 - application ?obj1 - object)  ;; application is required by object
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
      (exists (?obj1 - object) (requires-in ?inst1 ?obj1))
    )
    :effect (and
      (created-in ?inst1)
      (running-in ?inst1)
    )
  )

  ;; start an instance
  ;; instance is started if there is an object that requires it
  (:action start-in
    :parameters (?inst1 - instance)
    :precondition (and
      (created-in ?inst1)
      (not (running-in ?inst1))
      (exists (?obj1 - object) (requires-in ?inst1 ?obj1))
    )
    :effect (running-in ?inst1)
  )

  ;; stop an instance
  (:action stop-in
    :parameters (?inst1 - instance)
    :precondition (and
      (running-in ?inst1)
      (forall (?appn - application)
        (imply (requires-in ?inst1 ?appn)
          (not (running-app ?appn ?inst1))
        )
      )
    )
    :effect (not (running-in ?inst1))
  )

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

  ;; attach a storage volume to an instance
  ;; storage volume can be attached to one instance only; the instance can be either running or stopped
  (:action attach-vol
    :parameters (?vol1 - volume ?inst1 - instance)
    :precondition (and
      (created-in ?inst1)
      (created-vol ?vol1)
      (requires-in ?inst1 ?vol1)
      (not (exists (?instn - instance) (attached-vol ?vol1 ?instn)))
    )
    :effect (attached-vol ?vol1 ?inst1)
  )

  ;; detach a volume
  ;; all file systems dependent on volume are to be unmounted
  ;; and all applications dependent on file systems are to be stopped
  (:action detach-vol
    :parameters (?vol1 - volume ?inst1 - instance)
    :precondition (and
      (running-in ?inst1)
      (attached-vol ?vol1 ?inst1)
      (forall (?appn - application)
        (forall (?fsn - filesystem)
          (imply (and
              (running-app ?appn ?inst1)
              (requires-vol ?vol1 ?fsn)
              (requires-fs ?appn ?fsn)
            )
            (stopped-app ?appn ?inst1)
          )
        )
      )
    )
    :effect (not (attached-vol ?vol1 ?inst1))
  )

  ;; create a file system
  ;; file system requires a running instance with a volume attached
  (:action create-fs
    :parameters (?fs1 - filesystem ?vol1 - volume ?inst1 - instance)
    :precondition (and
      (not (created-fs ?fs1 ?vol1))
      (requires-vol ?vol1 ?fs1)
      (requires-in ?inst1 ?vol1)
      (running-in ?inst1)
      (attached-vol ?vol1 ?inst1)
    )
    :effect (created-fs ?fs1 ?vol1)
  )

  ;; mount a file system
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

  ;; install an application
  ;; application requires an instance and file systems
  (:action install-app
    :parameters (?app1 - application ?inst1 - instance)
    :precondition (and
      (not (installed-app ?app1 ?inst1))
      (requires-in ?inst1 ?app1)
      (forall (?fs1 - filesystem)
        (imply (requires-fs ?fs1 ?app1) (mounted-fs ?fs1 ?inst1))
      )
    )
    :effect (installed-app ?app1 ?inst1)
  )

  ;; start application
  ;; application requires an instance and file system(s)
  ;; all required applications, if there are any, start first
  (:action start-app
    :parameters (?app1 - application ?inst1 - instance)
    :precondition (and
      (running-in ?inst1)
      (requires-in ?inst1 ?app1)
      (installed-app ?app1 ?inst1)
      (not (running-app ?app1 ?inst1))
      (forall (?appn - application)
        (forall (?instn - instance)
          (imply (and (requires-in ?instn ?appn) (requires-app ?appn ?app1))
            (running-app ?appn ?instn)
          )
        )
      )
      (forall (?fs1 - filesystem)
        (imply (requires-fs ?fs1 ?app1) (mounted-fs ?fs1 ?inst1))
      )
    )
    :effect (running-app ?app1 ?inst1)
  )

  ;; stop application
  ;; all dependent applications, if there are any, stop first
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
)
