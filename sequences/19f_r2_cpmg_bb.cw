;@ schema_version: "0.0.2"
;@ sequence_version: "0.1"
;@ title: 19F R2 (CPMG)
;@ description: |
;@   1D 19F broadband R2 (CPMG) measurement
;@
;@   - with 1H decoupling
;@   - set d20 to desired echo spacing (e.g. 10-20 ms)
;@   - set vclist to desired number of CPMG cycles
;@ authors:
;@   - Chris Waudby <c.waudby@ucl.ac.uk>
;@ created: 2025-12-10
;@ last_modified: 2025-12-10
;@ repository: github.com/waudbygroup/pulseprograms
;@ status: beta
;@ experiment_type: [relaxation, 1d]
;@ features: [R2, cpmg, broadband]
;@ typical_nuclei: [19F, 1H]
;@ dimensions: [relaxation.duration, f1]
;@ acquisition_order: [f1, relaxation.duration]
;@ reference_pulse:
;@ - {channel: f1, duration: p1, power: pl1}
;@ - {channel: f2, duration: p3, power: pl2}
;@ relaxation: {type: R2, model: exponential-decay, channel: f1, duration: {counter: ncyc, scale: d20}}


#include <Avance.incl>
#include <Grad.incl>
#include <Delay.incl>

define list<loopcounter> ncyc=<$VCLIST>
/****************************/
/* Initialize loop counters */
/****************************/
"l1=0"


"d11=30m"
"d12=20u"

"p20=600u"
;"p21=12u"
;"spw20=plw1*pow(p1/p21,2)"

; for baseopt
;"acqt0=-p1*2/3.1416"
"acqt0=0"
"DELTA=d20*-0.5-p21*0.5"

1 ze 
  d11 pl12:f2
2 30m do:f2

  d1

  (p20:sp20 ph1):f1
3 DELTA
  (p21:sp21 ph2):f1
  DELTA
  lo to 3 times ncyc

  go=2 ph31 cpd2:f2
  d11 do:f2 mc #0 to 2 
     F1QF(calclc(ncyc, 1))

exit 
 

ph1 =0 2
ph2 =0 0 1 1 2 2 3 3
ph31=0 2 2 0

;pl12: f2 channel - power level for CPD/BB decoupling
;p16: homospoil/gradient pulse                       [0.5 msec]
;d1 : relaxation delay (excluding saturation time)
;d11: delay for disk I/O                             [30 msec]
;d12: delay for power switching                      [20 usec]
;d16: delay for homospoil/gradient recovery
;d20: length of single CPMG echo period              [10-20 ms]
;cpd2: decoupling according to sequence defined by cpdprg2
;pcpd2: f2 channel - 90 degree pulse for decoupling sequence
;p20: 600us BURBOP_19F_90
;spnam20: BURBOP_19F_90
;sp20: 20 kHz
;p20: 1000us BURBOP_19F_180
;spnam20: BURBOP_19F_180
;sp20: 20 kHz
;ns: 1 * n
;ds: 4


;for z-only gradients:
;gpz1: 41%

;use gradient files:   
;gpnam1: SMSQ10.100

