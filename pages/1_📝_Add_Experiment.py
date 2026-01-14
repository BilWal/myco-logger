"""
Add Experiment Page
Form to add new mushroom cultivation experiments.
"""

import streamlit as st
from datetime import date
import sys
from pathlib import Path

# Add parent directory to path to import database module
sys.path.append(str(Path(__file__).parent.parent))
import database
from assets import get_substrate_icon, get_status_icon, SUBSTRATE_ICONS
from styles import apply_custom_css


st.set_page_config(
    page_title="Add Experiment - Myco Logger",
    page_icon="📝",
    layout="wide"
)

# Apply custom styling
apply_custom_css()


def validate_form(experiment_name, substrate_type, inoculation_date):
    """Validate form inputs."""
    errors = []

    if not experiment_name or experiment_name.strip() == "":
        errors.append("Experiment name is required")

    if not substrate_type:
        errors.append("Substrate type is required")

    if not inoculation_date:
        errors.append("Inoculation date is required")
    elif inoculation_date > date.today():
        errors.append("Inoculation date cannot be in the future")

    return errors


def main():
    """Main function for Add Experiment page."""

    st.title("📝 Add New Experiment")
    st.markdown("Log a new mushroom cultivation experiment with substrate details and inoculation information.")

    st.divider()

    # Create form
    with st.form("add_experiment_form", clear_on_submit=True):
        st.subheader("Experiment Details")

        # Two columns for better organization
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Substrate Information")

            experiment_name = st.text_input(
                "Experiment Name *",
                placeholder="e.g., Oyster #1 - Cardboard",
                help="Give your experiment a unique, descriptive name"
            )

            substrate_type = st.selectbox(
                "Substrate Type *",
                options=[
                    "",
                    "cardboard",
                    "coffee grounds",
                    "straw",
                    "sawdust pellets",
                    "mix",
                    "other"
                ],
                help="Select the primary substrate material"
            )

            # Show substrate icon preview if selected
            if substrate_type and substrate_type != "":
                preview_col1, preview_col2 = st.columns([1, 4])
                with preview_col1:
                    substrate_icon = get_substrate_icon(substrate_type)
                    try:
                        st.image(substrate_icon, width=64)
                    except:
                        st.write("📦")
                with preview_col2:
                    st.caption(f"Selected: {substrate_type.title()}")

            substrate_details = st.text_area(
                "Substrate Details",
                placeholder="e.g., 70% corrugated cardboard, 30% coffee grounds",
                help="Describe the substrate composition (optional)",
                height=100
            )

            spawn_ratio = st.number_input(
                "Spawn Ratio (%)",
                min_value=0.0,
                max_value=50.0,
                value=10.0,
                step=0.5,
                help="Percentage of spawn to substrate by weight"
            )

            substrate_weight_kg = st.number_input(
                "Substrate Weight (kg)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=0.1,
                help="Dry weight of substrate before inoculation (optional)"
            )

        with col2:
            st.markdown("#### Container & Dates")

            container_type = st.selectbox(
                "Container Type",
                options=["bucket", "bag", "jar", "other"],
                help="Type of container used for cultivation"
            )

            inoculation_date = st.date_input(
                "Inoculation Date *",
                value=date.today(),
                max_value=date.today(),
                help="Date when spawn was added to substrate"
            )

            status = st.selectbox(
                "Initial Status",
                options=["inoculating", "colonizing"],
                index=0,
                help="Current status of the experiment"
            )

            st.markdown("")  # Spacer

        # Notes field spans full width
        st.markdown("#### Additional Notes")
        notes = st.text_area(
            "Notes",
            placeholder="Any additional observations or details about this experiment...",
            help="Optional notes about the experiment",
            height=120
        )

        # Submit button
        st.divider()
        submitted = st.form_submit_button("🍄 Add Experiment", use_container_width=True)

        if submitted:
            # Validate form
            errors = validate_form(experiment_name, substrate_type, inoculation_date)

            if errors:
                for error in errors:
                    st.error(f"❌ {error}")
            else:
                try:
                    # Prepare data for database
                    experiment_data = {
                        'experiment_name': experiment_name.strip(),
                        'substrate_type': substrate_type,
                        'substrate_details': substrate_details.strip() if substrate_details else None,
                        'spawn_ratio': spawn_ratio if spawn_ratio > 0 else None,
                        'substrate_weight_kg': substrate_weight_kg if substrate_weight_kg > 0 else None,
                        'container_type': container_type,
                        'inoculation_date': inoculation_date.strftime("%Y-%m-%d"),
                        'status': status,
                        'notes': notes.strip() if notes else None
                    }

                    # Add to database
                    experiment_id = database.add_experiment(**experiment_data)

                    # Show success message with celebration
                    st.balloons()
                    st.success(f"✅ Experiment '{experiment_name}' added successfully!")

                    # Show preview with icons
                    summary_col1, summary_col2 = st.columns([1, 4])
                    with summary_col1:
                        status_icon = get_status_icon(status)
                        try:
                            st.image(status_icon, width=64)
                        except:
                            st.write("🍄")
                    with summary_col2:
                        st.info(f"**Experiment #{experiment_id}** is now {status}!")
                        st.markdown(f"""
                        - **Substrate:** {substrate_type}
                        - **Container:** {container_type}
                        - **Inoculation Date:** {inoculation_date.strftime("%Y-%m-%d")}
                        """)

                except Exception as e:
                    st.error(f"❌ Error adding experiment: {str(e)}")

    # Help section in sidebar
    with st.sidebar:
        st.markdown("### 📝 Form Help")
        st.markdown("""
        **Required Fields (marked with *):**
        - Experiment Name
        - Substrate Type
        - Inoculation Date

        **Tips:**
        - Use descriptive names for easy identification
        - Accurate spawn ratio helps track performance
        - Substrate weight enables BE calculation later
        - Update status as experiment progresses
        """)

        st.divider()

        st.markdown("### 🍄 Substrate Types")
        st.markdown("""
        - **Cardboard**: Corrugated cardboard, shredded
        - **Coffee Grounds**: Used coffee grounds
        - **Straw**: Wheat, oat, or other straw
        - **Sawdust**: Hardwood sawdust pellets
        - **Mix**: Combination of substrates
        - **Other**: Custom substrate materials
        """)


if __name__ == "__main__":
    main()
