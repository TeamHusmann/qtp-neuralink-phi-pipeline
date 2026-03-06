# CLAUDE.md - Universe Simulator Rebuild Instructions

This document contains everything needed to rebuild the phi-structured universe simulator at `universe.eldon.food`.

## Project Overview

A Flask/Three.js application that simulates universe formation using the golden ratio (phi) as the organizing principle. Features include:
- Big Bang nucleosynthesis with phi-proportioned element creation
- Stellar evolution and element condensation
- Planetary system formation with phi-orbital spacing
- Earth timeline evolution with solar luminosity and tectonic modeling
- World classification system for exoplanets

**Live Site**: https://universe.eldon.food
**Source Location**: `/var/www/universe.eldon.food/`

---

## ASSUMPTIONS (Adjustable Parameters)

These are the key assumptions that drive the simulation. Adjust these to explore different universe models.

### Fundamental Constants

```python
# The Golden Ratio - core organizing principle
PHI = 1.618033988749895

# Speed of light (m/s)
C = 299792458

# Gravitational constant (m^3 kg^-1 s^-2)
G = 6.67430e-11

# Planck constant (J s)
H = 6.62607015e-34

# Boltzmann constant (J/K)
K_B = 1.380649e-23

# Stefan-Boltzmann constant (W m^-2 K^-4)
SIGMA_SB = 5.670374419e-8

# Solar luminosity today (W)
L_SUN_TODAY = 3.828e26

# Solar age (Gyr)
SOLAR_AGE_GYR = 4.57

# Solar radius (m)
R_SUN = 6.96e8

# Earth orbital radius (m)
AU = 1.496e11

# Earth radius (km)
EARTH_RADIUS_KM = 6371

# Present Earth surface temperature (K)
EARTH_T_SURFACE_PRESENT = 288

# Present greenhouse warming (K)
BASE_GREENHOUSE = 33.0
```

### Solar Evolution Assumptions

```python
# Zero-Age Main Sequence luminosity ratio
ZAMS_LUMINOSITY_RATIO = 0.70  # Sun was 70% as bright at formation

# Solar luminosity evolution model (linear approximation)
# L(t) = 0.70 + 0.30 * (4.57 - t_ga) / 4.57
# where t_ga is time in billion years ago

# ASSUMPTION: Linear luminosity increase
# Reality: Slightly nonlinear, but linear is good to ~2% over 4.5 Gyr
```

### Greenhouse Effect Assumptions

```python
# Climate sensitivity per CO2 doubling (K)
CO2_SENSITIVITY = 3.0  # Range in literature: 2.5-4.5 K

# Methane sensitivity per doubling (K)
CH4_SENSITIVITY = 0.5

# Water vapor feedback multiplier
H2O_FEEDBACK_COEFFICIENT = 5.0  # K per unit relative humidity change

# Present CO2 level (%)
PRESENT_CO2_PERCENT = 0.04

# Present CH4 level (ppm)
PRESENT_CH4_PPM = 1.9

# Maximum greenhouse warming cap (K)
MAX_GREENHOUSE_DELTA = 250

# Minimum greenhouse cooling cap (K)
MIN_GREENHOUSE_DELTA = -10
```

### Radioactive Heat Assumptions

```python
# Isotope half-lives (Gyr)
HALF_LIFE_U238 = 4.468
HALF_LIFE_U235 = 0.704
HALF_LIFE_TH232 = 14.05
HALF_LIFE_K40 = 1.248

# Present heat production (TW)
PRESENT_RADIOACTIVE_HEAT_TW = 20.0

# Isotope heat fractions (present day)
U238_HEAT_FRACTION = 0.39
U235_HEAT_FRACTION = 0.04
TH232_HEAT_FRACTION = 0.40
K40_HEAT_FRACTION = 0.17
```

### Tectonic Assumptions

```python
# Minimum radius for tectonics (km)
MIN_TECTONIC_RADIUS_KM = 2500

# Reference radius for scaling (km) - Earth
REFERENCE_RADIUS_KM = 6371

# Minimum heat index for active tectonics
MIN_HEAT_INDEX = 0.3

# Minimum water fraction for lubricated tectonics
MIN_WATER_FRACTION = 0.0001  # 0.01%

# Water enhancement factor for tectonics
WATER_TECTONIC_ENHANCEMENT = 2.0
```

