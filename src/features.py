import random
import numpy as np
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

df = pd.read_csv(
    BASE_DIR / "data" / "results.csv",
    encoding="latin1"
)

df["date"] = pd.to_datetime(df["date"])

def get_recent_matches(team, date, n):

    matches = df[
        (
            (df["home_team"] == team) |
            (df["away_team"] == team)
        )
        &
        (df["date"] < date)
    ]

    recent_matches = matches.tail(n)

    return recent_matches

def get_avg_goals_scored(team, recent_matches):

    gf = 0

    for index, row in recent_matches.iterrows():

        if row["home_team"] == team:
            gf = gf + row["home_score"]
        else:
            gf = gf + row["away_score"]

    if recent_matches.shape[0] == 0:
        return 0
    
    goal_avg = gf / recent_matches.shape[0]

    return goal_avg

def get_avg_goals_conceded(team, recent_matches):

    ga = 0

    for index, row in recent_matches.iterrows():

        if row["home_team"] == team:
            ga = ga + row["away_score"]
        else:
            ga = ga + row["home_score"]

    if recent_matches.shape[0] == 0:
        return 0
    
    goal_avg = ga / recent_matches.shape[0]

    return goal_avg


def get_win_percentage(team, recent_matches):
    
    wins = 0

    for index, row in recent_matches.iterrows():

        if team == row["home_team"]:
            if row["home_score"] > row["away_score"]:
                wins += 1

        else:
            if row["away_score"] > row["home_score"]:
                wins += 1

    if recent_matches.shape[0] == 0:
        return 0

    win_percentage = wins / recent_matches.shape[0]

    return win_percentage


def get_avg_points_per_match(team, recent_matches):

    if recent_matches.shape[0] == 0:
        return 0

    points = 0

    for index, row in recent_matches.iterrows():

        if row["home_score"] == row["away_score"]:
            points += 1

        elif row["home_team"] == team:

            if row["home_score"] > row["away_score"]:
                points += 3

        else:

            if row["away_score"] > row["home_score"]:
                points += 3

    avg_points_per_match = points / recent_matches.shape[0]

    return avg_points_per_match

def get_avg_goal_difference(team, recent_matches):

    if recent_matches.shape[0] == 0:
        return 0

    gf = 0
    ga = 0

    for index, row in recent_matches.iterrows():

        if row["home_team"] == team:
            gf += row["home_score"]
            ga += row["away_score"]

        else:
            gf += row["away_score"]
            ga += row["home_score"]

    gd = gf - ga

    avg_goal_difference = gd / recent_matches.shape[0]

    return avg_goal_difference


def get_draw_percentage(team, recent_matches):

    if recent_matches.shape[0] == 0:
        return 0
    
    draws = 0

    for index, row in recent_matches.iterrows():

        if row["home_score"] == row["away_score"]:
            draws+=1

    draw_percentage = draws / recent_matches.shape[0]

    return draw_percentage

def get_loss_percentage(team, recent_matches):

    if recent_matches.shape[0]==0:
        return 0
    
    losses = 0

    for index, row in recent_matches.iterrows():
        if team == row["home_team"]:
            if row["home_score"]<row["away_score"]:
                losses+=1
        else:
            if row["home_score"]>row["away_score"]:
                losses+=1

    lose_percentage = losses/recent_matches.shape[0]

    return lose_percentage


def create_feature_row(row, home_recent_matches, away_recent_matches):

    # Extract match information
    home_team = row["home_team"]
    away_team = row["away_team"]

    home_score = row["home_score"]
    away_score = row["away_score"]


    # Home team features
    home_avg_gf = get_avg_goals_scored(home_team, home_recent_matches)
    home_avg_ga = get_avg_goals_conceded(home_team, home_recent_matches)
    home_avg_gd = get_avg_goal_difference(home_team, home_recent_matches)

    home_win_percentage = get_win_percentage(home_team, home_recent_matches)
    home_draw_percentage = get_draw_percentage(home_team, home_recent_matches)
    home_loss_percentage = get_loss_percentage(home_team, home_recent_matches)

    home_avg_points = get_avg_points_per_match(home_team, home_recent_matches)


    # Away team features
    away_avg_gf = get_avg_goals_scored(away_team, away_recent_matches)
    away_avg_ga = get_avg_goals_conceded(away_team, away_recent_matches)
    away_avg_gd = get_avg_goal_difference(away_team, away_recent_matches)

    away_win_percentage = get_win_percentage(away_team, away_recent_matches)
    away_draw_percentage = get_draw_percentage(away_team, away_recent_matches)
    away_loss_percentage = get_loss_percentage(away_team, away_recent_matches)

    away_avg_points = get_avg_points_per_match(away_team, away_recent_matches)


    # Create target variable
    if home_score > away_score:
        result = "Home Win"

    elif home_score < away_score:
        result = "Away Win"

    else:
        result = "Draw"


    # Return one training example
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
        "away_avg_points": away_avg_points,

        "result": result
    }

