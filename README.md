# Sorare Backend

## Overview
A backend system for exploration, data extraction, and predictive modeling with Sorare NFT football cards data. This project provides tools to query the Sorare API for players, clubs, competitions, and card information, and includes models for price prediction.

## Features
- Extract player data from Sorare platform
- Fetch card information for specific players across different rarities
- Gather price history and statistics for Sorare cards
- Collect So5 scores and player performance data
- Support for major football competitions (Bundesliga, Ligue 1, La Liga, Serie A)
- Price prediction models for Sorare cards

## Project Structure
```
sorare-backend/
├── get_data/                 # Data extraction module
│   ├── main.py               # Main extraction functions
│   └── query_functions/      # GraphQL query functions for the Sorare API
├── models/                   # Predictive models
│   └── price_prediction/     # Price prediction algorithms
└── requirements.txt          # Project dependencies
```

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/sorare-backend.git
cd sorare-backend
```

2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

## Usage

### Extracting Player Data from a Club
```python
from get_data.query_functions.get_functions import get_players_from_club

# Get players from a specific club
players = get_players_from_club(club_slug="manchester-united")
```

### Getting All Cards for a Player
```python
from get_data.query_functions.get_functions import get_all_cards_from_player

# Get all limited cards for a player
cards = get_all_cards_from_player(
    player_slug="cristiano-ronaldo", 
    rarity_list="[limited]"
)
```

### Extracting Data for an Entire Competition
```python
from get_data.main import get_df_all_players_info_from_competition

# Get data for all players in a competition
df = get_df_all_players_info_from_competition(
    competition_slug="ligue-1-fr", 
    rarity_list="[limited]",
    verbose=True
)

# Save the results
df.to_csv("results_ligue1_limited.csv")
```

## License
[MIT License](LICENSE)

## Acknowledgements
- [Sorare](https://sorare.com/) for their API
- All contributors to this project
