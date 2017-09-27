# Realtime Travel times by car

Small Django app to download real-time (every 5 minutes) data about
car travel times in and around Amsterdam. Comes with a docker-compose.yml
that allows you to run a mapserver with this data locally. You can use
QGIS to look at these maps.


## Installing it
* Git clone this project (https://github.com/Amsterdam/reistijdenauto).
* In the project directory do a git clone on the Amsterdam mapserver docker
  (https://github.com/Amsterdam/mapserver). This will result in a subdirectory
  mapserver in the root of the reistijdenauto repository.


## Running it
To get the services built and running:
```
docker-compose up --build
```

To migrate the database and retrieve the latest data:
```
docker-compose run --rm web migrate
docker-compose run --rm web retrievedata
```

You now have:
* a REST interface to the data running on http://localhost:8000/reistijdenauto/
* a PostGIS database running on port 5432 containing the data
* a mapserver with a WFS and WMS service running on port 8070
    * WMS: http://localhost:8070/maps/reistijdenauto?REQUEST=GetCapabilities&SERVICE=wms
    * WFS: http://localhost:8070/maps/reistijdenauto?REQUEST=GetCapabilities&SERVICE=wfs
