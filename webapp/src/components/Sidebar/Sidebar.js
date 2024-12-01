import React, { useState } from "react";
import "./Sidebar.css";
import RadioButtonGroup from "../RadioGroup/RadioButtonGroup";
import {
  faPlay,
  faStop,
  faForward,
  faBackward,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import caja from "./caja.png";

function Sidebar() {
  const [isButtonDisabled, setIsButtonDisabled] = useState(false);

  const handleClick = async (value) => {
    setIsButtonDisabled(true); // Deshabilitar los botones

    try {
      const response = await fetch(`http://10.0.4.4:5000/${value}`, {
        method: "POST",
      });
      const data = await response.json();
      console.log(data);
    } catch (error) {
      console.error("Error fetching data:", error);
    }

    // Habilitar los botones después de 1 segundo
    setTimeout(() => {
      setIsButtonDisabled(false);
    }, 100);
  };

  return (
    <div className="sidebar">
      <img src={caja} alt="Description of the image" />
      <button
        className="sidebar-button"
        onClick={() => handleClick("start")}
        disabled={isButtonDisabled} // Deshabilitar el botón si isButtonDisabled es true
      >
        <FontAwesomeIcon icon={faPlay} /> Play
      </button>
      <button
        className="sidebar-button"
        onClick={() => handleClick("stop")}
        disabled={isButtonDisabled} // Deshabilitar el botón si isButtonDisabled es true
      >
        <FontAwesomeIcon icon={faStop} /> Stop
      </button>
      <button
        className="sidebar-button"
        onClick={() => handleClick("fast")}
        disabled={isButtonDisabled} // Deshabilitar el botón si isButtonDisabled es true
      >
        <FontAwesomeIcon icon={faForward} /> Faster
      </button>
      <button
        className="sidebar-button"
        onClick={() => handleClick("slow")}
        disabled={isButtonDisabled} // Deshabilitar el botón si isButtonDisabled es true
      >
        <FontAwesomeIcon icon={faBackward} /> Slower
      </button>
      <RadioButtonGroup />
    </div>
  );
}

export default Sidebar;
