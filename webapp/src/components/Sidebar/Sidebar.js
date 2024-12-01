// src/Sidebar.js
import React from "react";
import "./Sidebar.css";
import RadioButtonGroup from "../RadioGroup/RadioButtonGroup";
import {
  faPlay,
  faStop,
  faForward,
  faBackward,
} from "@fortawesome/free-solid-svg-icons";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";

const handleClick = async (value) => {
  try {
    const response = await fetch(`http://10.0.4.4:5000/${value}`, {
      method: "POST",
    });
    const data = await response.json();
    console.log(data);
  } catch (error) {
    console.error("Error fetching data:", error);
  }
};

function Sidebar() {
  return (
    <div className="sidebar">
      <button className="sidebar-button" onClick={() => handleClick("start")}>
        <FontAwesomeIcon icon={faPlay} /> Play
      </button>
      <button className="sidebar-button" onClick={() => handleClick("stop")}>
        <FontAwesomeIcon icon={faStop} /> Stop
      </button>
      <button className="sidebar-button" onClick={() => handleClick("fast")}>
        <FontAwesomeIcon icon={faForward} /> Faster
      </button>
      <button className="sidebar-button" onClick={() => handleClick("slow")}>
        <FontAwesomeIcon icon={faBackward} /> Slower
      </button>
      <RadioButtonGroup />
    </div>
  );
}

export default Sidebar;
