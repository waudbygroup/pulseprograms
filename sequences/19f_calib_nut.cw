;@ schema_version: "0.0.2"
;@ sequence_version: "0.2.0"
;@ title: Pulse nutation calibration
;@ description: |
;@   19F Pulse mutation calibration
;@
;@   - place calibration signal on-resonance
;@   - set cnst8 to nominal rf field in Hz (e.g. 60 for 60 Hz)
;@   - pulse length will be incremented in 45 degree steps
;@   - use 16 points in indirect dimension for nominal 720 degree nutation
;@   - ensure d1 is long enough for full relaxation between scans
;@   - tested with Topspin 3.7.0
;@ authors:
;@   - Chris Waudby <c.waudby@ucl.ac.uk>
;@ created: 2020-09-04
;@ last_modified: 2025-11-15
;@ repository: github.com/waudbygroup/pulseprograms
;@ status: beta
;@ experiment_type: [calibration, 1d]
;@ features: [nutation]
;@ typical_nuclei: [19F]
;@ dimensions: [calibration.duration, f1]
;@ acquisition_order: [f1, calibration.duration]
;@ reference_pulse:
;@ - {channel: f1, duration: p1, power: pl1}
;@ calibration:
;@   type: nutation
;@   channel: f1
;@   power: pl8
;@   duration: {type: linear, start: p9, step: p9}
;@   model: sine_modulated


#include <Avance.incl>
#include <Delay.incl>

"d11=30m"
"d12=20u"

; calculate power level and pulse length for desired rf field
#ifndef MANUAL
"p8=1s/(cnst8*4)"          ; pulse length for 90 degree pulse at desired rf field
"plw8=plw1*pow(p1/p8,2)"
#endif /*MANUAL*/

"p9=p8*0.5"
"inp9=p8*0.5"
"inf1=inp9"

1 ze
2 30m
  d1 pl8:f1

  p9:f1 ph1

  go=2 ph31

  d12 ipu9
  d11 mc #0 to 2 F1QF()

exit

ph1=0 2 2 0 1 3 3 1
ph31=0 2 2 0 1 3 3 1

;cnst8 : nominal rf field in Hz (e.g. 60 for 60 Hz)
;pl1 : f1 channel - power level for pulse (default)
;pl8 : f1 channel - power level for nutation calibration
;p1 : f1 channel -  high power pulse
;p8 : f1 channel -  90 degree pulse length at desired rf field
;p9 : f1 channel -  pulse length increment for nutation (45 degree)
;d1 : relaxation delay; 3-5 * T1
;NS: 1 * n
