import React, { useState } from "react";
import "./styles.css";

function RadioButtonGroup() {
  const [selectedValue, setSelectedValue] = useState("forward");
  const [isButtonDisabled, setIsButtonDisabled] = useState(false);

  const handleClick = async (value) => {
    setSelectedValue(value);
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
    <div className="radio-button-group">
      <button
        className={`radio-button ${
          selectedValue === "forward" ? "selected" : ""
        }`}
        onClick={() => handleClick("forward")}
        disabled={isButtonDisabled} // Deshabilitar el botón si isButtonDisabled es true
      >
        Forward
      </button>
      <button
        className={`radio-button ${
          selectedValue === "reverse" ? "selected" : ""
        }`}
        onClick={() => handleClick("reverse")}
        disabled={isButtonDisabled} // Deshabilitar el botón si isButtonDisabled es true
      >
        Backward
      </button>
    </div>
  );
}

export default RadioButtonGroup;
