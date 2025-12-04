;@ schema_version: "0.0.2"
;@ sequence_version: "0.2.2"
;@ title: 19F off-resonance R1rho relaxation dispersion
;@ description: |
;@   Off-resonance 19F R1rho as pseudo-3D
;@
;@   - set SL power in pl25
;@   - set SL durations in VPLIST
;@   - set SL offsets in FQ1LIST (must be !sfo hz!)
;@   - 4x expected scans will be acquired to cover z/-z and theta/theta-bar
;@ authors:
;@   - Chris Waudby <c.waudby@ucl.ac.uk>
;@   - Jan Overbeck
;@ citation:
;@   - Overbeck (2020)
;@ created: 2020-01-01
;@ last_modified: 2025-12-04
;@ repository: github.com/waudbygroup/pulseprograms
;@ status: beta
;@ experiment_type: [r1rho, 1d]
;@ features: [relaxation_dispersion, off_resonance, temperature_compensation]
;@ typical_nuclei: [19F, 1H]
;@ dimensions: [r1rho.duration, r1rho.offset, f1]
;@ acquisition_order: [f1, r1rho.duration, r1rho.offset]
;@ reference_pulse:
;@ - {channel: f1, duration: p1, power: pl1}
;@ - {channel: f2, duration: p3, power: pl2}
;@ r1rho: {channel: f1, power: pl25, duration: taulist, offset: fqlist, alignment: hard_pulse}



#include <Avance.incl>
#include <Grad.incl>

define list<pulse> taulist = <$VPLIST>
define list<frequency> fqlist = <$FQ1LIST>

"p2=p1*2"
#ifdef HDEC
"pcpd2=62.5u"          ; pulse length for 4kHz decoupling
"plw8=plw2*pow(p3/pcpd2,2)"
#endif /* HDEC */

"d11=30m"
"l1=0"  ; z/-z and theta/theta-bar
"l2=0"  ; vplist
"l3=0"

"cnst28=fqlist"
"p29=10*log10(plw25)"
"p3 = p1*pow(10,(10*log10(plw1) - p29)/20)"       ;90 degree SL pulse
"p6 = ((cnst28)/((1/(p3*4))))"            ; spin lock offset / spin lock power
"p7 = atan(p6)*180/PI"                    ; arc tan from this ratio = theta in deg
"p4 = p1*(1-p7/90)"                                          ; theta pulse length
"p5 = p1*(1+p7/90)"                                          ; 180-theta pulse length

"p30 = taulist.max"  ; maximum SL length for T compentation

aqseq 312

1 ze

#ifdef HDEC
  d11 pl12:f2
2 30m do:f2
#else
2 30m
#endif /* HDEC */

/*--------------------------------
; calculate hard pulse for offset
; dependent tip angle theta
; -------------------------------*/
  "cnst28=fqlist"
  "p6 = ((cnst28)/((1/(p3*4))))"            ; spin lock offset / spin lock power
  "p7 = atan(p6)*180/PI"                    ; arc tan from this ratio = theta in deg
  "p4 = p1*(1-p7/90)"                                          ; theta pulse length
  "p5 = p1*(1+p7/90)"                                          ; 180-theta pulse length

/* ---------------------------------
;     heating compensation
; --------------------------------*/
  "p32=taulist[l2]"
  "p31=p30-p32"
  if "p31 > 0.0"
    {
    1u fq=cnst30(bf ppm):f1
    1u pl25:f1
    (p31 ph1):f1
    }

   d1

/* ---------------------------------
;  transfer to theta and SL
; --------------------------------*/
1u fq=0:f1

if "l1 % 4 == 0"
{
  ; +z, theta
  (p44:sp30 ph1):f1
  1u
  (p44:sp30 ph10):f1
  1u pl1:f1
  p4 ph2          ; theta(y)
  1u fq=fqlist:f1
  1u pl25:f1
  (p32 ph1):f1    ; SL(x)
  1u fq=0:f1
  1u pl1:f1
  p4 ph4          ; theta(-y)
}
if "l1 % 4 == 1"
{
  ; -z, theta
  (p44:sp30 ph1):f1
  1u pl1:f1
  p4 ph4          ; theta(-y)
  1u fq=fqlist:f1
  1u pl25:f1
  (p32 ph3):f1    ; SL(-x)
  1u fq=0:f1
  1u pl1:f1
  p4 ph2          ; theta(y)
  1u
  (p44:sp30 ph10):f1
}
if "l1 % 4 == 2"
{
  ; +z, theta-bar
  (p44:sp30 ph1):f1
  1u
  (p44:sp30 ph10):f1
  1u pl1:f1
  p5 ph2          ; thetabar(y)
  1u fq=fqlist:f1
  1u pl25:f1
  (p32 ph3):f1    ; SL(-x)
  1u fq=0:f1
  1u pl1:f1
  p5 ph4          ; thetabar(-y)
}
if "l1 % 4 == 3"
{
  ; -z, theta-bar
  (p44:sp30 ph1):f1
  1u pl1:f1
  p5 ph4          ; thetabar(-y)
  1u fq=fqlist:f1
  1u pl25:f1
  (p32 ph1):f1    ; SL(x)
  1u fq=0:f1
  1u pl1:f1
  p5 ph2          ; thetabar(y)
  1u
  (p44:sp30 ph10):f1
}

/* ---------------------------------
;     anti-ringing
; --------------------------------*/
  1u pl1:f1
  p1 ph11
  d13
  p1 ph12
  d13
  p1 ph13
; ----------------------------------
#ifdef HDEC
  go=2 ph31 cpd2:f2

  10u do:f2
  10u iu1
  lo to 2 times 4

  30m mc #0 to 2
   F1QF(calclc(l2,1))
   F2QF(calclist(fqlist,1))
#else
 go=2 ph31

  10u iu1
  lo to 2 times 4

  30m mc #0 to 2
   F1QF(calclc(l2,1))
   F2QF(calclist(fqlist,1))
#endif /* HDEC */
 ; mc: F1 = r1rho.duration
 ;     F2 = r1rho.offset
exit


ph1=0
ph2=1
ph3=2
ph4=3
ph10=2
ph11=0
ph12=2 0
ph13=0 0 2 2
ph31=0 2 2 0

;pl1 : f1 channel - power level for pulse (default)
;p1 : f1 channel -  90 degree high power pulse
;p2 : f1 channel - 180 degree high power pulse
;d1 : relaxation delay; 1-5 * T1
;d11: delay for disk I/O    [30 msec]
;ns: 4 * n (actual ns will be 4x this value)
;ds: > 4

;p44: f1 channel - 180 degree shaped pulse
;sp30: f1 channel - shaped pulse 180 degree (Bip720,50,20.1)
;pl25: spin lock power
;VPLIST: list of spin lock lengths
;FQ1LIST: list of spin lock offsets !sfo hz!

;p30: maximum SL length used for highest power (for T compensation)
;cnst30: offset for T compensation (in ppm) [250 ppm]

;1H decoupling:
;pl2 : f2 channel - power level for pulse (default)
;p3 : f2 channel - 90 degree high power pulse
;pl12: f2 channel - power level for CPD/BB decoupling
;cpd2: decoupling according to sequence defined by cpdprg2
;pcpd2: f2 channel - 90 degree pulse for decoupling sequence
