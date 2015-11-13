import request from 'request';
import cheerio from 'cheerio';


request('https://www.mvg-live.de/ims/dfiStaticAuswahl.svc?haltestelle=Goetheplatz&ubahn=checked&bus=checked&tram=checked&sbahn=checked', (err, res, body) => {
  if(err && res.statusCode !== 200) throw 'Unexpected Error';

  const $ = cheerio.load(body);

  console.log($('table').html());

});
