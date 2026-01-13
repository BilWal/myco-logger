# 🍄 Myco Logger - Project Outline

## Project Overview
A Streamlit web application for tracking mushroom cultivation experiments, monitoring substrate performance, and analyzing harvest yields.

## Technology Stack
- **Frontend/Backend:** Streamlit (Python)
- **Database:** SQLite
- **Data Analysis:** Pandas
- **Visualization:** Matplotlib/Plotly
- **Deployment:** Streamlit Cloud (optional)

---

## File Structure
```
myco-logger/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── app.py                    # Main Streamlit application
├── database.py               # Database setup and functions
├── pages/
│   ├── 1_📝_Add_Experiment.py
│   ├── 2_📊_View_Experiments.py
│   ├── 3_📈_Analytics.py
│   └── 4_🌾_Add_Harvest.py
├── utils/
│   └── calculations.py       # Helper functions (BE calculation, etc)
└── data/
    ├── .gitkeep
    └── mushroom_tracker.db   # SQLite database (gitignored)
```

---

## Database Schema

### Table: experiments
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment ID |
| experiment_name | TEXT NOT NULL | User-friendly name |
| substrate_type | TEXT NOT NULL | Main substrate (cardboard, coffee, mix, etc) |
| substrate_details | TEXT | Composition details (e.g., "70% cardboard, 30% coffee") |
| spawn_ratio | REAL | Percentage (e.g., 10.0 for 10%) |
| substrate_weight_kg | REAL | Dry weight of substrate |
| container_type | TEXT | bucket, bag, etc |
| inoculation_date | DATE NOT NULL | When spawn was added |
| colonization_date | DATE | When fully colonized (NULL if not yet) |
| first_pin_date | DATE | When first pins appeared (NULL if not yet) |
| status | TEXT NOT NULL | inoculating/colonizing/pinning/fruiting/done/contaminated |
| contamination_type | TEXT | mold type if contaminated |
| contamination_notes | TEXT | Details about contamination |
| notes | TEXT | General notes |
| created_at | TIMESTAMP | Auto-set on creation |

### Table: harvests
| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER PRIMARY KEY | Auto-increment ID |
| experiment_id | INTEGER NOT NULL | Foreign key to experiments |
| flush_number | INTEGER NOT NULL | 1st, 2nd, 3rd flush |
| harvest_date | DATE NOT NULL | When harvested |
| weight_grams | REAL NOT NULL | Fresh weight in grams |
| quality_notes | TEXT | Notes on mushroom quality |
| photos | TEXT | Comma-separated photo filenames (optional) |
| created_at | TIMESTAMP | Auto-set on creation |

---

## Features by Page

### Home (app.py)
- Welcome message and overview
- Quick stats dashboard:
  - Total experiments
  - Active experiments
  - Success rate (non-contaminated %)
  - Total harvests
- Recent activity feed (last 5 experiments)

### Page 1: Add Experiment
- Form with fields:
  - Experiment name (text input)
  - Substrate type (selectbox: cardboard, coffee grounds, straw, sawdust, mix, other)
  - Substrate details (text area)
  - Spawn ratio (number input, %)
  - Substrate weight (number input, kg)
  - Container type (selectbox: bucket, bag, jar, other)
  - Inoculation date (date input)
  - Notes (text area)
- Submit button saves to database
- Success message with experiment ID

### Page 2: View Experiments
- Filterable table of all experiments
  - Filter by status (dropdown)
  - Filter by substrate type (dropdown)
  - Search by name (text input)
- Display key columns: name, substrate, status, inoculation date, days since inoculation
- Click row to expand and see full details
- Edit mode:
  - Update status
  - Add colonization date
  - Add first pin date
  - Mark as contaminated with notes
  - Update general notes
- Delete experiment (with confirmation)

### Page 3: Analytics
- Charts and insights:
  1. **Colonization Speed by Substrate**
     - Bar chart: avg days to colonization by substrate type
  2. **Success Rate by Substrate**
     - Pie or bar chart: contaminated vs successful
  3. **Biological Efficiency**
     - Bar chart: BE% by experiment (for completed ones with harvests)
  4. **Harvest Timeline**
     - Line chart: cumulative weight over time
  5. **Cost Analysis** (optional/future)
     - Input costs per substrate type
     - Calculate cost per kg harvested
- Filters to narrow analysis by date range or substrate

### Page 4: Add Harvest
- Select experiment (dropdown of active experiments)
- Form fields:
  - Flush number (auto-suggest next number)
  - Harvest date (date input)
  - Weight in grams (number input)
  - Quality notes (text area)
- Submit button saves to database
- Display total yield and BE for that experiment so far

---

## Key Calculations

### Biological Efficiency (BE)
```
BE = (Total fresh weight harvested / Dry substrate weight) × 100
```
Example: 1kg substrate → 800g mushrooms = 80% BE

Good oyster mushroom BE: 75-125%

### Days to Colonization
```
colonization_date - inoculation_date
```

