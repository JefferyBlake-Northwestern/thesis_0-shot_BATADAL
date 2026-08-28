"""Prompt assembly (Ch.4 §4.3.1, Factor A).

This prompt contains two framing templates, selected by the `framing` argument
that the run loop passes from each cell coordinate:
    framing="domain"  -> DOMAIN_FRAMING  (center-point default)
    framing="neutral" -> NEUTRAL_FRAMING (RQ2 ablation level)

Wording of DOMAIN_FRAMING integrates advisor-approved content: SCADA signal
taxonomy and the three hydraulic invariants (mass balance, pressure-flow
consistency, actuator coherence). NEUTRAL_FRAMING remains stripped of domain
context by design. The output contract (SYSTEM) is byte-identical across
framings so that any performance difference is attributable to framing alone.
"""

from __future__ import annotations

# --- Factor A = domain (center point) -------------------------------------------
DOMAIN_FRAMING = """
    You are an expert cyber-physical systems security analyst examining hourly SCADA \
    telemetry from a water distribution network for evidence of a cyber-physical attack. \
    Continuous signals report process state: tank levels (L_*), junction pressures (P_*), \
    and pipe and valve flows (F_*). Discrete signals report actuator positions: pump and \
    valve on/off states (S_*).

    In normal operation three physical invariants hold. Mass balance: tank levels rise \
    with inflow and fall with outflow; unexplained level changes suggest sensor spoofing. \
    Pressure-flow consistency: high flow rates correlate with pressure differentials \
    across connected nodes. Actuator coherence: pump and valve state changes produce \
    corresponding downstream changes in pressures, flows, and levels.

    Attacks typically manifest as violations of these invariants — tank levels decoupled \
    from reported pump activity, pressures inconsistent with flow, or actuator toggles \
    without observable downstream effect. Examine the window and determine whether any \
    hours show an attack.
    """

# --- Factor A = neutral (RQ2 ablation) ------------------------------------------
NEUTRAL_FRAMING = """
    You are analyzing a table of numeric sensor readings for anomalies. Each row is one time step; \
    columns are unlabeled signals. Some readings may be anomalous relative to the normal behavior \
    of the system. Examine each window and determine if any rows are anomalous.
"""

FRAMINGS = {"domain": DOMAIN_FRAMING, "neutral": NEUTRAL_FRAMING}

# Output contract -- fixed across every condition.
SYSTEM = (
    "Respond ONLY with a JSON object of the form "
    '{"verdict": "attack"|"normal", "flagged_hours": [int,...], '
    '"reasoning": "<one sentence>"}, where flagged_hours are zero-based row offsets '
    "within the window. No prose outside the JSON."
)


def build_prompt(window, framing="domain", representation="raw", reference="pure_zs"):
    if framing not in FRAMINGS:
        raise ValueError(f"unknown framing {framing!r}; expected one of {list(FRAMINGS)}")
    frame = FRAMINGS[framing]
    ref_block = ""
    if reference == "reference_augmented" and window.reference_csv:
        ref_block = f"\n\nReference window of normal operation:\n{window.reference_csv}\n"
    matrix = window.render(representation)
    user = f"{frame}{ref_block}\n\nWindow ({window.window_id}):\n{matrix}"
    return SYSTEM, user
