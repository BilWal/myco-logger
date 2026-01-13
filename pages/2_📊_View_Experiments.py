"""
View Experiments Page
Browse, filter, and manage mushroom cultivation experiments.
"""

import streamlit as st
import pandas as pd
from datetime import datetime, date
import sys
from pathlib import Path

# Add parent directory to path to import database module
sys.path.append(str(Path(__file__).parent.parent))
import database


st.set_page_config(
    page_title="View Experiments - Myco Logger",
    page_icon="📊",
    layout="wide"
)


def calculate_days_elapsed(inoculation_date):
    """Calculate days elapsed since inoculation."""
    if pd.isna(inoculation_date):
        return None

    if isinstance(inoculation_date, str):
        inoculation_date = datetime.strptime(inoculation_date, "%Y-%m-%d").date()
    elif isinstance(inoculation_date, datetime):
        inoculation_date = inoculation_date.date()

    today = date.today()
    delta = today - inoculation_date
    return delta.days


def filter_experiments(df, status_filter, substrate_filter, search_term, date_range):
    """Apply filters to experiments DataFrame."""
    filtered_df = df.copy()

    # Status filter
    if status_filter:
        filtered_df = filtered_df[filtered_df['status'].isin(status_filter)]

    # Substrate filter
    if substrate_filter:
        filtered_df = filtered_df[filtered_df['substrate_type'].isin(substrate_filter)]

    # Search by name
    if search_term:
        filtered_df = filtered_df[
            filtered_df['experiment_name'].str.contains(search_term, case=False, na=False)
        ]

    # Date range filter
    if date_range[0] and date_range[1]:
        filtered_df['inoculation_date_dt'] = pd.to_datetime(filtered_df['inoculation_date'])
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered_df = filtered_df[
            (filtered_df['inoculation_date_dt'] >= start_date) &
            (filtered_df['inoculation_date_dt'] <= end_date)
        ]
        filtered_df = filtered_df.drop('inoculation_date_dt', axis=1)

    return filtered_df


