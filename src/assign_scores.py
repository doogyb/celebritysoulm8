import analyse_words
import json


def assign_scores():
    db = json.load(open("../db/top-1000-handles.json", 'r'))
    i = 0
    for handle in db.keys():
        scores = analyse_words.query(handle[1:])
        db[handle]['Scores'] = scores
        print i
        i += 1


    fp = open("../db/temp.json", 'w')
    json.dump(db, fp, indent=4)

assign_scores()