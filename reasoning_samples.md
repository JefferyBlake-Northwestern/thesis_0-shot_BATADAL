# Final reasoning samples across all models, conditions, and outcomes

## gpt-5.6-sol — native — FN

**w0012 rep0** (tokens: None, latency: 21.7s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"Tank trajectories, pressure-flow relationships, and all pump and valve states remain physically coherent throughout the window."}

**w0013 rep0** (tokens: None, latency: 19.5s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"All reported flows match actuator states, pressure responses track pump and valve configurations, and tank-level changes remain physically plausible across the window."}

**w0014 rep0** (tokens: None, latency: 30.0s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"Pump and valve states consistently match their reported flows, pressure changes track topology and actuator transitions, and tank-level evolution shows no clear unexplained discontinuity."}

## gpt-5.6-sol — native — FP

**w0069 rep0** (tokens: None, latency: 17.5s)

> {"verdict":"attack","flagged_hours":[19,20,21,22,23],"reasoning":"Valve V2 is abruptly closed from hour 19 onward, eliminating its previously substantial flow and creating a sustained abnormal pressure separation across the connected nodes."}

**w0007 rep1** (tokens: None, latency: 36.2s)

> {"verdict":"attack","flagged_hours":[13],"reasoning":"At hour 13, L_T4 abruptly drops from 4.33 to 2.90 despite PU7 activating with substantial flow, violating tank mass-balance and actuator-response consistency."}

**w0011 rep1** (tokens: None, latency: 25.4s)

> {"verdict":"attack","flagged_hours":[10,11,12,13,14,15,16,17,18,19,20,21,22,23],"reasoning":"L_T6 becomes frozen at exactly 5.5 despite substantial changes in pump flows, actuator states, and surrounding tank behavior, indicating a spoofed or stuck level signal."}

## gpt-5.6-sol — native — TN

**w0000 rep0** (tokens: None, latency: 12.5s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"All reported flows match actuator states, pressure responses track pump and valve changes, and tank-level evolution remains physically coherent throughout the window."}

**w0001 rep0** (tokens: None, latency: 21.3s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"All actuator states match reported flows, switching events produce coherent pressure responses, and tank-level changes follow plausible operating dynamics without isolated invariant violations."}

**w0002 rep0** (tokens: None, latency: 28.7s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"Actuator states consistently match reported flows, pressure changes track pump and valve transitions, and tank-level trajectories show no isolated unexplained discontinuities."}

## gpt-5.6-sol — native — TP

**w0027 rep0** (tokens: None, latency: 11.4s)

> {"verdict":"attack","flagged_hours":[4,5,6,7,8,9],"reasoning":"L_T2 is implausibly clamped at exactly 4.90 for six consecutive hours despite changing pump states, flows, and surrounding tank dynamics, indicating likely sensor spoofing."}

**w0051 rep0** (tokens: None, latency: 17.7s)

> {"verdict":"attack","flagged_hours":[4],"reasoning":"Hour 4 shows an implausible abrupt L_T2 drop from 4.10 to 1.48 followed by a rapid rebound, without corresponding flow or actuator changes, indicating likely level-sensor spoofing."}

**w0053 rep0** (tokens: None, latency: 19.1s)

> {"verdict":"attack","flagged_hours":[4],"reasoning":"Hour 4 shows an abrupt, unexplained L_T2 drop from 4.10 to 1.48 without a commensurate actuator or flow change, violating tank mass balance."}

## gpt-5.6-sol — obfuscated — FN

**w0012 rep0** (tokens: None, latency: 39.6s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"All major flow and pressure changes align with corresponding actuator-state transitions, with no clear mass-balance, pressure-flow, or actuator-coherence violation."}

**w0013 rep0** (tokens: None, latency: 23.0s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"Actuator transitions are accompanied by coherent pressure and flow responses, with no clear mass-balance, pressure-flow, or actuator-effect violations."}

**w0014 rep0** (tokens: None, latency: 34.6s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"All major flow and pressure transitions align with corresponding actuator-state changes, with no clear mass-balance, pressure-flow, or actuator-coherence violation."}

## gpt-5.6-sol — obfuscated — FP

**w0049 rep0** (tokens: None, latency: 11.1s)

> {"verdict":"attack","flagged_hours":[20,21,22,23],"reasoning":"At hour 20 col_0030 abruptly collapses from 166.161 to 0.415 and remains pinned despite sustained flows and unchanged actuator states, violating pressure-flow and actuator coherence."}

**w0062 rep1** (tokens: None, latency: 20.7s)

> {"verdict":"attack","flagged_hours":[18,19,20,21,22,23],"reasoning":"At hour 18 col_0000 abruptly collapses from about 100 to -1.111 and remains pinned there despite restored actuator and flow conditions, violating pressure-flow and actuator coherence."}

**w0023 rep2** (tokens: None, latency: 31.7s)

