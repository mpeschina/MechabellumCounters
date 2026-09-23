import streamlit as st
import os
from PIL import Image
import base64
import re


#
# local run: streamlit run streamlit_app.py
#


# Define the path to the image folder
image_folder = os.path.join(os.getcwd(), "images")

# Define the list of units and map them to local .jpg image file paths in the /images folder
unit_images = {
    "Crawler": "crawler.jpg",
    "Fang": "fang.jpg",
    "Hound": "hound.jpg",
    "Void Eye": "void_eye.jpg",
    "Marksman": "marksman.jpg",
    "Arclight": "arclight.jpg",
    "Wasp": "wasp.jpg",
    "Mustang": "mustang.jpg",
    "Sledgehammer": "sledgehammer.jpg",
    "Steelballs": "steelball.jpg",
    "Stormcaller": "stormcaller.jpg",
    "Phoenix": "phoenix.jpg",
    "Phantom Ray": "phantom_ray.jpg",
    "Tarantula": "tarantula.jpg",
    "Sabertooth": "sabertooth.jpg",
    "Rhino": "rhino.jpg",
    "Hacker": "hacker.jpg",
    "Wraith": "wraith.jpg",
    "Scorpion": "scorpion.jpg",
    "Vulcan": "vulcan.jpg",
    "Fortress": "fortress.jpg",
    "Melting Point": "melting_point.jpg",
    "Sandworm": "sandworm.jpg",
    "Raiden": "raiden.jpg",
    "Overlord": "overlord.jpg",
    "War Factory": "war_factory.jpg",
    "Abyss": "abyss.jpg",
    "Mountain": "mountain.jpg",
    "Fire Badger": "fire_badger.jpg",
    "Typhoon": "typhoon.jpg",
    "Farseer": "farseer.jpg"
}


st.set_page_config(
    layout = 'wide',
    page_title = 'Mechabellum Unit Counters'
)


#st.write("""
#    <style>
#    /* Center-align and enlarge the checkbox */
#    [data-baseweb="checkbox"] {
#        display: flex;
#        justify-content: center;
#        align-items: center;  /* Align vertically */
#        transform: scale(1.5);  /* Enlarge the checkbox */
#    }
#    </style>
#    """, unsafe_allow_html=True)


# this distributes the space of col. equally. removes responsivenes
#st.write('''<style>
#[data-testid="column"] {
#    width: calc(12.5% - 1rem) !important;
#    flex: 1 1 calc(12.5% - 1rem) !important;
#    min-width: calc(12.5% - 1rem) !important;
#}
#</style>''', unsafe_allow_html=True)


#st.write("""<style>
#    /* Reduce space between components */
#        .block-container {
#        padding: 1rem 1rem 1rem 1rem !important; /* Adjust to reduce space around the whole block */
#    }
#    </style>
#   """, unsafe_allow_html=True)


show_sliders = st.sidebar.checkbox("Show Weight Sliders")

#
# db
#
# Initialize session state to track selected units.
if 'selected_units' not in st.session_state:
    st.session_state.selected_units = []
if 'weights' not in st.session_state:
    st.session_state.weights = {unit: 1 for unit in unit_images.keys()}



# Helper function to convert image to base64
def get_image_as_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()


def unit_key(unit):
    """Return a stable, CSS-safe key for a unit name."""
    return re.sub(r"[^a-z0-9_]", "_", unit.lower().replace(" ", "_"))


def toggle_unit(unit):
    if unit in st.session_state.selected_units:
        st.session_state.selected_units.remove(unit)
    else:
        st.session_state.selected_units.append(unit)


# A Streamlit button is used for each tile so the artwork itself is the control,
# while CSS supplies the image, hover feedback, selected outline, and checkmark.
tile_image_css = []
for unit, filename in unit_images.items():
    img_base64 = get_image_as_base64(os.path.join(image_folder, filename))
    tile_image_css.append(
        f"[class*='st-key-unit_tile_{unit_key(unit)}'] button {{ "
        f"background-image: url('data:image/jpeg;base64,{img_base64}'); }} "
        f"[class*='st-key-unit_tile_{unit_key(unit)}'] button::before {{ "
        f"content: '{unit}'; }}"
    )

