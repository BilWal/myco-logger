"""
Add Harvest Page
Record harvest yields for mushroom cultivation experiments.
"""

import streamlit as st
from datetime import date
import sys
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).parent.parent))
import database
from assets import get_status_icon, get_substrate_icon
from styles import apply_custom_css
from utils.calculations import calculate_biological_efficiency


st.set_page_config(
    page_title="Add Harvest - Myco Logger",
    page_icon="🌾",
    layout="wide"
)

# Apply custom styling
apply_custom_css()


def main():
    """Main function for Add Harvest page."""

    st.title("🌾 Add Harvest")
    st.markdown("Record a harvest yield for one of your cultivation experiments.")

    st.divider()

    # Load all experiments
    all_experiments = database.get_all_experiments()

    if all_experiments.empty:
        st.info("No experiments yet. Add an experiment on the '📝 Add Experiment' page first.")
        return

    # Only show non-contaminated experiments
    eligible = all_experiments[all_experiments['status'] != 'contaminated'].copy()

    if eligible.empty:
        st.info("No eligible experiments. All current experiments are contaminated.")
        return

    # Experiment selector
    experiment_options = eligible['id'].tolist()

    selected_id = st.selectbox(
        "Select Experiment",
        options=experiment_options,
        format_func=lambda x: (
            f"{eligible[eligible['id'] == x]['experiment_name'].values[0]}"
            f" — {eligible[eligible['id'] == x]['substrate_type'].values[0]}"
            f" ({eligible[eligible['id'] == x]['status'].values[0].title()})"
        )
    )

    experiment = database.get_experiment_by_id(selected_id)

    # Experiment preview row
    if experiment:
        col1, col2, col3 = st.columns([1, 5, 2])

        with col1:
            status_icon = get_status_icon(experiment['status'])
            try:
                st.image(status_icon, width=48)
            except:
                st.write("🍄")

        with col2:
            st.markdown(f"**{experiment['experiment_name']}**")
            substrate_icon = get_substrate_icon(experiment['substrate_type'])
            subcol1, subcol2 = st.columns([1, 10])
            with subcol1:
                try:
                    st.image(substrate_icon, width=24)
                except:
                    pass
            with subcol2:
                substrate_label = experiment['substrate_type']
                weight_label = f"{experiment['substrate_weight_kg']} kg" if experiment['substrate_weight_kg'] else "weight not set"
                st.caption(f"{substrate_label} • {weight_label}")

        with col3:
            total_weight = database.get_total_harvest_weight(selected_id)
            st.metric("Total Harvested", f"{total_weight:.0f} g")

    st.divider()

    # Get suggested flush number
    next_flush = database.get_next_flush_number(selected_id)

    # Harvest form
    with st.form("add_harvest_form", clear_on_submit=True):
        st.subheader("Harvest Details")

        col1, col2 = st.columns(2)

        with col1:
            flush_number = st.number_input(
                "Flush Number",
                min_value=1,
                value=next_flush,
                step=1,
                help=f"Auto-suggested next flush: {next_flush}"
            )

            harvest_date = st.date_input(
                "Harvest Date *",
                value=date.today(),
                max_value=date.today(),
                help="Date the mushrooms were harvested"
            )

        with col2:
            weight_grams = st.number_input(
                "Weight (grams) *",
                min_value=0.0,
                value=0.0,
                step=1.0,
                help="Fresh weight of harvested mushrooms"
            )

        quality_notes = st.text_area(
            "Quality Notes",
            placeholder="e.g., Beautiful pins, some cracking, good size...",
            help="Optional notes on mushroom quality",
            height=100
        )

        submitted = st.form_submit_button("🌾 Record Harvest", use_container_width=True)

        if submitted:
            errors = []
            if weight_grams <= 0:
                errors.append("Weight must be greater than 0")
            if harvest_date > date.today():
                errors.append("Harvest date cannot be in the future")

            if errors:
                for err in errors:
                    st.error(f"❌ {err}")
            else:
                try:
                    harvest_data = {
                        'experiment_id': selected_id,
                        'flush_number': flush_number,
                        'harvest_date': harvest_date.strftime("%Y-%m-%d"),
                        'weight_grams': weight_grams,
                        'quality_notes': quality_notes.strip() if quality_notes else None
                    }

                    harvest_id = database.add_harvest(**harvest_data)

                    st.balloons()
                    st.success(f"✅ Harvest recorded! (ID: {harvest_id})")

                    # Show updated totals
                    total_weight = database.get_total_harvest_weight(selected_id)

                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("This Flush", f"{weight_grams:.0f} g")
                    with col2:
                        st.metric("Total Yield", f"{total_weight:.0f} g")
                    with col3:
                        if experiment and experiment['substrate_weight_kg']:
                            be = calculate_biological_efficiency(total_weight, experiment['substrate_weight_kg'])
                            st.metric("Biological Efficiency", f"{be}%")
                        else:
                            st.metric("BE%", "N/A", help="Set substrate weight on experiment to enable")

                except Exception as e:
                    st.error(f"❌ Error recording harvest: {str(e)}")

    # Harvest history for selected experiment
    st.divider()
    st.subheader("📋 Harvest History")

    harvests_df = database.get_harvests_by_experiment(selected_id)

    if not harvests_df.empty:
        # Add running total column
        harvests_df['Running Total (g)'] = harvests_df['weight_grams'].cumsum()

        display_df = harvests_df[['flush_number', 'harvest_date', 'weight_grams', 'Running Total (g)', 'quality_notes']].copy()
        display_df.columns = ['Flush', 'Date', 'Weight (g)', 'Running Total (g)', 'Quality Notes']

        st.dataframe(display_df, hide_index=True, use_container_width=True)

        # BE summary if substrate weight is available
        if experiment and experiment['substrate_weight_kg']:
            total_weight = harvests_df['weight_grams'].sum()
            be = calculate_biological_efficiency(total_weight, experiment['substrate_weight_kg'])

            st.divider()
            be_col1, be_col2 = st.columns([1, 2])
            with be_col1:
                st.metric("Current BE", f"{be}%")
            with be_col2:
                if be >= 75:
                    st.success("On track for good BE (target: 75-125%)")
                else:
                    st.info("More flushes may improve BE (target: 75-125%)")
    else:
        st.info("No harvests recorded yet for this experiment. Use the form above to log your first flush.")

    # Sidebar help
    with st.sidebar:
        st.markdown("### 🌾 Harvest Help")
        st.markdown("""
        **Flush:** Each round of fruiting is called a flush.
        Most substrates produce 2-3 flushes.

        **Biological Efficiency (BE):**
        `BE = (Total harvest / Dry substrate) × 100`

        Good oyster mushroom BE: **75-125%**

        **Tips:**
        - Weigh mushrooms fresh after harvest
        - Record each flush separately
        - Include quality notes for comparison
        """)


if __name__ == "__main__":
    main()