> {"verdict":"attack","flagged_hours":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],"reasoning":"The invariant col_0037 reading remains frozen at 1.472 throughout substantial actuator, flow, and pressure changes, indicating a spoofed level sensor decoupled from system dynamics."}

## gpt-5.6-sol — obfuscated — TN

**w0000 rep0** (tokens: None, latency: 20.0s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"All abrupt flow and pressure changes align with actuator-state transitions and produce coherent downstream responses, with no clear invariant violation."}

**w0001 rep0** (tokens: None, latency: 27.4s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"All major pressure, flow, and level changes align with actuator-state transitions, with no clear invariant violations."}

**w0002 rep0** (tokens: None, latency: 32.6s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"All major pressure, flow, and level changes align with corresponding actuator-state transitions, with no clear invariant violations."}

## gpt-5.6-sol — obfuscated — TP

**w0026 rep0** (tokens: None, latency: 32.6s)

> {"verdict":"attack","flagged_hours":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],"reasoning":"The invariant values of col_0011 and col_0037 across the entire window despite repeated actuator-driven flow and pressure changes indicate frozen or spoofed level telemetry."}

**w0028 rep0** (tokens: None, latency: 42.1s)

> {"verdict":"attack","flagged_hours":[20,21,22,23],"reasoning":"col_0019 reports the actuator off while col_0013 remains near 49 instead of dropping to its established off-state baseline near 1.5, violating actuator-flow coherence."}

**w0029 rep0** (tokens: None, latency: 52.4s)

> {"verdict":"attack","flagged_hours":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],"reasoning":"The continuous signal col_0037 remains implausibly frozen at 1.472 throughout substantial actuator and hydraulic changes, indicating persistent sensor spoofing and process-state decoupling."}

## gpt-5.6-sol — schema_preserved — FN

**w0012 rep0** (tokens: None, latency: 28.0s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"All actuator transitions have corresponding flow and pressure responses, while tank-level trajectories remain smooth and consistent with changing operating conditions."}

**w0013 rep0** (tokens: None, latency: 17.4s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"Actuator transitions consistently correspond to expected flow and pressure changes, while tank-level variations follow recurring operational patterns without clear invariant violations."}

**w0014 rep0** (tokens: None, latency: 29.2s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"All actuator transitions have coherent flow and pressure responses, while tank-level changes remain consistent with the observed operating states."}

## gpt-5.6-sol — schema_preserved — FP

**w0011 rep0** (tokens: None, latency: 13.5s)

> {"verdict":"attack","flagged_hours":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],"reasoning":"Reported tank levels are physically impossible throughout the window, with L_T2 continuously negative and L_T1 later falling below zero despite sustained pump activity, indicating persistent level-process inconsistency."}

**w0011 rep1** (tokens: None, latency: 12.5s)

> {"verdict":"attack","flagged_hours":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],"reasoning":"All hours contain physically impossible negative tank levels, especially L_T2 throughout and L_T1 from hour 16 onward, indicating persistent level-sensor spoofing."}

**w0076 rep1** (tokens: None, latency: 20.0s)

> {"verdict":"attack","flagged_hours":[18,19,20,21,22,23],"reasoning":"A sustained anomalous V2 closure begins at hour 18, with F_V2 collapsing to -1.111 and associated pressure shifts persisting through hour 23."}

## gpt-5.6-sol — schema_preserved — TN

**w0000 rep0** (tokens: None, latency: 11.7s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"All actuator transitions have corresponding flow and pressure responses, while tank-level changes remain smooth and physically plausible throughout the window."}

**w0001 rep0** (tokens: None, latency: 24.7s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"Actuator transitions consistently produce corresponding flow and pressure responses, while tank-level changes remain smooth and operationally plausible with no clear invariant violations."}

**w0002 rep0** (tokens: None, latency: 30.0s)

> {"verdict":"normal","flagged_hours":[],"reasoning":"All actuator transitions have coherent flow and pressure responses, while tank-level changes remain plausibly coupled to the operating states without clear invariant violations."}

## gpt-5.6-sol — schema_preserved — TP

**w0026 rep1** (tokens: None, latency: 23.6s)

> {"verdict":"attack","flagged_hours":[17,18,19,20,21],"reasoning":"L_T2 is unnaturally frozen at -1.803 for five consecutive hours despite ongoing actuator activity and substantial changes in other tank levels, indicating likely sensor spoofing."}

**w0028 rep1** (tokens: None, latency: 16.1s)

> {"verdict":"attack","flagged_hours":[6],"reasoning":"At hour 6, F_V2 abruptly reports the closed-flow value despite S_V2 remaining open, with simultaneous pressure shifts indicating actuator-state/flow incoherence."}

**w0029 rep1** (tokens: None, latency: 66.3s)

