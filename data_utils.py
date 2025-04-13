import requests
import pandas as pd

# DRIVER STANDINGS
def get_current_driver_standings():
    url = "http://ergast.com/api/f1/current/driverStandings.json"
    res = requests.get(url).json()
    standings = res['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    data = []
    for s in standings:
        driver = s['Driver']
        data.append({
            'Position': s['position'],
            'Driver': f"{driver['givenName']} {driver['familyName']}",
            'Points': int(s['points']),
            'Wins': s['wins'],
            'Nationality': driver['nationality'],
            'Constructor': s['Constructors'][0]['name']
        })
    return pd.DataFrame(data)

# CONSTRUCTOR STANDINGS
def get_current_constructor_standings():
    url = "http://ergast.com/api/f1/current/constructorStandings.json"
    res = requests.get(url).json()
    standings = res['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    data = []
    for s in standings:
        data.append({
            'Position': s['position'],
            'Constructor': s['Constructor']['name'],
            'Points': int(s['points']),
            'Wins': s['wins'],
            'Nationality': s['Constructor']['nationality']
        })
    return pd.DataFrame(data)

# POINTS BY RACE
def get_driver_points_by_race():
    points = []
    for rnd in range(1, 25):
        url = f"http://ergast.com/api/f1/current/{rnd}/driverStandings.json"
        res = requests.get(url).json()
        races = res['MRData']['StandingsTable']['StandingsLists']
        if not races:
            continue
        for s in races[0]['DriverStandings']:
            driver = s['Driver']
            points.append({
                'Round': rnd,
                'Driver': f"{driver['givenName']} {driver['familyName']}",
                'Points': float(s['points']),
                'Race': races[0]['round']
            })
    df = pd.DataFrame(points)
    df['Round'] = df['Round'].astype(int)
    return df

# QUALIFYING VS RACE
def get_qualifying_vs_race_delta():
    results = []
    for rnd in range(1, 25):
        q_url = f"http://ergast.com/api/f1/current/{rnd}/qualifying.json"
        r_url = f"http://ergast.com/api/f1/current/{rnd}/results.json"
        q_data = requests.get(q_url).json()['MRData']['RaceTable']['Races']
        r_data = requests.get(r_url).json()['MRData']['RaceTable']['Races']
        if not q_data or not r_data:
            continue
        q_results = {x['Driver']['driverId']: x['position'] for x in q_data[0]['QualifyingResults']}
        for r in r_data[0]['Results']:
            driver_id = r['Driver']['driverId']
            qual_pos = int(q_results.get(driver_id, 0))
            race_pos = int(r['position'])
            delta = qual_pos - race_pos
            results.append({
                'Round': rnd,
                'Driver': f"{r['Driver']['givenName']} {r['Driver']['familyName']}",
                'Qualifying Position': qual_pos,
                'Race Position': race_pos,
                'Position Delta': delta
            })
    return pd.DataFrame(results)

# FASTEST LAP TIMES
def get_fastest_lap_times():
    url = "http://ergast.com/api/f1/current/results.json?limit=1000"
    res = requests.get(url).json()
    races = res['MRData']['RaceTable']['Races']
    data = []
    for race in races:
        round_num = int(race['round'])
        race_name = race['raceName']
        date = race['date']
        for result in race['Results']:
            driver = result['Driver']
            if result.get('FastestLap') and result['FastestLap'].get('Time'):
                data.append({
                    'Round': round_num,
                    'Race': race_name,
                    'Date': date,
                    'Driver': f"{driver['givenName']} {driver['familyName']}",
                    'Time': result['FastestLap']['Time']['time']
                })
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# PIT STOP DATA
def get_pit_stop_data():
    all_pit_data = []
    for rnd in range(1, 11):
        url = f"http://ergast.com/api/f1/current/{rnd}/pitstops.json?limit=100"
        res = requests.get(url).json()
        stops = res['MRData']['RaceTable']['Races']
        if not stops: continue
        for stop in stops[0]['PitStops']:
            driver = stop['driverId']
            duration = float(stop['duration'])
            lap = int(stop['lap'])
            all_pit_data.append({
                'Round': rnd,
                'Driver': driver,
                'Lap': lap,
                'Duration (s)': duration
            })
    return pd.DataFrame(all_pit_data)
