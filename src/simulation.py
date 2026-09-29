import random
import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from src.features import (
    get_recent_matches,
    get_avg_goals_scored,
    get_avg_goals_conceded,
    get_avg_goal_difference,
    get_win_percentage,
    get_draw_percentage,
    get_loss_percentage,
    get_avg_points_per_match
)

RECENT_MATCHES = 10

team_name_mapping = {
    "South Korea": "Korea Republic",
    "United States": "USA",
    "Turkey": "Turkiye",
    "Curacao": "Curcao",
    "Ivory Coast": "Cote d'Ivoire",
    "Iran": "IR Iran",
    "New Zealand": "Aotearoa New Zealand",
    "Cape Verde": "Cabo Verde"
}


BASE_DIR = Path(__file__).resolve().parent.parent

best_model = joblib.load(
    BASE_DIR / "models" / "best_model.pkl"
)

def get_dataset_team_name(team):
    return team_name_mapping.get(team, team)

def create_prediction_features(home_team, away_team, date):

    # Convert display names to dataset names
    home_team_data = get_dataset_team_name(home_team)
    away_team_data = get_dataset_team_name(away_team)


    # Get recent matches
    home_recent_matches = get_recent_matches(
        home_team_data,
        date,
        RECENT_MATCHES
    )

    away_recent_matches = get_recent_matches(
        away_team_data,
        date,
        RECENT_MATCHES
    )


    # Check if enough matches exist
    if (
        len(home_recent_matches) < RECENT_MATCHES
        or
        len(away_recent_matches) < RECENT_MATCHES
    ):
        return None


    # Home team features
    home_avg_gf = get_avg_goals_scored(
        home_team_data,
        home_recent_matches
    )

    home_avg_ga = get_avg_goals_conceded(
        home_team_data,
        home_recent_matches
    )

    home_avg_gd = get_avg_goal_difference(
        home_team_data,
        home_recent_matches
    )

    home_win_percentage = get_win_percentage(
        home_team_data,
        home_recent_matches
    )

    home_draw_percentage = get_draw_percentage(
        home_team_data,
        home_recent_matches
    )

    home_loss_percentage = get_loss_percentage(
        home_team_data,
        home_recent_matches
    )

    home_avg_points = get_avg_points_per_match(
        home_team_data,
        home_recent_matches
    )


    # Away team features
    away_avg_gf = get_avg_goals_scored(
        away_team_data,
        away_recent_matches
    )

    away_avg_ga = get_avg_goals_conceded(
        away_team_data,
        away_recent_matches
    )

    away_avg_gd = get_avg_goal_difference(
        away_team_data,
        away_recent_matches
    )

    away_win_percentage = get_win_percentage(
        away_team_data,
        away_recent_matches
    )

    away_draw_percentage = get_draw_percentage(
        away_team_data,
        away_recent_matches
    )

    away_loss_percentage = get_loss_percentage(
        away_team_data,
        away_recent_matches
    )

    away_avg_points = get_avg_points_per_match(
        away_team_data,
        away_recent_matches
    )


    return {
        "home_avg_gf": home_avg_gf,
        "home_avg_ga": home_avg_ga,
        "home_avg_gd": home_avg_gd,
        "home_win_percentage": home_win_percentage,
        "home_draw_percentage": home_draw_percentage,
        "home_loss_percentage": home_loss_percentage,
        "home_avg_points": home_avg_points,

        "away_avg_gf": away_avg_gf,
        "away_avg_ga": away_avg_ga,
        "away_avg_gd": away_avg_gd,
        "away_win_percentage": away_win_percentage,
        "away_draw_percentage": away_draw_percentage,
        "away_loss_percentage": away_loss_percentage,
        "away_avg_points": away_avg_points
    }

def simulate_score(result, probabilities):

    home_win_prob = probabilities[
        list(best_model.classes_).index("Home Win")
    ]

    draw_prob = probabilities[
        list(best_model.classes_).index("Draw")
    ]

    away_win_prob = probabilities[
        list(best_model.classes_).index("Away Win")
    ]

    if result == "Home Win":

        if home_win_prob > 0.65:
            home_score = np.random.choice([1, 2, 3], p=[0.25, 0.50, 0.25])
            away_score = np.random.choice([0, 1], p=[0.70, 0.30])

        else:
            home_score = np.random.choice([1, 2, 3], p=[0.40, 0.45, 0.15])
            away_score = np.random.choice([0, 1, 2], p=[0.55, 0.35, 0.10])

            if home_score <= away_score:
                home_score = away_score + 1

    elif result == "Away Win":

        if away_win_prob > 0.65:
            away_score = np.random.choice([1, 2, 3], p=[0.25, 0.50, 0.25])
            home_score = np.random.choice([0, 1], p=[0.70, 0.30])

        else:
            away_score = np.random.choice([1, 2, 3], p=[0.40, 0.45, 0.15])
            home_score = np.random.choice([0, 1, 2], p=[0.55, 0.35, 0.10])

            if away_score <= home_score:
                away_score = home_score + 1

    else:  # Draw

        home_score = np.random.choice([0, 1, 2], p=[0.30, 0.50, 0.20])
        away_score = home_score

    return home_score, away_score


