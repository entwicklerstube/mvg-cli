import chai from 'chai';
import sinon from 'sinon';
import sinonChai from 'sinon-chai';

chai.use(sinonChai);

global.chai = chai;
global.expect = chai.expect;
global.sinon = sinon;
