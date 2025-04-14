import requests
import pandas as pd

# Fetch current season year
def get_current_season():
    url = "https://ergast.com/api/f1/current.json"
    response = requests.get(url)
    data = response.json()
    season = data['MRData']['RaceTable']['season']
    return season

# Fetch current driver standings
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
def get_driver_points_progression():
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

    # Now calculate cumulative points for each driver
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
