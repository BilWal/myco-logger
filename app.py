"""
Myco Logger - Mushroom Cultivation Experiment Tracker
Main application page with dashboard and statistics.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import database


# Page configuration
st.set_page_config(
    page_title="🍄 Myco Logger",
    page_icon="🍄",
    layout="wide"
)


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

    # Header
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

        # Calculate days since inoculation
        recent_df['Days Since Inoculation'] = recent_df['inoculation_date'].apply(
            calculate_days_since_inoculation
        )

        # Select and rename columns for display
        display_df = recent_df[[
            'experiment_name',
            'substrate_type',
            'status',
            'inoculation_date',
            'Days Since Inoculation'
        ]].copy()

        display_df.columns = [
            'Name',
            'Substrate',
            'Status',
            'Inoculation Date',
            'Days Elapsed'
        ]

        # Apply color coding to status column
        def color_status(val):
            colors = {
                'inoculating': 'background-color: #e3f2fd',
                'colonizing': 'background-color: #fff3e0',
                'pinning': 'background-color: #f3e5f5',
                'fruiting': 'background-color: #e8f5e9',
                'done': 'background-color: #f5f5f5',
                'contaminated': 'background-color: #ffebee'
            }
            return colors.get(val, '')

        # Display table with styling
        styled_df = display_df.style.applymap(
            color_status,
            subset=['Status']
        )

        st.dataframe(
            styled_df,
            use_container_width=True,
            hide_index=True
        )

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
