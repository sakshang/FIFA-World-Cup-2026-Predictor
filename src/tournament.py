import random
import pandas as pd
from src.simulation import (
    simulate_group,
    get_group_table,
    simulate_knockout_match
)

groups = {
    "A": [
        "Mexico",
        "South Africa",
        "South Korea",
        "Czechia"
    ],

    "B": [
        "Canada",
        "Bosnia and Herzegovina",
        "Qatar",
        "Switzerland"
    ],

    "C": [
        "Brazil",
        "Morocco",
        "Haiti",
        "Scotland"
    ],

    "D": [
        "United States",
        "Paraguay",
        "Australia",
        "Turkey"
    ],

    "E": [
        "Germany",
        "Curacao",
        "Ivory Coast",
        "Ecuador"
    ],

    "F": [
        "Netherlands",
        "Japan",
        "Sweden",
        "Tunisia"
    ],

    "G": [
        "Belgium",
        "Egypt",
        "Iran",
        "New Zealand"
    ],

    "H": [
        "Spain",
        "Cape Verde",
        "Saudi Arabia",
        "Uruguay"
    ],

    "I": [
        "France",
        "Senegal",
        "Iraq",
        "Norway"
    ],

    "J": [
        "Argentina",
        "Algeria",
        "Austria",
        "Jordan"
    ],

    "K": [
    "Portugal",
    "Congo DR",
    "Uzbekistan",
    "Colombia"
    ],

    "L": [
        "England",
        "Croatia",
        "Ghana",
        "Panama"
    ]
}

def generate_group_fixtures(group):

    matches = []

    for i in range(len(group)):

        for j in range(i + 1, len(group)):

            matches.append(
                (group[i], group[j])
            )

    return matches

all_group_results = {}
all_group_tables = {}

for group_name, teams in groups.items():

    fixtures = generate_group_fixtures(teams)

    results = simulate_group(
        fixtures,
        "2026-06-11"
    )

    table = get_group_table(
        teams,
        results
    )

    all_group_results[group_name] = results
    all_group_tables[group_name] = table

for group_name, table in all_group_tables.items():

    print(f"\n========== GROUP {group_name} ==========")

    print(table)

def get_qualified_teams(all_group_tables):

    qualified = []

    for group_name, table in all_group_tables.items():

        first_place = table.index[0]
        second_place = table.index[1]

        qualified.append({
            "team": first_place,
            "group": group_name,
            "position": 1,
            "Pts": table.loc[first_place, "Pts"],
            "GD": table.loc[first_place, "GD"],
            "GF": table.loc[first_place, "GF"]
        })

        qualified.append({
            "team": second_place,
            "group": group_name,
            "position": 2,
            "Pts": table.loc[second_place, "Pts"],
            "GD": table.loc[second_place, "GD"],
            "GF": table.loc[second_place, "GF"]
        })

    third_place_teams = []

    for group_name, table in all_group_tables.items():

        third_place = table.index[2]

        third_place_teams.append({
            "team": third_place,
            "group": group_name,
            "position": 3,
            "Pts": table.loc[third_place, "Pts"],
            "GD": table.loc[third_place, "GD"],
            "GF": table.loc[third_place, "GF"]
        })

    third_place_teams = sorted(
        third_place_teams,
        key=lambda x: (
            x["Pts"],
            x["GD"],
            x["GF"]
        ),
        reverse=True
    )

    qualified.extend(third_place_teams[:8])

    return pd.DataFrame(qualified)

qualified_teams = get_qualified_teams(all_group_tables)

qualified_lookup = {}

for _, row in qualified_teams.iterrows():
    key = f"{row['group']}{row['position']}"
    qualified_lookup[key] = row["team"]

third_place_teams = [
    row["team"]
    for _, row in qualified_teams.iterrows()
    if row["position"] == 3
]

random.shuffle(third_place_teams)

print("\n========== QUALIFIED TEAMS ==========")
print(qualified_teams)
print(f"\nTotal qualified teams: {len(qualified_teams)}")

