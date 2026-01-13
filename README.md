# 🍄 Myco Logger

A Streamlit web application for tracking mushroom cultivation experiments, substrate performance, and harvest yields.

## Features

- **Experiment Tracking**: Log substrate compositions, spawn ratios, and container types
- **Progress Monitoring**: Track colonization times, pinning dates, and growth stages
- **Harvest Recording**: Document yields across multiple flushes
- **Analytics Dashboard**: Visualize colonization speeds, success rates, and biological efficiency
- **Contamination Tracking**: Record and analyze contamination patterns

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/myco-logger.git
cd myco-logger
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the Streamlit app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Project Structure

```
myco-logger/
├── app.py                    # Main application and home page
├── database.py               # SQLite database functions
├── requirements.txt          # Python dependencies
├── pages/                    # Streamlit multi-page app pages
│   ├── 1_📝_Add_Experiment.py
│   ├── 2_📊_View_Experiments.py
│   ├── 3_📈_Analytics.py
│   └── 4_🌾_Add_Harvest.py
├── utils/                    # Helper functions
│   └── calculations.py
└── data/                     # SQLite database storage
    └── mushroom_tracker.db
```

## Database Schema

### Experiments Table
- Experiment details (name, substrate type, composition)
- Spawn ratio and substrate weight
- Container information
- Key dates (inoculation, colonization, pinning)
- Status tracking and contamination notes

### Harvests Table
- Linked to experiments
- Flush number and harvest date
- Weight measurements
- Quality notes

## Key Metrics

**Biological Efficiency (BE)**
```
BE = (Total Fresh Weight Harvested / Dry Substrate Weight) × 100
```
Good oyster mushroom grows typically achieve 75-125% BE.

## Development

### Phase 1 (MVP)
- [x] Database setup
- [x] Home page with statistics
- [x] Add experiment functionality
- [x] View and filter experiments
- [x] Basic analytics

### Phase 2 (Planned)
- [ ] Harvest tracking and recording
- [ ] Biological efficiency calculations
- [ ] Advanced analytics and comparisons
- [ ] Photo uploads
- [ ] Data export (CSV)
- [ ] Cost tracking

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

Built for mushroom cultivation enthusiasts tracking their grows from spore to harvest.

## Support

For issues or questions, please open an issue on GitHub.
