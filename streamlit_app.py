"""Main Streamlit application: selection, scoring, dialogs, and rendering."""

import os

import streamlit as st

from ui_styles import inject_app_styles, unit_key
from unit_data import (
    RATING_DETAILS,
    UNIT_IMAGES,
    UNIT_MATRIX,
    UNIT_OVERRIDES,
    UNITS,
    UNITS_TECH,
)


st.set_page_config(layout="wide", page_title="Mechabellum Unit Counters")
image_folder = os.path.join(os.getcwd(), "images")

show_sliders = st.sidebar.checkbox("Show Weight Sliders")
if "selected_units" not in st.session_state:
    st.session_state.selected_units = []
if "weights" not in st.session_state:
    st.session_state.weights = {unit: 1 for unit in UNIT_IMAGES}
if "show_de_tier" not in st.session_state:
    st.session_state.show_de_tier = False

inject_app_styles(image_folder)


def toggle_unit(unit):
    if unit in st.session_state.selected_units:
        st.session_state.selected_units.remove(unit)
    else:
        st.session_state.selected_units.append(unit)


with st.container(key="unit_picker_grid"):
    for unit in UNIT_IMAGES:
        selected = unit in st.session_state.selected_units
        with st.container(key=f"unit_tile_{unit_key(unit)}{'_selected' if selected else ''}"):
            st.button(
                unit,
                key=f"unit_button_{unit_key(unit)}",
                use_container_width=True,
                on_click=toggle_unit,
                args=(unit,),
            )
            if show_sliders and selected:
                st.session_state.weights[unit] = st.slider(
                    " ",
                    key=f"slider:{unit}",
                    min_value=1,
                    max_value=5,
                    value=st.session_state.weights[unit],
                )


def get_matchup_rating(candidate, enemy):
    """Return one curated rating and whether a tech override supplied it."""
    enemy_index = UNITS.index(enemy)
    if ":" not in candidate:
        return UNIT_MATRIX[candidate][enemy_index], "Base matchup"

    base_unit = candidate.split(":", 1)[0]
    overrides = UNIT_OVERRIDES[candidate]
    if enemy in overrides:
        return overrides[enemy], "Tech override"
    return UNIT_MATRIX[base_unit][enemy_index], "Base matchup fallback"


def get_counter_score(selected_units, weights):
    all_candidates = UNITS + UNITS_TECH
    scores = {candidate: 0 for candidate in all_candidates}
    divisors = {candidate: 0 for candidate in all_candidates}

    for enemy in selected_units:
        for candidate in all_candidates:
            rating, _ = get_matchup_rating(candidate, enemy)
            scores[candidate] += rating * weights[enemy]
            divisors[candidate] += weights[enemy]

    if selected_units:
        scores = {
            candidate: scores[candidate] / divisors[candidate]
            if divisors[candidate]
            else 0
            for candidate in scores
        }
    return sorted(scores.items(), key=lambda item: item[1], reverse=True)


S_TIER = "S Tier (4-5 points)"
A_TIER = "A Tier (3-4 points)"
B_TIER = "B Tier (2-3 points)"
C_TIER = "C Tier (1-2 points)"
DE_TIER = "D/E Tier (0-1 point)"


def get_tier_for_score(score):
    if 4 < score <= 5:
        return S_TIER
    if 3 < score <= 4:
        return A_TIER
    if 2 < score <= 3:
        return B_TIER
    if 1 < score <= 2:
        return C_TIER
    return DE_TIER


def classify_by_tier(best_counters):
    tier_bins = {tier: [] for tier in (S_TIER, A_TIER, B_TIER, C_TIER, DE_TIER)}
    for unit, score in best_counters:
        tier_bins[get_tier_for_score(score)].append(unit)

    base_unit_tiers = {
        unit: tier
        for tier, units in tier_bins.items()
        for unit in units
        if ":" not in unit
    }
    for tier, units in tier_bins.items():
        tier_bins[tier] = [
            unit
            for unit in units
            if ":" not in unit
            or base_unit_tiers.get(unit.split(":", 1)[0]) != tier
        ]
    return tier_bins


@st.dialog("Counter Breakdown", width="small")
def show_counter_details(counter_unit, overall_score, enemies, normalized_weights):
    st.markdown(
        f'<h2 style="margin: 0 0 .75rem; color: #ff4b4b !important;">{counter_unit}</h2>',
        unsafe_allow_html=True,
    )
    score_column, tier_column = st.columns(2)
    score_column.metric("Overall score", f"{overall_score:.2f} / 5")
    tier_column.metric("Tier", get_tier_for_score(overall_score).split(" ", 1)[0])
    st.caption(get_tier_for_score(overall_score))
    st.write("This score is the weighted average of the selected enemy matchups.")

    for enemy in enemies:
        rating, source = get_matchup_rating(counter_unit, enemy)
        grade, explanation = RATING_DETAILS[rating]
        weight = normalized_weights[enemy]
        st.markdown(f"**{enemy} — {grade} ({rating}/5)**")
        st.caption(
            f"{source} · Weight: {weight:.0%} · "
            f"Weighted contribution: {rating * weight:.2f}"
        )
        st.caption(explanation)


selected_units = st.session_state.selected_units
raw_weights = st.session_state.weights
total_weight = sum(raw_weights[unit] for unit in selected_units)
weights = {
    unit: raw_weights[unit] / total_weight for unit in selected_units
} if total_weight else {}
best_counters = get_counter_score(selected_units, weights)
tiered_counters = classify_by_tier(best_counters)
counter_scores = dict(best_counters)


if not selected_units:
    st.info("Please select enemy units to get counters")
else:
    st.write("Best Counter Units by Tier:")
    for tier, units in tiered_counters.items():
        st.markdown(f"**{tier}**")
        if tier == DE_TIER and units and not st.session_state.show_de_tier:
            if not st.button(
                f"Show D/E Tier ({len(units)} units)",
                key="show_de_tier_button",
                type="primary",
            ):
                continue
            st.session_state.show_de_tier = True

        if not units:
            st.caption("empty")
            continue

        with st.container(key=f"tier_grid_{unit_key(tier)}"):
            for result_index, unit in enumerate(units):
                if ":" in unit:
                    base_unit, tech_name = (part.strip() for part in unit.split(":", 1))
                else:
                    base_unit, tech_name = unit, None

                with st.container(
                    key=f"result_card_{unit_key(base_unit)}_{unit_key(tier)}_{result_index}"
                ):
                    if st.button(
                        unit,
                        key=f"result_image_{unit_key(base_unit)}_{unit_key(tier)}_{result_index}",
                        use_container_width=True,
                        help=f"Show why {unit} is recommended",
                    ):
                        show_counter_details(unit, counter_scores[unit], selected_units, weights)
                    if tech_name:
                        st.markdown(f"**{tech_name}**")
