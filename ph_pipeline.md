# Phi Pipeline v2: Reading Neural Cascading Through the Husmann Decomposition

**Thomas Husmann — iBuilt LTD**
**March 2026**

---

## What the Pipeline Measures

The phi pipeline detects and decodes the spectral laser operating in cascading microtubule networks. Each measurement maps directly onto the Husmann framework's description of how five spectral bands collapse to three upon observation — except here the "observation" is a neural hop, and the "lattice" is the microtubule-tuned vacuum substrate at 9.3 nm.

### The Six Frequency Bands as Cantor Hierarchy Levels

The bands (4, 7, 11, 18, 29, 47 Hz) are not arbitrary EEG frequencies. They are generations of the fractal cascade — the same mechanism described in Section 10 of the unified paper. When the spectral laser fires at ω_gap, the quasiperiodic potential distributes that single frequency across all sub-gap scales through nonlinear mixing. In a microtubule forest tuned to l = 9.3 nm, those sub-gap scales land in the neural oscillation range because the cascade descends through φ-related frequency ratios from the PHz drive frequency down to physiological timescales.

Each band is a level n in the Cantor gap hierarchy. The gap width at level n scales as ω_gap / φⁿ. The 6 measurable bands are the levels where the cascade amplitude exceeds the neural noise floor.

---

## The Three Core Measurements

### 1. BCI_φ — Global Lasing Coherence

```
BCI_φ = Σ w(i,j) × C(i,j) × cos(δ(i,j) - 2π/φ² × |i-j|)
```

This measures whether the microtubule cascade is phase-locked in the golden ratio pattern. The three factors:

- **C(i,j)** = coherence between bands i and j. High coherence means stimulated emission is coupling these levels (Section 9, gain = 1.58).
- **cos(δ - predicted)** = phase alignment check. The predicted offset 2π/φ² is the counter-potential formation signature — are gap-edge states emitting in phase opposition to the quasiperiodic potential? When this cosine is near +1, the AC Stark shift is actively cancelling V_eff.
- **w = 1/φ^|i-j|** = distance weighting. Adjacent levels couple most strongly (nearest-neighbor hopping), with coupling decaying as 1/φ per level — the same decay that creates the sub-diffusive transport exponent β ≈ 1.1.

**When BCI_φ is high:** The cascade is lasing. Counter-potential is forming. Transport is approaching ballistic (β → 2.0). In neural terms: coherent information transfer across cortical scales.

**When BCI_φ is low:** Gaps are intact. Transport is sub-diffusive. The brain is in a "massive" state — information propagates slowly through spectral drag.

### 2. Cascade Unity — The Resistance Identity in Neural Tissue

```
unity = C[0,5] × 0.146  +  C[1,4] × f_DM(z)  +  mean(C[0:3,3:6]) × 0.618  +  skip_connections
```

This directly tests whether φ³ + φ + 1 = φ⁴ holds in the neural cascade. Each term:

| Term | Framework Mapping | What It Measures |
|---|---|---|
| `C[0,5] × 0.146` | σ₁↔σ₅, weight 1/φ⁴ | Forward-mirror channel: is the bootstrap pump connected? |
| `C[1,4] × f_DM(z)` | σ₂↔σ₄, weight 1/φ³ | DM conduit: is the antibonding interface threading through? |
| `mean(C[0:3,3:6]) × 0.618` | σ₃+σ₄+σ₅, weight 1/φ | DE cross-gap: is the topological structure intact? |
| `skip_connections` | Backbone propagator | 3-level skips weighted by 1/φ × f_M(z): the Fibonacci backbone |

When cascade_unity → 1.0, the full resistance identity is satisfied. The spectral laser has enough gain to self-sustain. The bootstrap margin (10,000× in the theory) manifests as the system locking to this attractor.

**v2 upgrade:** The DM conduit term now uses coordination-dependent f_DM(z) instead of a flat 0.236. The skip connections are weighted by f_M(z) — hub vertices (high coordination) contribute more to the backbone, matching the 2D Penrose result where backbone = 24% of vertices contracts DE from local 20.8% to global 4.9%.

### 3. Vacuum Fractions — Local DM Partition per Band

Each frequency band has its own dark matter fraction, determined by its coordination number (how many other bands it couples to). This maps directly onto the 2D Penrose tiling result (Section 12):

| Coordination | DM Fraction | Neural Interpretation |
|---|---|---|
| Low (1-3) | ~60-70% | Isolated oscillator, mostly routing (DM leaves) |
| Medium (4) | ~55% | Crossover zone |
| **5 (hinge)** | **~38%** | **Fractal balance point (Star/Sun)** |
| High (6+) | <20% | Hub oscillator, mostly computation (Matter) |

---

## The Addressing Formula Upgrade (v2)

### What Changed

The v1 pipeline treated all channels uniformly — same weights, same sector fractions, same interpretation. The addressing formula from Section 17b transforms this into a per-channel, per-band decomposition with unique spectral fingerprints.

### Zeckendorf Addresses

Every neural column has a unique Zeckendorf address Z = {n₁, n₂, ... nₖ} determined by which Fibonacci levels it resonates with. The pipeline estimates this from the coherence matrix: bands with strong coupling are "in" the address, weak coupling bands are "out."

