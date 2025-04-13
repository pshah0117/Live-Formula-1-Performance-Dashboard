import streamlit as st
from data_utils import (
    get_current_driver_standings,
    get_current_constructor_standings,
    get_driver_points_by_race,
    get_qualifying_vs_race_delta,
    get_fastest_lap_times,
    get_pit_stop_data
)

import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="F1 Live Dashboard", layout="wide")
st.title("🏎️ Formula 1 2024 Live Insights Dashboard")

# DRIVER STANDINGS
st.header("👨‍💼 Driver Standings (Current Season)")
df = get_current_driver_standings()
st.dataframe(df)

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=df, x="Points", y="Driver", palette="coolwarm", ax=ax)
ax.set_title("Driver Points Standings")
st.pyplot(fig)

# CONSTRUCTOR STANDINGS
st.header("🏭 Constructor Standings (Current Season)")
team_df = get_current_constructor_standings()
st.dataframe(team_df)

fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(data=team_df, x="Points", y="Constructor", palette="viridis", ax=ax2)
ax2.set_title("Constructor Points Standings")
st.pyplot(fig2)

# POINTS PROGRESSION
st.header("📈 Driver Points Progression Over Races")
points_df = get_driver_points_by_race()
st.line_chart(points_df.set_index("Round").drop(columns="Race"))

# QUALIFYING VS RACE POSITION DELTA
st.header("🚥 Qualifying vs Race Position Delta")
delta_df = get_qualifying_vs_race_delta()
selected_driver = st.selectbox("Select a Driver", delta_df['Driver'].unique())
filtered_delta = delta_df[delta_df['Driver'] == selected_driver]

fig3, ax3 = plt.subplots(figsize=(10, 6))
sns.lineplot(data=filtered_delta, x="Round", y="Position Delta", marker="o", ax=ax3)
ax3.axhline(0, color='gray', linestyle='--')
ax3.set_title(f"Race vs Qualifying Delta: {selected_driver}")
st.pyplot(fig3)

# FASTEST LAP TIMES
st.header("⚡ Fastest Lap Times")
fastest_df = get_fastest_lap_times()
selected_race = st.selectbox("Choose Race for Fastest Lap View", sorted(fastest_df['Race'].unique(), reverse=True))
filtered_lap = fastest_df[fastest_df['Race'] == selected_race]
st.dataframe(filtered_lap)

fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(data=filtered_lap, x="Time", y="Driver", ax=ax4, palette="magma")
ax4.set_title(f"Fastest Laps - {selected_race}")
st.pyplot(fig4)

# PIT STOP ANALYSIS
st.header("⛽ Pit Stop Durations (Rounds 1–10)")
pit_df = get_pit_stop_data()
selected_round_pit = st.selectbox("Choose Round for Pit Analysis", sorted(pit_df['Round'].unique(), reverse=True))
round_pit = pit_df[pit_df['Round'] == selected_round_pit]
st.dataframe(round_pit.sort_values(by="Duration (s)"))

fig5, ax5 = plt.subplots(figsize=(10, 6))
sns.boxplot(data=round_pit, y="Driver", x="Duration (s)", ax=ax5, palette="coolwarm")
ax5.set_title(f"Pit Stop Durations — Round {selected_round_pit}")
st.pyplot(fig5)
