import similarity_measure
import json
import itertools


def global_comparison(write_to_file=False):
    # Find the highest similarity between the 1000 twitter users
    db = json.load(open("../db/english-users.json"))
    rankings = {}

    for handle in db.keys():
        rankings[handle] = {}
    for handle, other_handle in itertools.combinations(db.keys(), 2):
        rankings[handle][other_handle] = similarity_measure.\
            difference(db[handle]["scores"], db[other_handle]["scores"])

    if write_to_file:
        fp = open("../db/comparisons.json", 'w')
        print "writing dictionary comparisons to file"
        json.dump(rankings, fp, indent=4)

    return rankings


def find_most_similar(score):
    db = json.load(open("../db/handles/english-users.json"))

    max_score = 0
    max_handle = ""

    for handle, handle_values in zip(db.keys(), db.values()):
        similarity_score = similarity_measure.difference(score, handle_values['scores'])
        if similarity_score > max_score:
            max_score = similarity_score
            max_handle = handle

    return max_handle


def db_as_list():
    db = json.load(open("../db/comparisons.json"))
    # save the dictionary format as a list of triples, with
    # handles as first pair and corresponding score as second

    list_form = []

    for key in db.keys():
        for name, measure in zip(db[key].keys(), db[key].values()):
            list_form.append((key, name, measure))

    return list_form


def order_by_similarity(write_to_file=False):

    list_form = db_as_list()
    list_form.sort(key=lambda x: x[2])

    if write_to_file:
        fp = open("../db/ordered_comparisons.json", 'w')
        json.dump(list_form, fp, indent=4)
        print "Writing ordered list to file"

    return list_form


def recalculate_lists():
    global_comparison(True)
    order_by_similarity(True)
