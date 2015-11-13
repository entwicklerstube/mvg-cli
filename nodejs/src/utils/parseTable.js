import cheerio from 'cheerio';

export default function create(DOM) {
  class ParseTable {
    $ = undefined
    length = 0
    trips = 0
    station = 'unknown'
    serverTime = '00:00'
    subways = []

    constructor() {
      this.$ = cheerio.load(DOM);
      // let tramLines = ['20','17','12','18','16','19','15','25','21','22','28','27'];

      this.length = this.$('tr').length;
      this.trips = this.$('.rowOdd, .rowEven').length;
      this.station = this.$('.headerStationColumn').text();
      this.serverTime = this.$('.serverTimeColumn').text();
      this.subways = this.findByType('ubahn');
    }

    findByType(type) {
      let lines = [];
      const availableTypes = ['ubahn', 'bus', 'sbahn', 'tram'];
      if(availableTypes.indexOf(type) < 0) throw `error: ${type} is not available as mvg type`;

      const that = this;

      this.$('.rowOdd, .rowEven').each(function() {
        lines.push({
          route: that.$(this).find('.lineColumn').text(),
          station: that.cleanStationTitle(that.$(this).find('.stationColumn').text()),
          arrivingIn: that.$(this).find('.inMinColumn').text()
        });
      });

      return [{
        route: 'U6',
        station: 'Garching-Forschungszentrum',
        arrivingIn: 0
      }];
    }

    cleanStationTitle(title) {
      return title.replace(/^\s+|\s+$/g, '');
    }
  }

  return new ParseTable();
}
