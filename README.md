# Basic experiments with Elasticsearch and Kibana

This repository has a super simple python script that grabs process
info and throws it into an Elasticsearch instance. The intention is to
use Kibana to visualise the data. It is by no means efficient, but
provides an easy data source for Kibana to evaluate some of its
features.

## Usage

Set up a vanilla docker container of Elasticsearch and Kibana. Below
commands are taken from the [official documentation][kibana] for
Kibana E.g.

```plaintext
$ docker network create elastic
$ docker run --rm -t -i -e 'ELASTICSEARCH_HOSTS=http://es:9200' --net=elastic --name=kibana docker.elastic.co/kibana/kibana:7.13.4-amd64
$ docker run  -e "discovery.type=single-node"  --name=es --net=elastic -t -i --rm docker.elastic.co/elasticsearch/elasticsearch:7.13.4-amd64
```

Then fire up the python script as follows (where the ip address is of
Elasticsearch container):

```plaintext
$ ./ps-sensor.py 172.18.0.2
```

The script has a couple options which can be seen with `--help` but
the default should suffice.

```plaintext
$ ./ps-sensor.py --help
usage: ps-sensor.py [-h] [--interval INTERVAL] [--iterations ITERATIONS] [--id ID] [--index INDEX] host

positional arguments:
  host                  elasticsearch host

optional arguments:
  -h, --help            show this help message and exit
  --interval INTERVAL, -i INTERVAL
                        sleep time between scanning processes
  --iterations ITERATIONS
                        number of iterations
  --id ID               numeric value appended on end of index
  --index INDEX         base index name
```

Then go to Kibana -> *Stack Management* -> *Index Patterns* and create
a pattern that captures the `ps-*` index. When prompted, select
`timestamp` filed as a time field. From here it is possible to access
the data in the discover and dashboard views.

[kibana]: https://www.elastic.co/guide/en/kibana/current/docker.html

## Other bits

Copyright Karim Kanso, 2021. All rights reserved. Licensed under GPLv3.
