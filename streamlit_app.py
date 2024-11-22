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
    "Marksman": "marksman.jpg",
    "Arclight": "arclight.jpg",
    "Wasp": "wasp.jpg",
    "Mustang": "mustang.jpg",
    "Sledgehammer": "sledgehammer.jpg",
    "Steelballs": "steelball.jpg",
    "Stormcaller": "stormcaller.jpg",
    "Phoenix": "phoenix.jpg",
    "Rhino": "rhino.jpg",
    "Hacker": "hacker.jpg",
    "Wraith": "wraith.jpg",
    "Scorpion": "scorpion.jpg",
    "Vulcan": "vulcan.jpg",
    "Fortress": "fortress.jpg",
    "Melting Point": "melting_point.jpg",
    "Overlord": "overlord.jpg",
    "Sandworm": "sandworm.jpg",
    "War Factory": "war_factory.jpg",
    "Fire Badger": "fire_badger.jpg",
    "Typhoon": "typhoon.jpg",
    "Sabertooth": "sabertooth.jpg",
    "Tarantula": "tarantula.jpg", 
    "Farseer": "farseer.jpg",
    "Phantom Ray": "phantom_ray.jpg"
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


cols_per_row = 13  # 12 items per row
cols_per_row_output = 16

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
show_sliders = st.checkbox("Show Weight Sliders")
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
    "Crawler":      [C, B, A, E, E, A, D, A, A, E, D, A, E, C, E, A, A, E, D, D, E, D, B, E, C, E],
    "Fang":         [D, C, A, B, D, E, C, E, A, D, A, E, E, E, C, B, C, D, D, D, E, E, D, D, D, A],
    "Marksman":     [D, D, C, S, D, D, D, D, D, A, D, S, A, C, B, D, D, A, D, D, A, C, D, B, C, D],
    "Arclight":     [S, S, E, C, S, S, D, D, E, E, E, E, E, E, D, E, E, E, D, E, D, D, D, D, E, E],
    "Wasp":         [S, D, C, S, C, D, S, S, S, B, A, S, E, A, A, A, B, C, S, A, S, D, S, S, E, B],
    "Mustang":      [D, B, B, E, B, C, E, E, C, A, D, B, D, D, E, D, D, C, D, D, D, D, D, D, D, B],
    "Sledgehammer": [A, S, C, A, E, S, C, D, B, E, D, B, E, E, D, E, D, E, D, E, D, B, D, D, D, E],
    "Steelballs":   [D, D, B, A, E, A, B, C, A, E, A, E, E, D, B, C, B, E, D, D, B, A, D, A, B, E],
    "Stormcaller":  [D, S, B, S, E, D, D, D, C, E, E, S, E, S, A, B, A, E, E, D, D, A, B, A, B, E],
    "Phoenix":      [S, E, D, S, D, D, S, A, S, C, S, S, A, S, S, S, D, B, S, A, S, B, S, S, D, D],
    "Rhino":        [C, C, C, S, E, B, B, D, S, E, C, A, E, A, A, D, E, E, D, E, A, A, D, D, A, E],
    "Hacker": 		[D, E, E, S, E, D, D, S, E, E, D, C, E, D, D, E, D, E, D, E, A, A, D, S, E, E],
    "Wraith": 	    [S, B, D, S, S, B, A, A, S, D, A, S, C, A, A, A, E, E, A, A, A, D, A, S, D, D],
    "Scorpion":     [D, S, D, A, E, A, A, S, D, E, D, A, E, C, S, D, D, E, D, D, S, S, D, A, B, E],
    "Vulcan": 	    [S, S, D, B, E, S, B, D, D, E, D, C, E, D, C, D, D, E, D, D, A, B, D, B, C, E],
    "Fortress":     [D, D, B, S, E, C, A, D, D, E, A, S, E, B, A, C, E, E, D, D, S, A, C, S, A, E],
    "Melting Point":[D, D, C, A, D, C, B, D, D, B, S, S, S, A, S, S, C, B, B, B, A, A, B, S, A, A],
    "Overlord":     [S, D, D, S, D, D, S, S, C, D, S, S, A, S, S, S, D, C, S, A, S, B, S, S, A, S],
    "Sandworm":     [B, B, S, S, E, B, A, D, S, E, C, A, E, B, A, C, D, E, C, D, S, A, B, A, S, E],
    "War Factory":  [B, A, A, S, E, A, S, A, B, E, A, D, E, A, S, B, D, E, A, C, S, A, A, S, S, E],
    "Fire Badger":  [S, S, D, B, E, A, C, D, A, E, D, D, E, E, D, E, D, E, D, E, C, B, D, D, D, E],
    "Typhoon":      [A, S, D, C, S, B, D, D, D, D, E, D, C, E, D, D, D, D, D, D, D, C, D, D, D, B],
    "Sabertooth":   [D, C, C, A, E, B, B, A, D, E, B, A, E, B, A, D, D, E, D, D, A, D, C, E, E, E],
    "Tarantula":    [S, A, D, B, E, B, B, D, D, E, B, E, E, D, D, E, E, E, D, E, B, A, S, C, D, E],
    "Farseer":      [B, A, D, A, S, B, C, D, D, C, D, S, B, D, C, E, E, D, E, E, A, B, S, C, C, S],
                   #[C, A, D, A, A, B, B, D, D, C, C, D, B, A, D, B, D, D, D, D, D, B, C, D, C] # from internet guide
    "Phantom Ray":  [S, D, B, S, D, D, S, S, S, B, S, S, C, S, S, S, D, E, S, S, S, D, S, S, E, C]
}


# Function to calculate the counter score
def get_counter_score(selected_units, unit_matrix, weights):
    scores = {unit: 0 for unit in unit_matrix.keys()}
    
    for selected in selected_units:
        for unit, counters in unit_matrix.items():
            index = list(unit_matrix.keys()).index(selected)
            score = counters[index]
            scores[unit] += score * weights[selected]
    
    if (len(selected_units) > 0):
        divider = sum([weights[s] for s in selected_units])
        scores = {k: scores[k] / divider for k in scores.keys()}
    # Sort by the highest total score and return the sorted list
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
        if 4 <= score <= 5:
            tier_bins["S Tier (4-5 points)"].append(unit)
        elif 3 <= score < 4:
            tier_bins["A Tier (3-4 points)"].append(unit)
        elif 2 <= score < 3:
            tier_bins["B Tier (2-3 points)"].append(unit)
        elif 1 <= score < 2:
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
            # Get the image path and render the image
            img_path = os.path.join(image_folder, unit_images[unit])
            img_base64 = get_image_as_base64(img_path)
            with cols[idx % cols_per_row_output]:
                # Display the image
                st.markdown(
                    f"""
                    <div style="text-align: center;">
                        <img src="data:image/jpeg;base64,{img_base64}" style="width:100%; border-radius: 10px;">
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                #<p>{unit}</p>

