# Myco Logger - Development Instructions for Claude Code

## Project Goal
Build a Streamlit web application to track mushroom cultivation experiments from inoculation to harvest, with analytics on substrate performance and yields.

---

## Phase 1: Initial Setup (Do This First)

### Task 1: Create Project Structure
```
Create the following folder structure:
myco-logger/
├── app.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
├── pages/
│   ├── 1_📝_Add_Experiment.py
│   ├── 2_📊_View_Experiments.py
│   └── 3_📈_Analytics.py
├── utils/
│   └── calculations.py
└── data/
    └── .gitkeep
```

### Task 2: Set Up Files
Copy the content from the artifacts I provided for:
- requirements.txt
- README.md
- .gitignore

---

## Phase 2: Database Layer (database.py)

### Task 3: Create database.py
Build a SQLite database module with the following:

**Database Schema:**

Table: `experiments`
- id: INTEGER PRIMARY KEY AUTOINCREMENT
- experiment_name: TEXT NOT NULL
- substrate_type: TEXT NOT NULL (cardboard, coffee, straw, sawdust, mix, other)
- substrate_details: TEXT (composition description)
- spawn_ratio: REAL (percentage like 10.0)
- substrate_weight_kg: REAL (dry weight)
- container_type: TEXT (bucket, bag, jar, other)
- inoculation_date: DATE NOT NULL
- colonization_date: DATE (can be NULL)
- first_pin_date: DATE (can be NULL)
- status: TEXT NOT NULL (inoculating, colonizing, pinning, fruiting, done, contaminated)
- contamination_type: TEXT (can be NULL)
- contamination_notes: TEXT (can be NULL)
- notes: TEXT
- created_at: TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Required Functions:**
1. `init_database()` - Creates tables if they don't exist, returns connection
2. `add_experiment(**kwargs)` - Insert new experiment, return id
3. `get_all_experiments()` - Return all experiments as pandas DataFrame
4. `get_experiment_by_id(experiment_id)` - Return single experiment as dict
5. `update_experiment(experiment_id, **kwargs)` - Update experiment fields
6. `delete_experiment(experiment_id)` - Delete experiment
7. `get_experiments_by_status(status)` - Filter experiments by status
8. `get_stats()` - Return dict with: total_count, active_count, contaminated_count, success_rate

**Implementation Notes:**
- Database file location: `data/mushroom_tracker.db`
- Use context managers for connections
- Add error handling for all database operations
- Use parameterized queries to prevent SQL injection
- Return pandas DataFrames for easy Streamlit integration

---

## Phase 3: Home Page (app.py)

### Task 4: Create app.py
Build the main landing page with:

**Requirements:**
1. Page configuration:
   - Title: "🍄 Myco Logger"
   - Icon: 🍄
   - Layout: wide

2. Initialize database on first run (call init_database())

3. Display header and description

4. Query and display stats in 4 columns using st.columns():
   - Total Experiments
   - Active Experiments  
   - Contaminated
   - Success Rate (%)

5. Show recent experiments table:
   - Last 5 experiments
   - Columns: Name, Substrate, Status, Inoculation Date, Days Since Inoculation
   - Calculate "Days Since Inoculation" dynamically
   - Use st.dataframe() with appropriate styling

6. Add navigation info for multi-page app in sidebar

**Styling:**
- Use st.metric() for stats display
- Use color coding: green for success, red for contamination
- Make table sortable and filterable

---

## Phase 4: Add Experiment Page

### Task 5: Create pages/1_📝_Add_Experiment.py
Build form to add new experiments:

**Form Fields:**
1. Experiment Name (text_input, required)
2. Substrate Type (selectbox: cardboard, coffee grounds, straw, sawdust pellets, mix, other)
3. Substrate Details (text_area, optional - describe composition)
4. Spawn Ratio % (number_input, 0-50%, default 10)
5. Substrate Weight kg (number_input, 0-100kg, step 0.1, optional)
6. Container Type (selectbox: bucket, bag, jar, other)
7. Inoculation Date (date_input, default today, cannot be future)
8. Notes (text_area, optional)

**Behavior:**
- Use st.form() to group inputs
- Validate required fields before submission
- Validate inoculation date (cannot be in future)
- On submit:
  - Call database.add_experiment()
  - Show success message with experiment ID
  - Clear form or offer "Add Another" button
- Handle errors gracefully with st.error()

**Layout:**
- Use two columns for better organization
- Left column: substrate info
- Right column: dates and container info
- Notes field spans full width

---

## Phase 5: View Experiments Page

### Task 6: Create pages/2_📊_View_Experiments.py
Build page to view and manage experiments:

**Features:**

1. **Filters (in sidebar):**
   - Status filter (multiselect: all statuses)
   - Substrate type filter (multiselect: all types)
   - Date range filter (date_input for start/end)
   - Search by name (text_input)

2. **Main Table:**
   - Display filtered experiments
   - Columns: Name, Substrate, Status, Container, Inoculation Date, Days Elapsed, Actions
   - Calculate days elapsed dynamically
   - Color code status column
   - Make table sortable

3. **Experiment Details (expandable):**
   - Click row to expand and show all fields
   - Display in organized sections

4. **Edit Functionality:**
   - Button to enter edit mode for selected experiment
   - Allow updating:
     - Status (dropdown)
     - Colonization date (if status changed to colonizing/pinning/fruiting)
     - First pin date (if status changed to pinning/fruiting)
     - Mark as contaminated (with type and notes)
     - General notes
   - Save button to update database
   - Cancel button to exit edit mode

