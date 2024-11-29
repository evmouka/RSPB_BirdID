import { useNavigate, useLocation } from "react-router-dom";
import "./bird_result.css"
import { useState, useEffect } from "react";

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

const BirdResult: React.FC = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const birdFromRoute = location.state;


    const [birdData, setBirdData] = useState(birdFromRoute || {});
    const [birdDescription, setBirdDescription] = useState('');

    useEffect(() => {    
        if (birdData) {
            window.scrollTo({ top: 0, behavior: 'smooth' });
          const summaryKey = Object.keys(birdData).find(key => key.trim() === 'summary');
          if (summaryKey !== undefined) {
            setBirdDescription(birdData[summaryKey]);
          }
        }
      }, [birdData]);

      const getPlumageColors = (plumage: string) => {
        return plumage
            .replace(/Plumage colour\(s\):/, '') // Remove the label
            .split(/[,/]/) // Split by comma or slash
            .map((color) => color.trim()) // Trim extra whitespace
            .filter((color) => color !== ""); // Remove empty values
    };



      if (!birdData) {
        return <div>Loading...</div>;
    }
    const handleClick = () => {
        navigate("/chat");
      };

    const plumageColours = getPlumageColors(birdData.plumage_colour);

  return (
    <div className="flex flex-col h-screen w-full">
            <div className="header icon-text">
            <div onClick={handleClick} className="arrow cursor-pointer">
                <img src="/images/arrow_left.png"/>
            </div>
            <div className="bird-name">
                <p className="large medium">
                    {birdData.name}
                </p>
            </div>
        </div>

        <div className="images">

            <div className="image-list">
                <img className="image-list" src={birdData.picture}/>
                {/* <ul className="no-bullet">
                    <li><img src="/images/housesparrow2.png"/></li>
                    <li><img src="/images/housesparrow.png"/></li>
                </ul> */}
            </div>
            
            <div className="caption">
                <div className="caption-content icon-text">
                    <div className="caption-icon">
                        <img src="/images/cameraicon.png"/>
                    </div>
                    <div className="caption-text">
                        <p>{birdData.name}</p>
                    </div>
                </div>
                <div className="menu-icon">
                    <img src="/images/threedots.png"/>
                </div>
            </div>
        </div>

        <div className="information" style={{paddingLeft: "1em"}}>
            <div className="bird-title" style={{fontSize: "xx-large"}}>
                <h2>{birdData.name}</h2>
            </div>
            <div className="bird-gender" style={{fontSize: "large"}}>
                <ul className="no-bullet">
                    {birdData.sex_age_variations == "male" ? <li>Male</li>
                    : <li>Female</li>}
                </ul>
            </div>
            <div className="bird-match">
                <p className="blue">45% match</p>
            </div>
            <div className="conservation-status">
                <p>UK Conservation status: <span className="dot red"></span>Red <img src="/images/information.svg" width="16px" height="16px"/></p>
            </div>
            <div className="icon-text">
                <div className="location-icon">
                    <img src="/images/location.svg"/>
                </div>
                <div className="location-text">
                    <p> UK resident</p>
                </div>
            </div>

            <div className="description">
                    <p>{birdDescription}</p>
            </div>

            <button className="big-green">
                <div className="icon-text">
                    <img src="/images/save.svg"/>
                    Add to my list
                </div>
            </button>
        </div>

        <div className="features" style={{paddingLeft: "1em"}}>
            <div className="features-heading">
                <p className="strong">Key features</p>
            </div>
            
            <div className="features-cards">
                <div className="features-item">
                    <div className="features-stats">
                        <p className="medium">Size</p>
                        <p className="small">14-15cm</p>
                    </div>
                    <div className="features-content">
                        <img src="/images/birdscale.svg"/>
                    </div>
                </div>
                <div className="features-item">
                    <div className="features-stats">
                        <p className="medium">Feathers</p>
                    </div>
                    {plumageColours.map((color, index) => (
                        <div key={index} className="colours icon-text">
                            <div className="icon">
                                <span className={`dot ${color.toLowerCase().replace(/ /g, '-')}`}></span>
                                </div>
                                <div className="colour">
                                    <p>{color}</p>
                                    </div>
                                    </div>
                                ))}
                </div>
                <div className="features-item">
                    <div className="features-stats">
                        <p className="medium">Size</p>
                        <p className="small">{birdData.size}</p>
                    </div>
                </div>
                <div className="features-item">
                    <div className="features-stats">
                        <p className="medium">Beak</p>
                        <p className="small">{birdData.beak_shape_1}</p>
                    </div>
                    <div className="features-content">
                        <img src="/images/Beak.png"/>
                    </div>
                </div>
                <div className="features-item">
                    <div className="features-stats">
                        <p className="medium">{birdData.leg_colour}</p>
                    </div>
                    <div className="colours icon-text">
                        <div className="icon">
                            <span className="dot brown"></span>
                        </div>
                        <div className="colour">
                            <p>Brown</p>
                        </div>
                    </div>
                </div>
                <div className="features-item">
                    <div className="features-stats">
                        <p className="medium">Tail</p>
                        <p className="small">Double</p>
                    </div>
                    <div className="features-content">
                        <img src="/images/Tail.png"/>
                    </div>
                </div>  
            </div>
        </div>
    </div>
  );
};

export default BirdResult;