### Carbon-Silicate Cycle Assumptions

```python
# Volcanic CO2 release rate (normalized to present = 1.0)
VOLCANIC_RATE_PRESENT = 1.0

# Weathering rate constants
WEATHERING_ACTIVATION_ENERGY = 0.09  # per K

# Temperature coefficient for weathering
WEATHERING_TEMP_SENSITIVITY = 0.09  # 9% per degree

# CO2 sensitivity for weathering
WEATHERING_CO2_SENSITIVITY = 0.5  # exponent for CO2 dependence
```

### World Classification Assumptions

```python
# Formation temperature brackets (K)
BRACKET_ICE = 150      # Below = icy composition
BRACKET_ROCK = 500     # 150-500 = rocky composition
BRACKET_REFRACTORY = 1500  # 500-1500 = mixed, >1500 = refractory

# Habitable zone boundaries (AU for solar-type star)
HZ_INNER = 0.95
HZ_OUTER = 1.67

# Mass thresholds (Earth masses)
MASS_DWARF_MAX = 0.1
MASS_TERRAN_MAX = 2.0
MASS_SUPERTERRAN_MAX = 10.0
MASS_NEPTUNIAN_MAX = 50.0
# Above 50 = Jovian

# Atmosphere escape velocity threshold (km/s at 1 AU equivalent)
ATMOSPHERE_RETENTION_VESC = 6.0
```

### Big Bang Nucleosynthesis Assumptions

```python
# Primordial abundance ratios (by mass)
HYDROGEN_FRACTION = 0.75
HELIUM_FRACTION = 0.25
LITHIUM_TRACE = 1e-9

# Phi-scaling for element creation
# Each subsequent element abundance = previous / PHI^n
```

---

## Key Mathematical Models

### 1. Solar Luminosity Evolution

```python
def solar_luminosity_at_time(time_ga):
    """
    Calculate Sun's luminosity relative to today.

    Args:
        time_ga: Time in billions of years ago (0 = now, 4.57 = Sun's birth)

    Returns:
        Relative luminosity (1.0 = today)
    """
    if time_ga <= 0:
        return 1.0
    if time_ga >= SOLAR_AGE_GYR:
        return ZAMS_LUMINOSITY_RATIO

    t_fraction = (SOLAR_AGE_GYR - time_ga) / SOLAR_AGE_GYR
    return ZAMS_LUMINOSITY_RATIO + (1.0 - ZAMS_LUMINOSITY_RATIO) * t_fraction
```

### 2. Equilibrium Temperature

```python
def equilibrium_temperature(luminosity_ratio, orbital_radius_au, albedo=0.3):
    """
    Calculate blackbody equilibrium temperature without greenhouse.

    T_eq = (L * L_sun / (16 * pi * sigma * r^2))^0.25 * (1 - albedo)^0.25
    """
    L = luminosity_ratio * L_SUN_TODAY
    r = orbital_radius_au * AU
    T_eq = ((L * (1 - albedo)) / (16 * math.pi * SIGMA_SB * r**2)) ** 0.25
    return T_eq
```

### 3. Greenhouse Temperature (Calibrated)

```python
def greenhouse_temperature(T_eq, co2_percent, ch4_ppm=0, h2o_relative=1.0):
    """
    Calculate surface temperature with greenhouse effect.
    Calibrated so present Earth = 288K with +33K greenhouse.
    """
    # Base greenhouse effect (present-day Earth)
    BASE_GREENHOUSE = 33.0

    # CO2 effect as delta from present
    co2_factor = math.log2(max(0.0001, co2_percent) / PRESENT_CO2_PERCENT)
    co2_warming = CO2_SENSITIVITY * co2_factor

    # Methane effect
    if ch4_ppm > 0:
        ch4_factor = math.log2(max(0.1, ch4_ppm) / PRESENT_CH4_PPM)
        ch4_warming = CH4_SENSITIVITY * ch4_factor
    else:
        ch4_warming = 0

    # Water vapor feedback
    h2o_warming = H2O_FEEDBACK_COEFFICIENT * (h2o_relative - 1.0)

    # Total greenhouse effect
    delta_T = BASE_GREENHOUSE + co2_warming + ch4_warming + h2o_warming
    delta_T = max(MIN_GREENHOUSE_DELTA, min(MAX_GREENHOUSE_DELTA, delta_T))

    return T_eq + delta_T
```

