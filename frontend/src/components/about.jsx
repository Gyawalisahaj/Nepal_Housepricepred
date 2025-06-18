 import React from "react";

const About = () => {
  return (
    <div className="max-w-3xl mx-auto px-4 py-10">
      <h1 className="text-3xl font-bold mb-6 text-center">About This Project</h1>
      <p className="text-lg mb-4">
        The Housing Price Prediction is a full stack machinelearning project that estimate the house price on the basis of input feature like BHK, Bath, Road Access, Facing direction and Area.
      </p>
      <p className="text-lg mb-4">
        This project uses web scraping via BeautifulSoup for data collection, extensive EDA, and Random Forest with hyperparameter tuning for accurate predictions. It is deployed using Flask and presented with a simple UI.
      </p>
      <p className="text-lg">
        It aims to assist buyers, sellers, and real estate professionals in understanding price trends and making informed decisions. The project is open-source and available on GitHub.
      </p>
    </div>
  );
};

export default About;
