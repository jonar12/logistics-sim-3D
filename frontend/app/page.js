'use client';
import styles from './page.module.css';
import { useState, useRef } from 'react';
import '@aws-amplify/ui-react/styles.css';
import { Button, ButtonGroup, Flex } from '@aws-amplify/ui-react';

export default function Home() {
	let [location, setLocation] = useState('');
	let [scaleFactor, setScaleFactor] = useState('');
	const [boxes, setBoxes] = useState([]);
	const [robots, setRobots] = useState([]);
	const [pilas, setPilas] = useState([]);
	const running = useRef(null);

	let setup = () => {
		console.log('Hola');
		fetch('http://localhost:8000/simulations', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
		})
			.then(resp => resp.json())
			.then(data => {
				setLocation(data['Location']);
			});
	};

	const handleStart = () => {
		running.current = setInterval(() => {
			fetch('http://localhost:8000' + location)
				.then(res => res.json())
				.then(data => {
					setBoxes(data['boxes']);
					setRobots(data['robots']);
				});
		}, 50);
	};

	const handleStop = () => {
		clearInterval(running.current);
	};

	return (
		<div className={styles.page}>
			<ButtonGroup variation="primary">
				<Button onClick={setup}>Setup</Button>
				<Button onClick={handleStart}>Start</Button>
				<Button onClick={handleStop}>Stop</Button>
			</ButtonGroup>
			<Flex direction={'column'}>
				<svg
					width="600"
					height="600"
					style={{ backgroundColor: 'lightgray' }}
					xmlns="http://www.w3.org/2000/svg"
				>
					{pilas.map(pila => {
						return (
							<circle
								cx={pila[0] * scaleFactor}
								cy={pila[1] * scaleFactor}
								r="8"
								fill="yellow"
							/>
						);
					})}
					{boxes.map(box => {
						return (
							<circle
								cx={box.pos[0] * scaleFactor}
								cy={box.pos[1] * scaleFactor}
								r="7"
								fill="blue"
							/>
						);
					})}
					{robots.map(robot => {
						return (
							<circle
								cx={robot.pos[0] * scaleFactor}
								cy={robot.pos[1] * scaleFactor}
								r="6"
								fill="red"
							/>
						);
					})}
				</svg>
			</Flex>
		</div>
	);
}