### 4. Radioactive Heat Production

```python
def radioactive_heat_at_time(time_ga):
    """
    Calculate internal heat from radioactive decay.
    Uses half-life decay for U238, U235, Th232, K40.
    """
    def decay_factor(half_life):
        return 2 ** (time_ga / half_life)

    heat = PRESENT_RADIOACTIVE_HEAT_TW * (
        U238_HEAT_FRACTION * decay_factor(HALF_LIFE_U238) +
        U235_HEAT_FRACTION * decay_factor(HALF_LIFE_U235) +
        TH232_HEAT_FRACTION * decay_factor(HALF_LIFE_TH232) +
        K40_HEAT_FRACTION * decay_factor(HALF_LIFE_K40)
    )
    return heat
```

### 5. Tectonic Vigor

```python
def tectonic_vigor(radius_km, mass_ratio_earth, time_ga, ree_enrichment=1.0, water_fraction=0.001):
    """
    Calculate tectonic activity index (0-1 scale).

    Tectonics require:
    1. Sufficient size (>2500 km radius)
    2. Sufficient internal heat
    3. Water for mantle lubrication
    """
    # Size factor
    if radius_km < MIN_TECTONIC_RADIUS_KM:
        size_factor = 0.0
    else:
        size_factor = min(1.0, radius_km / REFERENCE_RADIUS_KM)

    # Heat factor
    heat_tw = radioactive_heat_at_time(time_ga) * mass_ratio_earth * ree_enrichment
    present_earth_heat = PRESENT_RADIOACTIVE_HEAT_TW
    heat_index = heat_tw / present_earth_heat
    heat_factor = min(1.0, heat_index / MIN_HEAT_INDEX) if heat_index > MIN_HEAT_INDEX else 0.0

    # Water factor
    if water_fraction < MIN_WATER_FRACTION:
        water_factor = 0.0
    else:
        water_factor = min(WATER_TECTONIC_ENHANCEMENT, 1.0 + math.log10(water_fraction / MIN_WATER_FRACTION))

    # Combined vigor
    vigor = size_factor * heat_factor * min(1.0, water_factor)
    return min(1.0, max(0.0, vigor))
```

### 6. Carbon-Silicate Cycle

```python
def carbon_silicate_cycle_rate(temperature_k, co2_level, tectonic_vigor):
    """
    Calculate net CO2 flux from weathering vs volcanism.

    Negative = net removal (weathering dominates)
    Positive = net addition (volcanism dominates)
    """
    # Weathering rate (removes CO2)
    weathering = math.exp(WEATHERING_ACTIVATION_ENERGY * (temperature_k - 288))
    weathering *= (co2_level / PRESENT_CO2_PERCENT) ** WEATHERING_CO2_SENSITIVITY

    # Volcanic rate (adds CO2)
    volcanic = tectonic_vigor * VOLCANIC_RATE_PRESENT

    return volcanic - weathering
```

---

## Earth Timeline Data

The simulation includes key epochs in Earth's history:

| Time (Ga) | Event | CO2 (%) | CH4 (ppm) | Atmosphere |
|-----------|-------|---------|-----------|------------|
| 4.5 | Formation | 30 | 10000 | Primordial CO2/N2/H2O |
| 4.4 | Magma Ocean Cools | 20 | 5000 | Steam atmosphere |
| 4.0 | Late Heavy Bombardment | 10 | 2000 | Thick CO2 atmosphere |
| 3.5 | First Life | 5 | 1000 | Reducing atmosphere |
| 2.4 | Great Oxidation | 1 | 10 | O2 appears |
| 2.1 | Snowball Earth | 0.1 | 1 | Near-frozen |
| 0.7 | Second Snowball | 0.05 | 1 | Near-frozen |
| 0.54 | Cambrian | 0.5 | 2 | Modern-like |
| 0.3 | Carboniferous | 0.03 | 1 | High O2 |
| 0.06 | Dinosaur Era | 0.2 | 3 | Warm greenhouse |
| 0.01 | Ice Ages | 0.02 | 0.5 | Glacial cycles |
| 0 | Present | 0.04 | 1.9 | Current |

---

## API Endpoints

### Solar/Climate APIs

