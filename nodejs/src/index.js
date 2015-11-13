import request from 'request';
import cheerio from 'cheerio';
import iconv from 'iconv-lite';

const RequestURL = [
  `https://`,  // protocol
  `www.mvg-live.de`,  // url
  `/ims/dfiStaticAuswahl.svc`, // endpoint
  `?haltestelle=Hauptbahnhof`, // station of interesst
  `&ubahn=checked`, // look for subway
  `&bus=checked`, // look for bus
  `&tram=checked`, // look for tram
  `&sbahn=checked` // look for sbahn
].join('');

request({
  uri: RequestURL,
  encoding: null
}, (err, res, body) => {
  if(err && res.statusCode !== 200) throw 'Unexpected Error';
  // console.log(body);

  var utf8String = iconv.decode(new Buffer(body), "ISO-8859-1");
  console.log(utf8String);

  // const $ = cheerio.load(body);
  // console.log($('table').html());
});
