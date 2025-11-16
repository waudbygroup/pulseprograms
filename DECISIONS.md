# Decision Log

## 2025-11-14: Consistent naming with dot notation
**Decision:** Use dot syntax for parameter references (e.g. `spinlock.offset`)
**Rationale:** Clear and allows easy programmatic lookup
**Alternatives considered:** Arbitrary names and hard-coded lookups
**Consequences:** Change from v0.0.1

## 2025-11-14: Rename nuclei_hint to typical_nuclei
**Decision:** Rename nuclei_hint to typical_nuclei.
This parameter should be a mapping to channels, from f1 onwards.
Use `nothing` if no nucleus employed for a channel.
Multiple suggested parameter mappings can be given as a list.
Examples:
* [1H]
* [[1H, 19F, 31P]]
* [19F, 1H]
* [[1H, 19F], 13C]
* [1H, nothing, 15N]
* [1H, 13C, 15N, 2H]
**Rationale:** Clear but flexible
**Alternatives considered:** Disallowing multiple recommendations - but what about zg490.cw?
Giving recommendations as a list (e.g. `[[1H, 13C], [19F, 13C]]`) - but this creates type instability.
Using a pipe character to separate alternatives, e.g. `[1H | 19F | 31P]` - but this adds a new
type of syntax to parse. 
**Consequences:** Change from v0.0.1. Multiple alternatives does introduce complexity but this seems unavoidable.


## 2025-11-15: Parameter and list reference syntax

**Decision:** Use bare parameter/variable names without special delimiters (e.g., `Dlist`, `ncyc`, `t2delay`, `d20`, `pl8`) in annotations. Parameter references are distinguished from literals by context: names are parameters, numbers are literals, objects with keys define programmatic generation.
- For programmatically generated values, use structured syntax: `{type: linear, start: cnst1, end: cnst2, length: l3}`

**Rationale:** 
- The context makes it obvious whether a value is a parameter lookup versus a literal (e.g., `duration: Dlist` is clearly a variable, `duration: 0.001` is clearly a number)
- NMRTools already has the machinery to resolve parameter names by looking them up in acqus files and following references to list files
- Reduces syntactic noise and improves readability
- Bruker's own pulse programme syntax uses bare names for list variables, so this maintains consistency with the source material
- The schema's job is to document which parameters are used, not to encode how to resolve them (that's NMRTools' responsibility)
- Different list definition methods in pulse programmes all define a variable name in code:
```
  define list<delay> Dlist = { 0.1 0.2 0.3 }        # hardcoded values
  define list<delay> D2list = <mydelaylist>         # named file
  define list<delay> D3list = <$VDLIST>             # parameter-referenced file
```
  These variable names can be referenced in annotations, and NMRTools handles resolution.

**Alternatives considered:**
- `<$Dlist>` or `<Dlist>` syntax: Explicitly marks parameter references but adds unnecessary visual clutter when context already disambiguates. Would also require deciding when to use `<$...>` versus `<...>` based on how the list is defined in the pulse programme, which is an implementation detail the schema shouldn't need to specify
- `${Dlist}` or `$Dlist`: Similar to above, adds syntax without adding clarity

**Consequences:**
- Parser must distinguish bare names (parameter references) from numbers (literals) from objects (structured definitions)
- NMRTools is responsible for resolving parameter names to actual values by:
  1. Parsing pulse programme to find list definitions
  2. If hardcoded (`{ 0.1 0.2 0.3 }`), extract values directly
  3. If file reference (`<mydelaylist>` or `<$VDLIST>`), lookup parameter if needed, then load file
- Dimension definitions in the schema reference the parameter/variable name directly:
```yaml
  ;@ relaxation:
  ;@   duration: Dlist
  ;@ dimensions: [relaxation.duration, f1]
```
- Schema examples:
```yaml
  # Direct list variable reference
  ;@ relaxation:
  ;@   duration: D3list
  
  # List with parameter-based scaling
  ;@ relaxation:
  ;@   duration: {variable: ncyc, scale: d20}
  
  # List with constant scaling  
  ;@ relaxation:
  ;@   duration: {variable: ncyc, scale: 0.004}
  
  # Fixed parameter (not a list)
  ;@ spinlock:
  ;@   power: pl8
  ;@   duration: d18
  ;@   offset: fqlist  # this is a list variable
  
  # Programmatically generated
  ;@ diffusion:
  ;@   gradient_strength: {type: linear, start: cnst1, end: cnst2, count: l3}
```
- This will require supporting implementation in NMRTools...



## 2025-11-15: Experiment type and feature vocabulary

