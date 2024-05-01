from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Read the player data
player_data = pd.read_csv('player_data.csv', encoding='latin1')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def results():
    # Get player names from the form
    player1 = request.form['player1']
    player2 = request.form['player2']

    # Filter the player data for the two players
    player1_data = player_data[player_data['Name'] == player1]
    player2_data = player_data[player_data['Name'] == player2]

    # Find common tournaments between the two players
    common_tournaments = set(player1_data['Tournament Name']).intersection(set(player2_data['Tournament Name']))

    # Initialize counters
    player1_wins = 0
    player2_wins = 0
    matches_played = 0

    # Loop through common tournaments
    for tournament in common_tournaments:
        # Check if the tournament is present in both players' data
        if (player1_data['Tournament Name'] == tournament).any() and (player2_data['Tournament Name'] == tournament).any():
            # Get the division for each player for the current tournament
            player1_division = player1_data[player1_data['Tournament Name'] == tournament]['Division'].iloc[0]
            player2_division = player2_data[player2_data['Tournament Name'] == tournament]['Division'].iloc[0]

            # Check if divisions match
            if player1_division == player2_division:
                # Get the finish position for each player for the current tournament
                player1_finish = player1_data[(player1_data['Tournament Name'] == tournament) & (player1_data['Division'] == player1_division)]['Finish Position'].iloc[0]
                player2_finish = player2_data[(player2_data['Tournament Name'] == tournament) & (player2_data['Division'] == player2_division)]['Finish Position'].iloc[0]

                # Update counters based on finish position
                if player1_finish < player2_finish:
                    player1_wins += 1
                elif player2_finish < player1_finish:
                    player2_wins += 1

                matches_played += 1

    # Prepare the results to be displayed
    result_text = f"{player1} and {player2} have played {matches_played} tournaments against each other."
    result_text += f" {player1} has won {player1_wins} times."
    result_text += f" {player2} has won {player2_wins} times."

    return render_template('results.html', result=result_text)

if __name__ == '__main__':
    app.run(debug=True)