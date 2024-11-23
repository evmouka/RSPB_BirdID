import { useNavigate } from "react-router-dom";

interface BirdIdentityProps {
  imageSrc: string; 
  birdName: string;
  imageSize: string
}

const BirdIdentity = ({imageSrc, birdName, imageSize}: BirdIdentityProps) => {

  const navigate = useNavigate();

    const handleClick = () => {
        navigate("/result");
      };

  return (
    <div style={{ textAlign: "center", padding: "20px", display: "flex", flexDirection: "column", alignItems: "center", width: imageSize }}>
     <img
        src={imageSrc}
        alt="Descriptive Alt Text"
        style={{ maxWidth: "300px", height: "300px", marginBottom: "20px", borderRadius: "50%" }}
      />
      <h1 style={{ margin: "10px 0", fontSize: "xx-large" }}>New Species Identified!</h1> {/* Static header */}
      <h2 style={{ margin: "10px 0", fontSize: "xx-large", fontWeight: "bold" }}>{birdName}</h2>
      <button
      onClick={handleClick}
        style={{
          padding: "10px 20px",
          backgroundColor: "#57A627",
          color: "#fff",
          border: "none",
          borderRadius: "9999px",
          cursor: "pointer",
          display: "inline-flex",
          alignItems: "center",
          height: "50px",
          gap: "8px",
        }}
      >
        <img 
          src="../../public/Plus.svg" 
          alt="Add" 
          width="15" 
          height="15"
          />
        Add to my list
      </button>
    </div>
  );
};

export default BirdIdentity;
