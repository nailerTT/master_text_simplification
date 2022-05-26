import csv

header_list = ["s_id","sentence"]

data_list = [
    [0,"We slept in what had once been the gymnasium."],
    [1,"The floor was of varnished wood, with stripes and circles painted on it, for the games that were formerly played there; the hoops for the basketball nets were still in place, though the nets were gone."],
    [2,"There was old sex in the room and loneliness, and expectation, of something without a shape or name."]
]

with open("eval_test.csv", mode="w", encoding="utf-8-sig", newline="") as f:
    
    writer = csv.writer(f)

    writer.writerow(header_list)

    writer.writerows(data_list)