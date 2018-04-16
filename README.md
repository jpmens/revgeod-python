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
