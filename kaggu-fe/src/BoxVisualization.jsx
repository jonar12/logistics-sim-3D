import {
  Badge,
  Button,
  Card,
  Flex,
  Heading,
  Loader,
  Text,
  View,
} from "@aws-amplify/ui-react";
import "@aws-amplify/ui-react/styles.css";
import { Canvas } from "@react-three/fiber";
import axios from "axios";
import { useEffect, useState } from "react";
import Scene from "./components/Scene";

const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: false,
  headers: {
    "Content-Type": "application/json",
  },
});

// Main component
const BoxVisualization = () => {
  const [simulationId, setSimulationId] = useState(null);
  const [boxes, setBoxes] = useState([]);
  const [lifts, setLifts] = useState([]);
  const [container, setContainer] = useState(null);
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isRunning, setIsRunning] = useState(false);

  // Initialize simulation
  const initializeSimulation = async () => {
    try {
      setLoading(true);
      setError(null);

      const { data } = await api.post("/simulations");
      const id = data.Location.split("/").pop();
      setSimulationId(id);

      // Set container corners from the API response
      setContainer(data.container);
      // Set lift data from the API response
      setLifts(data.lifts);
      // Set boxes data from the API response
      setBoxes(data.boxes);
      console.log("Container data: ", data.container);
    } catch (error) {
      let errorMessage = "Failed to initialize simulation";
      if (error.response) {
        errorMessage = `Server error: ${error.response.status}`;
      } else if (error.request) {
        errorMessage = "No response from server";
      } else {
        errorMessage = error.message;
      }
      setError(errorMessage);
      console.error("Error details:", error);
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
      // Set boxes data from the API response
      setBoxes(data.boxes);
      // Set lift data from the API response
      setLifts(data.lifts);
      setStep(data.step);
    } catch (error) {
      let errorMessage = "Failed to step simulation";
      if (error.response) {
        errorMessage = `Server error: ${error.response.status}`;
      } else if (error.request) {
        errorMessage = "No response from server";
      } else {
        errorMessage = error.message;
      }
      setError(errorMessage);
      console.error("Error details:", error);
    }
  };

  // Handle continuous simulation
  useEffect(() => {
    let interval;
    if (isRunning) {
      interval = setInterval(() => {
        stepSimulation();
      }, 50);
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
            {isRunning ? "Pause Simulation" : "Start Simulation"}
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
            <Scene boxes={boxes} lifts={lifts} container={container} />
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
            Stacked Boxes: {boxes.filter((box) => box.is_stacked).length}
          </Text>
        </Flex>
      </Flex>
    </Card>
  );
};

export default BoxVisualization;
