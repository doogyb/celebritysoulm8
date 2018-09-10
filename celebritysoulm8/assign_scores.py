import analyse_words
import json


def assign_scores():
    db = json.load(open("db/top-handles.json", 'r'))
    i = 0
    for handle in list(db.keys()):
        if not db[handle]['Scores']:
            scores = analyse_words.query(handle[1:])
            print(handle)
            if not scores:
                print("Exiting loop now")
                break
            print((handle, scores))
            db[handle]['Scores'] = scores
            print(i)
            i += 1

    fp = open("../db/temp.json", 'w')
    json.dump(db, fp, indent=4)
    fp.close()
    fp = open("../db/top-handles.json", "w")
    json.dump(db, fp, indent=4)


def count_assigned_scores():
    db = json.load(open("../db/top-handles.json", 'r'))
    return len([x for x in list(db.values()) if not x['Scores']])


print((count_assigned_scores()))
