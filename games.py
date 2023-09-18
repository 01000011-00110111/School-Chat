
# from flask_socketio import emit

# @socketio.on('update_score')
# def update_score(score):
#     emit('score_updated', score, broadcast=True)

# @socketio.on('update_top_scores')
# def update_top_scores(score):
#     # print(top_scores)
#     top_scores.append(score)
#     emit('top_scores_updated', top_scores)

# @socketio.on('connect_game')
# def connect():
#     # print('Client connected')
#     emit('top_scores_updated', top_scores)