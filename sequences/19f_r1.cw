;@ schema_version: "0.0.2"
;@ sequence_version: "0.1.1"
;@ title: 19F R1
;@ description: |
;@   1D 19F R1 measurement
;@
;@   - with optional 1H decoupling (use -DHDEC flag)
;@ authors:
;@   - Chris Waudby <c.waudby@ucl.ac.uk>
;@ created: 2024-05-21
;@ last_modified: 2025-11-15
;@ repository: github.com/waudbygroup/pulseprograms
;@ status: beta
;@ experiment_type: [relaxation, 1d]
;@ features: [R1, inversion_recovery, broadband]
;@ typical_nuclei: [19F, 1H]
;@ dimensions: [relaxation.duration, f1]
;@ acquisition_order: [f1, relaxation.duration]
;@ reference_pulse:
;@ - {channel: f1, duration: p1, power: pl1}
;@ - {channel: f2, duration: p3, power: pl2}
;@ relaxation: {type: R1, model: inversion_recovery, channel: f1, duration: t1delay}


#include <Avance.incl>
#include <Grad.incl>
#include <Delay.incl>

define list<delay> t1delay = <$VDLIST>

"d11=30m"
"d12=20u"

"l1=0"

; calculate 5kHz purge pulse
"p11=50u"
"plw11=plw1*pow(p1/p11,2)"

"p2=p1*2"

; for baseopt
"acqt0=-p1*2/3.1416"

"DELTA=1m"

1 ze 
#ifdef HDEC
  d11 pl12:f2
2 30m do:f2
#else
  d11
2 30m
#endif /* HDEC */

  "DELTA=t1delay[l1]-p16-d16-4u"

  ; purge
  20u pl11:f1
  (2mp ph11):f1
  20u
  (3mp ph12):f1

  d1
  4u UNBLKGRAD
  4u pl1:f1

  p2 ph1     ; 180
  p16:gp1
  d16
  4u BLKGRAD
  DELTA

  p1 ph2     ; 90

#ifdef HDEC
  go=2 ph31 cpd2:f2
  d11 do:f2 mc #0 to 2 
     F1QF(calclc(l1, 1))
#else
  go=2 ph31 
  d11 mc #0 to 2 
     F1QF(calclc(l1, 1))
#endif /* HDEC */

exit 
 

ph1 = 0 1 2 3
ph2 = 0 0 0 0 1 1 1 1 2 2 2 2 3 3 3 3
ph31= 0 0 0 0 1 1 1 1 2 2 2 2 3 3 3 3

;pl1: f1 channel - power level for pulse (default)
;pl11: f1 channel - 5 kHz purge pulse
;pl12: f2 channel - power level for CPD/BB decoupling
;p1 : f1 channel -  90 degree high power pulse
;p2 : f1 channel - 180 degree high power pulse
;p16: homospoil/gradient pulse                       [1 msec]
;d1 : relaxation delay (excluding saturation time)
;d11: delay for disk I/O                             [30 msec]
;d12: delay for power switching                      [20 usec]
;d16: delay for homospoil/gradient recovery
;cpd2: decoupling according to sequence defined by cpdprg2
;pcpd2: f2 channel - 90 degree pulse for decoupling sequence
;ns: 4 * n
;ds: 4


;for z-only gradients:
;gpz1: 41%

;use gradient files:   
;gpnam1: SMSQ10.100

