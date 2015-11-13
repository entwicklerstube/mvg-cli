import chalk from 'chalk';
import moment from 'moment';
import readlineSync from 'readline-sync';
import logUpdate from 'log-update';
import LoadData from './utils/loadData';

// Clear CLI
process.stdout.write("\u001b[2J\u001b[0;0H");
// Print a header
console.log(
  chalk.black.bgYellow('                    MVG                     ')
);

let startStation = undefined;

if(process.argv && process.argv[2]) {
  startStation = process.argv[2];
} else {
  startStation = readlineSync.question('From what station do you want to start? : ')
}

console.log(
  chalk.yellow(`Show all trips from ${chalk.yellow.underline(startStation)}`)
);

let LiveData = [];
let LastRefresh = +new Date()

const updateData = () => {
  LoadData({
    station: startStation
  }, (err, data) => {
    if(err) throw `Error: ${err}`;
    LiveData = data;
    LastRefresh = +new Date();
  });
}
String.prototype.paddingLeft = function (paddingValue) {return String(paddingValue + this).slice(-paddingValue.length);};

updateData();

setInterval(() => {
  updateData();
}, 5000);

  let tmpl = '';
setInterval(() => {
  if(LiveData.length > 0) {
    let deps = [];

    // console.log(LiveData.departures);

    LiveData.departures.map((dep) => {
      deps.push(` ${chalk.white.bgRed(dep.route.paddingLeft("   ")+" ")} in ${dep.arrivingIn.paddingLeft("  ")} minutes to ${dep.station}\n`);
    });


    tmpl = `
 ${chalk.black.bgWhite(`From ${LiveData.station}`)}  Last refresh: ${moment(LastRefresh).format('HH:mm:ss')}
- - - - - - - - - - - - - - - - - - - - - - - - - - -
${deps.join('')} - - - - - - - - - - - - - - - - - - - - - - - - - - -
`;
  } else {
    tmpl = `
    Loading...
    `;
  }
  logUpdate(tmpl);
},100);
