const Container = ({ width, height, depth }) => {
	// Calculate center position assuming the container starts at (0, 0, 0)
	const centerX = width / 2;
	const centerY = height / 2;
	const centerZ = depth / 2;

	return (
		<mesh position={[centerX, centerY, centerZ]}>
			<boxGeometry args={[width, height, depth]} />
			<meshStandardMaterial color="yellow" transparent opacity={0.3} />
		</mesh>
	);
};

export default Container;
