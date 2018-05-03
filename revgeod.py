#!/usr/bin/env python

import json
import os
from bottle import run, request, route, get
import bottle
import Geohash
#from geopy.geocoders import Nominatim
#from geopy.geocoders import GoogleV3
#from geopy.point import Point
from opencage.geocoder import OpenCageGeocode
import redis
import paho.mqtt.publish as mqtt
from creds import *
import datetime

reverse_timeout = 4
precision = 8

geocoder = OpenCageGeocode(apikey)  # from creds.py

class Stat(object):
    def __init__(self, names):
        self.start = datetime.datetime.utcnow()
        self.counter = {}
        for name in names:
            self.counter[name] = 0

    def reset(self):
        for name in self.counter.keys():
            self.counter[name] = 0

    def count(self, name):
        counter = 0
        if name in self.counter:
            counter = self.counter[name]
        counter += 1
        self.counter[name] = counter

    def result(self, name):
        counter = 0
        if name in self.counter:
            counter = self.counter[name]
        return counter

my_stat = Stat(['rev', 'stats', 'geohash_failed', 'cache_ok', 'cache_failed', 'geocode_ok', 'geocode_failed'])

bottle.debug(True)
@get('/stats')
def stats():
    my_stat.count('stats')
    hit_rate = 0.0
    if my_stat.result('rev') != 0:
       hit_rate = my_stat.result('cache_ok') / my_stat.result('rev') * 100.0

    return json.dumps({
        'uptime': (datetime.datetime.utcnow() - my_stat.start).total_seconds(),
        'counter': my_stat.counter
    })

@get('/rev')
def rev():
    my_stat.count('rev')
    lat = float(request.query['lat'])
    lon = float(request.query['lon'])

    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=9)

    try:
        geohash = Geohash.encode(lat, lon, precision=precision)
    except:
        my_stat.count('geohash_failed')
        return None

    print "{lat}, {lon} = {geohash}".format(lat=lat, lon=lon, geohash=geohash)


    raw = None
    cached = False
    key = 'ghash:%s' % (geohash)
    val = r.get(key)
    print key, val
    if val is None:
        try:
            #p = Point(lat, lon)
            ## geolocator = Nominatim(timeout=2)
            #geolocator = GoogleV3(timeout=5, api_key=apikey)
            #address, (latitude, longitude) = geolocator.reverse(p, exactly_one=True)

            address = geocoder.reverse_geocode(lat, lon, no_record=1, limit=1)

            # print "LOC====",json.dumps(address, indent=4)

            village = address[0]['formatted']

            r.set(key, json.dumps(address))
            my_stat.count('geocode_ok')
        except Exception as e:
            print str(e)
            village = "{%s}" % (key)    # enclose in curly braces so that users *see* it's a token
            my_stat.count('geocode_failed')

    else:
        raw = json.loads(val)
        if raw:
            cached = True
            village = raw[0]['formatted']
            my_stat.count('cache_ok')
        else:
            village = "{%s}" % (key)    # enclose in curly braces so that users *see* it's a token
            my_stat.count('cache_failed')
    
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
