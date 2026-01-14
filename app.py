"""
Myco Logger - Mushroom Cultivation Experiment Tracker
Main application page with dashboard and statistics.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import database
from assets import LOGO_HEADER, get_status_icon, verify_assets
from styles import apply_custom_css


# Page configuration
st.set_page_config(
    page_title="Myco Logger",
    page_icon="🍄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_custom_css()


def calculate_days_since_inoculation(inoculation_date):
    """Calculate days elapsed since inoculation date."""
    if pd.isna(inoculation_date):
        return None

    if isinstance(inoculation_date, str):
        inoculation_date = datetime.strptime(inoculation_date, "%Y-%m-%d").date()
    elif isinstance(inoculation_date, datetime):
        inoculation_date = inoculation_date.date()

    today = date.today()
    delta = today - inoculation_date
    return delta.days


def main():
    """Main application function."""

    # Initialize database on first run
    database.init_database()

    # Verify assets (show warning in sidebar if missing)
    asset_status = verify_assets()
    if not asset_status['all_present']:
        with st.sidebar:
            st.warning("⚠️ Some assets missing:")
            for item in asset_status['missing']:
                st.text(f"- {item}")

    # Display logo header
    try:
        st.image(LOGO_HEADER, use_column_width=True)
    except:
        st.title("🍄 Myco Logger")

    st.markdown("""
    ### Track Your Mushroom Cultivation Experiments
    Monitor substrate performance, colonization times, and yields from inoculation to harvest.
    """)

    st.divider()

    # Get statistics
    stats = database.get_stats()

    # Display stats in columns
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="Total Experiments",
            value=stats['total_count']
        )

    with col2:
        st.metric(
            label="Active Experiments",
            value=stats['active_count']
        )

    with col3:
        st.metric(
            label="Contaminated",
            value=stats['contaminated_count'],
            delta=None if stats['contaminated_count'] == 0 else f"-{stats['contaminated_count']}",
            delta_color="inverse"
        )

    with col4:
        st.metric(
            label="Success Rate",
            value=f"{stats['success_rate']}%",
            delta=None
        )

    st.divider()

    # Recent experiments section
    st.subheader("📋 Recent Experiments")

    # Get all experiments
    df = database.get_all_experiments()

    if not df.empty:
        # Get last 5 experiments
        recent_df = df.head(5).copy()

        # Display each experiment with icons
        for idx, row in recent_df.iterrows():
            col1, col2, col3 = st.columns([1, 6, 2])

            with col1:
                # Display status icon
                status_icon = get_status_icon(row['status'])
                try:
                    st.image(status_icon, width=48)
                except:
                    st.write("🍄")

            with col2:
                st.markdown(f"**{row['experiment_name']}**")
                st.caption(f"{row['substrate_type']} • {row['status'].title()}")

            with col3:
                days = calculate_days_since_inoculation(row['inoculation_date'])
                if days is not None:
                    st.metric("Days", days, label_visibility="collapsed")

            st.divider()

    else:
        st.info("No experiments yet. Add your first experiment using the '📝 Add Experiment' page in the sidebar.")

    # Sidebar navigation info
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        st.markdown("""
        Use the pages above to:
        - **📝 Add Experiment**: Log new cultivation experiments
        - **📊 View Experiments**: Browse, filter, and edit experiments
        - **📈 Analytics**: View charts and performance metrics
        """)

        st.divider()

        st.markdown("### 📊 Quick Stats")
        st.markdown(f"**Total Experiments:** {stats['total_count']}")
        st.markdown(f"**Active:** {stats['active_count']}")
        st.markdown(f"**Success Rate:** {stats['success_rate']}%")


if __name__ == "__main__":
    main()
