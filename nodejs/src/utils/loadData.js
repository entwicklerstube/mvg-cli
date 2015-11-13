import request from 'request';
import cheerio from 'cheerio';
import iconv from 'iconv-lite';
import ParseTable from './parseTable';

export default function create(config, callback) {
  class LoadData {
    startStation = config.station

    constructor() {
      const RequestURI = [
        `https://`,  // protocol
        `www.mvg-live.de`,  // url
        `/ims/dfiStaticAuswahl.svc`, // endpoint
        `?haltestelle=${this.startStation}`, // station of interesst
        `&ubahn=checked`, // look for subway
        `&bus=checked`, // look for bus
        `&tram=checked`, // look for tram
        `&sbahn=checked` // look for sbahn
      ].join('');

      request({
        uri: RequestURI,
        encoding: null
      }, (err, res, body) => {
        if(err && res.statusCode !== 200) callback('Error: Had problems to connect to mvg-page', null);
        const DOM = iconv.decode(new Buffer(body), "ISO-8859-1");
        callback(null, ParseTable(DOM));
      });
    }
  }

  return new LoadData();
}