def simulate_match(home_team, away_team, date):

    # Create features for the match
    features = create_prediction_features(
        home_team,
        away_team,
        date
    )

    # If features cannot be created
    if features is None:
        return None

    # Convert features into a DataFrame
    features_df = pd.DataFrame([features])

    # Get probabilities for each possible result
    probabilities = best_model.predict_proba(features_df)[0]

    # Get the class names
    classes = best_model.classes_

    # Simulate one result using the probabilities
    result = np.random.choice(
        classes,
        p=probabilities
    )

    # Generate a score that matches the result
    home_score, away_score = simulate_score(
    result,
    probabilities
    )

    return {
        "result": result,
        "home_score": home_score,
        "away_score": away_score
    }


def predict_match(home_team, away_team, date):

    # Create features
    features = create_prediction_features(
        home_team,
        away_team,
        date
    )

    if features is None:
        print("Not enough previous matches.")
        return


    # Convert dictionary to DataFrame
    features_df = pd.DataFrame([features])


    # Predict result
    prediction = best_model.predict(features_df)[0]


    # Predict probabilities
    probabilities = best_model.predict_proba(features_df)[0]


    # Class names
    classes = best_model.classes_


    print(f"\n{home_team} vs {away_team}\n")

    for cls, prob in zip(classes, probabilities):

        if cls == "Home Win":
            print(f"{home_team} Win : {prob*100:.2f}%")

        elif cls == "Away Win":
            print(f"{away_team} Win : {prob*100:.2f}%")

        else:
            print(f"Draw : {prob*100:.2f}%")

    print()

    if prediction == "Home Win":
        print(f"Predicted Winner: {home_team}")

    elif prediction == "Away Win":
        print(f"Predicted Winner: {away_team}")

    else:
        print("Predicted Result: Draw")


def simulate_group(fixtures, date):

    results = []

    for home_team, away_team in fixtures:

        match_result = simulate_match(
            home_team,
            away_team,
            date
        )

        if match_result is None:
            continue

        results.append({
            "home_team": home_team,
            "away_team": away_team,
            "result": match_result["result"],
            "home_score": match_result["home_score"],
            "away_score": match_result["away_score"]
        })

    return results


def simulate_knockout_match(
    home_team,
    away_team,
    date
):

    result = simulate_match(
        home_team,
        away_team,
        date
    )

    home_score = result["home_score"]
    away_score = result["away_score"]

    penalty_score = None

    # Winner after 90 minutes
    if home_score > away_score:
        winner = home_team

    elif away_score > home_score:
        winner = away_team

    # Draw after 90 minutes
    else:

        # Extra time
        home_score += np.random.choice([0, 1])
        away_score += np.random.choice([0, 1])

        # Winner after extra time
        if home_score > away_score:
            winner = home_team

        elif away_score > home_score:
            winner = away_team

        # Still draw -> penalty shootout
        else:

            home_penalties = np.random.randint(3, 6)
            away_penalties = np.random.randint(3, 6)

            while home_penalties == away_penalties:
                away_penalties = np.random.randint(3, 6)

            penalty_score = (
                home_penalties,
                away_penalties
            )

            if home_penalties > away_penalties:
                winner = home_team
            else:
                winner = away_team

    return {
        "home_team": home_team,
        "away_team": away_team,
        "home_score": home_score,
        "away_score": away_score,
        "penalty_score": penalty_score,
        "winner": winner
    }

def create_group_standings(teams, results):

    standings = {}

    # Create starting statistics for every team
    for team in teams:
        standings[team] = {
            "P": 0,
            "W": 0,
            "D": 0,
            "L": 0,
            "GF": 0,
            "GA": 0,
            "GD": 0,
            "Pts": 0
        }

    # Process every match
    for match in results:

        home_team = match["home_team"]
        away_team = match["away_team"]

        result = match["result"]

        home_score = match["home_score"]
        away_score = match["away_score"]

        # Matches played
        standings[home_team]["P"] += 1
        standings[away_team]["P"] += 1

        # Goals scored
        standings[home_team]["GF"] += home_score
        standings[away_team]["GF"] += away_score

        # Goals conceded
        standings[home_team]["GA"] += away_score
        standings[away_team]["GA"] += home_score

        # Match result
        if result == "Home Win":

            standings[home_team]["W"] += 1
            standings[away_team]["L"] += 1
            standings[home_team]["Pts"] += 3

        elif result == "Away Win":

            standings[away_team]["W"] += 1
            standings[home_team]["L"] += 1
            standings[away_team]["Pts"] += 3

        elif result == "Draw":

            standings[home_team]["D"] += 1
            standings[away_team]["D"] += 1

            standings[home_team]["Pts"] += 1
            standings[away_team]["Pts"] += 1

    # Calculate goal difference
    for team in teams:
        standings[team]["GD"] = (
            standings[team]["GF"] -
            standings[team]["GA"]
        )

    return standings

def get_group_table(teams, results):

    standings = create_group_standings(
        teams,
        results
    )

    table = pd.DataFrame(standings).T

    table = table.sort_values(
        by=["Pts", "GD", "GF"],
        ascending=[False, False, False]
    )

    return table
