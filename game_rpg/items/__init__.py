import json
import os
from glob import glob


def _load():
	data = {}
	for name_file in listfile:
		items = json.load(open(name_file))
		for name, item in items["items"].items():
			if not  item.get("type_item"):
				item["type_item"] = items["type"]

			item["namespace"] = items["namespace"]
			name = items["namespace"] + "/" + name
			if name in data:
				print(f"WARNING - {name}")

			data[name] = item
	return data


def sort_id_items(by: str):
	data = {}
	for id_item , item in DATA["items"].items():
		name = str(item.get(by, None))
		if not name:
			continue

		if not data.get(name):
			data[name] = []

		data[name].append(id_item)
	return data


DATA = {}
path = os.path.dirname(os.path.realpath(__file__))
listfile = glob(path + "/*.item")
DATA["items"] = _load()
DATA["items_by_quality"] = sort_id_items("quality")
DATA["items_by_type"] = sort_id_items("type_item")
DATA["items_by_namspace"] = sort_id_items("namespace")


if __name__ == '__main__':
	with open("./items.json", "w") as data:
		data.write(json.dumps(DATA, indent=4))