5. **Delete Functionality:**
   - Delete button with confirmation dialog
   - Use st.warning() and require explicit confirmation

**Implementation Notes:**
- Use st.data_editor() for interactive table if possible
- Use session_state to track selected experiment and edit mode
- Refresh data after updates

---

## Phase 6: Analytics Page

### Task 7: Create pages/3_📈_Analytics.py
Build analytics dashboard:

**Charts to Include:**

1. **Colonization Speed by Substrate Type**
   - Bar chart showing average days to colonization
   - Only include experiments with colonization_date set
   - Group by substrate_type
   - Use matplotlib or plotly

2. **Success Rate by Substrate Type**
   - Pie chart or stacked bar chart
   - Show contaminated vs successful
   - Calculate percentage for each substrate type

3. **Status Distribution**
   - Pie chart of current status counts
   - Color code: inoculating (blue), colonizing (yellow), fruiting (green), contaminated (red), done (gray)

4. **Timeline View**
   - Line chart showing experiments over time
   - X-axis: date
   - Y-axis: count of experiments at each status

5. **Summary Statistics Table**
   - Average days to colonization by substrate
   - Success rate by substrate
   - Total experiments per substrate type

**Filters:**
- Date range selector in sidebar
- Substrate type filter
- Include/exclude contaminated experiments toggle

**Implementation:**
- Use plotly for interactive charts
- Display charts in columns for better layout
- Add data table below each chart
- Handle empty data gracefully (show message if no data)

---

## Phase 7: Helper Functions

### Task 8: Create utils/calculations.py
Build helper calculation functions:

**Functions Needed:**
1. `calculate_days_elapsed(start_date, end_date=None)`
   - If end_date is None, use today
   - Return integer days

2. `calculate_success_rate(total, contaminated)`
   - Return percentage as float

3. `format_date(date_string)`
   - Convert database date to readable format
   - Handle None values

4. `get_status_color(status)`
   - Return color code for status
   - Used for styling

5. `validate_date(date_input)`
   - Check if date is valid
   - Check if date is not in future
   - Return True/False with error message

**Notes:**
- Use python datetime module
- Add docstrings to all functions
- Include error handling

---

## Phase 8: Testing & Polish

### Task 9: Test Complete Workflow
Test the following user flows:

1. **Add Experiment Flow:**
   - Open Add Experiment page
   - Fill all required fields
   - Submit successfully
   - Verify it appears in View Experiments
   - Verify stats update on home page

2. **Update Experiment Flow:**
   - Go to View Experiments
   - Select an experiment
   - Update status to "colonizing"
   - Add colonization date
   - Save changes
   - Verify changes persist

3. **Analytics Flow:**
   - Add several experiments with different substrates
   - Mark some as colonized with dates
   - Mark some as contaminated
   - View analytics page
   - Verify charts display correctly

4. **Edge Cases:**
   - Empty database on first run
   - Invalid date inputs
   - Required field validation
   - Deleting experiments

### Task 10: Refinements
- Add loading spinners for database operations
- Improve error messages
- Add tooltips/help text
- Ensure responsive design
- Add keyboard shortcuts where appropriate
- Improve visual hierarchy

---

## Development Tips

**Iterative Approach:**
1. Build each phase completely before moving to next
2. Test after each phase
3. Commit to git after each working phase
4. Don't try to do everything at once

**Debugging:**
- Use st.write() to debug variables
- Check database file is being created in data/ folder
- Use try/except blocks and log errors
- Test with small datasets first

**Streamlit Tips:**
- Use st.cache_data for database queries
- Use session_state for maintaining state between reruns
- Remember Streamlit reruns the entire script on interaction
- Use st.spinner() for long operations

---

## Success Criteria

Phase 1 Complete When:
- [ ] Can add experiments with all fields
- [ ] Experiments display in table
- [ ] Can filter and search experiments
- [ ] Can update experiment status and dates
- [ ] Can delete experiments
- [ ] Basic analytics charts display
- [ ] Stats on home page are accurate
- [ ] No errors in normal operation
- [ ] Data persists between app restarts

---

## Next Steps (Future Phases)

After Phase 1 is working:
1. Add harvest tracking (new table and page)
2. Calculate biological efficiency
3. Add photo upload capability
4. Export data to CSV
5. Cost tracking features
6. More advanced analytics

---

## Questions to Ask During Development

1. Should substrate_weight_kg be required or optional?
2. Should we allow editing inoculation_date after creation?
3. What date format should we display (MM/DD/YYYY or DD/MM/YYYY)?
4. Should we add confirmation dialogs for status changes?
5. Do you want notifications when experiments reach certain milestones?

---

## Example Git Commits

```
git commit -m "feat: initial project structure"
git commit -m "feat: database schema and CRUD functions"
git commit -m "feat: home page with stats dashboard"
git commit -m "feat: add experiment form with validation"
git commit -m "feat: view experiments with filters"
git commit -m "feat: analytics page with charts"
git commit -m "fix: date validation on experiment form"
git commit -m "style: improve table formatting"
git commit -m "docs: update README with usage instructions"
```

---

## Ready to Start?

Begin with Phase 1 (project setup) and work through each phase sequentially. Test thoroughly after each phase before moving forward.

Good luck! 🍄