st.markdown(
    """
    <style>
    /* Keyed containers let native Streamlit widgets participate in a CSS Grid. */
    [class*="st-key-unit_picker_grid"],
    [class*="st-key-tier_grid_"] {
        display: grid !important;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: .5rem;
        width: 100%;
    }
    [class*="st-key-unit_picker_grid"] > [data-testid="stElementContainer"],
    [class*="st-key-tier_grid_"] > [data-testid="stElementContainer"] {
        min-width: 0;
        width: 100%;
        margin: 0 !important;
    }
    @media (min-width: 641px) {
        [class*="st-key-unit_picker_grid"],
        [class*="st-key-tier_grid_"] {
            grid-template-columns: repeat(8, minmax(0, 1fr));
        }
    }
    @media (min-width: 1200px) {
        [class*="st-key-unit_picker_grid"],
        [class*="st-key-tier_grid_"] {
            grid-template-columns: repeat(14, minmax(0, 1fr));
        }
    }
    [class*="st-key-unit_tile_"] button {
        position: relative;
        box-sizing: border-box;
        width: 100%;
        aspect-ratio: 248 / 378;
        min-height: 0;
        padding: clamp(.35rem, 1.2vw, .7rem);
        border: 0;
        border-radius: 12px;
        background-color: transparent;
        background-position: center;
        background-repeat: no-repeat;
        background-size: cover;
        box-shadow: none;
        color: white;
        font-size: clamp(.65rem, 1vw, .95rem);
        font-weight: 700;
        text-align: left;
        text-shadow: none;
        transition: transform 140ms ease, filter 140ms ease, box-shadow 140ms ease, border-color 140ms ease;
    }
    [class*="st-key-unit_tile_"] button [data-testid="stMarkdownContainer"] {
        visibility: hidden;
    }
    [class*="st-key-unit_tile_"] button::before {
        position: absolute;
        z-index: 2;
        top: 50%;
        left: 50%;
        width: fit-content;
        max-width: calc(100% - 16px);
        padding: clamp(.45rem, 1vw, .85rem) clamp(.65rem, 1.5vw, 1.35rem);
        border-radius: 50%;
        background: radial-gradient(ellipse at center, rgba(0, 0, 0, .72) 0%, rgba(0, 0, 0, .42) 28%, rgba(0, 0, 0, 0) 70%);
        color: #fff;
        font-size: clamp(.65rem, 1vw, .95rem);
        font-weight: 400;
        line-height: 1.2;
        text-align: center;
        text-shadow: none;
        transform: translate(-50%, -50%);
        pointer-events: none;
    }
    [class*="st-key-unit_tile_"] button:hover {
        filter: brightness(1.15);
        transform: scale(1.035);
        box-shadow: none;
        z-index: 1;
    }
    [class*="_selected"] button {
        border: clamp(2px, .35vw, 5px) solid #000;
        filter: brightness(.84);
        box-shadow: none;
    }
    [class*="_selected"] button:hover {
        filter: brightness(.98);
    }
    [class*="_selected"] button::after {
        content: "✓";
        position: absolute;
        z-index: 3;
        top: clamp(3px, .55vw, 8px);
        right: clamp(3px, .6vw, 9px);
        display: grid;
        place-items: center;
        width: clamp(16px, 2vw, 27px);
        height: clamp(16px, 2vw, 27px);
        border-radius: 50%;
        background: #000;
        color: #fff;
        font-size: clamp(11px, 1.4vw, 19px);
        font-weight: 900;
        line-height: 1;
        text-shadow: none;
        box-shadow: none;
    }
    .result-card {
        min-width: 0;
        text-align: center;
    }
    .result-card img {
        display: block;
        width: 100%;
        aspect-ratio: 248 / 378;
        border-radius: 10px;
        object-fit: cover;
    }
    .result-card p {
        margin: .25rem 0 0;
        font-size: clamp(.65rem, 1vw, .95rem);
        overflow-wrap: anywhere;
    }
    """ + "\n".join(tile_image_css) + "</style>",
    unsafe_allow_html=True,
)

# Each item stays in its own native container, while the parent CSS Grid
# controls wrapping and the number of columns at each viewport width.
with st.container(key="unit_picker_grid"):
    for unit in unit_images:
        key = unit_key(unit)
        selected = unit in st.session_state.selected_units
        with st.container(key=f"unit_tile_{key}{'_selected' if selected else ''}"):
            st.button(
                unit,
                key=f"unit_button_{key}",
                use_container_width=True,
                on_click=toggle_unit,
                args=(unit,),
            )

            # Add a weight slider below each selected unit (range 1 to 5).
            if show_sliders and selected:
                st.session_state.weights[unit] = st.slider(
                    " ",
                    key=f"slider:{unit}",
                    min_value=1,
                    max_value=5,
                    value=st.session_state.weights[unit],
                )

# Display the output: sorted list of selected units
#st.write("Selected Units:")
#st.write(sorted(st.session_state.selected_units))

