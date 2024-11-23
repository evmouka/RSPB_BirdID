import "./bird_result.css"
import { useEffect, useState } from "react";

interface Identification {
    name: string;
    picture: string;
    summary: string;
    user_data: any;
  }
  
  type Identifications = Identification[];
  

const BirdResult: React.FC = () => {

    const [imageSrc, setImageSrc] = useState("")
    const [birdName, SetBirdName] = useState("")

    const fetchData = async () => {
        await fetch("http://localhost:5000/birds", {
        method: "POST",
        headers: {
          "Content-Type": "Application/json"
        },
        body: JSON.stringify({
          "message": "I saw a black bird with a yellow beak and a fan tail",
          "categoryPrompt": "",
          "categories": {},
        })
      })
      .then((res) => {
        if (!res.ok) throw new Error("Failed to fetch response");
        return res.json();
      })
      .then((response) => {
        const data = response.data;
        const birdResult: Identifications = data.identifications;

        setImageSrc(birdResult[0].picture);
        SetBirdName(birdResult[0].name);
      })}

      fetchData();
  
  return (
    <div className="flex flex-col h-screen w-full">
            <div className="header icon-text">
            <div className="arrow">
                <img src="/images/arrow_left.png"/>
            </div>
            <div className="bird-name">
                <p className="large medium">
                    {birdName}
                </p>
            </div>
        </div>

        <div className="images">

            <div className="image-list">
                <img className="image-list" src="/images/housesparrow2.png"/>
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
                        <p>Adult female House Sparrow</p>
                    </div>
                </div>
                <div className="menu-icon">
                    <img src="/images/threedots.png"/>
                </div>
            </div>
        </div>

        <div className="information">
            <div className="bird-title">
                <h2>House sparrow</h2>
            </div>
            <div className="bird-gender">
                <ul className="no-bullet">
                    <li>Male</li>
                    <li>Female</li>
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
                <p>These noisy and sociable birds are found around the world, thanks to their cheerful ability to make the most of humanity's rubbish and wastefulness.</p>
            </div>

            <button className="big-green">
                <div className="icon-text">
                    <img src="/images/save.svg"/>
                    Add to my list
                </div>
            </button>
        </div>

        <div className="features">
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
                    <div className="colours icon-text">
                        <div className="icon">
                            <span className="dot brown"></span>
                        </div>
                        <div className="colour">
                            <p>Brown</p>
                        </div>
                    </div>
                    <div className="colours icon-text">
                        <div className="icon">
                            <span className="dot grey"></span>
                        </div>
                        <div className="colour">
                            <p>Grey</p>
                        </div>
                    </div>
                    <div className="colours icon-text">
                        <div className="icon">
                            <span className="dot cream"></span>
                        </div>
                        <div className="colour">
                            <p>Cream</p>
                        </div>
                    </div>
                </div>
                <div className="features-item">
                    <div className="features-stats">
                        <p className="medium">Size</p>
                        <p className="small">Brown streaked belly and breast</p>
                    </div>
                </div>
                <div className="features-item">
                    <div className="features-stats">
                        <p className="medium">Beak</p>
                        <p className="small">Short, stubby and pointed</p>
                    </div>
                    <div className="features-content">
                        <img src="/images/Beak.png"/>
                    </div>
                </div>
                <div className="features-item">
                    <div className="features-stats">
                        <p className="medium">Legs</p>
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