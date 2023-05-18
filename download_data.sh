echo "Downloading osmconvert..."
# download convert to filter out a country
wget -O - http://m.m.i24.cc/osmconvert.c | cc -x c - -lz -O3 -o osmconvert

echo "Downloading data for: $1 (e.g. germany)"
curl -o data/$1-latest.osm.pbf http://download.geofabrik.de/europe/$1-latest.osm.pbf

echo "Filtering to specific coordinates: $2 and saving it to $3"
# change this
./osmconvert data/$1-latest.osm.pbf -b=$2 -o=data/$3.osm