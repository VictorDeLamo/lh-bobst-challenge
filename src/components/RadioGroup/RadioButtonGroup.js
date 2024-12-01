import React, { useState } from "react";

import "./styles.css";

function RadioButtonGroup() {
  const [selectedValue, setSelectedValue] = useState("play");

  const handleClick = async (value) => {
    setSelectedValue(value);

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

  return (
    <div className="radio-button-group">
      <button
        className={`radio-button ${selectedValue === "play" ? "selected" : ""}`}
        onClick={() => handleClick("forward")}
      >
        Forward
      </button>
      <button
        className={`radio-button ${selectedValue === "stop" ? "selected" : ""}`}
        onClick={() => handleClick("reverse")}
      >
        Backward
      </button>
    </div>
  );
}

export default RadioButtonGroup;
