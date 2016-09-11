import similarity_measure
import json
import itertools


def global_comparison():
    # Find the highest similarity between the 1000 twitter users
    db = json.load(open("../db/top-1000-handles.json"))
    rankings = {}

    # for handle in db.keys():
    #     rankings[handle] = {}
    #     for other_handle in db.keys():
    #         if other_handle not in rankings[handle] and not handle is other_handle:
    #             rankings[handle][other_handle] = similarity_measure.\
    #                  difference(db[handle]["Scores"], db[other_handle]["Scores"])

    for handle in db.keys():
        rankings[handle] = {}
    for handle, other_handle in itertools.combinations(db.keys(), 2):
        rankings[handle][other_handle] = similarity_measure.\
            difference(db[handle]["Scores"], db[other_handle]["Scores"])

    fp = open("../db/comparisons.json", 'w')
    print "writing to file"
    json.dump(rankings, fp, indent=4)

def find_most_similar():
    db = json.load(open("../db/comparisons.json"))
    max = 0
    for key in db.keys():
        for name, measure in zip(db[key].keys(), db[key].values()):
            if measure > max:
                max = measure
                pair = name + " : " + key + " ->  " + str(measure)

    return pair

print find_most_similar()