def main():
    """Main function for View Experiments page."""

    st.title("📊 View Experiments")
    st.markdown("Browse, filter, and manage your cultivation experiments.")

    # Initialize session state
    if 'selected_experiment_id' not in st.session_state:
        st.session_state.selected_experiment_id = None
    if 'edit_mode' not in st.session_state:
        st.session_state.edit_mode = False
    if 'delete_confirm' not in st.session_state:
        st.session_state.delete_confirm = False

    # Load all experiments
    df = database.get_all_experiments()

    # Sidebar filters
    with st.sidebar:
        st.markdown("### 🔍 Filters")

        # Status filter
        all_statuses = ['inoculating', 'colonizing', 'pinning', 'fruiting', 'done', 'contaminated']
        status_filter = st.multiselect(
            "Status",
            options=all_statuses,
            default=[]
        )

        # Substrate type filter
        if not df.empty:
            substrate_types = df['substrate_type'].unique().tolist()
        else:
            substrate_types = []

        substrate_filter = st.multiselect(
            "Substrate Type",
            options=substrate_types,
            default=[]
        )

        # Search by name
        search_term = st.text_input(
            "Search by Name",
            placeholder="Enter experiment name..."
        )

        # Date range filter
        st.markdown("**Date Range**")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From", value=None, key="start_date")
        with col2:
            end_date = st.date_input("To", value=None, key="end_date")

        date_range = (start_date, end_date)

        # Clear filters button
        if st.button("Clear All Filters", use_container_width=True):
            st.session_state.clear()
            st.rerun()

    st.divider()

    if df.empty:
        st.info("No experiments found. Add your first experiment using the '📝 Add Experiment' page.")
        return

    # Apply filters
    filtered_df = filter_experiments(df, status_filter, substrate_filter, search_term, date_range)

    if filtered_df.empty:
        st.warning("No experiments match the selected filters.")
        return

    # Calculate days elapsed
    filtered_df['Days Elapsed'] = filtered_df['inoculation_date'].apply(calculate_days_elapsed)

    # Display count
    st.markdown(f"**Showing {len(filtered_df)} of {len(df)} experiments**")

    # Display experiments table
    display_df = filtered_df[[
        'id',
        'experiment_name',
        'substrate_type',
        'status',
        'container_type',
        'inoculation_date',
        'Days Elapsed'
    ]].copy()

    display_df.columns = [
        'ID',
        'Name',
        'Substrate',
        'Status',
        'Container',
        'Inoculation Date',
        'Days Elapsed'
    ]

    # Display table
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ID": st.column_config.NumberColumn("ID", width="small"),
            "Name": st.column_config.TextColumn("Name", width="medium"),
            "Substrate": st.column_config.TextColumn("Substrate", width="medium"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Container": st.column_config.TextColumn("Container", width="small"),
            "Inoculation Date": st.column_config.DateColumn("Inoculation Date", width="medium"),
            "Days Elapsed": st.column_config.NumberColumn("Days Elapsed", width="small")
        }
    )

    st.divider()

    # Experiment selection and details
    st.subheader("🔍 Experiment Details & Management")

    # Select experiment by ID
    experiment_ids = display_df['ID'].tolist()
    selected_id = st.selectbox(
        "Select Experiment by ID",
        options=experiment_ids,
        format_func=lambda x: f"ID {x} - {display_df[display_df['ID'] == x]['Name'].values[0]}"
    )

    if selected_id:
        st.session_state.selected_experiment_id = selected_id
        experiment = database.get_experiment_by_id(selected_id)

        if experiment:
            # Display experiment details
            with st.expander("📋 View Full Details", expanded=True):
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.markdown("**Basic Information**")
                    st.write(f"**ID:** {experiment['id']}")
                    st.write(f"**Name:** {experiment['experiment_name']}")
                    st.write(f"**Status:** {experiment['status']}")
                    st.write(f"**Container:** {experiment['container_type']}")

                with col2:
                    st.markdown("**Substrate Details**")
                    st.write(f"**Type:** {experiment['substrate_type']}")
                    st.write(f"**Details:** {experiment['substrate_details'] or 'N/A'}")
                    st.write(f"**Spawn Ratio:** {experiment['spawn_ratio']}%" if experiment['spawn_ratio'] else "**Spawn Ratio:** N/A")
                    st.write(f"**Weight:** {experiment['substrate_weight_kg']} kg" if experiment['substrate_weight_kg'] else "**Weight:** N/A")

                with col3:
                    st.markdown("**Important Dates**")
                    st.write(f"**Inoculation:** {experiment['inoculation_date']}")
                    st.write(f"**Colonization:** {experiment['colonization_date'] or 'Not set'}")
                    st.write(f"**First Pin:** {experiment['first_pin_date'] or 'Not set'}")
                    st.write(f"**Created:** {experiment['created_at']}")

                if experiment['contamination_type'] or experiment['contamination_notes']:
                    st.markdown("**Contamination Info**")
                    st.write(f"**Type:** {experiment['contamination_type'] or 'N/A'}")
                    st.write(f"**Notes:** {experiment['contamination_notes'] or 'N/A'}")

                if experiment['notes']:
                    st.markdown("**Notes**")
                    st.write(experiment['notes'])

            # Edit mode
            if not st.session_state.edit_mode:
                col1, col2 = st.columns([1, 1])
                with col1:
                    if st.button("✏️ Edit Experiment", use_container_width=True):
                        st.session_state.edit_mode = True
                        st.rerun()
                with col2:
                    if st.button("🗑️ Delete Experiment", use_container_width=True):
                        st.session_state.delete_confirm = True
                        st.rerun()
            else:
                # Edit form
                with st.form("edit_experiment_form"):
                    st.markdown("### Edit Experiment")

                    col1, col2 = st.columns(2)

                    with col1:
                        new_status = st.selectbox(
                            "Status",
                            options=['inoculating', 'colonizing', 'pinning', 'fruiting', 'done', 'contaminated'],
                            index=['inoculating', 'colonizing', 'pinning', 'fruiting', 'done', 'contaminated'].index(experiment['status'])
                        )

                        new_colonization_date = st.date_input(
                            "Colonization Date",
                            value=datetime.strptime(experiment['colonization_date'], "%Y-%m-%d").date() if experiment['colonization_date'] else None
                        )

                        new_first_pin_date = st.date_input(
                            "First Pin Date",
                            value=datetime.strptime(experiment['first_pin_date'], "%Y-%m-%d").date() if experiment['first_pin_date'] else None
                        )

                    with col2:
                        new_contamination_type = st.text_input(
                            "Contamination Type",
                            value=experiment['contamination_type'] or ""
                        )

                        new_contamination_notes = st.text_area(
                            "Contamination Notes",
                            value=experiment['contamination_notes'] or "",
                            height=100
                        )

                    new_notes = st.text_area(
                        "General Notes",
                        value=experiment['notes'] or "",
                        height=120
                    )

                    col1, col2 = st.columns(2)
                    with col1:
                        save_button = st.form_submit_button("💾 Save Changes", use_container_width=True)
                    with col2:
                        cancel_button = st.form_submit_button("❌ Cancel", use_container_width=True)

                    if save_button:
                        try:
                            update_data = {
                                'status': new_status,
                                'colonization_date': new_colonization_date.strftime("%Y-%m-%d") if new_colonization_date else None,
                                'first_pin_date': new_first_pin_date.strftime("%Y-%m-%d") if new_first_pin_date else None,
                                'contamination_type': new_contamination_type if new_contamination_type else None,
                                'contamination_notes': new_contamination_notes if new_contamination_notes else None,
                                'notes': new_notes if new_notes else None
                            }

                            database.update_experiment(selected_id, **update_data)
                            st.success("✅ Experiment updated successfully!")
                            st.session_state.edit_mode = False
                            st.rerun()

                        except Exception as e:
                            st.error(f"❌ Error updating experiment: {str(e)}")

                    if cancel_button:
                        st.session_state.edit_mode = False
                        st.rerun()

            # Delete confirmation
            if st.session_state.delete_confirm:
                st.warning("⚠️ Are you sure you want to delete this experiment? This action cannot be undone.")

                col1, col2 = st.columns(2)
                with col1:
                    if st.button("✅ Yes, Delete", use_container_width=True, type="primary"):
                        try:
                            database.delete_experiment(selected_id)
                            st.success("✅ Experiment deleted successfully!")
                            st.session_state.selected_experiment_id = None
                            st.session_state.delete_confirm = False
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error deleting experiment: {str(e)}")

                with col2:
                    if st.button("❌ Cancel", use_container_width=True):
                        st.session_state.delete_confirm = False
                        st.rerun()


if __name__ == "__main__":
    main()