```
GET /api/earth/climate/<time_ga>
    Returns climate state at specified time
    Response: {solar_luminosity, T_equilibrium, T_surface, greenhouse_effect, co2, ch4}

GET /api/earth/solar-evolution
    Returns solar luminosity over time
    Response: Array of {time_ga, luminosity, T_equilibrium}

GET /api/earth/tectonics/<time_ga>
    Returns tectonic state at specified time
    Response: {radioactive_heat_tw, tectonic_vigor, mantle_temp_estimate}

GET /api/earth/faint-sun-paradox
    Returns explanation of the paradox and how Earth solved it
```

### World Classification APIs

```
GET /api/world/classify
    Query params: mass_earth, radius_earth, orbital_au, star_luminosity, star_temp_k
    Returns: {size_class, composition, zone, habitability_score, has_atmosphere}

GET /api/world/examples
    Returns list of example worlds with classifications
```

### Universe Evolution APIs

```
GET /api/phi
    Returns golden ratio value

GET /api/timeline
    Returns universe formation timeline

GET /api/elements
    Returns element condensation data

GET /api/earth-timeline
    Returns Earth evolution events
```

---

## File Structure

```
/var/www/universe.eldon.food/
├── app.py                 # Flask backend with all models
├── templates/
│   └── index.html         # Three.js frontend visualization
├── static/
│   ├── css/
│   │   └── style.css      # UI styling
│   └── js/
│       └── universe.js    # Three.js scene management
├── .env                   # Environment variables (GITHUB_TOKEN)
├── BUILD_UNIVERSE.md      # Detailed changelog and documentation
└── requirements.txt       # Python dependencies
```

---

## Dependencies

### Python (requirements.txt)
```
Flask==2.3.3
gunicorn==21.2.0
python-dotenv==1.0.0
```

### Frontend (CDN)
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
```

---

## Deployment

### Nginx Configuration
```nginx
server {
    listen 443 ssl http2;
    server_name universe.eldon.food;

    location / {
        proxy_pass http://127.0.0.1:5200;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /static/ {
        alias /var/www/universe.eldon.food/static/;
    }
}
```

### Running the Server
```bash
cd /var/www/universe.eldon.food
source venv/bin/activate
gunicorn -w 2 -b 127.0.0.1:5200 app:app
```

---

## Faint Young Sun Paradox Explanation

**The Problem**: The Sun was only 70% as bright 4 billion years ago. With today's atmosphere, Earth would have been frozen solid. Yet geological evidence shows liquid water existed.

**The Solution**: Much higher CO2 and CH4 levels created a stronger greenhouse effect:

| Time | Solar Brightness | CO2 | Greenhouse | T_surface |
|------|------------------|-----|------------|-----------|
| 4.0 Ga | 74% | 10% | +66K | ~302K (warm!) |
| 2.5 Ga | 82% | 1% | +48K | ~288K (comfortable) |
| 0 Ga | 100% | 0.04% | +33K | 288K (today) |

**Key Insight**: The carbon-silicate cycle acts as a thermostat. More volcanism + less weathering at low temps = CO2 buildup = warming. Higher temps = more weathering = CO2 removal = cooling.

---

## Why Water + Tectonics?

**Question**: Can a planet have liquid water without plate tectonics?

**Answer**: Yes, but stability is the problem.

### Scenarios:

1. **Ice moons** (Europa, Enceladus): Tidal heating + ice shell = subsurface ocean, no tectonics needed

2. **H2 greenhouses**: Thick hydrogen atmosphere can trap heat even without CO2 cycle

3. **Young planets**: Initial heat can maintain warmth temporarily

### Why Earth Needs Tectonics:

Earth maintains stable surface water for 4+ billion years because:
1. **Carbon-silicate thermostat** requires tectonics (volcanism + weathering)
2. **Volatile recycling** returns water to surface from subduction
3. **Magnetic field** from convection protects atmosphere from solar wind

**Bottom line**: Water CAN exist without tectonics, but STABLE surface water over billions of years requires the carbon-silicate cycle feedback, which requires plate tectonics.

---

## Version History

- **v2.1** (2025-03-06): Added solar evolution, tectonic modeling, climate calibration
- **v2.0** (2025-03-05): Added world classification system
- **v1.0** (2025-03-04): Initial phi-structured universe with element condensation

---

*This document is the authoritative source for rebuilding the universe simulator.*
