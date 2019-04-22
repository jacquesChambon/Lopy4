# -*- coding: utf-8 -*-

"""
This is a flask server called by the Sigfox callback mechanism.

It receives the frames from Sigfox and store the data in a MongoDB database.

(C) Remi Jolin - 2018-2019
"""

from __future__ import print_function, division

from flask import Flask, request, jsonify
from pymongo import MongoClient
from datetime import datetime
import random
from pprint import pprint
from construct import Struct, Int8ub, Padding

app = Flask(__name__)

resp = dict(r=0)
random.seed()

format_rvb = Struct(
    Padding(5),
    'r' / Int8ub,
    'v' / Int8ub,
    'b' / Int8ub
)


def utcnow():
    return datetime.utcnow()


def store_data(call_name):
    """
    extract data from request and store it in DB
    :param call_name:
    :return:
    """
    result = dict(call=call_name,
                  now=utcnow(),
                  method=request.method,
                  headers=dict(h for h in request.headers),
                  ip=request.remote_addr,
                  json=request.json)
    print('result /', call_name)
    pprint(result)

    db_r = db.devices.save(result)
    print('db_r:', db_r)
    return result


@app.route('/device', methods=['POST', 'PUT'])
def read_device_info():
    """
    upload (receive) frames and send no response back to the device.

    Just store the received data and ack the message to Sigfox
    :return:
    """
    store_data('device')
    return jsonify(dict(result='ok'))


@app.route('/bidir', methods=['POST', 'PUT'])
def read_device_info_bidir():
    """
    Get a message from the device, store it and return a 3 bytes random value
    if the device needs an answer
    :return:
    """
    store_data('bidir')

    device = request.json['device']
    r, v, b = random.randrange(256), random.randrange(256), random.randrange(256)
    resp = format_rvb.build(dict(r=r, v=v, b=b)).encode('hex')
    response = {device: (dict(downlinkData=resp) if request.json['ack'] else dict(noData=True))}
    print('response:', response)
    return jsonify(response)


@app.route('/service_ack', methods=['POST', 'PUT'])
def service_ack():
    """
    receive service ack message from Sigfox

    Just store the received data and ack the message to Sigfox
    :return:
    """
    store_data('service_ack')
    return jsonify(dict(result='ok'))


db = MongoClient('mongodb://localhost/', tz_aware=True).sipy

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)

# fin
