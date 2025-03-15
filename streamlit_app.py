import streamlit as st
import os
from PIL import Image
import base64


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


#cols_per_row = 13  # 12 items per row
#cols_per_row_output = 16
# make it configurable for different screens
cols_per_row = st.sidebar.slider(
    "Select the number of columns per row:",
    min_value=2,
    max_value=24,
    value=13,  # Default value
    step=1
)
cols_per_row_output = st.sidebar.slider(
    "Select the number of columns per row for output:",
    min_value=5,
    max_value=24,
    value=16, # Default value
    step=1
)
show_sliders = st.sidebar.checkbox("Show Weight Sliders")

#
# db
#
# Initialize session state to track selected units (checkboxes)
if 'selected_units' not in st.session_state:
    st.session_state.selected_units = []
if 'weights' not in st.session_state:
    st.session_state.weights = {unit: 1 for unit in unit_images.keys()}



# Helper function to convert image to base64
def get_image_as_base64(img_path):
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Create a list to keep track of unit names and images in a grid
unit_list = list(unit_images.keys())
num_units = len(unit_list)
# Loop through the units and create the grid layout
for i in range(0, num_units, cols_per_row):
    cols = st.columns(cols_per_row)
    for j, unit in enumerate(unit_list[i:i+cols_per_row]):
        with cols[j]:
            #c = st.container()

            # Add or remove the unit from the selected_units list based on the checkbox state
            if st.checkbox(f" ", key=f"checkbox:{unit}", value=(unit in st.session_state.selected_units)):
                if unit not in st.session_state.selected_units:
                    st.session_state.selected_units.append(unit)
            else:
                if unit in st.session_state.selected_units:
                    st.session_state.selected_units.remove(unit)

            # Determine the border based on the updated state
            if unit in st.session_state.selected_units:
                border_style = "border: 3px solid black;"
            else:
                border_style = "border: 3px solid transparent;"  # Invisible border for layout consistency

            # Render the image with the correct border style AFTER the checkbox state is determined
            img_path = os.path.join(image_folder, unit_images[unit])
            img_base64 = get_image_as_base64(img_path)

            # Display the image first with the appropriate border
            st.markdown(
                f"""
                <div style="text-align: center;">
                    <img src="data:image/jpeg;base64,{img_base64}" style="width:100%; {border_style} border-radius: 10px;">
                    <p>{unit}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            # Add a weight slider below each unit (range 1 to 5)
            if show_sliders and unit in st.session_state.selected_units:
                st.session_state.weights[unit] = st.slider(f" ", key=f"slider:{unit}", min_value=1, max_value=5, value=st.session_state.weights[unit])

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
    "Crawler":      [C, B, D, A, E, E, A, D, A, A, E, E, D, B, D, A, E, C, E, A, A, D, E, E, D, E, D, D],
    "Fang":         [D, C, D, A, E, B, D, E, C, E, A, B, D, D, D, A, E, E, E, C, B, D, B, B, D, E, E, D],
    "Hound":        [A, A, C, D, D, E, C, D, D, B, E, E, D, C, D, D, E, D, D, D, C, D, E, E, D, D, D, D],
    "Marksman":     [D, D, B, C, S, D, D, D, D, D, A, D, B, D, D, S, A, C, B, D, D, D, D, A, D, A, C, D],
    "Arclight":     [S, S, B, E, C, E, S, D, D, E, E, E, D, D, E, E, E, E, D, E, E, D, E, E, E, D, D, D],
    "Wasp":         [S, D, S, C, S, C, D, S, S, S, B, D, S, S, A, S, E, A, A, A, B, S, B, B, A, S, D, D],
    "Mustang":      [D, B, D, B, E, B, C, E, E, D, A, C, D, D, D, B, D, D, E, D, D, D, B, B, D, D, D, D],
    "Sledgehammer": [A, S, B, C, A, E, S, C, D, B, E, E, D, D, D, B, E, E, D, E, D, D, E, E, E, D, B, D],
    "Steelballs":   [D, D, B, C, A, E, A, B, C, A, E, E, B, D, A, E, E, D, B, C, B, D, E, E, D, B, A, C],
    "Stormcaller":  [D, S, D, B, S, E, D, D, D, C, E, E, B, B, E, S, E, S, A, B, A, E, E, E, D, D, A, D],
    "Phoenix":      [S, E, S, D, S, D, D, S, A, S, C, S, S, S, S, S, A, S, S, S, D, S, D, C, A, S, B, D],
    "Phantom Ray":  [A, D, S, C, S, C, D, S, S, S, C, C, S, S, S, S, A, S, S, S, D, S, D, C, A, S, B, D],
    "Tarantula":    [A, A, B, D, B, E, B, B, D, D, E, E, C, D, D, C, E, D, B, D, D, D, E, E, D, B, A, D],
    "Sabertooth":   [D, C, D, C, A, E, B, B, A, D, E, E, A, C, B, A, E, B, A, D, D, D, E, E, D, A, A, A],
    "Rhino":        [C, C, B, C, S, E, B, B, D, S, E, E, B, D, C, A, E, A, A, D, E, D, E, E, E, A, A, A],
    "Hacker": 		[D, E, C, E, S, E, D, D, S, E, E, E, D, D, D, C, E, D, D, E, D, D, E, E, E, A, A, D],
    "Wraith": 	    [S, B, S, D, S, S, B, A, A, S, D, D, A, A, A, S, C, A, A, A, E, A, D, D, A, S, D, D],
    "Scorpion":     [D, S, A, D, A, E, A, A, S, D, E, E, B, D, D, A, E, C, S, D, D, D, E, E, D, S, S, B],
    "Vulcan": 	    [S, S, A, D, B, E, S, B, D, D, E, E, D, D, D, C, E, D, C, D, D, D, E, E, D, A, B, D],
    "Fortress":     [D, D, C, B, S, E, C, A, D, D, E, E, A, C, A, S, E, B, A, C, E, D, D, E, D, S, A, A],
    "Melting Point":[D, D, D, C, A, D, C, A, D, D, B, B, A, B, S, S, S, A, S, S, C, B, A, B, B, A, A, A],
    "Sandworm":     [B, B, B, S, S, E, B, A, D, S, E, E, B, B, C, A, E, B, A, C, D, C, E, E, D, S, A, A],
    "Raiden":       [S, D, S, C, S, D, D, S, S, S, A, A, S, S, S, S, S, S, S, S, D, B, C, D, S, S, A, B],
    "Overlord":     [S, D, S, D, S, D, D, S, S, S, D, D, S, S, S, S, S, S, S, S, D, S, B, C, S, S, A, A],
    "War Factory":  [B, A, A, A, S, E, A, S, A, B, E, E, S, A, A, D, E, A, S, B, D, A, E, E, C, S, A, A],
    "Fire Badger":  [S, S, B, D, B, E, A, C, D, A, E, E, D, D, D, D, E, E, D, E, D, D, E, E, E, C, B, D],
    "Typhoon":      [A, S, B, D, C, S, B, D, D, D, D, D, B, D, E, D, C, E, D, D, D, D, D, D, D, D, C, D],
    "Farseer":      [C, A, A, D, A, A, B, B, D, C, C, C, C, D, D, B, A, D, B, D, D, D, D, D, D, B, C, C]
}
# add individual units with tech. <Unit Name>: <Tech Name>
unit_overrides = {
    "Crawler: Acid": {"War Factory": B, "Sandworm": B},
    "Fang: Rage": {"Stormcaller": C},
    "Fang: Ignite": {"Fortress": A, "Melting Point": A, "Sandworm": B, "Raiden": A, "Overlord": A, "War Factory": A},
    "Marksman: Anti-Air": {"Phantom Ray": S, "Wrait": S, "Phoenix": S, "Overlord": S, "Raiden": S},
    "Arclight: Anti-Air": {"Wasp": S, "Wrait": D},
    "Arclight: Charged-Shot": {"Sledgehammer": B, "Steelballs": A, "Rhino": C, "Vulcan": B},
    "Wasp: Anti-Air": {"Overlord": A},
    "Mustang: Anti-Air": {"Phantom Ray": A, "Wrait": B, "Overlord": A},
    "Mustang: Missile": {"Stormcaller": B, "Phantom Ray": A, "Farseer": A},
    "Mustang: Range": {"Farseer": A},
    "Sledgehammer: Armor-Piercing": {"Rhino": B},
    "Sledgehammer: Range": {"Vulcan": C},
    "Steelballs: Range": {"War Factory": C},
    "Phoenix: Range": {"Farseer": C},
    "Phantom Ray: Armor": {"Mustang": A},
    "Tarantula: Anti-Air": {"Wasp": S, "Phoenix": D, "Phantom Ray": C, "Wrait": A},
    "Rhino: Whirlwind": {"Steelballs": B},
    "Hacker: Range": {"Tarantula": C, "Vulcan": A},
    "Rhino: Field-Main": {"Typhoon": A},
    "Scorpion: Range+Siege": {"Stormcaller": A},
    "Scorpion: Doubleshot+Range+Siege+Acid": {"Fortress": B, "Melting Point": B},
    "Fortress: Anti-Air": {"Wasp": B},
    "Fortress: Fang": {"Steelballs": A, "Sandworm": C},
    "Melting Point: Energy-Diff": {"Fang": B, "Wasp": B, "Mustang": B, "Sledgehammer": A},
    "Sandworm: Anti-Air": {"Wasp": B, "Phoenix": A, "Phantom Ray": C, "Wrait": A, "Raiden": A, "Overlord": C},
    "Overlord: Mothership": {"Phoenix": A, "Overlord": C},
    "Typhoon: Anti-Air": {"Phantom Ray": A, },
    "Farseer: Missile": {"Stormcaller": B, "Phantom Ray": A, "Overlord": B},
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
    st.markdown(f"**{tier}**")
    if units:  # Only display if there are units in the tier
        cols = st.columns(cols_per_row_output)
        for idx, unit in enumerate(units):
            # Check for base unit and tech name
            if ":" in unit:
                base_unit, tech_name = unit.split(":", 1)
                base_unit = base_unit.strip()
                tech_name = tech_name.strip()
            else:
                base_unit = unit
                tech_name = None

            img_path = os.path.join(image_folder, unit_images[base_unit])
            img_base64 = get_image_as_base64(img_path)


            with cols[idx % cols_per_row_output]:
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <img src="data:image/jpeg;base64,{img_base64}" style="width:100%; border-radius: 10px;">
                        <p><b>{tech_name if tech_name else ""}</b></p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

