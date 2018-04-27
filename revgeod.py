#!/usr/bin/env python

import json
import os
from bottle import run, request, route, get
import bottle
import Geohash
from geopy.geocoders import Nominatim
from geopy.geocoders import GoogleV3
from geopy.point import Point
import redis
import paho.mqtt.publish as mqtt
from creds import *

reverse_timeout = 4
precision = 7

bottle.debug(True)

@get('/rev')
def rev():
    lat = float(request.query['lat'])
    lon = float(request.query['lon'])

    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=9)

    try:
        geohash = Geohash.encode(lat, lon, precision=precision)
    except:
        return None

    print "{lat}, {lon} = {geohash}".format(lat=lat, lon=lon, geohash=geohash)


    raw = None
    cached = False
    key = 'ghash:%s' % (geohash)
    val = r.get(key)
    print key, val
    if val is None:
        try:
            p = Point(lat, lon)
            # geolocator = Nominatim(timeout=2)
            geolocator = GoogleV3(timeout=5, api_key=apikey)
            address, (latitude, longitude) = geolocator.reverse(p, exactly_one=True)

            print "LOC====",json.dumps(address)

            village = address

            r.set(key, json.dumps(address))
        except Exception as e:
            print str(e)
            village = "{%s}" % (key)    # enclose in curly braces so that users *see* it's a token

    else:
        raw = json.loads(val)
        if raw:
            cached = True
            village = raw
        else:
            village = "{%s}" % (key)    # enclose in curly braces so that users *see* it's a token
    
    addr = {
        'village' : village,
    }

    ca = "N"
    if cached:
        ca = "Y"
    raw = json.dumps(dict(address=addr))
    full = "{lat}, {lon} = {geohash} cached={ca} {raw}".format(lat=lat, lon=lon, geohash=geohash, raw=raw, ca=ca)
    full = "{geohash} cached={ca} {lat}, {lon} {raw}".format(lat=lat, lon=lon, geohash=geohash, raw=raw, ca=ca)

    print raw

    auth = None
    if username is not None:
        auth = {
            'username' : username,
            'password' : password
        }
    mqtt.single('_revgeo', full, hostname="127.0.0.1", auth=auth)
    return raw



run(host='127.0.0.1', port=8865)
