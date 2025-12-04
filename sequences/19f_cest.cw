;@ schema_version: "0.0.2"
;@ sequence_version: "0.1.4"
;@ title: 19F CEST
;@ description: |
;@   1D 19F CEST measurement
;@
;@   - set nominal saturation power cnst25 (in Hz)
;@   - saturation applied for duration d18 during recycle delay
;@   - additional relaxation delay of d1 applied without saturation
;@   - use '-DHDEC' for 1H decoupling during acquisition
;@   - tested with Topspin 3.7.0
;@ authors:
;@   - Chris Waudby <c.waudby@ucl.ac.uk>
;@ created: 2025-08-01
;@ last_modified: 2025-12-04
;@ repository: github.com/waudbygroup/pulseprograms
;@ status: beta
;@ experiment_type: [cest, 1d]
;@ features: []
;@ typical_nuclei: [19F]
;@ dimensions: [cest.offset, f1]
;@ acquisition_order: [f1, cest.offset]
;@ reference_pulse:
;@ - {channel: f1, duration: p1, power: pl1}
;@ cest: {channel: f1, power: pl25, duration: d18, offset: F19sat}

#include <Avance.incl>
#include <Grad.incl>
#include <Delay.incl>


define list<frequency> F19sat = <$FQ1LIST>

"d11=30m"
"d12=20u"

"p25=1000000/(4*cnst25)" ; SL 90 pulse length
"plw25=plw1*pow(p1/p25,2)" ; SL power

#ifdef HDEC
"pcpd2=62.5u"          ; pulse length for 4kHz decoupling
"plw12=plw2*pow(p3/pcpd2,2)"
#endif /* HDEC */

; for baseopt
"acqt0=-p1*2/3.1416"

1 ze 
#ifdef HDEC
  d11 pl12:f2
2 d11 do:f2
#else
2 d11
#endif /* HDEC */

  d1

  ; CEST period
  4u pl25:f1 
  4u F19sat:f1
  d18 cw:f1 ph11
  4u do:f1 

  ; purge
  4u UNBLKGRAD
  p16:gp1
  d16 pl1:f1 fq=0:f1
  4u BLKGRAD

/* ---------------------------------
; anti-ringing
; --------------------------------*/
 p1 ph1
 4u
 p1 ph2
 4u
 p1 ph3
;------------------------------------

#ifdef HDEC
  go=2 ph31 cpd2:f2
  d11 do:f2 mc #0 to 2 
     F1QF(calclist(F19sat, 1))
#else
  go=2 ph31 
  d11 mc #0 to 2 
     F1QF(calclist(F19sat, 1))
#endif /* HDEC */

exit 
  

ph1 =0
ph2 =2 0
ph3 =0 0 2 2 1 1 3 3
ph11=0 
ph31=0 2 2 0 1 3 3 1


;p16: homospoil/gradient pulse                       [1 msec]
;d1 : relaxation delay (excluding saturation time)
;d11: delay for disk I/O                             [30 msec]
;d12: delay for power switching                      [20 usec]
;d16: delay for homospoil/gradient recovery
;d18: saturation time
;pl8: f1 channel - power level for CEST saturation
;ns: 1 * n
;ds: 4


;for z-only gradients:
;gpz1: 41%

;use gradient files:   
;gpnam1: SMSQ10.100

