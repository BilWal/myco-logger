"""
Custom styling module for Myco Logger.
Provides CSS styling and color palette for consistent visual theme.
"""

import streamlit as st

# Color palette
COLORS = {
    'sage_green': '#8B9E7D',
    'terracotta': '#C4825B',
    'cream': '#F5F5DC',
    'dark_brown': '#3E2723',
    'off_white': '#FAFAFA',
    'white': '#FFFFFF',
    'light_gray': '#E0E0E0',
    'success_green': '#4CAF50',
    'warning_yellow': '#FFC107',
    'error_red': '#F44336',
}


def apply_custom_css():
    """Apply custom CSS styling to the Streamlit app."""
    st.markdown(f"""
    <style>
        /* Main app background - subtle gradient */
        .stApp {{
            background: linear-gradient(to bottom, {COLORS['cream']}, {COLORS['off_white']});
        }}

        /* Sidebar styling */
        [data-testid="stSidebar"] {{
            background-color: {COLORS['sage_green']};
            color: {COLORS['white']};
        }}

        [data-testid="stSidebar"] .stMarkdown {{
            color: {COLORS['white']};
        }}

        /* Headers */
        h1, h2, h3 {{
            color: {COLORS['dark_brown']};
            font-family: 'Helvetica Neue', sans-serif;
        }}

        /* Metric cards */
        [data-testid="stMetricValue"] {{
            color: {COLORS['dark_brown']};
            font-size: 2rem;
            font-weight: 600;
        }}

        [data-testid="stMetricLabel"] {{
            color: {COLORS['sage_green']};
            font-size: 1rem;
        }}

        /* Buttons */
        .stButton > button {{
            background-color: {COLORS['sage_green']};
            color: {COLORS['white']};
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.3s ease;
        }}

        .stButton > button:hover {{
            background-color: {COLORS['terracotta']};
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}

        /* Forms */
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stDateInput > div > div > input {{
            border-radius: 8px;
            border: 2px solid {COLORS['light_gray']};
            background-color: {COLORS['white']};
        }}

        .stTextInput > div > div > input:focus,
        .stNumberInput > div > div > input:focus,
        .stTextArea > div > div > textarea:focus {{
            border-color: {COLORS['sage_green']};
            box-shadow: 0 0 0 2px {COLORS['sage_green']}33;
        }}

        /* DataFrames/Tables */
        .stDataFrame {{
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}

        /* Success/Error/Warning messages */
        .stSuccess {{
            background-color: {COLORS['success_green']}22;
            border-left: 4px solid {COLORS['success_green']};
            border-radius: 4px;
            padding: 1rem;
        }}

        .stError {{
            background-color: {COLORS['error_red']}22;
            border-left: 4px solid {COLORS['error_red']};
            border-radius: 4px;
            padding: 1rem;
        }}

        .stWarning {{
            background-color: {COLORS['warning_yellow']}22;
            border-left: 4px solid {COLORS['warning_yellow']};
            border-radius: 4px;
            padding: 1rem;
        }}

        /* Cards/containers */
        .element-container {{
            margin-bottom: 1rem;
        }}

        /* Custom status badge styling */
        .status-badge {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.25rem 0.75rem;
            border-radius: 16px;
            font-size: 0.875rem;
            font-weight: 500;
        }}

        .status-inoculating {{
            background-color: {COLORS['light_gray']};
            color: {COLORS['dark_brown']};
        }}

        .status-colonizing {{
            background-color: {COLORS['warning_yellow']}44;
            color: {COLORS['dark_brown']};
        }}

        .status-pinning {{
            background-color: {COLORS['sage_green']}44;
            color: {COLORS['dark_brown']};
        }}

        .status-fruiting {{
            background-color: {COLORS['success_green']}44;
            color: {COLORS['dark_brown']};
        }}

        .status-done {{
            background-color: {COLORS['sage_green']};
            color: {COLORS['white']};
        }}

        .status-contaminated {{
            background-color: {COLORS['error_red']}44;
            color: {COLORS['dark_brown']};
        }}

        /* Hide Streamlit branding */
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}

        /* Expander styling */
        .streamlit-expanderHeader {{
            background-color: {COLORS['off_white']};
            border-radius: 8px;
            font-weight: 500;
        }}

    </style>
    """, unsafe_allow_html=True)


def get_status_color(status: str) -> str:
    """
    Get color for status indicator.

    Args:
        status: Status string

    Returns:
        str: Hex color code
    """
    status_colors = {
        'inoculating': COLORS['light_gray'],
        'colonizing': COLORS['warning_yellow'],
        'pinning': COLORS['sage_green'],
        'fruiting': COLORS['success_green'],
        'done': COLORS['sage_green'],
        'contaminated': COLORS['error_red'],
    }
    return status_colors.get(status.lower(), COLORS['light_gray'])
