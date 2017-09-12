#!/usr/bin/env python3

import os
import sqlite3
from datetime import datetime, timedelta

from flask import Flask, g, jsonify, request, send_from_directory


DATEFORMAT = '%Y-%m-%dT%H:%M:%S'


app = Flask(__name__, static_folder='build/static')
app.config.update({
    'DATABASE': os.path.join(app.root_path, 'db.sqlite3'),
    'DEBUG': True,
    'SECRET_KEY': 'development key',
})


def connect_db():
    rv = sqlite3.connect(app.config['DATABASE'], detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
        g.sqlite_db.row_factory = sqlite3.Row
    return g.sqlite_db


@app.route('/', defaults={'path': None})
@app.route('/<path:path>')
def serve(path):
    print('serve', path)
    if not path:
        return send_from_directory('build', 'index.html')
    else:
        return send_from_directory('build', path)


@app.route('/nodes')
def nodes():
    db = get_db()
    cur = db.execute('select distinct node from temperature')
    nodes = [x['node'] for x in cur.fetchall()]
    return jsonify({'nodes': nodes})


@app.route("/node/<node>/current")
def temperature(node):
    db = get_db()
    cur = db.execute(
        'select temperature, humidity, battery, strftime("%Y-%m-%dT%H:%M:%SZ", datetime) as dt '
        'from temperature '
        'where node = ? '
        'order by dt desc '
        'limit 1',
        (node,))
    row = dict(cur.fetchone())
    return jsonify(row)


@app.route("/node/<node>/history")
def history(node):
    now = datetime.now()
    from_date = request.args.get('from', None)
    if from_date is not None:
        from_date = datetime.strptime(from_date, DATEFORMAT)
    else:
        from_date = now - timedelta(days=2)

    to_date = request.args.get('to', None)
    if to_date is not None:
        to_date = datetime.strptime(to_date, DATEFORMAT)
    else:
        to_date = now

    entries = []
    db = get_db()
    cursor = db.execute(
        'select strftime("%Y-%m-%dT%H:%M:00Z", datetime) as dt, '
        '       avg(temperature) as temperature, '
        '       avg(humidity) as humidity, '
        '       avg(battery) as battery '
        'from temperature '
        'where node = ? and datetime >= ? and datetime <= ? '
        'group by dt '
        'order by dt asc',
        (node,
         from_date,
         to_date))
    for row in cursor:
        entries.append({
            'temperature': row['temperature'],
            'humidity': row['humidity'],
            'battery': row['battery'],
            'datetime': row['dt'],
        })
    return jsonify({'entries': entries})


@app.route("/node/<node>/temperature/add", methods=['POST'])
def add_temperature(node):
    data = request.get_json()
    db = get_db()
    db.execute(
        'insert into temperature '
        '(datetime, temperature, humidity, battery, sequence, node) values '
        '(datetime(), :temperature, :humidity, :battery, :sequence, :node)',
        data)
    db.commit()
    return jsonify({'status': 'ok'})


if __name__ == "__main__":
    app.debug = True
    app.run(host='0.0.0.0')
