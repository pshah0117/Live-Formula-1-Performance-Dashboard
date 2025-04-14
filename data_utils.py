import requests
import pandas as pd

# 1. Get current F1 season
def get_current_season():
    url = "https://ergast.com/api/f1/current.json"
    response = requests.get(url)
    data = response.json()
    season = data['MRData']['RaceTable']['season']
    return season

# 2. Get current driver standings
def get_current_driver_standings():
    url = "https://ergast.com/api/f1/current/driverStandings.json"
    response = requests.get(url)
    data = response.json()

    standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']
    
    drivers = []
    for s in standings:
        driver = s['Driver']
        constructors = s['Constructors'][0]
        drivers.append({
            'Position': int(s['position']),
            'Driver': f"{driver['givenName']} {driver['familyName']}",
            'Points': int(float(s['points'])),
            'Wins': int(s['wins']),
            'Nationality': driver['nationality'],
            'Constructor': constructors['name']
        })
        
    return pd.DataFrame(drivers)

# 3. Get current constructor standings
def get_current_constructor_standings():
    url = "https://ergast.com/api/f1/current/constructorStandings.json"
    response = requests.get(url)
    data = response.json()

    standings = data['MRData']['StandingsTable']['StandingsLists'][0]['ConstructorStandings']
    
    constructors = []
    for s in standings:
        constructor = s['Constructor']
        constructors.append({
            'Position': int(s['position']),
            'Constructor': constructor['name'],
            'Points': int(float(s['points'])),
            'Wins': int(s['wins']),
            'Nationality': constructor['nationality']
        })
        
    return pd.DataFrame(constructors)

# 4. Get driver cumulative points by race
def get_driver_points_by_race():
    url = "https://ergast.com/api/f1/current/results.json?limit=1000"
    response = requests.get(url)
    data = response.json()

    races = data['MRData']['RaceTable']['Races']
    points_tracker = {}

    for race in races:
        round_num = int(race['round'])
        race_name = race['raceName']
        for result in race['Results']:
            driver_name = f"{result['Driver']['givenName']} {result['Driver']['familyName']}"
            points = int(float(result['points']))

            if driver_name not in points_tracker:
                points_tracker[driver_name] = []

            points_tracker[driver_name].append({
                'Round': round_num,
                'Race': race_name,
                'Points': points
            })

    rounds = sorted(list({pt['Round'] for driver in points_tracker.values() for pt in driver}))
    race_names = {pt['Round']: pt['Race'] for driver in points_tracker.values() for pt in driver}

    data = {'Round': rounds, 'Race': [race_names[r] for r in rounds]}
    for driver, results in points_tracker.items():
        cumulative = 0
        driver_points = []
        result_dict = {r['Round']: r['Points'] for r in results}
        for r in rounds:
            cumulative += result_dict.get(r, 0)
            driver_points.append(cumulative)
        data[driver] = driver_points

    return pd.DataFrame(data)

# 5. Get qualifying vs race position delta for last race
def get_qualifying_vs_race_delta():
    # First, get the last race round
    last_race_url = "https://ergast.com/api/f1/current/last.json"
    race_resp = requests.get(last_race_url).json()
    round_num = race_resp['MRData']['RaceTable']['round']

    # Get race results
    race_results_url = f"https://ergast.com/api/f1/current/{round_num}/results.json"
    qual_results_url = f"https://ergast.com/api/f1/current/{round_num}/qualifying.json"

    race_data = requests.get(race_results_url).json()
    qual_data = requests.get(qual_results_url).json()

    race_pos = {}
    for res in race_data['MRData']['RaceTable']['Races'][0]['Results']:
        name = f"{res['Driver']['givenName']} {res['Driver']['familyName']}"
        race_pos[name] = int(res['position'])

    qual_pos = {}
    for res in qual_data['MRData']['RaceTable']['Races'][0]['QualifyingResults']:
        name = f"{res['Driver']['givenName']} {res['Driver']['familyName']}"
        qual_pos[name] = int(res['position'])

    deltas = []
    for driver in qual_pos:
        delta = race_pos.get(driver, None)
        if delta is not None:
            deltas.append({
                'Driver': driver,
                'Qualifying': qual_pos[driver],
                'Race': race_pos[driver],
                'Delta': qual_pos[driver] - race_pos[driver]
            })

    return pd.DataFrame(deltas)

# 6. Get fastest lap times from last race
def get_fastest_lap_times():
    url = "https://ergast.com/api/f1/current/last/results.json"
    response = requests.get(url)
    data = response.json()

    laps = []
    for res in data['MRData']['RaceTable']['Races'][0]['Results']:
        driver = res['Driver']
        name = f"{driver['givenName']} {driver['familyName']}"
        if 'FastestLap' in res:
            time = res['FastestLap']['Time']['time']
            laps.append({'Driver': name, 'Fastest Lap': time})

    return pd.DataFrame(laps)

# 7. Get pit stop data for the last race
def get_pit_stop_data():
    race_info = requests.get("https://ergast.com/api/f1/current/last.json").json()
    round_num = race_info['MRData']['RaceTable']['round']

    url = f"https://ergast.com/api/f1/current/{round_num}/pitstops.json?limit=1000"
    response = requests.get(url)
    data = response.json()

    stops = data['MRData']['RaceTable']['Races'][0]['PitStops']
    result = [{
        "Driver": s['driverId'].capitalize(),
        "Lap": int(s['lap']),
        "Stop": int(s['stop']),
        "Time": s['duration']
    } for s in stops]

    return pd.DataFrame(result)
