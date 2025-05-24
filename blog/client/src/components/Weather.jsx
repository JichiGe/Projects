import React, { useState, useEffect } from "react";
import "../style/weather.css";

const apiKey = "7888de52400879ba21f982e43ccb07ea";
const apiUrl = "https://api.openweathermap.org/data/2.5/weather?";
const iconUrlPrefix = "https://openweathermap.org/img/wn/";

const Weather = () => {
  const [data, setData] = useState(null);
  const [location, setLocation] = useState({ lat: null, lng: null });

  useEffect(() => {
    const fetchData = async () => {
      try {
        const position = await getCurrentPosition();
        const { latitude, longitude } = position.coords;
        setLocation({ lat: latitude, lng: longitude });
      } catch (error) {
        console.error("Error getting location:", error);
      }
    };

    fetchData();
  }, []);

  useEffect(() => {
    const getWeatherData = async () => {
      if (location.lat && location.lng) {
        try {

          const response = await fetch(
            `${apiUrl}lat=${location.lat}&lon=${location.lng}&appid=${apiKey}`
          );
          const weatherData = await response.json();
          setData(weatherData);
        } catch (error) {
          console.error("Error fetching weather data:", error);
        }
      }
    };

    getWeatherData();
  }, [location]);


  const getCurrentPosition = () => {
    return new Promise((resolve, reject) => {
      navigator.geolocation.getCurrentPosition(resolve, reject);
    });
  };

  return (
    <div className="weather-container">
      {data && data.weather ? (
        <table id="container">
          <tbody>
            <tr>
              <td rowSpan="5">
                <img
                  src={`${iconUrlPrefix}${data.weather[0].icon}@2x.png`}
                  alt="weather icon"
                />
              </td>
              <td>
                <h1>Current Weather: {data.weather[0].description.toUpperCase()}</h1>
              </td>
            </tr>
            <tr>
              <td>Location: {data.name}, {data.sys.country}</td>
            </tr>
            <tr>
              <td>Temperature: {Math.round(data.main.temp - 273.15)}℃, Feels Like: {Math.round(data.main.feels_like - 273.15)}℃</td>
            </tr>
            <tr>
              <td>Humidity: {data.main.humidity}%</td>
            </tr>
            <tr>
              <td>Wind Speed: {data.wind.speed} meters/second</td>
            </tr>
            <tr>
              <td>Pressure: {data.main.pressure} Pa</td>
            </tr>
          </tbody>
        </table>
      ) : (
        <p>Did not get the location from the User or Over the limitation of the API usage </p>
      )}
    </div>
  );
};

export default Weather;