### Success Rate
```
(Non-contaminated experiments / Total experiments) × 100
```

---

## Phase 1 Implementation (MVP)
Start with these core features:
1. Database setup (database.py)
2. Home page with basic stats
3. Add Experiment page (full functionality)
4. View Experiments page (display + basic filters)
5. Simple analytics (colonization time chart)

**Skip for now:**
- Add Harvest page (Phase 2)
- Advanced analytics
- Photo uploads
- Cost tracking

---

## Phase 2 Enhancements
After MVP works:
- Add Harvest functionality
- Biological Efficiency calculations
- More detailed analytics
- Photo upload for experiments
- Export data to CSV
- Email notifications (optional)

---

## Development Steps for Claude Code

### Step 1: Initialize Project
```bash
# Create project structure
mkdir myco-logger
cd myco-logger
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install streamlit pandas matplotlib sqlite3

# Create initial files
touch app.py database.py
mkdir pages utils data
touch pages/1_📝_Add_Experiment.py
touch pages/2_📊_View_Experiments.py
touch utils/calculations.py
touch data/.gitkeep

# Create requirements.txt
pip freeze > requirements.txt
```

### Step 2: Database Setup (database.py)
Create functions:
- `init_database()` - Creates tables if they don't exist
- `add_experiment(**kwargs)` - Insert new experiment
- `get_all_experiments()` - Return all experiments as DataFrame
- `get_experiment_by_id(id)` - Get single experiment
- `update_experiment(id, **kwargs)` - Update experiment fields
- `delete_experiment(id)` - Delete experiment
- `get_experiments_by_status(status)` - Filter by status
- Connection management (context manager or helper functions)

### Step 3: Home Page (app.py)
- Import streamlit
- Set page config (title, icon, layout)
- Initialize database on first run
- Display title and description
- Query database for stats:
  - Total experiments count
  - Active experiments (status not 'done' or 'contaminated')
  - Success rate calculation
- Display stats in columns (st.columns)
- Show recent experiments in table

### Step 4: Add Experiment Page
- Create form with all required fields
- Use appropriate Streamlit input widgets:
  - st.text_input() for name
  - st.selectbox() for dropdowns
  - st.number_input() for numbers
  - st.date_input() for dates
  - st.text_area() for notes
- Validate inputs (required fields)
- On submit, call database.add_experiment()
- Show success message with st.success()
- Option to add another or view experiments

### Step 5: View Experiments Page
- Load all experiments into DataFrame
- Add filters in sidebar:
  - Status filter (multiselect)
  - Substrate type filter (multiselect)
  - Date range filter
- Display filtered table with st.dataframe()
- Add "days since inoculation" calculated column
- Make table interactive (click to expand)
- Add edit form for selected experiment
- Update database on changes

### Step 6: Basic Analytics Page
- Query experiments with colonization dates
- Group by substrate_type
- Calculate average days to colonization
- Create bar chart with matplotlib or plotly
- Display chart with st.pyplot() or st.plotly_chart()
- Add success rate pie chart
- Display summary statistics

### Step 7: Testing & Refinement
- Test all CRUD operations
- Verify data persistence
- Check edge cases (empty database, invalid inputs)
- Improve UI/UX based on usage
- Add error handling

### Step 8: Deployment (Optional)
- Push to GitHub
- Connect to Streamlit Cloud
- Deploy app
- Test in production

---

## Code Conventions
- Use snake_case for variables and functions
- Add docstrings to all functions
- Use type hints where appropriate
- Keep functions small and focused
- Commit frequently with clear messages
- Add comments for complex logic

---

## Git Workflow
```bash
# Initial commit
git init
git add .
git commit -m "Initial commit: project structure"

# Feature branches
git checkout -b feature/database-setup
# ... make changes ...
git add .
git commit -m "Add database initialization and CRUD functions"
git checkout main
git merge feature/database-setup

# Regular commits
git add .
git commit -m "Add experiment form with validation"
git push origin main
```

---

## Testing Checklist
- [ ] Database creates successfully
- [ ] Can add experiment with all fields
- [ ] Can add experiment with minimal fields
- [ ] Experiments appear in view page
- [ ] Filters work correctly
- [ ] Can update experiment status
- [ ] Can update dates (colonization, pinning)
- [ ] Can mark as contaminated
- [ ] Can delete experiment
- [ ] Stats calculate correctly
- [ ] Charts display properly
- [ ] App handles empty database gracefully
- [ ] Date validation works (no future dates)
- [ ] Required fields are enforced

---

## Future Ideas
- Multi-user support with authentication
- Mobile app version
- Barcode/QR code for experiments
- Integration with sensors (temp/humidity logging)
- Automated photo timelapse
- Recipe database for substrate mixes
- Community features (share results)
- Machine learning for contamination prediction
- Integration with climate control systems

---

## Resources
- [Streamlit Documentation](https://docs.streamlit.io)
- [SQLite Python Tutorial](https://docs.python.org/3/library/sqlite3.html)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Mushroom Cultivation Resources](https://www.shroomery.org/)
