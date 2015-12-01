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

def signal_handler(signal, frame):
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

    print ('%s%s From %s %s' % (fg('black'), bg('white'), station, attr('reset')))

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
        print ('%s%s Ubahn %s' % (fg('white'), bg('yellow'), attr('reset')))
        if len(ubahn)==0:
                print ('%s No Ubahn from this station %s' % (fg('yellow'), attr('res_bold')))
        for idx, x in enumerate(ubahn):
            if idx == 0:
                print ('%s%s %s %s' % (fg('white'), bg('red'), x, attr('reset')))
            else:
                print x
        print "-" * 50

    if len(sbahn)>0 or not hide:
        print '\n'
        print ('%s%s Sbahn %s' % (fg('white'), bg('green'), attr('reset')))
        if len(sbahn)==0:
                print ('%s No Sbahn from this station %s' % (fg('yellow'), attr('res_bold')))
        for idx, x in enumerate(sbahn):
            if idx == 0:
                print ('%s%s %s %s' % (fg('white'), bg('red'), x, attr('reset')))
            else:
                print x
        print "-" * 50

    if len(tram)>0 or not hide:
        print '\n'
        print ('%s%s Tram %s' % (fg('white'), bg('cyan'), attr('reset')))
        if len(tram)==0:
                print ('%s No Tram from this station %s' % (fg('yellow'), attr('res_bold')))
        for idx, x in enumerate(tram):
            if idx == 0:
                print ('%s%s %s %s' % (fg('white'), bg('red'), x, attr('reset')))
            else:
                print x
        print "-" * 50

    if len(bus)>0 or not hide:
        print '\n'
        print ('%s%s Bus %s' % (fg('white'), bg('blue'), attr('reset')))
        if len(bus)==0:
                print ('%s No Bus/Tram from this station %s' % (fg('yellow'), attr('res_bold')))
        for idx, x in enumerate(bus):
            if idx == 0:
                print ('%s%s %s %s' % (fg('white'), bg('red'), x, attr('reset')))
            else:
                print x

def printHelp():
    print 'mvg.py -s <station>'
    print '       -t : refresh every 10 sec'
    print '       -x : hide empty lists'
    print '       -h : this help'

def main(argv):
    station = ''
    loop = False
    hide = False

    try:
        opts, args = getopt.getopt(argv,"htxs:", ['station='])
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