> {"verdict":"attack","flagged_hours":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23],"reasoning":"Persistent impossible negative tank readings and extreme level trajectories across the entire window indicate sustained level-sensor spoofing inconsistent with the otherwise coherent actuator and flow telemetry."}

## grok-4 — native — FN

**w0012 rep0** (tokens: None, latency: 103.1s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Actuator states match reported flows, tank levels move consistently with pump and valve activity (including faster T1 fill while V2 is closed), and pressures track those flows without invariant breaks."}

**w0013 rep0** (tokens: None, latency: 237.4s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Pump and valve states match their flows, pressures move with those actuators, and tank level trends follow the reported inflows, outflows, and plausible demand without invariant breaks."}

**w0014 rep0** (tokens: None, latency: 156.4s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Pump and valve states match their flows, pressure shifts align with actuator changes, and tank level trends are consistent with reported inflows, outflows, and demand."}

## grok-4 — native — FP

**w0018 rep0** (tokens: None, latency: 238.9s)

> {"verdict": "attack", "flagged_hours": [10, 11], "reasoning": "T7 rises while PU10 is reported off and then falls at roughly twice the earlier no-pump drain rate, violating mass balance and pump-level coherence."}

**w0024 rep0** (tokens: None, latency: 349.0s)

> {"verdict": "attack", "flagged_hours": [15, 16, 17, 18, 19, 20, 21, 22], "reasoning": "PU2 stays off while T1 drains from 3.73 m to 1.30 m and T2 rises for six hours with PU4/PU5 off, decoupling tank levels from reported pump activity and violating mass balance."}

**w0033 rep0** (tokens: None, latency: 480.1s)

> {"verdict": "attack", "flagged_hours": [3, 4, 5, 6, 7, 16, 17, 18, 19, 20, 21, 22], "reasoning": "T2 rises for many hours while PU4/PU5 are off and reported inflow is zero, violating mass balance and decoupling tank level from pump activity."}

## grok-4 — native — TN

**w0000 rep0** (tokens: None, latency: 157.7s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Pump/valve states match their flows and downstream pressures, and tank level trends align with pump activity without mass-balance or actuator-coherence violations."}

**w0001 rep0** (tokens: None, latency: 115.5s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Actuator states match corresponding flows and downstream pressures throughout, and tank levels move consistently with pump/valve activity under typical diurnal demand, so no invariant violations are evident."}

**w0002 rep0** (tokens: None, latency: 143.6s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Actuator states match flows, pressures follow pump curves and valve open/closed differentials, and tank levels obey mass balance (T1 rises faster and T2 drains while V2 is closed)."}

## grok-4 — native — TP

**w0028 rep0** (tokens: None, latency: 85.3s)

> {"verdict": "attack", "flagged_hours": [6], "reasoning": "Hour 6 has S_V2 open and P_J14/P_J422 equalized as if the valve is open, yet F_V2 is zero, violating actuator-flow and pressure-flow invariants."}

**w0029 rep0** (tokens: None, latency: 164.7s)

> {"verdict": "attack", "flagged_hours": [13], "reasoning": "L_T7 falls by 2.13 in hour 13 while PU10 turns on with positive flow, violating mass-balance and actuator-coherence invariants."}

**w0052 rep0** (tokens: None, latency: 117.8s)

> {"verdict": "attack", "flagged_hours": [4], "reasoning": "L_T2 falls 2.62 in a single hour as PU4/PU8 switch off and then rebounds while those pumps stay off, violating mass-balance and actuator-coherence invariants."}

## grok-4 — obfuscated — FN

**w0012 rep0** (tokens: None, latency: 335.0s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Actuator on/off changes align with matching flow near-zero versus running readings and tank-like levels evolve smoothly with those pump cycles, so mass-balance, pressure-flow, and actuator-coherence invariants hold."}

**w0014 rep0** (tokens: None, latency: 318.5s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Actuator on/off states line up exactly with the expected on/off readings of related flows and pressures, tank-like signals change only gradually, and no mass-balance, pressure-flow, or actuator-coherence violations appear in the window."}

**w0026 rep0** (tokens: None, latency: 184.4s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Pump and valve toggles line up with matching shifts in flows and pressures, and gradual tank-like signals move with those actuator patterns, so mass-balance, pressure-flow, and actuator-coherence invariants hold."}

## grok-4 — obfuscated — FP

**w0001 rep0** (tokens: None, latency: 116.8s)

> {"verdict": "attack", "flagged_hours": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20], "reasoning": "Implausible frozen/spoofed readings (e.g. -3.757, 4.808, 0.415, -1.163) plus actuator changes without matching level/pressure/flow responses violate mass-balance, pressure-flow and actuator-coherence invariants."}

**w0002 rep0** (tokens: None, latency: 74.3s)

> {"verdict": "attack", "flagged_hours": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], "reasoning": "Multiple sensors freeze at physically implausible negative or constant values with sudden unexplained jumps that violate mass-balance, pressure-flow, and actuator-coherence invariants."}

**w0003 rep0** (tokens: None, latency: 98.7s)

> {"verdict": "attack", "flagged_hours": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], "reasoning": "Sensors show physically impossible negatives, a long freeze of a previously ~170 reading at 0.415, and actuator/flow/level decoupling, violating mass-balance and pressure-flow invariants from hour 3 onward."}

## grok-4 — obfuscated — TN

**w0000 rep0** (tokens: None, latency: 138.4s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Apparent discontinuities in continuous signals align with actuator on/off transitions, and no unexplained mass-balance or pressure-flow invariant violations are present."}

**w0005 rep0** (tokens: None, latency: 351.9s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Every large jump in continuous signals lines up with an actuator toggle and tank-like traces fill while the associated pumps are on and drain while they are off, so mass-balance, pressure-flow, and actuator-coherence invariants hold."}

**w0006 rep0** (tokens: None, latency: 137.2s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Actuator toggles align with corresponding drops or rises in related flows and pressures, and tank-like signals evolve smoothly without unexplained decoupling, so the window is consistent with normal operation."}

## grok-4 — obfuscated — TP

**w0013 rep0** (tokens: None, latency: 64.3s)

> {"verdict": "attack", "flagged_hours": [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], "reasoning": "Multiple continuous sensors freeze at unphysical constants (e.g. -1.111, -1.163, 0.415, -3.757, 1.505, 4.808) from hour 3 through 21 while actuators still toggle, violating mass-balance and actuator-coherence invariants."}

**w0015 rep0** (tokens: None, latency: 100.7s)

> {"verdict": "attack", "flagged_hours": [3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 16, 17, 18, 19, 20, 21, 22, 23], "reasoning": "Multiple sensors stick at implausible constants (-3.757, 4.808, -1.163, -1.111, 0.415) that violate mass-balance and pressure-flow invariants relative to neighboring hours and actuator states."}

**w0028 rep0** (tokens: None, latency: 448.1s)

> {"verdict": "attack", "flagged_hours": [6], "reasoning": "Hour 6 violates actuator coherence: a pump status stays ON while its flow drops to the off-state placeholder (~-1.11) and several related pressures/flows spike inconsistently with adjacent hours."}

## grok-4 — schema_preserved — FN

**w0012 rep0** (tokens: None, latency: 124.9s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Actuator toggles match corresponding flow changes, tank levels move with implied inflows/outflows, and pressure-flow coupling remains consistent, so no physical-invariant violations appear in the window."}

**w0013 rep0** (tokens: None, latency: 92.7s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Pump/valve states match their flows throughout, tank levels follow plausible fill/drain cycles with those actuators, and pressure shifts track the same on/off changes, so the three invariants hold."}

**w0014 rep0** (tokens: None, latency: 234.7s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Pump and valve states match their flows and produce corresponding pressure and tank-level responses, so the three physical invariants hold throughout the window."}

## grok-4 — schema_preserved — FP

**w0001 rep0** (tokens: None, latency: 211.7s)

> {"verdict": "attack", "flagged_hours": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], "reasoning": "Tank T2 reports physically impossible negative levels in every hour (with T1 and T7 also negative later), violating mass-balance and indicating persistent sensor spoofing."}

**w0003 rep0** (tokens: None, latency: 167.6s)

> {"verdict": "attack", "flagged_hours": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], "reasoning": "L_T2 is physically impossible (negative) in every hour and L_T1 also goes negative while PU1 reports maximum inflow, violating mass-balance and indicating sensor spoofing."}

**w0005 rep0** (tokens: None, latency: 174.2s)

> {"verdict": "attack", "flagged_hours": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], "reasoning": "L_T2 is negative in every hour, which is physically impossible for a tank level and indicates persistent sensor spoofing."}

## grok-4 — schema_preserved — TN

**w0000 rep0** (tokens: None, latency: 73.9s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Actuator toggles match corresponding flows and produce coherent pressure and tank-level responses, with no mass-balance or pressure-flow invariant breaks."}

**w0002 rep0** (tokens: None, latency: 91.5s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Actuator states match corresponding flows, tank levels move with inflows/outflows (including L_T6 holding at a plausible full setpoint), and pressure changes track pump/valve toggles, so the three invariants hold across the window."}

**w0004 rep0** (tokens: None, latency: 127.4s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Tank trajectories, pressure-flow coupling, and actuator-to-process responses remain consistent with mass balance and actuator coherence across the window, including delayed level effects after pump/valve toggles."}

## grok-4 — schema_preserved — TP

**w0015 rep0** (tokens: None, latency: 269.2s)

> {"verdict": "attack", "flagged_hours": [8, 9, 10, 11, 12, 19, 20, 21, 22, 23], "reasoning": "L_T7 plunges by ~2m into unphysical negative values exactly when PU10 turns on (hours 8 and 19) and stays negative, decoupling tank level from reported inflow and violating mass-balance and actuator-coherence."}

**w0026 rep0** (tokens: None, latency: 83.8s)

> {"verdict": "attack", "flagged_hours": [9, 17], "reasoning": "S_V2 remains open while F_V2 collapses to -1.111 and P_J415 drops sharply, violating actuator-flow-pressure coherence at those hours."}

**w0027 rep0** (tokens: None, latency: 67.3s)

> {"verdict": "attack", "flagged_hours": [4, 5, 6, 7, 8, 9], "reasoning": "L_T2 is frozen at exactly -2.084 for six consecutive hours despite changing pump/valve activity, violating mass-balance and indicating tank-level sensor spoofing."}

## opus-5 — native — FN

**w0026 rep0** (tokens: 11509, latency: 142.3s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "All pump/valve states match their reported flows, pressures at J256/J415/J306/J317 track the corresponding pump activity (high when on, low when off), and tank trajectories (T3 with PU4, T5 with PU8, T7 with PU10, T2 saturating at its 5.40 cap where F_V2 collapses to F_PU7) are consistent with mass balance, so no invariant violation is evident."}

**w0015 rep1** (tokens: 7582, latency: 98.0s)

> {"verdict": "normal", "reasoning": "All tank level trajectories track their associated pump/valve flows with a consistent one-hour lag (T3 with PU4, T4 with PU7, T5 with PU8, T6 with PU10, T2 with V2, T1 with PU1/PU2 minus V2), every actuator state matches its reported flow, and pressure changes (J256, J415, J317, J302/306, J14/J422) respond coherently to each actuator transition including the V2 closure and PU2 shutdown.", "flagged_hours": []}

**w0015 rep2** (tokens: 14894, latency: 192.7s)

> {"verdict": "normal", "reasoning": "All actuator states match their reported flows, tank levels track pump/valve activity coherently (T1 rises when V2 closes, T2 drains with V2 shut, T3 follows PU4, T5 follows PU8, T4 follows PU7), and pressure changes (P_J256 with PU4, P_J317 with PU10, P_J14/P_J422 divergence at valve closure, P_J269 drop when PU2 stops) are all consistent with the flow and actuator changes, so no invariant violation is evident."}

## opus-5 — native — FP

**w0000 rep0** (tokens: 1249, latency: 19.5s)

> {"verdict": "attack", "flagged_hours": [17, 18, 19, 20, 21, 22, 23], "reasoning": "From row 17 onward valve V2 is commanded closed (S_V2=0, F_V2=0) with an anomalous sustained pressure split across J14/J422 (≈40 vs ≈29 instead of the prior ~1 psi differential), and tank T2 drains monotonically from 5.24 to 1.39 with no compensating inflow, indicating a malicious actuator manipulation."}

**w0001 rep0** (tokens: 908, latency: 13.0s)

> {"verdict": "attack", "flagged_hours": [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], "reasoning": "From the hour PU2 is switched off, L_T1 falls monotonically from ~4.5 to 0.71 despite PU1 (and later PU2) reporting sustained high inflow of 117-120 units, a clear mass-balance/actuator-coherence violation consistent with tank-level spoofing."}

**w0003 rep0** (tokens: 1794, latency: 26.7s)

> {"verdict": "attack", "flagged_hours": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], "reasoning": "From hour 10 onward PU2 is reported off while F_PU1 jumps to an implausibly high 112-122 with pump-discharge pressure P_J269 collapsing from ~38 to ~20-26, and tank T1 steadily drains from 4.53 to 1.04 despite this reported maximal inflow — violating both pressure-flow consistency and mass balance."}

## opus-5 — native — TN

**w0002 rep0** (tokens: 15318, latency: 196.0s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "All actuator states match their reported flows, pressures at J256/J415/J306/J317/J14 respond correctly to PU4/PU7/PU8/PU10/V2 switching, and every tank's level trend follows its supplying pump (the few one-hour rises with zero reported flow occur exactly at pump-shutdown snapshots and are consistent with instantaneous sampling), so no invariant violation indicative of an attack is present."}

**w0041 rep0** (tokens: 9007, latency: 111.5s)

> {"verdict": "normal", "reasoning": "All pump/valve states match their reported flows, tank levels rise and fall consistently with the corresponding inflows/outflows, and the second-half regime change (V2 closing when T2 hits its 5.5 m ceiling, with T2 then draining, PU1/PU2 flow dropping and head at J14 rising) is physically coherent pump-curve/valve behavior rather than an invariant violation."}

**w0042 rep0** (tokens: 12779, latency: 159.7s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "All tank levels track their controlling actuators with consistent lags (T2↔V2, T3↔PU4, T4↔PU7, T5↔PU8, T6/T7↔PU10), pressures rise/fall coherently with the corresponding pump flows, and the PU2 shutdown in the final hours produces a physically consistent single-pump flow increase, discharge-pressure drop, and T1 drawdown, so no invariant violations are evident."}

## opus-5 — native — TP

**w0015 rep0** (tokens: 1131, latency: 16.3s)

> {"verdict": "attack", "flagged_hours": [22, 23], "reasoning": "When PU2 is shut off the reported PU1 flow jumps to ~113 (total delivery roughly halved) yet the pump-discharge pressure P_J269 collapses from ~37 to ~26 and P_J422 drops sharply, an inversion of the pressure-flow relationship that indicates spoofed flow/pressure telemetry rather than a genuine pump transition."}

**w0027 rep0** (tokens: 963, latency: 15.6s)

> {"verdict": "attack", "flagged_hours": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], "reasoning": "Tank T1 drains monotonically from ~4.45 m to 0.82 m even though PU1 reports sustained maximum inflow (115–121 L/s, with PU2 re-engaged near the end) and no corresponding outflow or pressure signature appears, a clear mass-balance/actuator-coherence violation indicative of level-sensor spoofing."}

**w0028 rep0** (tokens: 1520, latency: 20.4s)

> {"verdict": "attack", "flagged_hours": [20, 21, 22, 23], "reasoning": "At row 20 valve V2 is commanded closed (S_V2 1→0, F_V2 51.4→0) with no operational justification while tank T2 is at its upper limit, and T2 then drains monotonically (4.40→4.00→3.29→2.40→1.52) alongside an abrupt decoupling of P_J14/P_J422 and a collapse of P_J300/P_J289, indicating a malicious valve-manipulation attack sustained through the end of the window."}

## opus-5 — obfuscated — FN

**w0014 rep0** (tokens: 12785, latency: 165.6s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Every discrete actuator transition (col_0027, col_0023, col_0019, col_0008, col_0032) is matched by coherent step changes in the associated flow/pressure channels (col_0024, col_0002, col_0000, col_0013, col_0031/col_0012/col_0007), tank-like signals rise and fall in phase with their driving pumps, and the residual variability (e.g., the periodic bimodal swings of col_0005 with mild inverse pressure response) is consistent with demand-driven operation rather than invariant violation."}

**w0029 rep0** (tokens: 9557, latency: 116.7s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Every discrete actuator toggle (col_0018, col_0019, col_0023, col_0027, col_0032, col_0008) is matched by an immediate, correctly-signed change in its associated flow/pressure channels (col_0030, col_0000, col_0002/col_0005, col_0024/col_0015, col_0001/col_0031, col_0013/col_0039), and tank-level trends (col_0038, col_0029) track inflow states with normal one-hour lag, so no mass-balance, pressure-flow, or actuator-coherence invariant is violated in this window.}"}

**w0036 rep0** (tokens: 10132, latency: 122.5s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Every discrete actuator toggle (col_0019, col_0008, col_0023, col_0027, col_0032, col_0014) is matched by the expected simultaneous step in its associated flow/pressure channels (col_0000, col_0013/col_0039, col_0005/col_0002, col_0024/col_0015, col_0001/col_0031, col_0003/col_0021), and tank-like levels evolve smoothly with no unexplained jumps or flow-pressure inversions."}

## opus-5 — obfuscated — FP

**w0000 rep0** (tokens: 8766, latency: 95.0s)

> {"verdict": "attack", "flagged_hours": [16], "reasoning": "At hour 16 the pump state S (col_0008) is reported ON yet its associated pipe flow collapses to the exact idle value (col_0013 = 1.505) with the downstream pressure col_0039 dropping to its lowest observed level (91.7), matching the OFF-state signature of hours 2, 6 and 7 — an actuator/flow coherence violation, while all other hours' discrete-continuous couplings (col_0027→col_0024, col_0032→col_0001, col_0023→col_0005/col_0002, col_0019→col_0000) remain consistent."}

**w0003 rep0** (tokens: 10463, latency: 125.6s)

> {"verdict": "attack", "flagged_hours": [7, 8], "reasoning": "At hours 7-8 three actuators (col_0027, col_0008, col_0019) drop out simultaneously while a group of pressure/flow sensors (col_0017, col_0016, col_0042, col_0006, col_0001) hold bit-identical values across the two hours instead of responding, and tank signal col_0033 shows its fastest rise (+0.41/+0.52) precisely when its supply pipe col_0000 reads shut off (-1.111), violating both mass balance and actuator coherence."}

**w0005 rep0** (tokens: 15824, latency: 190.1s)

> {"verdict": "attack", "flagged_hours": [21, 22, 23], "reasoning": "All pump/valve states map coherently to their flows and downstream pressures throughout the window, but in the final hours tank col_0028 keeps draining (-0.45, -0.48, -0.34) to unprecedented lows while its feeding pump (col_0008) reports steady ~48 unit inflow for consecutive hours — a mass-balance violation (level decoupled from reported pump activity) not seen in any earlier on-cycle, where the same flow produced consistent level rises."}

## opus-5 — obfuscated — TN

**w0009 rep0** (tokens: 7980, latency: 98.1s)

> {"verdict": "normal", "reasoning": "Every discrete actuator transition (col_0008, col_0018, col_0019, col_0023, col_0027, col_0032) is matched by the expected step in its associated flow/pressure channels (col_0013/col_0039, col_0030/col_0021, col_0000, col_0002/col_0005, col_0024/col_0015, col_0001/col_0031), and tank-level signals evolve smoothly and consistently with the reported inflows, so no invariant violation is evident.", "flagged_hours": []}

**w0016 rep0** (tokens: 149, latency: 5.0s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Actuator toggles (col_0027, col_0019, col_0013/col_0032, col_0040-group) consistently coincide with corresponding jumps in flows and pressures (e.g., col_0024, col_0031, col_0013, col_0030), and tank/level trends drift smoothly with no unexplained decoupling, so the window appears consistent with normal operation."}

**w0017 rep0** (tokens: 14672, latency: 176.1s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Every discrete actuator state maps consistently to its associated flow (col_0000/col_0019, col_0030/col_0018, col_0024/col_0027, col_0013-0039/col_0008, col_0002-0005/col_0023, col_0031/col_0032), and all tank levels (col_0017, col_0029, col_0033, col_0035, col_0038) rise and fall with one-hour lag exactly in accordance with the corresponding pump/valve states and downstream pressures, so no mass-balance, pressure-flow, or actuator-coherence violations appear in the window."}

## opus-5 — obfuscated — TP

**w0013 rep0** (tokens: 10326, latency: 127.2s)

> {"verdict": "attack", "reasoning": "Hours 4-5 show several sensors (col_0016=41.089, col_0042=39.304, col_0006=28.094, col_0017=-1.876) frozen at bit-identical values while all other pressures/flows/levels continue to change, and the tank trace col_0033 rises steeply (2.36→4.00) despite most pumps being switched off — a spoofing/replay signature violating mass balance and pressure-flow consistency.", "flagged_hours": [4, 5]}

**w0015 rep0** (tokens: 5061, latency: 65.8s)

> {"verdict": "attack", "flagged_hours": [17, 18, 19, 20, 21, 22, 23], "reasoning": "From row 17 onward col_0036 jumps ~+16 units and stays elevated while its normally tightly coupled neighbors (col_0016, col_0006) instead decline, and col_0000 collapses to a frozen -1.111 with no consistent downstream pressure/flow response, indicating spoofed level/flow telemetry decoupled from actuator state."}

**w0027 rep0** (tokens: 9782, latency: 113.4s)

> {"verdict": "attack", "reasoning": "Signal col_0017 is frozen at exactly -2.084 for six consecutive hours (rows 4-9) despite drifting hour-to-hour before and after, coinciding with erratic single-hour toggling of pump col_0027 and abnormal pressure excursions (col_0036/col_0016/col_0031 spikes) inconsistent with the rest of the window, indicating sensor spoofing/replay concealment.", "flagged_hours": [4, 5, 6, 7, 8, 9]}

## opus-5 — schema_preserved — FN

**w0012 rep0** (tokens: 8353, latency: 103.3s)

> {"verdict": "normal", "reasoning": "Actuator states track their flows consistently (PU7/PU8/PU10/V2 all show correct on/off flow signatures), tank levels move coherently with the corresponding pump/valve activity (T2 with V2, T5 with PU8, T3 with PU4, T1 filling while V2 shut and draining when open), and pressures respond appropriately to pump/valve transitions, so no invariant violation warrants flagging.", "flagged_hours": []}

**w0014 rep0** (tokens: 9198, latency: 116.8s)

> {"verdict": "normal", "reasoning": "All actuator states match their corresponding flows (PU4/PU7/PU8/PU10/V2 on-off transitions align with flow values), and tank levels T1–T5, T7 rise and fall coherently with the pumps/valve feeding them (e.g., T5 tracks PU8, T4 drops one hour after PU7 shuts, T2 rises only while V2 is open), so despite the quasi-periodic swings in P_J256 no mass-balance, pressure-flow, or actuator-coherence invariant is clearly violated.", "flagged_hours": []}

**w0053 rep0** (tokens: 10463, latency: 143.1s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "Every pump/valve state transition (PU2, PU4, PU7, PU8, PU10) is matched by the expected flow step and downstream pressure change (e.g., P_J269 drops 47→30 when S_PU2 goes 0 and recovers to 41.6 when it returns; P_J256 tracks S_PU4), and tank trajectories (T3, T4, T5, T7) rise and fall in line with their feeding pumps, so the residual level/inflow discrepancies for T1 and T7 are within plausible diurnal demand variation rather than invariant violations."}

## opus-5 — schema_preserved — FP

**w0001 rep0** (tokens: 1472, latency: 22.5s)

> {"verdict": "attack", "flagged_hours": [17, 18, 19, 20, 21, 22, 23], "reasoning": "L_T1 drifts monotonically downward into physically impossible negative values and keeps falling even after PU2 is re-energized (S_PU2=1, F_PU2≈178) with PU1 also delivering ~154 units — an inflow that earlier in the window clearly raised the tank — indicating a spoofed/decoupled T1 level sensor rather than genuine drawdown."}

**w0002 rep0** (tokens: 8952, latency: 110.4s)

> {"verdict": "attack", "reasoning": "Tank T7 collapses by ~3.1 units at hour 13→14 (more than twice any comparable pump-off decline) and then keeps falling to its window minimum through hours 15–17 even though PU10 is reported ON at its highest flows of the window (52.3, 52.0, 49.1) with normal downstream pressures (P_J415 ≈ 116–117), a clear mass-balance/actuator-coherence violation indicating spoofed level or flow reporting.", "flagged_hours": [14, 15, 16, 17]}

**w0003 rep0** (tokens: 1009, latency: 15.8s)

> {"verdict": "attack", "reasoning": "From row 13 onward L_T1 falls monotonically (4.13 → -0.79, going physically impossible negative) even though PU1 is commanded on with a sustained high, even increasing, flow (~176-192) and PU2 is off with its flow frozen at 0.415, indicating spoofed tank-level/pump telemetry decoupled from mass balance.", "flagged_hours": [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]}

## opus-5 — schema_preserved — TN

**w0000 rep0** (tokens: 3153, latency: 43.5s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "All actuator states align with their pump/valve flows (off-states give residual flows, on-states give nominal flows), tank levels rise and fall consistently with the corresponding pump activity (e.g., T3 with PU4, T5 with PU7, T1 with V2 closure), and the V2 shutdown at hour 17 produces coherent downstream pressure changes (P_J14 rise, P_J422 drop), so no invariant violation indicative of attack is present."}

**w0009 rep0** (tokens: 15204, latency: 200.3s)

> {"verdict": "normal", "reasoning": "Every actuator state matches its pump/valve flow (on-state flows vs. fixed off-state offsets), pressures at J269/J256/J415/J317/J306 shift coherently with PU2/PU4/PU7/PU10/PU8 toggles, and all tank trajectories (T1 with PU1/PU2, T2 with V2, T3 with PU4, T5 with PU8, T7 with PU10) rise and fall in step with their supply actuators, so no invariant violation is evident."}

**w0017 rep0** (tokens: 7156, latency: 90.3s)

> {"verdict": "normal", "flagged_hours": [], "reasoning": "All discrete actuator states track their corresponding flows (pumps/valve show zero-baseline flow when off and nominal flow when on), pressure levels shift coherently with pump/valve toggles (e.g., P_J269 and P_J14 respond to PU2 and V2 state changes), and tank trajectories follow their feeding pumps with a consistent one-step lag, so no invariant violation indicative of spoofing is evident."}

## opus-5 — schema_preserved — TP

**w0013 rep0** (tokens: 3944, latency: 50.5s)

> {"verdict": "attack", "flagged_hours": [17, 18, 19, 20, 21, 22, 23], "reasoning": "L_T1 declines monotonically to physically impossible negative values (0.83 → -1.12) even though PU1 reports continuous high flow (~185-190) and PU2 comes back online at the end, a clear mass-balance/actuator-coherence violation indicative of level-sensor spoofing, accompanied by erratic P_J256 spikes (~194) unsupported by any pump/valve flow change."}

**w0015 rep0** (tokens: 13674, latency: 164.8s)

> {"verdict": "attack", "flagged_hours": [17, 18, 19, 20, 21, 22, 23], "reasoning": "From hour 17 onward valve V2 is driven closed (F_V2 collapses from ~115 to -1.111) with an abrupt P_J14 jump to ~71 and a sustained monotonic drain of T2 (-1.8 to -3.9) while T1 abnormally over-fills to ~4.3, and at hours 21-23 PU2 is dropped with F_PU1 pushed to an out-of-range 176-178 and P_J269 collapsing to ~31 — a coordinated actuator/hydraulic deviation from the stable regime of the first 17 hours."}

**w0026 rep0** (tokens: 3576, latency: 48.1s)

> {"verdict": "attack", "flagged_hours": [9, 17], "reasoning": "At these two hours the V2 valve reports S_V2=1 (open) yet F_V2 collapses to ~-1.1 (no flow) while P_J300/P_J14 spike and P_J415 drops sharply, an actuator-state/flow incoherence not seen in other PU7-off hours (rows 4-5) where F_V2 remained ~107-110."}

