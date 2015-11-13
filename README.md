<img src="resources/readme.logo.png" align="right" />
# MVG - Command Line Interface

## Node version
<p align="center">
  <img src="resources/node-preview.gif"/>
</p>
Install
```
npm install mvg-cli -g
```

Usage
```
Usage: mvg [station]

  station    Name of an registered stop-station in the MVV network (not required)
```
[Read more in the nodejs-README](nodejs/README.md)


## Python Version

Dependencies:

    pip install beautifulsoup4
    pip install colored
    pip install requests

Usage:

Edit the line "station = u'Unterföhring'" with your Station.
eg:

    station = u'Sendlinger Tor'

and then do

    python mvg.py

<p align="center">
  <img src="resources/mvpy.png" />
</p>
