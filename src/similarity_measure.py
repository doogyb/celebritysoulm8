from math import sqrt


def adjust_scale(vector):
    return [x - 50 for x in vector]


def normalize(vector):
    length = sqrt(sum([x**2 for x in vector]))
    return [x/length for x in vector]


def score_to_normalized_vector(score):
    # score is a dictionary with emotional styles as string keys and the values as integers
    return normalize(adjust_scale(list(score.values())))


def difference(score1, score2):
    score1 = score_to_normalized_vector(score1)
    score2 = score_to_normalized_vector(score2)

    diff = 0
    for i in range(len(score1)):
        diff += score1[i] * score2[i]

    return diff
