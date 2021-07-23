#! /usr/bin/env python3

# Copyright (C) 2021 Karim Kanso
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import psutil
import argparse
import time
from datetime import datetime
from elasticsearch import Elasticsearch, ElasticsearchWarning
import warnings

# ignore warnings about no authentication enabled
warnings.filterwarnings('ignore', category=ElasticsearchWarning)

parser = argparse.ArgumentParser()
parser.add_argument(
    'host',
    help='elasticsearch host'
)
parser.add_argument(
    '--interval','-i',
    type=float,
    default=30,
    help='sleep time between scanning processes'
)
parser.add_argument(
    '--iterations',
    type=int,
    default=-1,
    help='number of iterations'
)
parser.add_argument(
    '--id',
    type=int,
    default=1,
    help='numeric value appended on end of index'
)
parser.add_argument(
    '--index',
    type=str,
    default='ps',
    help='base index name'
)
args = parser.parse_args()

es = Elasticsearch(hosts=[args.host])

last = time.monotonic()
for p in psutil.process_iter(): p.cpu_percent()

while args.iterations == -1 or args.iterations > 0:
    time.sleep(time.monotonic() - last + args.interval)

    timestamp = datetime.now().astimezone().isoformat()
    last = time.monotonic()
    docs = []
    for p in psutil.process_iter():
        with p.oneshot():
            docs.append(
                {
                    'pid': p.pid,
                    'ppid': p.ppid(),
                    'name': p.name(),
                    'percent': p.cpu_percent(),
                    'timestamp': timestamp,
                    'times': p.cpu_times()._asdict(),
                    'memory': p.memory_info()._asdict()
                }
            )

    print(f'saving: {timestamp}')
    for doc in docs:
        es.index(index=f'{args.index}-{args.id}', body=doc)

    args.iterations = max(args.iterations - 1, -1)