S = 5 # unit wins, >95% HP left with nearly no damage
A = 4 # unit wins, 60-95% HP left
B = 3 # unit wins, 10-60% HP left
C = 2 # unit wins, <10% HP left
D = 1 # unit loose, Opponent is damaged
E = 0 # unit loose, Opponent >95% HP
unit_matrix = {
    "Crawler":      [C, B, D, A, A, E, E, A, D, A, A, E, E, D, B, D, A, E, C, E, A, A, D, E, E, D, E, D, E, D, D],
    "Fang":         [D, C, D, C, A, E, B, D, D, C, E, A, B, D, D, D, A, E, D, E, C, B, D, B, B, D, D, D, E, E, D],
    "Hound":        [A, A, C, D, D, D, E, C, D, D, B, E, E, D, C, D, D, E, D, D, D, C, D, E, E, D, E, D, D, D, D],
    "Void Eye":     [D, D, A, C, D, D, E, C, B, D, B, E, E, B, C, C, A, E, C, D, D, B, D, E, E, D, E, D, A, C, C],
    "Marksman":     [D, D, B, B, C, S, D, D, D, D, D, S, D, B, D, D, S, A, C, B, D, D, D, D, A, D, D, D, A, C, D],
    "Arclight":     [S, S, B, C, E, C, E, A, D, D, E, E, E, D, D, D, D, E, E, D, E, E, D, E, E, E, E, D, D, D, D],
    "Wasp":         [S, D, S, D, C, S, C, D, S, S, S, B, D, S, S, A, S, E, S, S, S, B, S, B, B, A, D, A, S, D, D],
    "Mustang":      [D, B, D, D, B, D, B, C, E, E, D, A, C, D, D, D, B, D, D, E, D, D, D, B, B, D, D, B, D, D, D],
    "Sledgehammer": [A, A, B, D, C, A, E, S, C, D, B, E, E, D, D, D, B, E, E, D, E, D, D, E, E, E, E, D, D, B, D],
    "Steelballs":   [D, D, B, B, B, A, E, A, B, C, A, E, E, B, C, A, E, E, D, B, C, B, D, E, E, D, E, B, B, A, C],
    "Stormcaller":  [D, S, D, D, B, S, E, C, D, D, C, E, E, B, B, E, S, E, S, A, B, A, E, E, E, D, E, C, D, A, D],
    "Phoenix":      [S, E, S, S, D, S, D, D, S, A, S, C, D, S, S, S, S, A, S, S, S, D, S, D, B, A, D, S, S, B, D],
    "Phantom Ray":  [A, D, S, S, C, S, C, D, S, S, S, C, C, S, S, S, S, A, S, S, S, D, S, D, C, A, D, S, S, B, D],
    "Tarantula":    [A, A, B, D, D, B, E, B, B, D, D, E, E, C, D, D, C, E, D, B, D, D, D, E, E, D, E, D, B, A, C],
    "Sabertooth":   [D, C, D, D, C, A, E, B, B, D, D, E, E, A, C, B, A, E, B, A, D, D, D, E, E, D, E, D, A, A, A],
    "Rhino":        [C, C, B, D, C, A, E, B, B, D, S, E, E, B, D, C, A, E, A, A, D, E, D, E, E, E, E, D, A, A, A],
    "Hacker": 		[D, E, C, D, E, B, E, D, D, S, E, E, E, D, D, D, C, E, D, D, E, D, D, E, E, E, E, D, A, A, D],
    "Wraith": 	    [S, B, S, S, D, S, S, B, S, A, S, D, D, A, A, A, S, C, A, A, A, E, A, D, D, A, D, A, S, D, D],
    "Scorpion":     [D, A, A, D, D, A, E, A, A, S, D, E, E, B, D, D, A, E, C, S, D, D, D, E, E, D, E, D, S, S, B],
    "Vulcan": 	    [S, S, A, B, D, B, E, S, B, D, D, E, E, D, D, D, C, E, D, C, D, D, D, E, E, D, E, D, A, B, D],
    "Fortress":     [D, D, C, C, B, S, E, C, A, D, D, E, E, A, C, A, S, E, B, A, C, E, D, E, E, D, E, D, S, A, A],
    "Melting Point":[D, D, D, D, C, A, D, C, B, D, D, B, B, A, B, S, S, S, A, S, S, C, B, A, B, B, B, B, A, A, A],
    "Sandworm":     [B, B, B, B, S, S, E, B, A, D, S, E, E, B, B, C, A, E, B, A, C, D, C, E, E, D, E, D, S, A, A],
    "Raiden":       [S, D, S, S, C, S, D, D, S, S, S, A, A, S, S, S, S, S, S, S, S, D, B, C, D, S, D, A, S, A, B],
    "Overlord":     [S, D, S, S, D, S, D, D, S, S, S, D, D, S, S, S, S, S, S, S, S, D, S, B, C, S, D, S, S, A, A],
    "War Factory":  [B, A, A, B, A, S, E, A, S, A, B, E, E, S, A, A, D, E, A, S, B, D, A, E, E, C, E, D, S, A, A],
    "Abyss":        [S, A, S, S, B, S, B, C, S, S, S, A, B, S, S, S, S, S, S, S, S, D, A, A, B, S, C, S, S, A, D],
    "Mountain":     [C, A, A, B, B, S, E, B, A, D, D, E, E, A, B, B, D, E, B, A, B, D, B, E, E, B, D, C, S, A, C],
    "Fire Badger":  [S, S, B, D, D, B, E, A, C, D, A, E, E, D, D, D, D, E, E, D, E, D, D, E, E, E, E, E, C, B, D],
    "Typhoon":      [A, S, B, D, D, C, S, B, D, D, D, D, D, B, D, E, D, C, E, D, D, D, D, D, D, D, D, C, D, C, D],
    "Farseer":      [C, A, A, D, C, A, A, B, B, D, D, C, C, D, D, D, B, A, D, B, D, D, D, D, D, D, C, D, B, C, C]
}
# add individual units with tech. <Unit Name>: <Tech Name>
unit_overrides = {
    "Crawler: Acid": {"War Factory": B, "Sandworm": B, "Mountain": B},
    "Fang: Rage": {"Stormcaller": C},
    "Fang: Ignite": {"Fortress": A, "Melting Point": A, "Sandworm": B, "Raiden": A, "Overlord": A, "War Factory": A, "Mountain": B},
    "Void Eye: Aerial Mod": {"Wasp": A, "Phoenix": B, "Phantom Ray": C,"Wrath": A, "Raiden": C, "Overlord": B,},
    "Marksman: Aerial Spec": {"Raiden": S},
    "Arclight: Anti-Air": {"Wasp": S, "Wraith": D},
    "Arclight: Charged-Shot": {"Sledgehammer": B, "Steelballs": A, "Rhino": C, "Vulcan": B},
    "Wasp: Aerial Spec": {"Overlord": A},
    "Wasp: Mod?": {"Wrath": C},
    "Mustang: Anti-Air": {"Phantom Ray": B, "Wraith": B, "Overlord": A, "Abyss": B},
    "Mustang: Missile": {"Stormcaller": B, "Phantom Ray": A, "Farseer": A},
    "Mustang: Range": {"Farseer": A},
    "Mustang: Map Pos": {"Stormcaller": D, "Abyss": D},
    "Sledgehammer: Armor-Piercing": {"Rhino": B},
    "Sledgehammer: Range": {"Vulcan": C},
    "Sledgehammer: Armor-Enchacment": {"Tarantula": C, "Vulcan": C, "Fire Badger": S},
    "Steelballs: Range": {"Hacker": B, "War Factory": C},
    "Steelballs: Armor": {"Crawler": B, "Fang": A},
    "Steelballs: Mechanical Div": {"Scorpion": B},
    "Steelballs: Map Pos": {"Marksman": C},
    "Stormcaller: Map Pos": {"Mustang": D, "Farseer": B},
    "Phoenix: Range": {"Farseer": C},
    "Phoenix: Map Pos": {"Overlord": C},
    "Phantom Ray: Armor": {"Fang": S, "Mustang": A},
    "Phantom Ray: Mod?": {"Farseer": D},
    "Tarantula: Anti-Air": {"Wasp": A, "Phoenix": D, "Phantom Ray": C, "Wraith": A},
    "Sabertooth: Secondary Armament": {"Hound": A, "Void Eye": B},
    "Sabertooth: Double SHot": {"Fortress": B, "Melting Point": A, "Sandworm": B},
    "Rhino: Whirlwind": {"Steelballs": B},
    "Rhino: Mod?": {"Steelballs": B},
    "Rhino: +UnitCover": {"Hacker": A},
    "Hacker: Range": {"Tarantula": C, "Vulcan": A},
    "Hacker: +UnitCover": {"Rhino": A},
    "Wraith: Shield + Repair ?": {"Typhoon": A},
    "Scorpion: Range+Siege": {"Stormcaller": A},
    "Scorpion: Doubleshot+Range+Siege+Acid": {"Fortress": B, "Melting Point": B},
    "Scorpion: Acid": {"Mountain": C},  
    "Fortress: Rocket Punch": {"Crawler": C, "Fang": B, "Steelballs": B, "Stormcaller": B, "Sandworm" :C},
    "Fortress: Anti-Air": {"Wasp": B,},
    "Fortress: Fang Prod": {"Steelballs": A, "Sandworm": C},
    "Melting Point: Energy-Diff": {"Fang": B, "Void Eye": C, "Wasp": B, "Mustang": B, "Sledgehammer": A},
    "Sandworm: Anti-Aerial": {"Wasp": B, "Phoenix": A, "Phantom Ray": C, "Wraith": A, "Raiden": A, "Overlord": C},
    "Overlord: Mothership": {"Phoenix": A},
    "Overlord: Armor Enchancement": {"Fang": S, "Mustang": A},
    "Abyss: Map Position": {"Phoenix": B},
    "Mountain: Antu Aircraft": {"Wasp": B, "Phoenix": B, "Phantom Ray": B, "Wraith": A, "Raiden": A, "Overlord": A},
    "Typhoon: Aerial Spec": {"Phantom Ray": A,"Overlord": C},
    "Farseer: Missile": {"Stormcaller": B, "Phantom Ray": A, "Overlord": B},
    "Farseer: Map Position": {"Stormcaller": C},
}

