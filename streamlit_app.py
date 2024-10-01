import streamlit as st
import os
from PIL import Image
import base64

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
    "Sabertooth": "sabertooth.jpg"
}


st.set_page_config(
    layout = 'wide',
    page_title = 'Mechabellum Unit Counters'
)

st.write("""
    <style>
    /* Center-align and enlarge the checkbox */
    [data-baseweb="checkbox"] {
        display: flex;
        justify-content: center;
        align-items: center;  /* Align vertically */
        transform: scale(1.5);  /* Enlarge the checkbox */
    }
    </style>
    """, unsafe_allow_html=True)





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
cols_per_row = 12  # 10 items per row

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

S = 5
A = 4
B = 3
C = 2
D = 1
E = 0
unit_matrix = {
    "Crawler":      [0, B, A, E, E, A, D, A, A, E, D, A, E, C, E, A, A, E, D, D, E, D, B],
    "Fang":         [D, 0, A, B, D, E, C, E, A, D, A, E, E, E, C, B, C, D, D, D, E, E, D],
    "Marksman":     [D, D, 0, S, D, D, D, D, D, A, D, S, A, C, B, D, D, A, D, D, A, C, D],
    "Arclight":     [S, S, E, 0, S, S, D, D, E, E, E, E, E, E, D, E, E, E, D, E, D, D, D],
    "Wasp":         [S, D, C, S, 0, D, S, S, S, B, A, S, E, A, A, A, B, C, S, A, S, D, S],
    "Mustang":      [D, B, B, E, B, 0, E, E, C, A, D, B, D, D, E, D, D, C, D, D, D, D, D],
    "Sledgehammer": [A, S, C, A, E, S, 0, D, B, E, D, B, E, E, D, E, D, E, D, E, D, B, D],
    "Steelballs":   [D, D, B, A, E, A, B, 0, A, E, A, E, E, D, B, C, B, E, D, D, B, A, D],
    "Stormcaller":  [D, S, B, S, E, D, D, D, 0, E, E, S, E, S, A, B, A, E, E, D, D, A, B],
    "Phoenix":      [S, E, D, S, D, D, S, A, S, 0, S, S, A, S, S, S, D, B, S, A, S, B, S],
    "Rhino":        [C, C, C, S, E, B, B, D, S, E, 0, A, E, A, A, D, E, E, D, E, A, A, D],
    "Hacker": 		[D, E, E, S, E, D, D, S, E, E, D, 0, E, D, D, E, D, E, D, E, A, A, D],
    "Wraith": 	    [S, B, D, S, S, B, A, A, S, D, A, S, 0, A, A, A, E, E, A, A, A, D, A],
    "Scorpion":     [D, S, D, A, E, A, A, S, D, E, D, A, E, 0, S, D, D, E, D, D, S, S, D],
    "Vulcan": 	    [S, S, D, B, E, S, B, D, D, E, D, C, E, D, 0, D, D, E, D, D, A, B, D],
    "Fortress":     [D, D, B, S, E, C, A, D, D, E, A, S, E, B, A, 0, E, E, D, D, S, A, C],
    "Melting Point":[D, D, C, A, D, C, B, D, D, B, S, S, S, A, S, S, 0, B, B, B, A, A, B],
    "Overlord":     [S, D, D, S, D, D, S, S, C, D, S, S, A, S, S, S, D, 0, S, A, S, B, S],
    "Sandworm":     [B, B, S, S, E, B, A, D, S, E, C, A, E, B, A, C, D, E, 0, D, S, A, B],
    "War Factory":  [B, A, A, S, E, A, S, A, B, E, A, D, E, A, S, B, D, E, A, 0, S, A, A],
    "Fire Badger":  [S, S, D, B, E, A, C, D, A, E, D, D, E, E, D, E, D, E, D, E, 0, B, D],
    "Typhoon":      [A, S, D, C, S, B, D, D, D, D, E, D, C, E, D, D, D, D, D, D, D, 0, D],
    "Sabertooth":   [D, C, C, A, E, B, B, A, D, E, B, A, E, B, A, D, D, E, D, D, A, D, 0],
}


# Function to calculate the counter score
def get_counter_score(selected_units, unit_matrix, weights):
    scores = {unit: 0 for unit in unit_matrix.keys()}
    
    for selected in selected_units:
        for unit, counters in unit_matrix.items():
            if selected != unit:  # Don't compare a unit against itself
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
cols_per_row_output = 16
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
                        <p>{unit}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