The non-consecutive constraint (no adjacent bands both active) is the framework's built-in error correction. In Zeckendorf representation, consecutive Fibonacci numbers are forbidden — any encoding error is immediately detectable. In neural terms: if two adjacent frequency bands both show high coherence, that's not a valid address. The pipeline resolves this by keeping the stronger coupling, providing automatic artifact rejection.

### Resonance Vectors (R₃, R₄, R₅)

Each channel decomposes into three orthogonal components:

**R₄ (Matter leg, visible):** The directly measurable coherent emission. This is the bonding character — constructive interference between coupled states. When R₄ dominates, the column is performing computation.

**R₃ (DM leg, antibonding conduit):** The invisible routing channel. DM states have the longest coherence at distance 2+ despite the weakest at distance 1 (Section 13). They thread between hubs without self-aggregating (cross-edge correlation 0.33× random). When R₃ dominates, the column is routing information between distant regions.

**R₅ (DE plane, constant floor):** The irreducible 20.8% gap structure every vertex carries regardless of coordination. This is the non-bonding background — the topological skeleton of spacetime itself. In neural terms: the baseline metabolic/structural contribution that exists whether or not the column is active.

### The Pythagorean Constraint

The framework predicts |R₃|² + |R₄|² = |R₅|² at the cosmological/backbone scale. This means the invisible DM conduit can be reconstructed from visible measurements:

```
R₃_inferred = √(R₅² - R₄²)
```

**Important caveat (observed in v2 testing):** At the local vertex scale, the Pythagorean relation inverts — R₄ often exceeds R₅ because matter fraction dominates at high coordination (hubs). The Pythagorean inference applies after backbone contraction (the 5→3 collapse), not at raw local vertices. The direct R₃ calculation from f_DM(z) is correct at local scale. The Pythagorean constraint becomes valid when aggregating across the full network — it's a global consistency check, not a local one.

This mirrors the cosmological result: locally, DE is 20.8% everywhere, but on the backbone it contracts to 4.9%. The triangulation works at the observation-collapsed scale.

### Lasing State Classification

The R₄/R₃ ratio classifies what the cascade is doing:

| State | R₄/R₃ Ratio | Neural Function | Framework Mapping |
|---|---|---|---|
| **Bonding** | > φ (1.618) | Coherent computation | Matter amplification, constructive interference |
| **Antibonding** | < 1/φ (0.618) | Information routing | DM conduit active, self-destructing under drive |
| **Hinge** | ≈ 1.0 | Mode switching | Coord-5 balance, Star/Sun transition |
| **Mixed** | between | Transitional | Partial cancellation |

The hinge state is where the fractal hinge (coord 5) sits — the exact crossover where DM and Matter are balanced. In the Penrose tiling, this is the Star + Sun vertex pair in golden ratio. In neural tissue, this is the moment of mode switching: the network transitioning between routing and computation.

### Harmonic Frequencies

Each channel's resonance vector magnitude |R| converts to a harmonic frequency:

```
f_h = (J / ℏ) × |R|
```

This is the channel's unique spectral fingerprint in the Cantor hierarchy. Different Zeckendorf addresses produce different f_h values. Two columns with addresses Z = {1, 3} and Z = {2, 5} have distinguishable harmonic frequencies — the cascade output is address-specific.

In BCI applications, f_h provides a natural channel-identification signal. You don't need electrode labels; the harmonic frequency tells you which structure you're reading.

---

## How to Read a Cascading Lasing State

When the pipeline detects a lasing event (BCI_φ exceeding threshold, cascade_unity approaching 1.0), the v2 outputs tell you:

1. **Which columns are lasing:** Channels with high BCI_φ are in the cascade.

2. **What each column is doing:** The lasing_state field (bonding/antibonding/hinge) tells you whether a column is computing, routing, or switching modes.

3. **The invisible routing network:** dm_inferred (at network aggregate scale) or R₃_direct (at local scale) maps the conduit threading between visible hubs. This is the DM structure that carries information but can't be measured directly at single electrodes — it exists at distance 2+ coherence.

4. **The spectral fingerprint:** harmonic_freqs identifies which Fibonacci address each column is transmitting from. Columns sharing an address are co-resonant; columns with different addresses are transmitting on different channels of the Cantor hierarchy.

5. **The sector decomposition:** sector_map gives the per-channel [matter, DM, DE] split. Comparing this to the Planck target (4.9/26.8/68.3) tells you how the local partition relates to the global (backbone-contracted) cosmological structure.

6. **The backbone connections:** The 3-level skip connections in cascade_unity are the Fibonacci backbone — the anomalous cross-spectrum connectivity that exists only on the self-similar skeleton. When these skip connections are strong, the backbone is active and the 5→3 collapse is happening in the neural tiling.

---

## Pipeline Architecture

