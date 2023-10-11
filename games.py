

def leaderboard(scores):
    # Initialize a dictionary to store the best scores for each user
    leaderboard = []
    
    # Parse the scores and update the leaderboard
    for score in scores:
        username, user_score = score.split(": ")
        user_score = int(user_score)

        # Check if the user is already in the leaderboard and update if necessary
        user_exists = False
        for entry in leaderboard:
            if entry[0] == username:
                user_exists = True
                if user_score > entry[1]:
                    entry[1] = user_score
                break

        if not user_exists:
            leaderboard.append([username, user_score])

    # Sort the leaderboard by scores in descending order
    sorted_leaderboard = sorted(leaderboard, key=lambda x: x[1], reverse=True)

    # Create an array of strings for the leaderboard
    return_array = [f"{user}: {score}" for user, score in sorted_leaderboard]

    return return_array