**Decision:** 
- Use snake_case for all vocabulary terms (e.g., `relaxation_dispersion`, `on_resonance`, `zz_start`)
- Dimensionality tags (1d, 2d, 3d) refer to frequency dimensions in the processed spectrum, not total dataset dimensions
- experiment_type contains fundamental experiment classes and building blocks
- features contains technical variations, implementation details, and established experiment orderings
- For composite experiments, list component types in experiment_type and use features to specify the ordering/connectivity (e.g., experiment_type: [noesy, hsqc], features: [noesy_hsqc])
- Match field conventions: r1rho implies dispersion; relaxation_dispersion + cpmg feature for CPMG dispersion; relaxation + cpmg feature for simple CPMG R2

**Rationale:**
- Snake_case is machine-parseable, grep-friendly, and avoids YAML quoting issues
- Dimensionality as "frequency dimensions" matches standard NMR nomenclature (R1 measurements are "1D experiments" despite acquiring multiple FIDs; HSQC is "2D" regardless of additional parameter dimensions)
- Total dataset dimensionality is derivable from the dimensions field, so 1d/2d/3d serves as a categorical experiment class label rather than a dimension count
- Compositional approach for experiment_type scales better than inventing vocabulary for every possible experiment combination
- Features specify ordering/connectivity for composite experiments, making both components discoverable while distinguishing variants
- Vocabulary reflects established field conventions to aid discovery and interpretation

**Alternatives considered:**
- Spaces in terms: Would require quoting, error-prone, not machine-friendly
- Hyphens (kebab-case): Less common in scientific naming, could be confused with mathematical operators
- Dots for hierarchy (r1rho.on_resonance): Conflicts with data structure referencing syntax (relaxation.duration); dots reserved for accessing fields within objects
- Compound vocabulary terms for all combinations (noesy_hsqc as experiment type): Doesn't scale; requires new terms for every possible ordering
- Dimensionality as total dataset dimensions: Conflicts with field conventions; less useful for discovery
- r1rho + relaxation_dispersion together: Redundant since r1rho implies dispersion by convention
- Separate r1rho_dispersion and cpmg_dispersion terms: More explicit but verbose; current approach matches how the field discusses these experiments

**Consequences:**
- Controlled vocabulary must be documented and expanded as new sequences are added
- Parser must handle multi-valued experiment_type arrays
- For composite experiments, both component types are searchable in experiment_type
- Features field distinguishes orderings (noesy_hsqc vs hsqc_noesy) and technical variations
- Dimensions field provides complete structural information; 1d/2d/3d is categorical only
- Must maintain VOCABULARY.md documenting all terms with brief definitions
- Review vocabulary periodically for consistency

**Example patterns:**
```yaml
# Simple experiments
;@ experiment_type: [cest, 1d]
;@ experiment_type: [relaxation, 1d]
;@ experiment_type: [hsqc, 2d]

# Technical variations
;@ experiment_type: [cest, 1d]
;@ features: [zz_start]

;@ experiment_type: [relaxation, 1d]
;@ features: [cpmg]

;@ experiment_type: [cross_correlated_relaxation, hsqc, 2d]
;@ features: [1h_coupled]

# Dispersion experiments
;@ experiment_type: [r1rho, 1d]
;@ features: [on_resonance, temperature_compensation]

;@ experiment_type: [relaxation_dispersion, 1d]
;@ features: [cpmg]

# Composite experiments
;@ experiment_type: [noesy, hsqc, 3d]
;@ features: [noesy_hsqc]

;@ experiment_type: [noesy, hsqc, 3d]
;@ features: [hsqc_noesy]

# Specialized named experiments
;@ experiment_type: [std, 1d]
;@ experiment_type: [waterlogsy, 1d]

# Dataset dimensionality vs experiment dimensionality
;@ experiment_type: [r1rho, 1d]  # "1D experiment"
;@ dimensions: [r1rho.power, r1rho.duration, f1]  # 3D dataset

;@ experiment_type: [std, 1d]  # "1D experiment"  
;@ dimensions: [std.state, f1]  # 2D dataset (sat/ref)

;@ experiment_type: [hsqc, 2d]  # "2D experiment"
;@ dimensions: [f2, f1]  # 2D dataset
```

**Vocabulary management:**
- Don't define complete vocabulary upfront
- Document new terms as sequences are added
- Maintain VOCABULARY.md with definitions
- Add new experiment_type terms only when established in literature or when multiple sequences would use them
- Use features liberally for one-off technical variations
- Rely on description field for highly specialized experiments without forcing into controlled vocabulary



## 2025-11-15: Sample type tags (not included)

**Decision:** Do not include sample type tags (e.g., `small_molecule`, `protein`, `biomolecular`, `nucleic_acid`) in the schema vocabulary.

**Rationale:**
- Pulse sequences are independent of sample type—the same sequence works identically for different samples (e.g., 19F R1ρ works for both fluorinated fragments and fluorinated proteins)
- Sequences that are genuinely specific to a sample class are already identifiable by experiment type (e.g., `hnco` is inherently protein-specific)
- Avoids maintenance burden and ambiguity (e.g., how to tag protein-ligand complexes)

