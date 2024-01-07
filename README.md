Description:

This project implements a machine learning model to predict the compressive strength (MPa) of concrete based on various features:

Components:
Cement (kg/m³)
Blast Furnace Slag (kg/m³)
Fly Ash (kg/m³)
Water (kg/m³)
Superplasticizer (kg/m³)
Coarse Aggregate (kg/m³)
Fine Aggregate (kg/m³)
Age (days)
Key Features:

Predicts concrete compressive strength with high accuracy.
Uses a variety of features for comprehensive analysis.
Offers flexibility in deployment options (local or cloud).
Potential Applications:

Optimizing concrete mix design for desired strength and cost.
Assessing the quality of existing concrete structures.
Predicting the long-term strength of concrete.
Model Training:

The model is trained on a dataset of concrete samples with known strengths and corresponding component values. Different machine learning algorithms can be used, depending on the desired accuracy and data characteristics.

Deployment Options:

Local: Run the model directly on your machine for development and testing purposes.
Cloud: Deploy the model as a web service on a cloud platform like AWS App Runner for wider accessibility and scalability.

Usage 
Send a POST request to the API endpoint with the Pokémon's features in the request body at http://localhost:5000/predict
OR you may upload a file for Batch Prediction using route '/predict_file" and your file with predicted outputs will be downloaded in your system when request method is "POST"

Contact
https://www.linkedin.com/in/aryan-gaur-b49550258/)https://www.linkedin.com/in/aryan-gaur-b49550258/
