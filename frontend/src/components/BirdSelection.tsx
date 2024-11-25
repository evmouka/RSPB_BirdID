import React from 'react';

interface Bird {
    [key: string]: string;
  name: string;
  picture: string;
}

interface BirdSelectionProps {
  birdResults: Bird[];
  setBirdResults: React.Dispatch<React.SetStateAction<Bird[]>>;
  setImageSrc: React.Dispatch<React.SetStateAction<string>>;
  SetBirdName: React.Dispatch<React.SetStateAction<string>>;
  //bird Summary requires the field passed from the request to be standard, currently it is "summary\n"
//   setBirdSummary: React.Dispatch<React.SetStateAction<string>>; 
}

const BirdSelection: React.FC<BirdSelectionProps> = ({
  birdResults,
  setBirdResults,
  setImageSrc,
  SetBirdName,
//   setBirdSummary
}) => {

  return (
    <div style={{ textAlign: "center", padding: "20px" }}>
      <h1 style={{ fontSize: "xx-large", marginBottom: "20px" }}>Select the Bird</h1>
      <div style={{ display: "flex", flexWrap: "wrap", justifyContent: "center", gap: "20px" }}>
        {birdResults.map((bird, index) => (
          <div
            key={index}
            onClick={() => {
              setBirdResults([bird]); // Keep only the selected bird
              setImageSrc(bird.picture);
              SetBirdName(bird.name);
            //   setBirdSummary(bird.summary);
            }}
            style={{
              cursor: "pointer",
              border: "1px solid #ccc",
              borderRadius: "8px",
              padding: "10px",
              textAlign: "center",
              width: "150px",
              boxShadow: "0 4px 6px rgba(0,0,0,0.1)",
              transition: "transform 0.2s",
            }}
          >
            <img
              src={bird.picture}
              alt={bird.name}
              style={{ maxWidth: "100%", height: "100px", objectFit: "cover", borderRadius: "8px" }}
            />
            <p style={{ marginTop: "10px", fontSize: "medium", fontWeight: "bold" }}>{bird.name}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BirdSelection;
