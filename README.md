Live-Formula-1-Performance-Dashboard
🏎️ Formula 1 Live Dashboard (Streamlit + Jolpica F1 API)
This project is a real-time Formula 1 dashboard built with Streamlit and powered by the Jolpica F1 API (a wrapper over the Ergast API that supports current and future seasons like 2025).

🚀 Features
Live Driver Standings with points, wins, nationality, and team

Live Constructor Standings

Points Progression for each driver across all races

Qualifying vs Race Position Delta for the latest race

Fastest Lap Times in the most recent Grand Prix

Pit Stop Summary including lap, stop count, and duration

🛠️ Run Locally
bash
Copy
Edit
pip install -r requirements.txt
streamlit run app.py
📡 API Used
Jolpica F1 API – A live, hosted mirror of the Ergast API, updated for 2025 and beyond.

📁 Project Structure
bash
Copy
Edit
├── app.py               # Streamlit app
├── data_utils.py        # Data-fetching utility functions
├── requirements.txt     # Dependencies
└── README.md            # Project info
