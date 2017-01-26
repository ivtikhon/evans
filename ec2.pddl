;;
;; This code was developed by Igor Tikhonin (igor.tikhonin@gmail.com) in 2014-2015.
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

(define (domain EC2)
	(:requirements :adl)
	(:types instance volume filesystem application)
	(:predicates
		;; instance states
		(running-in ?inst1 - instance)
		(stopped-in ?inst1 - instance)
		(created-in ?inst1 - instance)
		(terminated-in ?inst1 - instance)
		;; application states
		(running-app ?app1 - application ?inst1 - instance)
		(stopped-app ?app1 - application ?inst1 - instance)
		(installed-app ?app1 - application ?inst1 - instance)
		;; volume states
		(attached-vol ?vol1 - volume ?inst1 - instance)
		(detached-vol ?vol1 - volume ?inst1 - instance)
		;; file system states
		(created-fs ?fs1 - filesystem ?vol1 - volume)
		;; directives
		(startup-order-app ?app1 ?app2 - application)
		(vol-attach-to-in ?inst1 - instance ?vol1 - volume) 
		(app-run-on-in ?inst1 - instance ?app1 - application)
		(app-use-fs ?fs1 - filesystem ?app1 - application)
		(fs-create-on-vol ?vol1 - volume ?fs1 - filesystem)
	)
	; create and start an instance
	(:action launch-in
		:parameters (?inst1 - instance)
		:precondition (and (not (running-in ?inst1)) (or (not (created-in ?inst1)) (terminated-in ?inst1)))
		:effect (and
			(created-in ?inst1)
			(running-in ?inst1)
			(not (stopped-in ?inst1))
		)
	)
	; start an instance
	(:action start-in
		:parameters (?inst1 - instance)
		:precondition (and (created-in ?inst1) (or (stopped-in ?inst1) (not (running-in ?inst1))))
		:effect (and
			(running-in ?inst1)
			(not (stopped-in ?inst1))
		)
	)
	; stop an instance
	(:action stop-in
		:parameters (?inst1 - instance)
		:precondition (and
			(running-in ?inst1)
			(forall (?appn - application)
				(imply (running-app ?appn ?inst1)
					(stopped-app ?appn ?inst1)
				)
			)
		)
		:effect (stopped-in ?inst1)
	)
	; attache a storage volume
	; storage volumes can be attached to one instance only
	(:action attach-vol
		:parameters (?inst1 - instance ?vol1 - volume)
		:precondition (and 
			(or (running-in ?inst1) (stopped-in ?inst1))
			(vol-attach-to-in ?inst1 ?vol1)
			(not (exists (?instn - instance) (attached-vol ?vol1 ?instn)))
		)
		:effect (and 
			(attached-vol ?vol1 ?inst1)
			(not (detached-vol ?vol1 ?inst1))
		)
	)
	; detach a volume
	(:action detach-vol
		:parameters (?inst1 - instance ?vol1 - volume)
		:precondition (and 
			(or (running-in ?inst1) (stopped-in ?inst1))
			(attached-vol ?vol1 ?inst1)
			(forall (?appn - application)
				(imply (running-app ?appn ?inst1)
					(stopped-app ?appn ?inst1)
				)
			)
		)
		:effect (and 
			(detached-vol ?vol1 ?inst1)
			(not (attached-vol ?vol1 ?inst1))
		)
	)
	; create a file system
	(:action create-fs
		:parameters (?fs1 - filesystem ?vol1 - volume)
		:precondition (and
			(not (created-fs ?fs1 ?vol1))
			(fs-create-on-vol ?vol1 ?fs1)
			(exists (?inst1 - instance) (and (running-in ?inst1) (attached-vol ?vol1 ?inst1)))
		)
		:effect (created-fs ?fs1 ?vol1)
	)
	(:action install-app
		:parameters (?app1 - application ?inst1 - instance)
		:precondition (and
			(not (installed-app ?app1 ?inst1))
			(forall (?fs1 - filesystem)
				(imply (app-use-fs ?fs1 ?app1)
					(exists (?vol1 - volume) (and (fs-create-on-vol ?vol1 ?fs1) (attached-vol ?vol1 ?inst1) (created-fs ?fs1 ?vol1)))
				)
			)
		)
		:effect (installed-app ?app1 ?inst1)
	)
	(:action start-app
		:parameters (?app1 - application ?inst1 - instance)
		:precondition (and
			(running-in ?inst1)
			(app-run-on-in ?inst1 ?app1)
			(installed-app ?app1 ?inst1)
			(or (stopped-app ?app1 ?inst1) (not (running-app ?app1 ?inst1))) 
			(forall (?appn - application)
				(forall (?instn - instance)
					(imply (and (app-run-on-in ?instn ?appn) (startup-order-app ?appn ?app1))
						(running-app ?appn ?instn)
					)
				)
			)
			(forall (?fs1 - filesystem)
				(imply (app-use-fs ?fs1 ?app1)
					(exists (?vol1 - volume) (and (fs-create-on-vol ?vol1 ?fs1) (attached-vol ?vol1 ?inst1) (created-fs ?fs1 ?vol1)))
				)
			)
		)
		:effect (and
			(running-app ?app1 ?inst1)
			(not (stopped-app ?app1 ?inst1)) 
		)
	)
	(:action stop-app
		:parameters (?app1 - application ?inst1 - instance)
		:precondition (and
			(running-in ?inst1)
			(running-app ?app1 ?inst1)
			(forall (?appn - application)
				(forall (?instn - instance)
					(imply (and (running-app ?appn ?instn) (startup-order-app ?appn ?app1))
						(stopped-app ?appn ?instn)
					)
				)
			)
		)
		:effect (and
			(stopped-app ?app1 ?inst1)
			(not (running-app ?app1 ?inst1))
		)
	)
)
