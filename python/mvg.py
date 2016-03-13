#!/usr/bin/env python
#-*- coding: UTF-8 -*-
import requests
from bs4 import BeautifulSoup
import time
import os
from colored import fg, bg, attr
import sys, getopt
import signal
import imp

if sys.version_info.major == 2:
    from urllib import quote as urllib_quote
    imp.reload(sys)
    sys.setdefaultencoding('utf8')

    strip = lambda x: x.encode('latin-1').strip()

    def _build_line(line, time, place):
        return "{} - in {} minutes - to {}".format(line.decode('latin-1'),
                                                   time.decode('latin-1'),
                                                   place.decode('latin-1'))
else:
    from urllib.parse import quote as urllib_quote

    strip = lambda x: x.strip()

    def _build_line(line, time, place):
        return "{} - in {} minutes - to {}".format(line, time, place)


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
    print(attrc('reset'))
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def encode_request_string(station):
    station_url = station.encode("latin-1")
    station_url = urllib_quote(station_url)
    return station_url.lower()


def _print_line(lines, line_name):
    print(('{}{} {} {}'.format(fgc('white'),
                               bgc('yellow'),
                               line_name,
                               attrc('reset'))))
    if not lines:
        print(('{} No {} from this station {}'.format(fgc('yellow'),
                                                      line_name,
                                                      attrc('reset'))))
    else:
        try:
            for idx, x in enumerate(lines):
                if idx == 0:
                    print(('{}{} {} {}'.format(fgc('white'),
                                               bgc('red'),
                                               x,
                                               attrc('reset'))))
                else:
                    print(' ' + x)
        except:
            import ipdb; ipdb.set_trace()

def printStations(station, hide):
    ubahn=[]
    sbahn=[]
    tram=[]
    bus=[]

    station_url = encode_request_string(station)

    base_url = "http://www.mvg-live.de/ims/dfiStaticAuswahl.svc?haltestelle="
    r = requests.get(base_url + station_url + "&ubahn=checked&bus=checked&tram=checked&sbahn=checked")
    site = BeautifulSoup(r.text, "html.parser")

    table_line = [truc.text
                  for truc in site.find_all('td', {"class":"lineColumn"})]

    table_place = [truc.find(text=True, recursive=False)
                   for truc in site.find_all('td', {"class":"stationColumn"})]

    table_time = [truc.text
                  for truc in site.find_all('td', {"class":"inMinColumn"})
                  if truc.text]

    table_line  = [strip(truc) for truc in table_line]
    table_place = [strip(truc) for truc in table_place]
    table_time  = [strip(truc) for truc in table_time]

    print(('{}{} From {} {}'.format(fgc('black'), bgc('white'),
                                    station, attrc('reset'))))

    for i in range(1, len(table_line)):
        line = _build_line(table_line[i], table_time[i], table_place[i])
        if table_line[i][0] == "U":
            ubahn.append(line)
        elif table_line[i][0] == "S":
            sbahn.append(line)
        elif int(table_line[i]) < 50:
            tram.append(line)
        else:
            bus.append(line)

    if not hide:
        _print_line(ubahn, 'Ubahn')
        print('\n')
        _print_line(sbahn, 'Sbahn')
        print('\n')
        _print_line(tram, 'Tram')
        print('\n')
        _print_line(bus, 'Bus')


def printHelp():
    print('mvg.py -s <station>')
    print('       -t : refresh every 10 sec')
    print('       -x : hide empty lists')
    print('       -c : no color')
    print('       -h : this help')

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
        print('station is missing')
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
