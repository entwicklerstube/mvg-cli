import request from 'request';
import cheerio from 'cheerio';
import iconv from 'iconv-lite';
import readlineSync from 'readline-sync';
import ParseTable from './utils/parseTable';

let startStation = undefined;

if(process.argv && process.argv[2]) {
  startStation = process.argv[2];
} else {
  startStation = readlineSync.question('From what station do you want to start? : ')
}

const RequestURI = [
  `https://`,  // protocol
  `www.mvg-live.de`,  // url
  `/ims/dfiStaticAuswahl.svc`, // endpoint
  `?haltestelle=${startStation}`, // station of interesst
  `&ubahn=checked`, // look for subway
  `&bus=checked`, // look for bus
  `&tram=checked`, // look for tram
  `&sbahn=checked` // look for sbahn
].join('');

request({
  uri: RequestURI,
  encoding: null
}, (err, res, body) => {
  if(err && res.statusCode !== 200) throw 'Error: Had problems to connect to mvg-page';

  const utf8String = iconv.decode(new Buffer(body), "ISO-8859-1");
  console.log(ParseTable(utf8String).departures);

  // const $ = cheerio.load(body);
  // console.log($('table').html());
});
