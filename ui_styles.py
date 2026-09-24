"""CSS and Markdown injection for the Streamlit interface."""

import base64
import os
import re

import streamlit as st

from unit_data import UNIT_IMAGES


@st.cache_data
def get_image_as_base64(image_path):
    """Read and encode an image once per Streamlit cache lifetime."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def unit_key(unit):
    """Return a stable CSS-safe key for a unit name."""
    return re.sub(r"[^a-z0-9_]", "_", unit.lower().replace(" ", "_"))


def inject_app_styles(image_folder):
    """Inject responsive tile, result-card, and selection styles."""
    tile_image_css = []
    for unit, filename in UNIT_IMAGES.items():
        image_base64 = get_image_as_base64(os.path.join(image_folder, filename))
        tile_image_css.append(
            f"[class*='st-key-unit_tile_{unit_key(unit)}'] button, "
            f"[class*='st-key-result_card_{unit_key(unit)}_'] button {{ "
            f"background-image: url('data:image/jpeg;base64,{image_base64}'); }} "
            f"[class*='st-key-unit_tile_{unit_key(unit)}'] button::before {{ "
            f"content: '{unit}'; }}"
        )

    st.markdown(
        """
        <style>
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
        [class*="st-key-show_de_tier"] { margin-top: 1rem; }
        @media (min-width: 390px) and (max-width: 640px) {
            [class*="st-key-unit_picker_grid"], [class*="st-key-tier_grid_"] {
                grid-template-columns: repeat(5, minmax(0, 1fr));
            }
        }
        @media (min-width: 641px) {
            [class*="st-key-unit_picker_grid"], [class*="st-key-tier_grid_"] {
                grid-template-columns: repeat(8, minmax(0, 1fr));
            }
        }
        @media (min-width: 1200px) {
            [class*="st-key-unit_picker_grid"], [class*="st-key-tier_grid_"] {
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
            overflow: hidden;
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
        [class*="st-key-unit_tile_"] button [data-testid="stMarkdownContainer"],
        [class*="st-key-result_card_"] button [data-testid="stMarkdownContainer"] {
            visibility: hidden;
        }
        [class*="st-key-unit_tile_"] button::before {
            position: absolute;
            z-index: 2;
            top: 50%;
            left: 50%;
            box-sizing: border-box;
            display: block;
            width: calc(100% - 8px);
            max-height: calc(100% - 8px);
            overflow: hidden;
            padding: .25em .35em;
            border-radius: 50%;
            background: radial-gradient(ellipse at center, rgba(0, 0, 0, .72) 0%, rgba(0, 0, 0, .42) 28%, rgba(0, 0, 0, 0) 70%);
            color: #fff;
            font-size: clamp(.5rem, .75vw, .8rem);
            font-weight: 400;
            line-height: 1.1;
            text-align: center;
            white-space: normal;
            overflow-wrap: normal;
            word-break: normal;
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
        [class*="_selected"] button:hover { filter: brightness(.98); }
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
        }
        [class*="st-key-result_card_"] button {
            display: block;
            box-sizing: border-box;
            width: 100%;
            aspect-ratio: 248 / 378;
            min-height: 0;
            padding: 0;
            border: 0;
            border-radius: 10px;
            background-color: transparent;
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
            box-shadow: none;
            cursor: pointer;
            opacity: 1;
            transition: transform 140ms ease, filter 140ms ease, box-shadow 140ms ease;
        }
        [class*="st-key-result_card_"] button:hover {
            filter: brightness(1.12);
            transform: scale(1.025);
            box-shadow: 0 0 0 2px rgba(255, 255, 255, .75);
            z-index: 1;
        }
        [class*="st-key-result_card_"] button:focus-visible {
            outline: 3px solid #ffcc00;
            outline-offset: 3px;
        }
        [class*="st-key-result_card_"] button:active {
            filter: brightness(.92);
            transform: scale(.985);
        }
        """ + "\n".join(tile_image_css) + "</style>",
        unsafe_allow_html=True,
    )