UNITS = list(unit_matrix.keys())
UNITS_TECH = list(unit_overrides.keys())


# Function to calculate the counter score
def get_counter_score(selected_units, unit_matrix, weights):
    all_units = UNITS + UNITS_TECH
    scores = {unit: 0 for unit in all_units}
    div = {unit: 0 for unit in all_units}

    for selected in selected_units:
        for unit, counters in unit_matrix.items():
            index = UNITS.index(selected)
            scores[unit] += counters[index] * weights[selected]
            div[unit] += weights[selected]
        for unit, counters in unit_overrides.items():
            if selected in counters:
                scores[unit] += counters[selected] * weights[selected]
                div[unit] += weights[selected]

    if (len(selected_units) > 0):
        scores = {k: scores[k] / div[k] if scores[k]>0 else 0 for k in scores.keys()}
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


selected_units = st.session_state.selected_units
# Normalize the weights to make their sum equal to 1
raw_weights = st.session_state.weights
total_weight = sum(raw_weights.values())
weights = {unit: weight / total_weight for unit, weight in raw_weights.items()}
best_counters = get_counter_score(selected_units, unit_matrix, weights)


#
# output code
#
# Display the best counter units
#st.write("Best Counter Units:")
#for unit, score in best_counters:
#    st.write(f"{unit}: {score}")

