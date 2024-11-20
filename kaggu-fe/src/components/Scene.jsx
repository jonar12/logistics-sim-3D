import Container from "./Container";
import Axes from "./Axes";
import { OrbitControls } from "@react-three/drei";
import Box from "./Box";
import Lift from "./Lift";

const Scene = ({ boxes, lifts, container }) => {
  return (
    <>
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <gridHelper args={[200, 200]} />

      {/* Render the axes */}
      <Axes />

      {/* Render the container */}
      {container && (
        <Container
          width={container.width}
          height={container.height}
          depth={container.depth}
        />
      )}

      {/* Render the boxes */}
      {boxes.map((box, index) => (
        <Box
          key={index}
          position={[box.pos[0], box.pos[1], box.pos[2]]}
          dimensions={[box.WHD[0], box.WHD[1], box.WHD[2]]}
          color={box.color}
        />
      ))}

      {/* Render the lifts */}
      {lifts.map((lift, index) => (
        <Lift key={index} position={[lift.pos[0], lift.pos[1], lift.pos[2]]} />
      ))}

      <OrbitControls />
    </>
  );
};

export default Scene;
