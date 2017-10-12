;;
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
	(:types instance volume filesystem)
;	 application)
	(:predicates
		;; instance states
		(running-in ?inst1 - instance) ;; 'not running' is equal to 'stopped'
		(created-in ?inst1 - instance)
		(terminated-in ?inst1 - instance) ;; terminated instance can't be re-created, so 'not created' is not equal to 'terminated'
;		;; application states
;		(running-app ?app1 - application ?inst1 - instance) ;; 'not running' is equal to 'stopped'
;		(installed-app ?app1 - application ?inst1 - instance)
		;; volume states
		(attached-vol ?vol1 - volume ?inst1 - instance) ;; 'not attached' is equal to 'detached'
		;; file system states
		(created-fs ?fs1 - filesystem ?vol1 - volume)
;		(mounted-fs ?fs1 - filesystem)  ;; 'not mounted' id equal to 'unmounted'
		;; dependencies
		(requires-in ?inst1 - instance ?obj1 - object)
		(requires-vol ?vol1 - volume ?obj1 - object) 
	)

	; create and start an instance
	(:action launch-in
		:parameters (?inst1 - instance)
		:precondition (and
			(and (not (running-in ?inst1)) (not (created-in ?inst1)) (not (terminated-in ?inst1)))
			(exists (?obj1 - object) (requires-in ?inst1 ?obj1))
		)
		:effect (and
			(created-in ?inst1)
			(running-in ?inst1)
		)
	)

	;; start an instance
	(:action start-in
		:parameters (?inst1 - instance)
		:precondition (and
			(created-in ?inst1)
			(not (running-in ?inst1))
			(exists (?obj1 - object) (requires-in ?inst1 ?obj1))
		)
		:effect (running-in ?inst1)
	)

;	;; stop an instance
;	(:action stop-in
;		:parameters (?inst1 - instance)
;		:precondition (and
;			(running-in ?inst1)
;			(forall (?appn - application)
;				(imply (running-app ?appn ?inst1)
;					(stopped-app ?appn ?inst1)
;				)
;			)
;		)
;		:effect (stopped-in ?inst1)
;	)

	;; attach a storage volume to an instance
	;; storage volume can be attached to one instance only
	;; instance can be either running or stopped
	(:action attach-vol
		:parameters (?inst1 - instance ?vol1 - volume)
		:precondition (and 
			(created-in ?inst1)
			(requires-in ?inst1 ?vol1)
			(not (exists (?instn - instance) (attached-vol ?vol1 ?instn)))
		)
		:effect (attached-vol ?vol1 ?inst1)
	)

;	;; detach a volume
;	(:action detach-vol
;		:parameters (?inst1 - instance ?vol1 - volume)
;		:precondition (and 
;			(or (running-in ?inst1) (stopped-in ?inst1))
;			(attached-vol ?vol1 ?inst1)
;			(forall (?appn - application)
;				(imply (running-app ?appn ?inst1)
;					(stopped-app ?appn ?inst1)
;				)
;			)
;		)
;		:effect (and 
;			(detached-vol ?vol1 ?inst1)
;			(not (attached-vol ?vol1 ?inst1))
;		)
;	)
;
	;; create a file system
	(:action create-fs
		:parameters (?fs1 - filesystem ?vol1 - volume)
		:precondition (and
			(not (created-fs ?fs1 ?vol1))
			(requires-vol ?vol1 ?fs1)
			(exists (?inst1 - instance) (and (running-in ?inst1) (attached-vol ?vol1 ?inst1)))
		)
		:effect (created-fs ?fs1 ?vol1)
	)

;	(:action install-app
;		:parameters (?app1 - application ?inst1 - instance)
;		:precondition (and
;			(not (installed-app ?app1 ?inst1))
;			(forall (?fs1 - filesystem)
;				(imply (app-use-fs ?fs1 ?app1)
;					(exists (?vol1 - volume) (and (fs-create-on-vol ?vol1 ?fs1) (attached-vol ?vol1 ?inst1) (created-fs ?fs1 ?vol1)))
;				)
;			)
;		)
;		:effect (installed-app ?app1 ?inst1)
;	)
;	(:action start-app
;		:parameters (?app1 - application ?inst1 - instance)
;		:precondition (and
;			(running-in ?inst1)
;			(app-run-on-in ?inst1 ?app1)
;			(installed-app ?app1 ?inst1)
;			(or (stopped-app ?app1 ?inst1) (not (running-app ?app1 ?inst1))) 
;			(forall (?appn - application)
;				(forall (?instn - instance)
;					(imply (and (app-run-on-in ?instn ?appn) (startup-order-app ?appn ?app1))
;						(running-app ?appn ?instn)
;					)
;				)
;			)
;			(forall (?fs1 - filesystem)
;				(imply (app-use-fs ?fs1 ?app1)
;					(exists (?vol1 - volume) (and (fs-create-on-vol ?vol1 ?fs1) (attached-vol ?vol1 ?inst1) (created-fs ?fs1 ?vol1)))
;				)
;			)
;		)
;		:effect (and
;			(running-app ?app1 ?inst1)
;			(not (stopped-app ?app1 ?inst1)) 
;		)
;	)
;	(:action stop-app
;		:parameters (?app1 - application ?inst1 - instance)
;		:precondition (and
;			(running-in ?inst1)
;			(running-app ?app1 ?inst1)
;			(forall (?appn - application)
;				(forall (?instn - instance)
;					(imply (and (running-app ?appn ?instn) (startup-order-app ?appn ?app1))
;						(stopped-app ?appn ?instn)
;					)
;				)
;			)
;		)
;		:effect (and
;			(stopped-app ?app1 ?inst1)
;			(not (running-app ?app1 ?inst1))
;		)
;	)
)
