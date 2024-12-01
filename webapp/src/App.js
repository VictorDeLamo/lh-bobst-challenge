// src/App.js
import React, { useEffect } from "react";
import "./App.css";
import Sidebar from "./components/Sidebar/Sidebar";
import ChartComponent from "./components/ChartComponent";

function App() {
  const [dataEnergy, setDataEnergy] = React.useState([]);
  const [dataEnergyPrize, setDataEnergyPrize] = React.useState([]);
  const [dataAvgspeed, setDataAvgspeed] = React.useState([]);
  const [dataBoxes, setDataBoxes] = React.useState([]);
  const [dataInstspeed, setInstspeed] = React.useState([]);
  const [dataDistcenter, setDistcenter] = React.useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch("http://10.0.4.4:5000/data");
        const result = await response.json();
        setDataEnergy((prevDataEnergy) => [
          ...prevDataEnergy,
          { time: new Date().toLocaleTimeString(), value: result.energy },
        ]);
        setDataEnergyPrize((prevDataEnergyPrize) => [
          ...prevDataEnergyPrize,
          { time: new Date().toLocaleTimeString(), value: result.energyprize },
        ]);
        setDataAvgspeed((prevDataAvgspeed) => [
          ...prevDataAvgspeed,
          { time: new Date().toLocaleTimeString(), value: result.avgspeed },
        ]);
        setDataBoxes((prevDataBoxes) => [
          ...prevDataBoxes,
          { time: new Date().toLocaleTimeString(), value: result.boxes },
        ]);
        setInstspeed((prevDataInstspeed) => [
          ...prevDataInstspeed,
          { time: new Date().toLocaleTimeString(), value: result.instspeed },
        ]);
        setDistcenter((prevDataDistcenter) => [
          ...prevDataDistcenter,
          { time: new Date().toLocaleTimeString(), value: result.latdist },
        ]);
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    fetchData();
    const interval = setInterval(fetchData, 10000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <Sidebar />
      <div className="content">
        <h1>Bienvenido a mi aplicación React</h1>
        <div className="chart-grid">
          <ChartComponent data={dataEnergy} title="Energy consumption" />
          <ChartComponent data={dataEnergyPrize} title="Waste" />
          <ChartComponent data={dataAvgspeed} title="Live Data Chart 4" />
          <ChartComponent data={dataBoxes} title="Live Data Chart 5" />
          <ChartComponent data={dataInstspeed} title="Live Data Chart 6" />
          <ChartComponent data={dataDistcenter} title="Live Data Chart 6" />
        </div>
      </div>
    </div>
  );
}

export default App;
