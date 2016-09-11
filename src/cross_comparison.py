import similarity_measure
import json


def global_comparison():
    # Find the highest similarity between the 1000 twitter users
    db = json.load(open("../db/top-1000-handles.json"))
    rankings = {}

    for handle in db.keys():
        for other_handle in db.keys():
            if handle is not other_handle:
                rankings[handle][other_handle] = similarity_measure.\
                    difference(db[handle]["Score"], db[other_handle]["Score"])

    print rankings

global_comparison()

