"""
Analytics Page
Visualize experiment performance, substrate comparisons, and success rates.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import sys
from pathlib import Path

# Add parent directory to path to import database module
sys.path.append(str(Path(__file__).parent.parent))
import database
from assets import get_status_icon, get_substrate_icon
from styles import apply_custom_css, COLORS


st.set_page_config(
    page_title="Analytics - Myco Logger",
    page_icon="📈",
    layout="wide"
)

# Apply custom styling
apply_custom_css()


def calculate_days_to_colonization(row):
    """Calculate days between inoculation and colonization."""
    if pd.isna(row['inoculation_date']) or pd.isna(row['colonization_date']):
        return None

    inoc_date = pd.to_datetime(row['inoculation_date'])
    colon_date = pd.to_datetime(row['colonization_date'])
    return (colon_date - inoc_date).days


def filter_data(df, date_range, substrate_filter, exclude_contaminated):
    """Apply filters to DataFrame."""
    filtered_df = df.copy()

    # Date range filter
    if date_range[0] and date_range[1]:
        filtered_df['inoculation_date_dt'] = pd.to_datetime(filtered_df['inoculation_date'])
        start_date = pd.to_datetime(date_range[0])
        end_date = pd.to_datetime(date_range[1])
        filtered_df = filtered_df[
            (filtered_df['inoculation_date_dt'] >= start_date) &
            (filtered_df['inoculation_date_dt'] <= end_date)
        ]

    # Substrate filter
    if substrate_filter:
        filtered_df = filtered_df[filtered_df['substrate_type'].isin(substrate_filter)]

    # Exclude contaminated
    if exclude_contaminated:
        filtered_df = filtered_df[filtered_df['status'] != 'contaminated']

    return filtered_df


def main():
    """Main function for Analytics page."""

    st.title("📈 Analytics Dashboard")
    st.markdown("Visualize experiment performance and compare substrate effectiveness.")

    # Load data
    df = database.get_all_experiments()

    if df.empty:
        st.info("No experiments to analyze yet. Add experiments to see analytics.")
        return

    # Sidebar filters
    with st.sidebar:
        st.markdown("### 🔍 Filters")

        # Date range filter
        st.markdown("**Date Range**")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From", value=None, key="analytics_start_date")
        with col2:
            end_date = st.date_input("To", value=None, key="analytics_end_date")

        date_range = (start_date, end_date)

        # Substrate filter
        substrate_types = df['substrate_type'].unique().tolist()
        substrate_filter = st.multiselect(
            "Substrate Types",
            options=substrate_types,
            default=substrate_types
        )

        # Exclude contaminated toggle
        exclude_contaminated = st.checkbox(
            "Exclude Contaminated",
            value=False
        )

        if st.button("Reset Filters", use_container_width=True):
            st.rerun()

    # Apply filters
    filtered_df = filter_data(df, date_range, substrate_filter, exclude_contaminated)

    if filtered_df.empty:
        st.warning("No data matches the selected filters.")
        return

    st.markdown(f"**Analyzing {len(filtered_df)} experiments**")
    st.divider()

    # === Chart 1: Status Distribution ===
    st.subheader("📊 Status Distribution")

    status_counts = filtered_df['status'].value_counts()

    if not status_counts.empty:
        color_map = {
            'inoculating': COLORS['light_gray'],
            'colonizing': COLORS['warning_yellow'],
            'pinning': COLORS['sage_green'],
            'fruiting': COLORS['success_green'],
            'done': COLORS['sage_green'],
            'contaminated': COLORS['error_red']
        }

        fig_status = px.pie(
            values=status_counts.values,
            names=status_counts.index,
            title="Current Status of All Experiments",
            color=status_counts.index,
            color_discrete_map=color_map
        )

        # Update layout with custom colors
        fig_status.update_layout(
            plot_bgcolor=COLORS['off_white'],
            paper_bgcolor=COLORS['cream'],
            font_color=COLORS['dark_brown'],
        )

        st.plotly_chart(fig_status, use_container_width=True)
    else:
        st.info("No status data available")

    st.divider()

    # === Chart 2: Colonization Speed by Substrate ===
    st.subheader("⏱️ Colonization Speed by Substrate Type")

    # Calculate days to colonization
    df_with_colon = filtered_df[filtered_df['colonization_date'].notna()].copy()

    if not df_with_colon.empty:
        df_with_colon['days_to_colonization'] = df_with_colon.apply(
            calculate_days_to_colonization,
            axis=1
        )

        # Remove null values
        df_with_colon = df_with_colon[df_with_colon['days_to_colonization'].notna()]

        if not df_with_colon.empty:
            # Group by substrate type and calculate average
            avg_colonization = df_with_colon.groupby('substrate_type')['days_to_colonization'].agg(['mean', 'count']).reset_index()
            avg_colonization.columns = ['Substrate Type', 'Avg Days', 'Count']
            avg_colonization['Avg Days'] = avg_colonization['Avg Days'].round(1)

            # Create bar chart with custom colors
            fig_colon = px.bar(
                avg_colonization,
                x='Substrate Type',
                y='Avg Days',
                title='Average Days to Full Colonization',
                text='Avg Days',
                color='Substrate Type',
                color_discrete_map={
                    'cardboard': COLORS['terracotta'],
                    'coffee grounds': COLORS['dark_brown'],
                    'straw': COLORS['warning_yellow'],
                    'sawdust pellets': COLORS['sage_green'],
                    'mix': COLORS['sage_green'],
                }
            )
            fig_colon.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig_colon.update_layout(
                showlegend=False,
                plot_bgcolor=COLORS['off_white'],
                paper_bgcolor=COLORS['cream'],
                font_color=COLORS['dark_brown'],
            )

            col1, col2 = st.columns([2, 1])

            with col1:
                st.plotly_chart(fig_colon, use_container_width=True)

            with col2:
                st.markdown("**Summary Table**")
                st.dataframe(
                    avg_colonization,
                    hide_index=True,
                    use_container_width=True
                )
        else:
            st.info("No experiments with colonization dates available")
    else:
        st.info("No experiments with colonization dates available yet. Update experiments with colonization dates to see this chart.")

    st.divider()

    # === Chart 3: Success Rate by Substrate Type ===
    st.subheader("✅ Success Rate by Substrate Type")

    # Calculate success rate (non-contaminated) by substrate
    success_data = filtered_df.groupby('substrate_type').agg({
        'id': 'count',
        'status': lambda x: (x != 'contaminated').sum()
    }).reset_index()
    success_data.columns = ['Substrate Type', 'Total', 'Successful']
    success_data['Success Rate (%)'] = (success_data['Successful'] / success_data['Total'] * 100).round(1)
    success_data['Contaminated'] = success_data['Total'] - success_data['Successful']

    if not success_data.empty:
        # Create stacked bar chart
        fig_success = go.Figure()

        fig_success.add_trace(go.Bar(
            name='Successful',
            x=success_data['Substrate Type'],
            y=success_data['Successful'],
            marker_color=COLORS['success_green']
        ))

        fig_success.add_trace(go.Bar(
            name='Contaminated',
            x=success_data['Substrate Type'],
            y=success_data['Contaminated'],
            marker_color=COLORS['error_red']
        ))

        fig_success.update_layout(
            barmode='stack',
            title='Success vs Contamination by Substrate',
            xaxis_title='Substrate Type',
            yaxis_title='Number of Experiments',
            plot_bgcolor=COLORS['off_white'],
            paper_bgcolor=COLORS['cream'],
            font_color=COLORS['dark_brown'],
        )

        col1, col2 = st.columns([2, 1])

        with col1:
            st.plotly_chart(fig_success, use_container_width=True)

        with col2:
            st.markdown("**Success Rate Table**")
            display_success = success_data[['Substrate Type', 'Total', 'Success Rate (%)']].copy()
            st.dataframe(
                display_success,
                hide_index=True,
                use_container_width=True
            )
    else:
        st.info("No data available for success rate analysis")

    st.divider()

    # === Chart 4: Experiments Timeline ===
    st.subheader("📅 Experiments Timeline")

    timeline_df = filtered_df.copy()
    timeline_df['inoculation_date_dt'] = pd.to_datetime(timeline_df['inoculation_date'])
    timeline_df = timeline_df.sort_values('inoculation_date_dt')

    if not timeline_df.empty:
        # Count experiments by date
        timeline_counts = timeline_df.groupby('inoculation_date_dt').size().reset_index()
        timeline_counts.columns = ['Date', 'Count']
        timeline_counts['Cumulative'] = timeline_counts['Count'].cumsum()

        fig_timeline = go.Figure()

        fig_timeline.add_trace(go.Scatter(
            x=timeline_counts['Date'],
            y=timeline_counts['Cumulative'],
            mode='lines+markers',
            name='Cumulative Experiments',
            line=dict(color=COLORS['sage_green'], width=3),
            marker=dict(size=8, color=COLORS['terracotta'])
        ))

        fig_timeline.update_layout(
            title='Cumulative Experiments Over Time',
            xaxis_title='Date',
            yaxis_title='Total Experiments',
            hovermode='x unified',
            plot_bgcolor=COLORS['off_white'],
            paper_bgcolor=COLORS['cream'],
            font_color=COLORS['dark_brown'],
        )

        st.plotly_chart(fig_timeline, use_container_width=True)
    else:
        st.info("No timeline data available")

    st.divider()

    # === Summary Statistics ===
    st.subheader("📊 Summary Statistics")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Total Experiments", len(filtered_df))

    with col2:
        avg_days = None
        if not df_with_colon.empty and 'days_to_colonization' in df_with_colon.columns:
            avg_days = df_with_colon['days_to_colonization'].mean()
        if avg_days:
            st.metric("Avg Days to Colonization", f"{avg_days:.1f}")
        else:
            st.metric("Avg Days to Colonization", "N/A")

    with col3:
        contaminated_count = (filtered_df['status'] == 'contaminated').sum()
        if len(filtered_df) > 0:
            success_rate = ((len(filtered_df) - contaminated_count) / len(filtered_df) * 100)
            st.metric("Overall Success Rate", f"{success_rate:.1f}%")
        else:
            st.metric("Overall Success Rate", "N/A")

    # Detailed statistics table
    st.markdown("### 📋 Detailed Statistics by Substrate")

    detailed_stats = filtered_df.groupby('substrate_type').agg({
        'id': 'count',
        'status': lambda x: (x != 'contaminated').sum()
    }).reset_index()
    detailed_stats.columns = ['Substrate', 'Total Experiments', 'Successful']
    detailed_stats['Success Rate (%)'] = (detailed_stats['Successful'] / detailed_stats['Total Experiments'] * 100).round(1)

    # Add average colonization days
    if not df_with_colon.empty and 'days_to_colonization' in df_with_colon.columns:
        avg_colon_by_substrate = df_with_colon.groupby('substrate_type')['days_to_colonization'].mean().round(1)
        detailed_stats = detailed_stats.merge(
            avg_colon_by_substrate.rename('Avg Days to Colonization'),
            left_on='Substrate',
            right_index=True,
            how='left'
        )

    st.dataframe(detailed_stats, hide_index=True, use_container_width=True)


if __name__ == "__main__":
    main()
