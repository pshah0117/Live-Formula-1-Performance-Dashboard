**🏎️ Live Formula 1 Performance Dashboard**
Built with Streamlit & Jolpica F1 API
A real-time Formula 1 dashboard that delivers live insights into drivers, constructors, race stats, and performance trends — all in one place.

🚦 Overview

This dashboard provides up-to-date Formula 1 data using the Jolpica F1 API, a live-hosted and future-compatible version of the Ergast API that includes 2025 season data and beyond.

📊 Key Features

🧑‍✈️ Driver Standings – Position, points, wins, nationality, and constructor

🏭 Constructor Standings – Position, points, wins, nationality

📈 Driver Points Progression – Cumulative race-by-race comparison

🔄 Qualifying vs Race Position Delta – For the most recent race

⚡ Fastest Lap Times – Per driver in the latest Grand Prix

🛑 Pit Stop Summary – Lap-wise pit stop data with durations

🛠️ Run Locally
bash
Copy
Edit
# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
📦 Project Structure
graphql
Copy
Edit
📁 Live-Formula-1-Performance-Dashboard
├── app.py               # Main Streamlit app
├── data_utils.py        # API data fetching & transformation functions
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
📡 API Reference
Jolpica F1 API –
🔗 https://api.jolpi.ca
A hosted version of the Ergast Developer API with added support for the latest F1 seasons.