# Function to classify units into tiers based on score
def classify_by_tier(best_counters):
    tier_bins = {
        "S Tier (4-5 points)": [],
        "A Tier (3-4 points)": [],
        "B Tier (2-3 points)": [],
        "C Tier (1-2 points)": [],
        "D/E Tier (0-1 point)": []
    }

    for unit, score in best_counters:
        if 4 < score <= 5:
            tier_bins["S Tier (4-5 points)"].append(unit)
        elif 3 < score <= 4:
            tier_bins["A Tier (3-4 points)"].append(unit)
        elif 2 < score <= 3:
            tier_bins["B Tier (2-3 points)"].append(unit)
        elif 1 < score <= 2:
            tier_bins["C Tier (1-2 points)"].append(unit)
        else:
            tier_bins["D/E Tier (0-1 point)"].append(unit)

    return tier_bins

# Example usage
best_counters = get_counter_score(selected_units, unit_matrix, weights)
tiered_counters = classify_by_tier(best_counters)




# Display the best counter units in matrix format
st.write("Best Counter Units by Tier:")
for tier, units in tiered_counters.items():
    if units:  # Only display populated tiers.
        st.markdown(f"**{tier}**")
        with st.container(key=f"tier_grid_{unit_key(tier)}"):
            for unit in units:
                # Check for base unit and tech name.
                if ":" in unit:
                    base_unit, tech_name = unit.split(":", 1)
                    base_unit = base_unit.strip()
                    tech_name = tech_name.strip()
                else:
                    base_unit = unit
                    tech_name = None

                img_path = os.path.join(image_folder, unit_images[base_unit])
                img_base64 = get_image_as_base64(img_path)
                tech_label = f"<p><b>{tech_name}</b></p>" if tech_name else ""

                st.markdown(
                    f"""
                    <div class="result-card">
                        <img src="data:image/jpeg;base64,{img_base64}" alt="{base_unit}">
                        {tech_label}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

