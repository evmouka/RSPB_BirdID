import React, { useState, useEffect } from "react";

interface GameModeProps {
  onGameStart: (birdId: string, imageSrc: string) => void;
}

const GameMode: React.FC<GameModeProps> = ({ onGameStart }) => {
  const [birdId, setBirdId] = useState<string | null>(null); // Save the bird ID
  const [showImage, setShowImage] = useState(false);
  const [imageSrc, setImageSrc] = useState<string | null>(null); // Save image URL
  const [error, setError] = useState<string | null>(null); // Error state

  const handleGameStart = async () => {
    setError(null); // Clear previous errors
    setShowImage(false); // Reset image display
    try {
      const response = await fetch("http://localhost:5000/new-bird");

      if (!response.ok) {
        const errorData = await response.json();
        const errorMessage = errorData.error || "Failed to fetch bird data";
        throw new Error(errorMessage);
      }

      const data = await response.json();
      setBirdId(data.id); // Save the bird ID
      setImageSrc(data.image); // Save the image URL
      setShowImage(true); // Show the image

      // Pass birdId and imageSrc to parent component
      onGameStart(data.id, data.image);

      // Hide the image after 5 seconds
      setTimeout(() => {
        setShowImage(false);
      }, 5000);
    } catch (error: any) {
      console.error("Error fetching bird data:", error);
      setError(error.message); // Show error message
    }
  };

  return (
    <div>
      <button
        style={{
          background: "rgb(45,212,191)",
          borderRadius: "15px",
          color: "black",
          padding: "5px 20px",
          margin: "1rem"
        }}
        onClick={handleGameStart}
      >
        Start Game
      </button>

      {showImage && imageSrc && (
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
            zIndex: 10000, // Ensure the overlay is on top
          }}
        >
          <div
            style={{
              width: "500px",
              height: "500px",
              overflow: "hidden",
              borderRadius: "50%",
            }}
          >
            <img
              src={imageSrc}
              alt="Bird"
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