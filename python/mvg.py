#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import os
from colored import fg, bg, attr
import urllib
import sys, getopt
import signal

reload(sys)
sys.setdefaultencoding('utf8')

color = True

def fgc(p):
    global color
    if color:
        return fg(p)
    else:
        return ''

def bgc(p):
    global color
    if color:
        return bg(p)
    else:
        return ''

def attrc(p):
    global color
    if color:
        return attr(p)
    else:
        return ''

def signal_handler(signal, frame):
    print attrc('reset')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def encode_request_string(station):
    station_url = station.encode("latin-1")
    station_url = urllib.quote(station_url)
    return station_url.lower()

def printStations(station, hide):
    table_line = []
    table_place = []
    table_time = []

    ubahn=[]
    sbahn=[]
    tram=[]
    bus=[]

    station_url = encode_request_string(station)

    r = requests.get("http://www.mvg-live.de/ims/dfiStaticAuswahl.svc?haltestelle=" + station_url + "&ubahn=checked&bus=checked&tram=checked&sbahn=checked")
    site = BeautifulSoup(r.text, "html.parser")

    for truc in site.find_all('td', {"class":"lineColumn"}):
        table_line.append(truc.text.encode('latin-1').strip())

    for truc in site.find_all('td', {"class":"stationColumn"}):
        table_place.append(truc.find(text=True, recursive=False).encode('latin-1').strip())

    for truc in site.find_all('td', {"class":"inMinColumn"}):
        if truc.text:
            table_time.append(truc.text.encode('latin-1').strip())

    print ('%s%s From %s %s' % (fgc('black'), bgc('white'), station, attrc('reset')))

    for i in range(1,len(table_line)):
        if table_line[i][0]=="U":
            ubahn.append(table_line[i] + " - in " + table_time[i] + " minutes - to " + table_place[i].decode('latin-1'))
        elif table_line[i][0]=="S":
            sbahn.append(table_line[i] + " - in " + table_time[i] + " minutes - to " + table_place[i].decode('latin-1'))
        elif int(table_line[i]) < 50:
            tram.append(table_line[i] + " - in " + table_time[i] + " minutes - to " + table_place[i].decode('latin-1'))
        else:
            bus.append(table_line[i] + " - in " + table_time[i] + " minutes - to " + table_place[i].decode('latin-1'))

    if len(ubahn)>0 or not hide:
        print '\n'
        print ('%s%s Ubahn %s' % (fgc('white'), bgc('yellow'), attrc('reset')))
        if len(ubahn)==0:
                print ('%s No Ubahn from this station %s' % (fgc('yellow'), attrc('reset')))
        for idx, x in enumerate(ubahn):
            if idx == 0:
                print ('%s%s %s %s' % (fgc('white'), bgc('red'), x, attrc('reset')))
            else:
                print ' ' + x

    if len(sbahn)>0 or not hide:
        print '\n'
        print ('%s%s Sbahn %s' % (fgc('white'), bgc('green'), attrc('reset')))
        if len(sbahn)==0:
                print ('%s No Sbahn from this station %s' % (fgc('yellow'), attrc('reset')))
        for idx, x in enumerate(sbahn):
            if idx == 0:
                print ('%s%s %s %s' % (fgc('white'), bgc('red'), x, attrc('reset')))
            else:
                print ' ' + x

    if len(tram)>0 or not hide:
        print '\n'
        print ('%s%s Tram %s' % (fgc('white'), bgc('cyan'), attrc('reset')))
        if len(tram)==0:
                print ('%s No Tram from this station %s' % (fgc('yellow'), attrc('reset')))
        for idx, x in enumerate(tram):
            if idx == 0:
                print ('%s%s %s %s' % (fgc('white'), bgc('red'), x, attrc('reset')))
            else:
                print ' ' + x

    if len(bus)>0 or not hide:
        print '\n'
        print ('%s%s Bus %s' % (fgc('white'), bgc('blue'), attrc('reset')))
        if len(bus)==0:
                print ('%s No Bus/Tram from this station %s' % (fgc('yellow'), attrc('reset')))
        for idx, x in enumerate(bus):
            if idx == 0:
                print ('%s%s %s %s' % (fgc('white'), bgc('red'), x, attrc('reset')))
            else:
                print ' ' + x

def printHelp():
    print 'mvg.py -s <station>'
    print '       -t : refresh every 10 sec'
    print '       -x : hide empty lists'
    print '       -c : no color'
    print '       -h : this help'

def main(argv):
    global color
    station = ''
    loop = False
    hide = False

    try:
        opts, args = getopt.getopt(argv,"htxcs:", ['station='])
    except getopt.GetoptError:
        printHelp()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            printHelp()
            sys.exit()
        elif opt in ("-t"):
            loop = True
        elif opt in ("-x"):
            hide = True
        elif opt in ("-c"):
            color = False
        elif opt in ("-s", "--station"):
            station = arg

    if station == '':
        print 'station is missing'
        printHelp()
        sys.exit(3)

    if loop:
        while True:
            os.system('clear')
            printStations(station, hide)
            time.sleep(10)
    else:
        printStations(station, hide)

if __name__ == "__main__":
   main(sys.argv[1:])
