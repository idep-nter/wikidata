import json

from rdflib import Graph

from utils import (
    get_stdforms,
    get_labels,
    get_descriptions,
    get_ids,
    get_rankings,
    get_type,
)


class KbItem:
    def __init__(
        self, kbid, hrid, stdforms, labels, descriptions, ids, rankings, item_type
    ):
        self.kbid = kbid
        self.hrid = hrid
        self.stdforms = stdforms
        self.labels = labels
        self.descriptions = descriptions
        self.ids = ids
        self.rankings = rankings
        self.item_type = item_type


def main():
    with open("wikidata_ids.txt") as file:
        id_inpt = file.read()

    # parse input data
    g = Graph()
    g.parse("100_items_wikidata_subset.nt", format="nt")

    # make a list of ids and remove blank items
    id_lst = [i for i in id_inpt.split("\n") if i]

    with open("wiki_data.json", "w") as outfile:
        kb_list = []
        for i in id_lst:
            kbid = f"KB - {i} - W"
            stdforms = get_stdforms(i, g)
            hrid = f"{stdforms['en']} ({kbid})"
            labels = get_labels(i, g)
            descriptions = get_descriptions(i, g)
            ids = get_ids(i, g)
            rankings = get_rankings(i, g)
            item_type = get_type(i, g)

            # make an instance of an item
            kb = KbItem(
                kbid, stdforms, hrid, labels, descriptions, ids, rankings, item_type
            )

            kb_list.append(vars(kb))

        # saves the list of items into the json file
        json.dump(kb_list, outfile, indent=4, ensure_ascii=False)
        print("All items were successfully saved into json file!")


if __name__ == "__main__":
    main()
