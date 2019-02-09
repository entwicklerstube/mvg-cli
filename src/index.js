import React, { Component } from 'react';
import { render, Color, Box } from 'ink';

class MVG extends Component {
	constructor() {
		super();

		this.state = {
			i: 0
		};
	}

	componentDidMount() {
		this.timer = setInterval(() => {
			this.setState({
				i: this.state.i + 1
			});
		}, 100);
	}

	componentWillUnmount() {
		clearInterval(this.timer);
	}

	render() {
		const { foo } = this.props;
		return (
			<Box>
				<Box>a -{foo}</Box>
				<Box>b</Box>
				foo: bar: <Color green>{this.state.i} tests passed</Color>
			</Box>
		);
	}
}

render(<MVG foo='bar' />);
