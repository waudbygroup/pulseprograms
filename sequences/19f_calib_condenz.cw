;@ schema_version: "0.0.3"
;@ sequence_version: "0.1.2"
;@ title: CONDENZ 19F pulse calibration
;@ description: |
;@   CONDENZ 19F pulse calibration
;@
;@   - place calibration signal on-resonance
;@   - set cnst25 to nominal rf field in Hz (e.g. 60 for 60 Hz)
;@   - use offsets from +/- 5 x cnst25 for calculation, plus 100x off-resonance for reference
;@   - use '-DHDEC' for 1H decoupling during acquisition
;@   - ensure d1 is long enough for full relaxation between scans
;@   - tested on Topspin 3.7.0
;@ authors:
;@   - Chris Waudby <c.waudby@ucl.ac.uk>
;@ citation:
;@   - Jaladeep et al. JMR (2021)
;@ doi:
;@   - 10.1016/j.jmr.2021.107032
;@ created: 2026-03-10
;@ last_modified: 2026-04-30
;@ repository: github.com/waudbylab/pulseprograms
;@ status: beta
;@ experiment_type: [calibration, 1d]
;@ features: [condenz]
;@ typical_nuclei: [19F]
;@ dimensions: [calibration.offset, f1]
;@ acquisition_order: [f1, calibration.offset]
;@ reference_pulse:
;@ - {channel: f1, duration: p1, power: pl1}
;@ - {channel: f2, duration: p3, power: pl2}
;@ calibration:
;@   type: condenz
;@   channel: f1
;@   power: pl25
;@   duration: p26
;@   offset: F19sat


#include <Avance.incl>
#include <Delay.incl>
#include <Grad.incl>


"d11=30m"
"d12=20u"

; calculate power level and pulse length for desired rf field
"p25=1s/(cnst25*4)"          ; pulse length for 90 degree pulse at desired rf field
"plw25=plw1*pow(p1/p25,2)"
"p26=20*p25" ; 5 cycles of nutation (5 x 4 x 90)

define list<frequency> F19sat = <$FQ1LIST>

#ifdef HDEC
"pcpd2=62.5u"          ; pulse length for 4kHz decoupling
"plw12=plw2*pow(p3/pcpd2,2)"
#endif /* HDEC */


1 ze 
#ifdef HDEC
  d11 pl12:f2
2 d11 do:f2
#else
2 d11
#endif /* HDEC */

  d1

  ; CONDENZ pulse
  4u pl25:f1 
  4u F19sat:f1
  p26:f1 ph11

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

;cnst25 : nominal rf field in Hz (e.g. 1000 for 1000 Hz)
;pl1 : f1 channel - power level for pulse (default)
;pl25 : f1 channel - power level for nutation calibration (calculated)
;p1 : f1 channel -  high power pulse
;p25 : f1 channel -  90 degree pulse length at desired rf field (calculated)
;p26 : f1 channel -  pulse length for 5 cycles of nutation at desired rf field (calculated)
;d1 : relaxation delay; 3-5 * T1
;NS: 1 * n
;td1: 42