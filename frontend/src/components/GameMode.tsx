import { useState, useRef } from "react"

interface Identification {
    [key: string]: any; 
    name: string;
    picture: string;
    summary: string;
    user_data: any;
    beak_shape_1: string;
    size: string;
    leg_colour: string;
    tail_shape_1: string;
    plumage_colour: string;
    pattern_markings: string;
    sex_age_variations: string;
  }
  
  type Identifications = Identification[];
  
  const GameMode = () => {
    const [birdDescription, setBirdDescription] = useState("");
    const [birdData, setBirdData] = useState<Identification | null>(null);
    const [showImage, setShowImage] = useState(false);
    const imageRef = useRef<HTMLImageElement>(null);
    const [error, setError] = useState<string | null>(null); // Add error state
  
    const handleGameStart = async () => {
      setError(null); // Clear any previous errors
      try {
        const response = await fetch("http://localhost:5000/birds", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            message: "I saw a black bird with a yellow beak and a fan tail",
            categoryPrompt: "",
            categories: {},
            user_data: {},
          }),
        });
  
        if (!response.ok) {
          const errorData = await response.json(); // Try to get error details
          const errorMessage = errorData.error || "Failed to fetch bird data";
          throw new Error(errorMessage);
        }
  
        const data = await response.json();
        console.log(data)
        const birdResult: Identifications = data.data.identifications;
        console.log(birdResult)
  
        if (birdResult.length > 0) {
          setBirdData(birdResult[0]);
          const summaryKey = Object.keys(birdResult[0]).find(
            (key) => key.trim() === "summary"
          );
          if (summaryKey !== undefined) {
            setBirdDescription(birdResult[0][summaryKey]);
          }
          setShowImage(true);
          setTimeout(() => setShowImage(false), 3000);
        } else {
          console.error("No bird identifications returned.");
          setError("No bird found matching description."); // Set error message
        }
      } catch (error: any) {
        console.error("Error fetching bird data:", error);
        setError(error.message); // Set error message
      }
    };

  return (
    <div>
      <button style={{background: "green", borderRadius: "9999px", color:"white", padding:"5px"}} onClick={handleGameStart}>Start Game</button>
      {showImage && birdData && birdData.picture && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundColor: "rgba(0, 0, 0, 0.7)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            zIndex: 1000,
          }}
        >
          <div
            style={{
              width: "500px", // Fixed width
              height: "500px", // Fixed height
              overflow: "hidden",
              borderRadius: "50%",
            }}
          >
            <img
              src={birdData.picture}
              alt={birdData.name}
              style={{ width: "100%", height: "100%", objectFit: "cover" }}
            />
          </div>
        </div>
      )}
      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
};
    
    export default GameMode;