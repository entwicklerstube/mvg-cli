import React from 'react';
import { render } from 'ink';
import meow from 'meow';

import MVG from './renderer';

console.log('hey');

const cli = meow(
	`
	Usage
	  $ mvg

	Examples
	  $ mvg
`
);

render(<MVG {...cli.flags} />);