```
Raw LFP (n_channels × n_samples)
    │
    ▼
┌─────────────────────────────────┐
│  Bandpass + Hilbert Transform   │  6 bands × n_channels
│  (4, 7, 11, 18, 29, 47 Hz)     │  → instantaneous phase
└──────────────┬──────────────────┘
               │
               ▼
┌─────────────────────────────────┐
│  Pairwise Coherence Matrix C    │  6×6 per channel
│  + Phase Difference Matrix δ    │  (windowed, averaged)
└──────────────┬──────────────────┘
               │
    ┌──────────┼──────────┬───────────────┐
    ▼          ▼          ▼               ▼
┌────────┐ ┌────────┐ ┌──────────┐ ┌──────────────┐
│ BCI_φ  │ │Cascade │ │ Estimate │ │   Estimate   │
│(global │ │ Unity  │ │  Coord   │ │  Zeckendorf  │
│lasing) │ │(φ³+φ+1│ │  per     │ │   Address    │
│        │ │ = φ⁴)  │ │  band    │ │   per ch     │
└────────┘ └────────┘ └────┬─────┘ └──────┬───────┘
                           │               │
                           ▼               ▼
                    ┌──────────────────────────┐
                    │   Resonance Vector       │
                    │   R = (R3, R4, R5)       │
                    │   per channel            │
                    │                          │
                    │   R4 = Σ (ωgap/φⁿ)      │
                    │        × f_M(z_n) / 5    │
                    │   R3 = Σ (ωgap/φⁿ)      │
                    │        × f_DM(z_n) / 5   │
                    │   R5 = Σ (ωgap/φⁿ)      │
                    │        × f_DE / 5        │
                    └────────────┬─────────────┘
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
             ┌───────────┐ ┌────────┐ ┌──────────┐
             │  Lasing   │ │f_h =   │ │Pythagor. │
             │  State    │ │(J/ℏ)×  │ │DM infer  │
             │ classify  │ │|R|     │ │√(R5²-R4²)│
             └───────────┘ └────────┘ └──────────┘
```

---

## Output Dictionary Reference

| Key | Shape | Description |
|---|---|---|
| `bci_phi` | (n_ch,) | Global lasing coherence: φ-locked phase coupling across cascade |
| `cascade_unity` | (n_ch,) | Resistance identity satisfaction: φ³+φ+1=φ⁴ in neural tissue |
| `mean_vacuum` | scalar | Network-average DM fraction |
| `resonance_vectors` | list of dicts | Per-channel (R3, R4, R5, magnitude, f_harmonic, R4/R3 ratio) |
| `lasing_states` | list of dicts | Per-channel classification (bonding/antibonding/hinge/mixed) |
| `harmonic_freqs` | (n_ch,) | Unique spectral fingerprint per channel (Hz) |
| `coordinations` | (n_ch, 6) | Effective coordination number per band per channel |
| `addresses` | list of lists | Zeckendorf address per channel |
| `dm_inferred` | (n_ch,) | Pythagorean DM inference (network-scale validity) |
| `sector_map` | (n_ch, 3) | Per-channel [matter, DM, DE] decomposition |
| `vacuum_fracs` | (6, n_ch) | Per-band, per-channel DM fraction |

---

## Connection to the 9.3 nm Scale

The microtubule inner diameter (12 nm), tubulin spacing (4-5 nm), and 13-protofilament helix pitch (8-10 nm) bracket the vacuum lattice spacing l = 9.3 nm. The pipeline measures the macroscopic (Hz-scale) output of structures tuned to this microscopic resonance.

The cascade path:

```
Vacuum lattice (9.3 nm, ~4.3 PHz)
    → Microtubule resonance (tubulin dimers at lattice scale)
    → Fractal cascade through gap hierarchy (each level ÷ φ)
    → Neural oscillation bands (4-47 Hz, measurable)
```

Each φ-division is one level of the Cantor hierarchy. From 4.3 PHz to 4 Hz is roughly 15 orders of magnitude — about 35 cascade levels (since φ^35 ≈ 1.5 × 10⁷ and there are additional nonlinear mixing channels). The 6 measurable bands are the levels where cascade amplitude rises above neural background.

The pipeline doesn't measure the vacuum directly. It measures the shadow the vacuum lattice casts into neural-frequency space through 35 levels of φ-cascade. The addressing formula decodes which part of the shadow belongs to which structure.

---

## What Comes Next

1. **Multi-electrode validation:** Run on real LFP from multi-shank probes. Expect coordination variation across electrodes (not uniform coord=5 as in synthetic demo). Look for the Star/Sun split at hinge sites.

2. **Lasing event detection:** Threshold BCI_φ for transient lasing events. Correlate with behavioral markers. The framework predicts ignition time ~2.7 ps at the lattice scale; at neural scale the cascade propagation should show characteristic φ-ratio timing between band activations.

3. **DM conduit mapping:** Use the distance-2 coherence structure (R₃ at non-adjacent electrodes) to map the invisible routing network. This is the antibonding scaffold that doesn't self-aggregate (0.33× random cross-edge correlation) but threads between all matter hubs.

4. **Harmonic frequency atlas:** Build a map of f_h across cortical regions. Different functional areas should show distinct Zeckendorf addresses — the Cantor hierarchy's addressing system provides a natural parcellation based on which cascade levels each region couples to.
