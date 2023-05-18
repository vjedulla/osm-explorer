import osmium as osm
import pandas as pd



class OSMHandler(osm.SimpleHandler):
    def __init__(self):
        osm.SimpleHandler.__init__(self)
        self.osm_data = []
        self.osm_graph_relations = []

    def tag_inventory(self, elem, elem_type):

        if elem_type == 'way':
            row = [elem.id] + [
                x.ref for x in elem.nodes
            ]

            self.osm_graph_relations.append(row)

        if elem_type == 'relation':
            # skip them
            return

        for tag in elem.tags:
            has_location = hasattr(elem, "location")

            x = elem.location.lat if has_location and elem.location else None
            y = elem.location.lon if has_location and elem.location else None

            row = [
                elem_type, elem.id,
                elem.version, x, y,
                len(elem.tags), tag.k, tag.v
            ]

            self.osm_data.append(row)
        else:
            has_location = hasattr(elem, "location")
            x = elem.location.lat if has_location and elem.location else None
            y = elem.location.lon if has_location and elem.location else None

            row = [
                elem_type, elem.id,
                elem.version, x, y,
                0, None, None
            ]

            self.osm_data.append(row)

    def node(self, n):
        self.tag_inventory(n, "node")

    def way(self, w):
        self.tag_inventory(w, "way")

    def relation(self, r):
        self.tag_inventory(r, "relation")


osmhandler = OSMHandler()
# scan the input file and fills the handler list accordingly
osmhandler.apply_file("../data/tirana.osm")

# transform the list into a pandas DataFrame
data_colnames = ['type', 'id', 'version', 'lat', 'lon', 'ntags', 'tagkey', 'tagvalue']

df_osm = pd.DataFrame(osmhandler.osm_data, columns=data_colnames)
df_osm = df_osm.sort_values(by=['type', 'id'])

df_gr = pd.DataFrame(osmhandler.osm_graph_relations)


df_osm.to_csv('../data/raw_extracted_nodes.csv')
df_gr.to_csv('../data/raw_extracted_relations.csv')