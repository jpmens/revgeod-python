# revgeod

Ceci est un test.

```
virtualenv v
v/bin/pip install -r requirements.txt
v/bin/python revgeod.py
```

## t.conf

```xml
<entry key='geocoder.enable'>true</entry>
<entry key='geocoder.type'>nominatim</entry>
<entry key='geocoder.url'>http://127.0.0.1:8865/rev</entry>
<entry key='geocoder.onRequest'>true</entry>
<entry key='geocoder.format'>%t</entry>
```

```
mysql> select * from positions where id >= 10288;
*************************** 1. row ***************************
        id: 10288
  protocol: owntracks
  deviceid: 1
servertime: 2018-04-16 20:52:30
devicetime: 2018-04-16 20:52:29
   fixtime: 2018-04-16 20:52:29
     valid:
  latitude: 48.95833
 longitude: 3.99513
  altitude: 0
     speed: 0
    course: 0
   address: La Tuilerie, 51190 Oger, France     ◄ 
attributes: {"batteryLevel":11,"distance":0.0,"totalDistance":6342542.38,"motion":false}
  accuracy: 0
   network: null
*************************** 2. row ***************************
        id: 10289
  protocol: owntracks
  deviceid: 1
servertime: 2018-04-16 20:52:55
devicetime: 2018-04-16 20:52:54
   fixtime: 2018-04-16 20:52:54
     valid:
  latitude: 48.95833
 longitude: 3.99513
  altitude: 0
     speed: 0
    course: 0
   address: {ghash:u0dydb}    ◄ 
attributes: {"batteryLevel":11,"distance":0.0,"totalDistance":6342542.38,"motion":false}
  accuracy: 0
   network: null
```
