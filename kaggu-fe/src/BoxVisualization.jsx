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

// Container component to render the translucent yellow rectangle
const Container = ({ corners }) => {
	// Extract coordinates from corners
	const xCoords = corners.map(corner => corner[0]);
	const yCoords = corners.map(corner => corner[1]);
	const zCoords = corners.map(corner => corner[2]);

	// Calculate center position
	const centerX = (Math.min(...xCoords) + Math.max(...xCoords)) / 2;
	const centerY = (Math.min(...yCoords) + Math.max(...yCoords)) / 2;
	const centerZ = (Math.min(...zCoords) + Math.max(...zCoords)) / 2;

	// Calculate dimensions
	const width = Math.max(...xCoords) - Math.min(...xCoords);
	const height = Math.max(...yCoords) - Math.min(...yCoords);
	const depth = Math.max(...zCoords) - Math.min(...zCoords);

	return (
		<mesh position={[centerX, centerY, centerZ]}>
			<boxGeometry args={[width, height, depth]} />
			<meshStandardMaterial color="yellow" transparent opacity={0.3} />
		</mesh>
	);
};

// Main scene component
const Scene = ({ boxes, containerCorners }) => {
	return (
		<>
			<ambientLight intensity={0.5} />
			<pointLight position={[10, 10, 10]} />
			<gridHelper args={[100, 100]} />

			{/* Render the container */}
			{containerCorners && <Container corners={containerCorners} />}

			{/* Render the boxes */}
			{boxes.map((box, index) => (
				<Box
					key={index}
					position={[box.pos[0], box.pos[1], box.pos[2]]}
					dimensions={[box.WHD[0], box.WHD[1], box.WHD[2]]}
				/>
			))}

			<OrbitControls />
		</>
	);
};

// Box component to render individual boxes
// Box component to render individual boxes
const Box = ({ position, dimensions, color = '#1e40af' }) => {
	// Calculate the center position
	const centerX = position[0] + dimensions[0] / 2; // Corner X + half width
	const centerY = position[1] + dimensions[1] / 2; // Corner Y + half height
	const centerZ = position[2] + dimensions[2] / 2; // Corner Z + half depth

	return (
		<mesh position={[centerX, centerY, centerZ]}>
			<boxGeometry args={dimensions} />
			<meshStandardMaterial color={color} />
		</mesh>
	);
};

// Main component
const BoxVisualization = () => {
	const [simulationId, setSimulationId] = useState(null);
	const [boxes, setBoxes] = useState([]);
	const [containerCorners, setContainerCorners] = useState(null); // Store container corners
	const [step, setStep] = useState(0);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState(null);
	const [isRunning, setIsRunning] = useState(false);

	// Initialize simulation
	const initializeSimulation = async () => {
		try {
			setLoading(true);
			setError(null);

			const { data } = await api.post('/simulations');
			const id = data.Location.split('/').pop();
			setSimulationId(id);

			// Set container corners from the API response
			setContainerCorners(data.container_corners);
		} catch (error) {
			let errorMessage = 'Failed to initialize simulation';
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

	// Step simulation
	const stepSimulation = async () => {
		if (!simulationId) return;

		try {
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
		}
	};

	// Handle continuous simulation
	useEffect(() => {
		let interval;
		if (isRunning) {
			interval = setInterval(() => {
				stepSimulation();
			}, 100);
		}
		return () => clearInterval(interval);
	}, [isRunning, simulationId]);

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
						onClick={() => setIsRunning(!isRunning)}
						isDisabled={simulationId === null}
						variation="primary"
					>
						{isRunning ? 'Pause Simulation' : 'Start Simulation'}
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
						<Scene boxes={boxes} containerCorners={containerCorners} />
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
