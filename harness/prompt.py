"""Prompt assembly (Ch.4 §4.3.1, Factor A).

This prompt contains two framing templates, selected by the `framing` argument 
that the run loop passes from each cell coordinate:
    framing="domain"  -> DOMAIN_FRAMING  (center-point default)
    framing="neutral" -> NEUTRAL_FRAMING (RQ2 ablation level)

The output contract (SYSTEM) is maintained across the framings by design. Only the
domain context varies, so any performance difference is attributable to framing alone.
"""

from __future__ import annotations

# --- Factor A = domain (center point) -------------------------------------------
DOMAIN_FRAMING = """
    You are analyzing telemetry from a water distribution network for evidence of \
    a cyber-physical attack. The readings are hourly. Columns include: 
    tank levels (L_*), pump and valve flows (F_*), \
    pump and valve on/off states (S_*), \
    and junction pressures (P_*). 
    
    Attacks may manifest as physically inconsistent readings, for example: \
    tank levels that violate mass balance against inflow and outflow, or \
    pressures that decouple from pump activity. Examine the window and determine \
    whether any hours show an attack.
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