**Alternatives considered:**
- Include as features: Would clutter vocabulary with information that doesn't describe the pulse sequence
- Include as experiment_type modifier: Same issue - doesn't describe what the sequence does

**Consequences:**
- Sample-specific information documented in `description` field where relevant
- Dataset metadata (separate from pulse sequence schema) captures what sample was measured
- Schema remains focused on pulse sequence characteristics rather than application context



## 2025-11-15: Reference pulse documentation

**Decision:** Use `reference_pulse` field to document the fundamental power calibration for each channel, replacing the initial `hard_pulse` field.
```yaml
;@ reference_pulse:
;@ - {channel: f1, pulse: p1, power: pl1}
;@ - {channel: f3, pulse: p21, power: pl21}
```

Reference pulses are assumed to be 90° hard pulses unless otherwise noted in the sequence description.

**Rationale:**
- Establishes the calibrated pulse that serves as the power reference for all other pulse power calculations on that channel
- Essential for setup: user must calibrate these pulses before running the sequence
- Essential for processing: enables conversion of power levels (e.g., spinlock powers in dB) to field strengths (Hz) using the reference calibration
- The term "reference" makes clear this is the basis for other calculations, not just any hard pulse in the sequence
- 90° pulses are the universal standard for power calibration, so no angle field needed (YAGNI)

**Alternatives considered:**
- `hard_pulse`: Too generic, doesn't convey that this is the calibration reference
- `power_reference`: Less clear that it's a pulse calibration
- `calibrated_pulse`: Doesn't emphasize that it's used as a reference for other calculations
- `required_calibrations`: Too broad, could include other calibration types
- Including optional `angle` field: Adds complexity for hypothetical use cases; 90° is always the calibration standard

**Consequences:**
- Each channel that requires power calibration gets one reference pulse entry
- Spinlock powers, shaped pulse powers, etc. are implicitly referenced to the appropriate channel's reference pulse
- NMRTools can convert between dB (as stored in Bruker parameters) and Hz (physical field strength) using the reference pulse calibration
- Automated setup tools know which pulses must be calibrated before acquisition
- If a non-90° reference is ever needed, it can be documented in the description field and the schema extended at that time


## 2025-11-15: Feature ontology (deferred)

**Decision:** Use flat vocabulary with informal relationships documented in definitions. Defer formal ontology development until usage patterns emerge.

**Rationale:**
- At alpha stage with limited sequences, natural hierarchies and groupings are not yet apparent
- Some features have multiple valid parent categories (e.g., `watergate` is both water suppression and gradient-enhanced), making strict hierarchies problematic
- Premature ontology design leads to forced, awkward hierarchies that become obstacles rather than aids
- Flat vocabulary is simpler to maintain and won't become "wrong" as understanding evolves
- Relationships can be added later without modifying existing sequence annotations
- Let natural groupings emerge from actual usage rather than speculation

**Future approach (when ~50-100+ sequences exist):**
- Review vocabulary for natural groupings
- Create simple parent-child relationship file (e.g., `feature_ontology.yaml`)
- Enable search expansion (searching `water_suppression` includes `presaturation`, `watergate`, etc.)
- Consider multiple inheritance where features belong to multiple categories

**Consequences:**
- Current vocabulary definitions informally document relationships (e.g., "watergate - water suppression using gradient tailored excitation")
- Search currently requires explicit term matching
- Ontology can be added as a separate layer later without breaking existing annotations
- Focus remains on getting core schema right rather than perfecting categorization



## 2025-11-15: Parameter naming - duration vs time

**Decision:** Use `duration` for parameters specifying length of time, not `time`.
```yaml
;@ relaxation:
;@   duration: VDLIST

;@ r1rho:
;@   duration: VPLIST

;@ cest:
;@   duration: D18
```

**Rationale:**
- `duration` unambiguously means "length of time for which something happens"
- `time` is ambiguous and could mean: timestamp, evolution time, delay time, relaxation time constant, etc.
- Aligns with common NMR nomenclature: "spinlock duration", "mixing time duration", "saturation duration"
- Prevents confusion between time as a measurable (e.g., relaxation time T1) versus time as a parameter (how long to apply spinlock)

**Alternatives considered:**
- `time`: Too ambiguous, overloaded term in NMR context
- `length`: Could work but typically refers to spatial dimensions or pulse lengths
- `period`: Less common in NMR parameter naming

**Consequences:**
- All temporal parameters in experiment blocks use `duration`
- Consistent naming improves schema readability and searchability
- Clear distinction between duration (controllable parameter) and time constants (measured quantities)


<!-- TEMPLATE
## 2025-11-08: Dimension reference syntax
**Decision:** Use `<$VARIABLE>` syntax for parameter list references
**Rationale:** Distinguishes variable references from literal values
**Alternatives considered:** Plain variable names, $VARIABLE notation
**Consequences:** Requires parsing angle brackets, but makes intent clear
-->
