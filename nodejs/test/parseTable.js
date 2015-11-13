import DOM from './fixture/domTable';
import ParseTable from '../src/utils/parseTable';

describe('Table To Array', () => {
  it('returns the entries of the passed table (count tr`s)', () => {
    expect(ParseTable(DOM).length).to.equal(9);
  });

  it('returns the amount of the trips-data', () => {
    expect(ParseTable(DOM).trips).to.equal(7);
  });

  it('returns the station of interest', () => {
    expect(ParseTable(DOM).station).to.equal('Goetheplatz');
  });

  it('returns the server-time', () => {
    expect(ParseTable(DOM).serverTime).to.equal('11:30');
  });

  it('returns an array with the subway-data', () => {
    expect(ParseTable(DOM).subways[0]).to.deep.equal({
      route: 'U6',
      station: 'Garching-Forschungszentrum',
      arrivingIn: 0
    });
  });

  it('returns a repaired station-title', () => {
    expect(ParseTable(DOM).cleanStationTitle('\n      Garching-Forschungszentrum\n       \n')).to.equal('Garching-Forschungszentrum')
  });
});
