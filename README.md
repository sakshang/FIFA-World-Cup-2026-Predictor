# FIFA World Cup 2026 Predictor ⚽

A machine learning project that uses historical international football match data to predict match outcomes and simulate an entire FIFA World Cup-style tournament.

The project combines a Random Forest classification model with a tournament simulation engine to simulate group stages, qualification, knockout rounds, extra time, penalty shootouts, and the final.

> **Current Version: V1 — Baseline Model**

---

## 📌 Project Overview

The goal of this project is to explore how machine learning can be applied to football match prediction and tournament simulation.

For V1, the model uses historical team performance to estimate the probability of three possible match outcomes:

- Home Win
- Draw
- Away Win

These predictions are then used by a simulation engine to generate a complete tournament.

Each tournament simulation is stochastic, meaning that different simulations can produce different results.

---

## 🧠 Machine Learning Model

### Algorithm

**Random Forest Classifier**

The model was selected using GridSearchCV with 5-fold cross-validation.

### Hyperparameters

    n_estimators = 500
    max_depth = 10
    random_state = 42

### Model Performance

| Metric | Result |
|---|---:|
| Cross-validation accuracy | **53.44%** |
| Test accuracy | **53.34%** |

The test set was created using an 80/20 train-test split with `random_state=42`.

---

## 📊 Features

V1 uses the most recent 10 historical matches available for each team.

For both teams in a match, the following features are calculated:

1. Average goals scored
2. Average goals conceded
3. Average goal difference
4. Win percentage
5. Draw percentage
6. Loss percentage
7. Average points per match

This gives the model:

**7 features × 2 teams = 14 features**

### Feature Structure

    Home Team
    ├── Average Goals Scored
    ├── Average Goals Conceded
    ├── Average Goal Difference
    ├── Win Percentage
    ├── Draw Percentage
    ├── Loss Percentage
    └── Average Points Per Match

    Away Team
    ├── Average Goals Scored
    ├── Average Goals Conceded
    ├── Average Goal Difference
    ├── Win Percentage
    ├── Draw Percentage
    ├── Loss Percentage
    └── Average Points Per Match

Only matches occurring before the simulated match date are used when calculating historical features.

---

## 🏆 Tournament Simulation

The project goes beyond predicting individual matches.

The simulation engine generates a complete tournament consisting of group stages and knockout rounds.

### Group Stage

The V1 tournament structure contains:

- 12 groups
- 4 teams per group
- 6 matches per group
- 48 teams in total

Group tables are calculated using:

- Points
- Goal difference
- Goals scored

The top two teams from each group qualify automatically.

The 8 best third-placed teams also qualify.

This produces:

**32 knockout-stage teams**

### Knockout Stage

The simulation then runs:

    Round of 32
          ↓
    Round of 16
          ↓
    Quarter-finals
          ↓
    Semi-finals
          ↓
    Third-place Match
          ↓
    Final

### Knockout Match Rules

If a knockout match is level after 90 minutes:

1. Extra time is simulated.
2. If the match is still level, a penalty shootout is simulated.
3. A winner is selected.

---

## 📁 Project Structure

    FIFA World Cup 2026 Predictor/
    │
    ├── app/
    │
    ├── data/
    │   ├── results.csv
    │   └── training_df.csv
    │
    ├── models/
    │   └── best_model.pkl
    │
    ├── notebooks/
    │   └── fifa_prediction.ipynb
    │
    ├── src/
    │   ├── features.py
    │   ├── simulation.py
    │   └── tournament.py
    │
    ├── .gitignore
    ├── requirements.txt
    └── README.md

---

## 🔧 Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Joblib
- Jupyter Notebook
- Git
- GitHub

---

## ▶️ How to Run

### 1. Clone the repository

    git clone https://github.com/sakshang/FIFA-World-Cup-2026-Predictor.git
    cd FIFA-World-Cup-2026-Predictor

### 2. Install dependencies

    pip install -r requirements.txt

### 3. Run the tournament simulation

    python -m src.tournament

A complete tournament simulation will then be generated in the terminal.

---

## 📈 Example Simulation

A single simulation can produce a result such as:

    Match 101: Scotland 1 - 2 France → France
    Match 102: Algeria 2 - 1 Belgium → Algeria

    THIRD PLACE: Scotland 2 - 0 Belgium → Scotland

    🏆 FINAL: France 1 - 0 Algeria → France

The result above is **one random simulation** and should not be interpreted as a prediction of the actual tournament winner.

Running the simulation again can produce different results because match outcomes are sampled probabilistically.

---

## ⚠️ V1 Limitations

V1 is intentionally a relatively simple baseline model.

The current feature set does not include several factors that can influence football matches, such as:

- FIFA rankings
- Elo ratings
- Opponent-adjusted team strength
- Expected goals (xG)
- Shots
- Shots on target
- Possession
- Corners
- Set-piece performance
- Player-level information
- Squad strength
- Injuries and suspensions
- Tactical or formation information

The tournament qualification and tiebreaking logic is also a simplified implementation rather than a complete reproduction of every official FIFA tournament rule.

These limitations provide the foundation for future versions of the project.

---

## 🚀 Future Development — V2

The next version will focus on improving the quality and realism of the predictions by introducing richer football data.

Potential V2 features include:

- Elo ratings
- FIFA rankings
- Opponent-adjusted recent form
- Home/neutral venue information
- Expected goals (xG)
- Shots and shots on target
- Possession
- Corners
- Additional match statistics
- Player and squad information
- More recent football data

The objective of V2 is not simply to add more features, but to test whether these features provide measurable improvements over the V1 baseline.

---

## 📚 Dataset

V1 is based on the **International Football Matches 1872–Present** dataset.

The historical match data is used to calculate team performance statistics and construct the training dataset.

---

## 👨‍💻 Author

**Sakshang Singh**

B.Tech CSE — AI

This project is being developed as a hands-on machine learning project to explore football analytics, predictive modelling, and tournament simulation.