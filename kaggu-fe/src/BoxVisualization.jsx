import React, { useState, useEffect } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import axios from 'axios';
import {
	Button,
	Card,
	Heading,
	Flex,
	View,
	Text,
	Badge,
	Loader,
} from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';

const api = axios.create({
	baseURL: 'http://localhost:8000',
	withCredentials: false,
	headers: {
		'Content-Type': 'application/json',
	},
});

// Box component to render individual boxes
const Box = ({ position, dimensions, color = '#1e40af' }) => {
	return (
		<mesh position={position}>
			<boxGeometry args={dimensions} />
			<meshStandardMaterial color={color} />
		</mesh>
	);
};

// Main scene component
const Scene = ({ boxes }) => {
	return (
		<>
			<ambientLight intensity={0.5} />
			<pointLight position={[10, 10, 10]} />
			<gridHelper args={[100, 100]} />
			{boxes.map((box, index) => (
				<Box
					key={index}
					position={[box.pos[0], box.pos[1], box.pos[2]]}
					dimensions={[box.width, box.height, box.depth]}
				/>
			))}
			<OrbitControls />
		</>
	);
};

// Main component
const BoxVisualization = () => {
	const [simulationId, setSimulationId] = useState(null);
	const [boxes, setBoxes] = useState([]);
	const [step, setStep] = useState(0);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState(null);

	// Initialize simulation
	const initializeSimulation = async () => {
		try {
			setLoading(true);
			setError(null);

			const { data } = await api.post('/simulations');
			const id = data.Location.split('/').pop();
			setSimulationId(id);
		} catch (error) {
			let errorMessage = 'Failed to initialize simulation';
			if (error.response) {
				// The request was made and the server responded with a status code
				// that falls out of the range of 2xx
				errorMessage = `Server error: ${error.response.status}`;
			} else if (error.request) {
				// The request was made but no response was received
				errorMessage = 'No response from server';
			} else {
				// Something happened in setting up the request
				errorMessage = error.message;
			}
			setError(errorMessage);
			console.error('Error details:', error);
		} finally {
			setLoading(false);
		}
	};

	// Step simulation
	const stepSimulation = async () => {
		if (!simulationId) return;

		try {
			setLoading(true);
			setError(null);

			const { data } = await api.get(`/simulations/${simulationId}`);
			setBoxes(data.boxes);
			setStep(data.step);
		} catch (error) {
			let errorMessage = 'Failed to step simulation';
			if (error.response) {
				errorMessage = `Server error: ${error.response.status}`;
			} else if (error.request) {
				errorMessage = 'No response from server';
			} else {
				errorMessage = error.message;
			}
			setError(errorMessage);
			console.error('Error details:', error);
		} finally {
			setLoading(false);
		}
	};

	return (
		<Card padding="large" variation="elevated">
			<Flex direction="column" gap="medium">
				<Heading level={3}>3D Box Visualization</Heading>

				<Flex direction="row" gap="small" alignItems="center">
					<Button
						onClick={initializeSimulation}
						isDisabled={loading || simulationId !== null}
						variation="primary"
					>
						Initialize Simulation
					</Button>

					<Button
						onClick={stepSimulation}
						isDisabled={loading || simulationId === null}
						variation="primary"
					>
						Step Simulation
					</Button>

					{loading && <Loader size="small" />}
				</Flex>

				{error && (
					<View padding="small" backgroundColor="error.10">
						<Text color="error.80">{error}</Text>
					</View>
				)}

				<View
					height="600px"
					borderRadius="medium"
					backgroundColor="background.secondary"
				>
					<Canvas camera={{ position: [50, 50, 50] }}>
						<Scene boxes={boxes} />
					</Canvas>
				</View>

				<Flex direction="row" gap="small" alignItems="center">
					<Text>Current Step:</Text>
					<Badge variation="info">{step}</Badge>
					{simulationId && (
						<Text fontSize="small" color="font.tertiary">
							Simulation ID: {simulationId}
						</Text>
					)}
				</Flex>

				<Flex direction="column" gap="small">
					<Text fontSize="small" color="font.secondary">
						Statistics:
					</Text>
					<Text fontSize="small">Total Boxes: {boxes.length}</Text>
					<Text fontSize="small">
						Stacked Boxes: {boxes.filter(box => box.is_stacked).length}
					</Text>
				</Flex>
			</Flex>
		</Card>
	);
};

export default BoxVisualization;