round_of_32 = {
    "Match 73": (qualified_lookup["A2"], qualified_lookup["B2"]),
    "Match 75": (qualified_lookup["F1"], qualified_lookup["C2"]),
    "Match 76": (qualified_lookup["C1"], qualified_lookup["F2"]),
    "Match 78": (qualified_lookup["E2"], qualified_lookup["I2"]),
    "Match 83": (qualified_lookup["K2"], qualified_lookup["L2"]),
    "Match 84": (qualified_lookup["H1"], qualified_lookup["J2"]),
    "Match 86": (qualified_lookup["J1"], qualified_lookup["H2"]),
    "Match 88": (qualified_lookup["D2"], qualified_lookup["G2"])
}

third_place_match_numbers = [
    "Match 74",
    "Match 77",
    "Match 79",
    "Match 80",
    "Match 81",
    "Match 82",
    "Match 85",
    "Match 87"
]

third_place_opponents = [
    qualified_lookup["E1"],
    qualified_lookup["I1"],
    qualified_lookup["A1"],
    qualified_lookup["L1"],
    qualified_lookup["D1"],
    qualified_lookup["G1"],
    qualified_lookup["B1"],
    qualified_lookup["K1"]
]

for match_number, opponent, third_place_team in zip(
    third_place_match_numbers,
    third_place_opponents,
    third_place_teams
):
    round_of_32[match_number] = (
        opponent,
        third_place_team
    )

round_of_32_results = {}

for match_number, teams in round_of_32.items():

    home_team, away_team = teams

    result = simulate_knockout_match(
        home_team,
        away_team,
        "2026-06-30"
    )

    round_of_32_results[match_number] = result

    if result["penalty_score"] is not None:

        print(
        f"{match_number}: "
        f"{home_team} {result['home_score']} - "
        f"{result['away_score']} {away_team} "
        f"→ {result['winner']} "
        f"({result['penalty_score'][0]}-{result['penalty_score'][1]} pens)"
    )

    else:

        print(
            f"{match_number}: "
            f"{home_team} {result['home_score']} - "
            f"{result['away_score']} {away_team} "
            f"→ {result['winner']}"
    )

round_of_16 = {
    "Match 89": (
        round_of_32_results["Match 73"]["winner"],
        round_of_32_results["Match 74"]["winner"]
    ),

    "Match 90": (
        round_of_32_results["Match 75"]["winner"],
        round_of_32_results["Match 76"]["winner"]
    ),

    "Match 91": (
        round_of_32_results["Match 77"]["winner"],
        round_of_32_results["Match 78"]["winner"]
    ),

    "Match 92": (
        round_of_32_results["Match 79"]["winner"],
        round_of_32_results["Match 80"]["winner"]
    ),

    "Match 93": (
        round_of_32_results["Match 81"]["winner"],
        round_of_32_results["Match 82"]["winner"]
    ),

    "Match 94": (
        round_of_32_results["Match 83"]["winner"],
        round_of_32_results["Match 84"]["winner"]
    ),

    "Match 95": (
        round_of_32_results["Match 85"]["winner"],
        round_of_32_results["Match 86"]["winner"]
    ),

    "Match 96": (
        round_of_32_results["Match 87"]["winner"],
        round_of_32_results["Match 88"]["winner"]
    )
}

round_of_16_results = {}

for match_number, teams in round_of_16.items():

    home_team, away_team = teams

    result = simulate_knockout_match(
        home_team,
        away_team,
        "2026-07-04"
    )

    round_of_16_results[match_number] = result

    if result["penalty_score"] is not None:

        print(
        f"{match_number}: "
        f"{home_team} {result['home_score']} - "
        f"{result['away_score']} {away_team} "
        f"→ {result['winner']} "
        f"({result['penalty_score'][0]}-{result['penalty_score'][1]} pens)"
    )

    else:

        print(
        f"{match_number}: "
        f"{home_team} {result['home_score']} - "
        f"{result['away_score']} {away_team} "
        f"→ {result['winner']}"
    )

