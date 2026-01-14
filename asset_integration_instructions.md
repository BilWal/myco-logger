# Myco Logger - Asset Integration & Visual Styling Instructions

## Overview
Integrate custom generated icons and implement visual styling to transform the Myco Logger app from standard Streamlit to a branded, cohesive experience.

---

## Phase 1: Asset Organization

### Task 1: Create Assets Folder Structure
Create the following folder structure in the project root:

```
myco-logger/
└── assets/
    ├── icons/
    │   ├── status/
    │   └── substrates/
    └── branding/
```

### Task 2: Organize and Rename Assets
The following image files need to be moved and renamed:

**Status Icons → assets/icons/status/**
- `InoculatingStage.png` → `inoculating.png`
- `EarlyColonizingStage.png` → `colonizing_early.png`
- `ColonizingStage.png` → `colonizing.png`
- `PinningStage.png` → `pinning.png`
- `FruitingStage.png` → `fruiting.png`
- `HarvestedStage.png` → `done.png`
- `ContaminatedStage.png` → `contaminated.png`

**Substrate Icons → assets/icons/substrates/**
- `CardboardSubstrate.png` → `cardboard.png`
- `CoffeeGroundsSubstrate.png` → `coffee.png`
- `StrawSubstrate.png` → `straw.png`
- `SawdustPelletsSubstrate.png` → `sawdust.png`
- `MixedSubstrate.png` → `mixed.png`

**Branding → assets/branding/**
- `MycoLoggerHeaderLogo.png` → `logo_header.png`

Create a Python script or bash script to automate this renaming if needed.

---

## Phase 2: Create Asset Helper Module

### Task 3: Create assets.py
Create a new file `assets.py` in the project root to centralize asset paths:

**Requirements:**
```python
import os
from pathlib import Path

# Base paths
ASSETS_DIR = Path(__file__).parent / "assets"
ICONS_DIR = ASSETS_DIR / "icons"
STATUS_DIR = ICONS_DIR / "status"
SUBSTRATE_DIR = ICONS_DIR / "substrates"
BRANDING_DIR = ASSETS_DIR / "branding"

# Status icons mapping
STATUS_ICONS = {
    'inoculating': str(STATUS_DIR / 'inoculating.png'),
    'colonizing': str(STATUS_DIR / 'colonizing.png'),
    'pinning': str(STATUS_DIR / 'pinning.png'),
    'fruiting': str(STATUS_DIR / 'fruiting.png'),
    'done': str(STATUS_DIR / 'done.png'),
    'contaminated': str(STATUS_DIR / 'contaminated.png'),
}

# Substrate icons mapping
SUBSTRATE_ICONS = {
    'cardboard': str(SUBSTRATE_DIR / 'cardboard.png'),
    'coffee grounds': str(SUBSTRATE_DIR / 'coffee.png'),
    'coffee': str(SUBSTRATE_DIR / 'coffee.png'),  # alias
    'straw': str(SUBSTRATE_DIR / 'straw.png'),
    'sawdust pellets': str(SUBSTRATE_DIR / 'sawdust.png'),
    'sawdust': str(SUBSTRATE_DIR / 'sawdust.png'),  # alias
    'mix': str(SUBSTRATE_DIR / 'mixed.png'),
    'mixed': str(SUBSTRATE_DIR / 'mixed.png'),
    'other': str(SUBSTRATE_DIR / 'mixed.png'),  # fallback
}

# Branding
LOGO_HEADER = str(BRANDING_DIR / 'logo_header.png')

# Helper functions
def get_status_icon(status: str) -> str:
    """Get path to status icon, with fallback."""
    status_lower = status.lower()
    # Handle "colonizing" variations
    if 'coloniz' in status_lower and status_lower not in STATUS_ICONS:
        return STATUS_ICONS.get('colonizing', '')
    return STATUS_ICONS.get(status_lower, STATUS_ICONS.get('inoculating', ''))

def get_substrate_icon(substrate: str) -> str:
    """Get path to substrate icon, with fallback."""
    substrate_lower = substrate.lower()
    return SUBSTRATE_ICONS.get(substrate_lower, SUBSTRATE_ICONS.get('mixed', ''))

def verify_assets() -> dict:
    """Verify all assets exist and return status."""
    missing = []
    
    # Check status icons
    for status, path in STATUS_ICONS.items():
        if not os.path.exists(path):
            missing.append(f"Status icon: {status} ({path})")
    
    # Check substrate icons
    unique_substrate_paths = set(SUBSTRATE_ICONS.values())
    for path in unique_substrate_paths:
        if not os.path.exists(path):
            missing.append(f"Substrate icon: {path}")
    
    # Check branding
    if not os.path.exists(LOGO_HEADER):
        missing.append(f"Logo: {LOGO_HEADER}")
    
    return {
        'all_present': len(missing) == 0,
        'missing': missing
    }
```

---

## Phase 3: Custom CSS Styling

### Task 4: Create styles.py
Create `styles.py` for custom CSS to implement the visual theme:

**Requirements:**
```python
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
    """Get color for status indicator."""
    status_colors = {
        'inoculating': COLORS['light_gray'],
        'colonizing': COLORS['warning_yellow'],
        'pinning': COLORS['sage_green'],
        'fruiting': COLORS['success_green'],
        'done': COLORS['sage_green'],
        'contaminated': COLORS['error_red'],
    }
    return status_colors.get(status.lower(), COLORS['light_gray'])
```

---

## Phase 4: Update app.py (Home Page)

### Task 5: Integrate Assets and Styling into app.py

**Updates needed:**

1. **Import new modules at top:**
```python
from assets import LOGO_HEADER, get_status_icon, verify_assets
from styles import apply_custom_css
```

2. **Update page config:**
```python
st.set_page_config(
    page_title="Myco Logger",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

3. **Apply styling (right after page config):**
```python
apply_custom_css()
```

4. **Verify assets on load (optional but recommended):**
```python
# Check assets (only show if issues)
asset_status = verify_assets()
if not asset_status['all_present']:
    with st.sidebar:
        st.warning("⚠️ Some assets missing:")
        for item in asset_status['missing']:
            st.text(f"- {item}")
```

5. **Add logo header:**
```python
# Display logo
try:
    st.image(LOGO_HEADER, use_column_width=True)
except:
    st.title("🍄 Myco Logger")
```

6. **Update stats display to use icons:**
```python
# Get stats from database
stats = get_stats()  # your existing function

# Display stats in columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Experiments",
        value=stats['total_count']
    )

with col2:
    st.metric(
        label="Active",
        value=stats['active_count']
    )

with col3:
    st.metric(
        label="Contaminated",
        value=stats['contaminated_count']
    )

with col4:
    success_rate = stats.get('success_rate', 0)
    st.metric(
        label="Success Rate",
        value=f"{success_rate:.1f}%"
    )
```

7. **Update recent experiments table to include icons:**
```python
# Get recent experiments
recent = get_recent_experiments(limit=5)  # your existing function

if not recent.empty:
    st.subheader("Recent Experiments")
    
    # Add icons to dataframe display
    for idx, row in recent.iterrows():
        col1, col2, col3 = st.columns([1, 6, 2])
        
        with col1:
            # Display status icon
            status_icon = get_status_icon(row['status'])
            try:
                st.image(status_icon, width=48)
            except:
                st.write("🍄")
        
        with col2:
            st.write(f"**{row['experiment_name']}**")
            st.caption(f"{row['substrate_type']} • {row['status'].title()}")
        
        with col3:
            days = calculate_days_elapsed(row['inoculation_date'])
            st.metric("Days", days, label_visibility="collapsed")
        
        st.divider()
else:
    st.info("No experiments yet. Add your first experiment to get started!")
```

---

## Phase 5: Update Add Experiment Page

### Task 6: Update pages/1_📝_Add_Experiment.py

**Updates needed:**

1. **Add imports:**
```python
from assets import get_substrate_icon, SUBSTRATE_ICONS
from styles import apply_custom_css
import streamlit as st
```

2. **Apply styling:**
```python
apply_custom_css()
```

3. **Add substrate preview icons:**
```python
# When substrate type is selected, show icon preview
substrate_type = st.selectbox(
    "Substrate Type",
    options=list(SUBSTRATE_ICONS.keys())
)

# Show icon preview
col1, col2 = st.columns([1, 4])
with col1:
    substrate_icon = get_substrate_icon(substrate_type)
    try:
        st.image(substrate_icon, width=64)
    except:
        st.write("📦")
with col2:
    st.caption(f"Selected: {substrate_type.title()}")
```

4. **Enhance success message with celebration:**
```python
if st.form_submit_button("Add Experiment", type="primary"):
    # ... validation and database insert ...
    
    if success:
        st.balloons()  # Add celebration
        st.success(f"✅ Experiment '{experiment_name}' added successfully!")
        
        # Show preview with icon
        col1, col2 = st.columns([1, 4])
        with col1:
            status_icon = get_status_icon('inoculating')
            st.image(status_icon, width=64)
        with col2:
            st.info(f"Experiment #{experiment_id} is now inoculating!")
```

---

## Phase 6: Update View Experiments Page

### Task 7: Update pages/2_📊_View_Experiments.py

**Updates needed:**

1. **Add imports:**
```python
from assets import get_status_icon, get_substrate_icon
from styles import apply_custom_css, get_status_color
```

2. **Apply styling:**
```python
apply_custom_css()
```

3. **Update experiment display with icons:**
```python
# For each experiment in filtered view
for idx, experiment in filtered_experiments.iterrows():
    with st.container():
        col1, col2, col3, col4 = st.columns([1, 4, 2, 2])
        
        with col1:
            # Show status icon
            status_icon = get_status_icon(experiment['status'])
            try:
                st.image(status_icon, width=64)
            except:
                st.write("🍄")
        
        with col2:
            st.markdown(f"### {experiment['experiment_name']}")
            
            # Show substrate icon inline
            substrate_icon = get_substrate_icon(experiment['substrate_type'])
            subcol1, subcol2 = st.columns([1, 10])
            with subcol1:
                try:
                    st.image(substrate_icon, width=24)
                except:
                    pass
            with subcol2:
                st.caption(f"{experiment['substrate_type'].title()} • {experiment['container_type']}")
        
        with col3:
            # Status badge with color
            status_color = get_status_color(experiment['status'])
            st.markdown(
                f"<div class='status-badge status-{experiment['status'].lower()}'>"
                f"{experiment['status'].title()}</div>",
                unsafe_allow_html=True
            )
        
        with col4:
            days = calculate_days_elapsed(experiment['inoculation_date'])
            st.metric("Days", days)
        
        # Expandable details
        with st.expander("View Details"):
            detail_col1, detail_col2 = st.columns(2)
            
            with detail_col1:
                st.write("**Inoculation Date:**", experiment['inoculation_date'])
                if experiment.get('colonization_date'):
                    st.write("**Colonization Date:**", experiment['colonization_date'])
                st.write("**Spawn Ratio:**", f"{experiment['spawn_ratio']}%")
            
            with detail_col2:
                st.write("**Container:**", experiment['container_type'])
                st.write("**Notes:**", experiment['notes'] or "None")
            
            # Edit button
            if st.button("Edit", key=f"edit_{experiment['id']}"):
                # Trigger edit mode in session state
                st.session_state['editing_id'] = experiment['id']
                st.rerun()
        
        st.divider()
```

---

## Phase 7: Update Analytics Page

### Task 8: Update pages/3_📈_Analytics.py

**Updates needed:**

1. **Add imports:**
```python
from assets import get_status_icon, get_substrate_icon
from styles import apply_custom_css, COLORS
import matplotlib.pyplot as plt
import plotly.express as px
```

2. **Apply styling:**
```python
apply_custom_css()
```

3. **Enhance charts with custom colors:**
```python
# Example: Colonization speed chart
fig = px.bar(
    colonization_data,
    x='substrate_type',
    y='avg_days',
    title='Average Days to Colonization by Substrate',
    color='substrate_type',
    color_discrete_map={
        'cardboard': COLORS['terracotta'],
        'coffee grounds': COLORS['dark_brown'],
        'straw': COLORS['warning_yellow'],
        'sawdust pellets': COLORS['sage_green'],
        'mix': COLORS['sage_green'],
    }
)

fig.update_layout(
    plot_bgcolor=COLORS['off_white'],
    paper_bgcolor=COLORS['cream'],
    font_color=COLORS['dark_brown'],
)

st.plotly_chart(fig, use_container_width=True)
```

4. **Add substrate icons to legends/labels:**
```python
# When displaying substrate breakdown, show icons
st.subheader("Substrate Performance")

substrate_stats = get_substrate_stats()  # your function

for substrate, stats in substrate_stats.items():
    col1, col2, col3 = st.columns([1, 3, 2])
    
    with col1:
        icon = get_substrate_icon(substrate)
        try:
            st.image(icon, width=48)
        except:
            st.write("📦")
    
    with col2:
        st.write(f"**{substrate.title()}**")
        st.caption(f"{stats['count']} experiments")
    
    with col3:
        st.metric("Success Rate", f"{stats['success_rate']:.1f}%")
```

---

## Phase 8: Testing & Polish

### Task 9: Test Visual Integration

**Test checklist:**
- [ ] All status icons display correctly on home page
- [ ] All status icons display in view experiments page
- [ ] Substrate icons show in add experiment form
- [ ] Substrate icons display in analytics
- [ ] Logo displays on home page
- [ ] Custom colors applied throughout app
- [ ] Buttons have hover effects
- [ ] Status badges have correct colors
- [ ] Forms have consistent styling
- [ ] Tables/dataframes look clean
- [ ] Responsive on different screen sizes
- [ ] No broken image links
- [ ] Icons scale appropriately at different sizes

### Task 10: Handle Missing Assets Gracefully

Add fallback handling throughout:

```python
def safe_image_display(image_path, width=None, fallback_emoji="🍄"):
    """Display image with emoji fallback if image missing."""
    try:
        if os.path.exists(image_path):
            st.image(image_path, width=width)
        else:
            st.write(fallback_emoji)
    except Exception as e:
        st.write(fallback_emoji)
```

Use this function wherever images are displayed.

---

## Phase 9: Optional Enhancements

### Task 11: Additional Polish (if time permits)

1. **Loading states with custom messages:**
```python
with st.spinner("🍄 Growing your data..."):
    # Long operation
    pass
```

2. **Custom success/error messages:**
```python
# Instead of plain st.success()
st.markdown("""
    <div style='padding: 1rem; background-color: #4CAF5022; border-left: 4px solid #4CAF50; border-radius: 4px;'>
        <h4 style='margin: 0; color: #4CAF50;'>✅ Success!</h4>
        <p style='margin: 0.5rem 0 0 0;'>Experiment added successfully!</p>
    </div>
""", unsafe_allow_html=True)
```

3. **Animated transitions:**
```python
# Use st.empty() for smooth updates
placeholder = st.empty()
with placeholder.container():
    # Show loading
    st.spinner()
    
# Update with results
with placeholder.container():
    # Show content
    pass
```

4. **Tooltips and help text:**
```python
st.text_input(
    "Experiment Name",
    help="Give your experiment a memorable name"
)
```

---

## Deliverables

After completing all tasks, the app should have:

1. ✅ All custom icons properly organized in assets/ folder
2. ✅ Consistent visual theme using custom color palette
3. ✅ Status icons displayed throughout the app
4. ✅ Substrate icons shown in forms and views
5. ✅ Custom logo on home page
6. ✅ Enhanced CSS styling for all components
7. ✅ Graceful fallbacks for missing assets
8. ✅ Polished user experience with appropriate visual feedback

---

## File Changes Summary

**New Files:**
- `assets.py` - Asset path management
- `styles.py` - Custom CSS and styling
- `assets/` folder structure with all icons

**Modified Files:**
- `app.py` - Logo, icons, styling
- `pages/1_📝_Add_Experiment.py` - Substrate icons, styling
- `pages/2_📊_View_Experiments.py` - Status/substrate icons, badges
- `pages/3_📈_Analytics.py` - Charts with custom colors, icons

---

## Notes

- Keep icon display sizes consistent (48-64px for main displays, 24-32px for inline)
- Always provide emoji fallbacks for accessibility
- Test on both light and dark mode if user has that option
- Icons should load quickly (all are small PNG files)
- Consider adding alt text for accessibility
- Cache icon paths to avoid repeated file system checks

---

## Next Steps After Integration

Once assets are integrated, consider:
1. User testing to gather feedback on visual design
2. A/B testing different icon sizes
3. Adding more visual feedback (progress bars, animations)
4. Creating additional themed pages or sections
5. Mobile responsiveness testing
