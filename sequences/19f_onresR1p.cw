;@ schema_version: "0.0.2"
;@ sequence_version: "0.1.3"
;@ title: 19F on-resonance R1rho relaxation dispersion
;@ description: |
;@   On-resonance 19F R1rho (pseudo-3D)
;@
;@   - set SL durations in VPLIST
;@   - set SL power levels in VALIST !in dB!
;@   - set cnst28 to the desired on-resonance offset (in ppm)
;@   - with temperature compensation
;@   - use '-DHDEC' for 1H decoupling during acquisition
;@   - tested with Topspin 3.7.0
;@ authors:
;@   - Chris Waudby <c.waudby@ucl.ac.uk>
;@   - Jan Overbeck
;@ citation:
;@   - Hazlett et al. ChemRxiv (2025)
;@   - Overbeck (2020)
;@ doi:
;@   - 10.26434/chemrxiv-2025-vt1wg
;@ created: 2020-01-01
;@ last_modified: 2025-12-04
;@ repository: github.com/waudbygroup/pulseprograms
;@ status: beta
;@ experiment_type: [r1rho, 1d]
;@ features: [relaxation_dispersion, on_resonance, temperature_compensation]
;@ typical_nuclei: [19F, 1H]
;@ dimensions: [r1rho.duration, r1rho.power, f1]
;@ acquisition_order: [f1, r1rho.duration, r1rho.power]
;@ reference_pulse:
;@ - {channel: f1, duration: p1, power: pl1}
;@ - {channel: f2, duration: p3, power: pl2}
;@ r1rho: {channel: f1, power: powerlist, duration: taulist, offset: 0, alignment: hard_pulse}


/*--------------------------------
; Parameters to set
; -------------------------------*/
;cnst28 : offset of SL in ppm
;p30 : maximum SL length
;p31 : heating compensation SL length
;p32 : spin lock lenght T_ex
;pl25 : spin lock power, = sp4
;VPLIST : list of spin lock lengths
;VALIST : list of spin lock powers !in dB!

#include <Avance.incl>
#include <Grad.incl>
#include <Delay.incl>

define list<pulse> taulist = <$VPLIST>
define list<power> powerlist = <$VALIST>


"p2=p1*2"
#ifdef HDEC
"pcpd2=62.5u"          ; pulse length for 4kHz decoupling
"plw12=plw2*pow(p3/pcpd2,2)"
#endif /* HDEC */

"d11=30m"

"l2=0"
"l3=0"

; power (dB) for temperature compensation
"p30=taulist.max * 1.01"
"cnst35=powerlist.max"
"plw30=pow(10,-0.1*cnst35)"
"cnst34=plw30" ; maximum for T compensation

"cnst33=pow(10,-0.1*powerlist[l3])" ; SL power in W

aqseq 312


1 ze
#ifdef HDEC
  d11 pl12:f2
2 30m do:f2
#else
2 30m
#endif /* HDEC */
/*--------------------------------
; set SL delays and power
; -------------------------------*/
"p32=taulist[l2]"
"powerlist.idx = l3"
"cnst33=pow(10,-0.1*powerlist[l3])" ; SL power in W
"p31=p30-p32*(cnst33/cnst34)"

/* ---------------------------------
; relaxation delay (d1)
; --------------------------------*/
 d1


/* ---------------------------------
; heating compensation
; --------------------------------*/

if "p31 > 0.0"
 {
 1u fq=cnst30(bf ppm):f1
 1u pl30:f1
 (p31 ph1):f1
 }


/* ---------------------------------
; transfer to theta and SL
; --------------------------------*/
 30m
 1u fq=cnst28(bf ppm):f1
if "p32 == 0.0"
 {
 1u pl1:f1
 p1 ph4
 }
else
 {
 1u pl1:f1
 p1 ph4
 1u powerlist:f1
 (p32 ph1):f1 ; <-- this is the Spin Lock
}
;-----------------------------------

/* ---------------------------------
; transfer back to z
; --------------------------------*/
 1u pl1:f1
 p1 ph5
;------------------------------------

/* ---------------------------------
; anti-ringing
; --------------------------------*/
 1u pl1:f1
 p1 ph1
 4u
 p1 ph2
 4u
 p1 ph3
;------------------------------------

; 4u BLKGRAD
#ifdef HDEC
 go=2 ph31 cpd2:f2
 30m do:f2 mc #0 to 2
   F1QF(calclc(l2,1))
   F2QF(calclc(l3,1))
#else
 go=2 ph31
 30m mc #0 to 2
   F1QF(calclc(l2,1))
   F2QF(calclc(l3,1))
#endif /* HDEC */
 ; mc: F1(l2) = r1rho.duration
 ;     F2(l3) = r1rho.power
HaltAcqu, 1m
exit


ph1=0
ph2=2 0
ph3=0 0 2 2 1 1 3 3
ph4=1
ph5=3
ph31=0 2 2 0 1 3 3 1

;pl1 : f1 channel - power level for pulse (default)
;p1 : f1 channel - 90 degree high power pulse
;p2 : f1 channel - 180 degree high power pulse
;d1 : relaxation delay; 1-5 * T1
;d11: delay for disk I/O [30 msec]
;ns: 8 * n
;ds: 128

;cnst28: offset for on-resonance spinlock (in ppm)

;p30: maximum SL length used for highest power (for T compensation)
;pl30: maximum SL power (for T compensation)
;cnst30: offset for T compensation (in ppm) [250 ppm]

;1H decoupling:
;pl2 : f2 channel - power level for pulse (default)
;p3 : f2 channel - 90 degree high power pulse
;pl12: f2 channel - power level for CPD/BB decoupling
;cpd2: decoupling according to sequence defined by cpdprg2
;pcpd2: f2 channel - 90 degree pulse for decoupling sequence