quarter_finals = {
    "Match 97": (
        round_of_16_results["Match 89"]["winner"],
        round_of_16_results["Match 90"]["winner"]
    ),

    "Match 98": (
        round_of_16_results["Match 91"]["winner"],
        round_of_16_results["Match 92"]["winner"]
    ),

    "Match 99": (
        round_of_16_results["Match 93"]["winner"],
        round_of_16_results["Match 94"]["winner"]
    ),

    "Match 100": (
        round_of_16_results["Match 95"]["winner"],
        round_of_16_results["Match 96"]["winner"]
    )
}

quarter_final_results = {}

for match_number, teams in quarter_finals.items():

    home_team, away_team = teams

    result = simulate_knockout_match(
        home_team,
        away_team,
        "2026-07-09"
    )

    quarter_final_results[match_number] = result

    if result["penalty_score"] is not None:

        print(
        f"{match_number}: "
        f"{home_team} {result['home_score']} - "
        f"{result['away_score']} {away_team} "
        f"→ {result['winner']} "
        f"({result['penalty_score'][0]}-{result['penalty_score'][1]} pens)"
    )

    else:

        print(
        f"{match_number}: "
        f"{home_team} {result['home_score']} - "
        f"{result['away_score']} {away_team} "
        f"→ {result['winner']}"
    )

semi_finals = {
    "Match 101": (
        quarter_final_results["Match 97"]["winner"],
        quarter_final_results["Match 98"]["winner"]
    ),

    "Match 102": (
        quarter_final_results["Match 99"]["winner"],
        quarter_final_results["Match 100"]["winner"]
    )
}

semi_final_results = {}

for match_number, teams in semi_finals.items():

    home_team, away_team = teams

    result = simulate_knockout_match(
        home_team,
        away_team,
        "2026-07-11"
    )

    semi_final_results[match_number] = result

    if result["penalty_score"] is not None:

        print(
        f"{match_number}: "
        f"{home_team} {result['home_score']} - "
        f"{result['away_score']} {away_team} "
        f"→ {result['winner']} "
        f"({result['penalty_score'][0]}-{result['penalty_score'][1]} pens)"
    )

    else:

        print(
        f"{match_number}: "
        f"{home_team} {result['home_score']} - "
        f"{result['away_score']} {away_team} "
        f"→ {result['winner']}"
    )

third_place_match = (
    semi_finals["Match 101"][0]
    if semi_final_results["Match 101"]["winner"] == semi_finals["Match 101"][1]
    else semi_finals["Match 101"][1],

    semi_finals["Match 102"][0]
    if semi_final_results["Match 102"]["winner"] == semi_finals["Match 102"][1]
    else semi_finals["Match 102"][1]
)

final_match = (
    semi_final_results["Match 101"]["winner"],
    semi_final_results["Match 102"]["winner"]
)

third_place_result = simulate_knockout_match(
    third_place_match[0],
    third_place_match[1],
    "2026-07-18"
)

final_result = simulate_knockout_match(
    final_match[0],
    final_match[1],
    "2026-07-19"
)

if third_place_result["penalty_score"] is not None:

    print(
        f"\nTHIRD PLACE: "
        f"{third_place_match[0]} {third_place_result['home_score']} - "
        f"{third_place_result['away_score']} {third_place_match[1]} "
        f"→ {third_place_result['winner']} "
        f"({third_place_result['penalty_score'][0]}-"
        f"{third_place_result['penalty_score'][1]} pens)"
    )

else:

    print(
        f"\nTHIRD PLACE: "
        f"{third_place_match[0]} {third_place_result['home_score']} - "
        f"{third_place_result['away_score']} {third_place_match[1]} "
        f"→ {third_place_result['winner']}"
    )

if final_result["penalty_score"] is not None:

    print(
        f"\n🏆 FINAL: "
        f"{final_match[0]} {final_result['home_score']} - "
        f"{final_result['away_score']} {final_match[1]} "
        f"→ {final_result['winner']} "
        f"({final_result['penalty_score'][0]}-"
        f"{final_result['penalty_score'][1]} pens)"
    )

else:

    print(
        f"\n🏆 FINAL: "
        f"{final_match[0]} {final_result['home_score']} - "
        f"{final_result['away_score']} {final_match[1]} "
        f"→ {final_result['winner']}"
    )

