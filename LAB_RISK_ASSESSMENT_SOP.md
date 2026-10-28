# Laboratory Risk Assessment, SOP, and Commissioning Checklist

## 1. Scope and operating envelope

This procedure applies to CFRP electrification tests that involve:
- Heated CFRP specimens
- Electrical energisation via bench power supply
- Robotic movement and positioning
- Liquid couplant/chiller circulation
- Potential resin degradation products

No energised operation is permitted until Section 7 approvals are complete.

## 2. Risk assessment

| Hazard class | Typical hazards | Required controls | Stop-work triggers |
|---|---|---|---|
| Electrical | Shock/burn from live conductors; short-circuit current; damaged insulation | Touch-safe shrouding, insulated leads, pre-use insulation/continuity checks, current limit set before enable, bonded earths, lockable isolator | Exposed conductor, insulation damage, unexpected current rise, tripped protection |
| Thermal | Local hot spots, burns from heated CFRP/tooling, runaway heating | Independent overtemperature trip (Section 3), thermal shielding, no-touch hot-surface marking, calibrated temperature sensing | Temperature exceeds software limit, hardware trip activation, smoke/odour increase |
| Mechanical (robotic) | Collision/crush/impact from arm movement; trapped hands during fixture adjustment | Programmed exclusion zone, fixed barriers/markings, reduced-speed setup mode, interlocked guard where available, two-person setup verification | Human entry into exclusion zone during motion, unexpected path, collision warning/fault |
| Chemical | Epoxy/resin decomposition fumes and residues when overheated | Local fume extraction on before energisation, suitable gloves/eye protection, sealed waste container for contaminated wipes, SDS available at station | Fume extraction unavailable, visible smoke/plume, operator irritation symptoms |
| Liquid leakage | Couplant/chiller leaks causing slip/electrical bridging/corrosion | Hose integrity checks, drip tray + absorbent pads, leak sensor/visual checks, cable routing above liquid paths, immediate de-energisation on leak | Any active leak, pooling near electrical hardware, pump anomaly |

## 3. Independent overtemperature protection and emergency stop

1. **Primary control**: software/controller temperature limit for normal operation.
2. **Independent protection (mandatory)**: hardware thermal cut-out (independent sensor + relay/contactor path) that removes heater/power output without software intervention.
3. **Emergency stop arrangement**:
   - Accessible latching E-stop that simultaneously:
     - Removes electrical energisation to specimen and tooling
     - Commands robot safe stop (or power removal per robot safety architecture)
     - Stops liquid circulation pumps if leak/fire risk is present
   - E-stop function tested at start of each test day and recorded in checklist.

## 4. Fume extraction and overheated epoxy handling

- Confirm local extraction is active before any energised run.
- Keep extraction running through cool-down after power-off.
- If overheated epoxy is suspected (smoke, acrid odour, discoloration):
  1. Trigger E-stop / de-energise.
  2. Keep personnel outside exclusion zone until motion and electrical hazards are safe.
  3. Maintain extraction; do not disturb material until cool.
  4. Handle residues with chemical-resistant gloves and dispose via lab hazardous waste route.
  5. Log incident and quarantine specimen for supervisor review.

## 5. Robot exclusion zones and collision hazard controls

- Define and mark a physical exclusion zone around full robot swept volume plus tooling envelope.
- No personnel inside zone during automatic or jog motion except approved teach/setup mode with reduced speed and hold-to-run controls.
- Perform a dry-run path check at reduced speed after any program, fixture, or payload change.
- Maintain an unobstructed line of sight to robot and E-stop during motion.

## 6. Safe access, shutdown, and cool-down conditions

### Access allowed only when all are true
- Electrical output is disabled and verified at zero energy state.
- Robot is in safe stopped state.
- Surface temperature of CFRP/tooling is below site-defined touch-safe threshold.
- No active leak and extraction has cleared residual fumes.

### Normal shutdown sequence
1. Disable specimen energisation.
2. Stop robot motion and park in safe position.
3. Continue extraction and cooling flow until below touch-safe temperature.
4. Stop pumps/chiller when no residual heat risk remains.
5. Record completion and any anomalies.

## 7. Pre-energised commissioning and approval checklist

All items below must be checked and signed before energised operation.

| Item | Check | Status (Pass/Fail/N/A) | Sign/Date |
|---|---|---|---|
| Electrical safety | Cable condition, insulation, earthing, current limit, isolator function verified |  |  |
| Independent overtemperature trip | Hardware trip setpoint and trip test witnessed |  |  |
| Emergency stop | E-stop latching/reset and energy isolation test completed |  |  |
| Robot safety | Exclusion zone marked; dry-run collision check passed |  |  |
| Fume control | Extraction airflow confirmed; PPE and SDS available |  |  |
| Liquid system | Hose, fittings, drip tray, leak response materials verified |  |  |
| Shutdown/cool-down | Criteria reviewed with operators and demonstrated |  |  |
| Competency | Operators briefed on SOP and emergency response |  |  |

### Required approvals before energised operation

| Approver | Approval status | Name | Date |
|---|---|---|---|
| Laboratory safety responsible person |  |  |  |
| Robot safety responsible person |  |  |  |
| Electrical test supervisor/PI |  |  |  |

**Gate condition:** energised operation is prohibited until all required approvals above are recorded.
