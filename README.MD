# 🚲 Bicycle Sharing Dashboard

This project is a data visualization dashboard built using **Streamlit**, focused on analyzing a public bicycle sharing dataset. It allows users to explore key trends such as seasonal demand, holiday usage, and customer behavior patterns using interactive charts.

## 📊 Features

- Visualize bike rentals per season, weekday, and working/holiday status.
- Explore average rentals per year and season.
- Group rental counts into Low, Medium, High (clustering-based binning).
- RFM analysis for customer segmentation based on rental activity.

## 🛠️ How to Run Locally

1. Clone this repository:
   ```bash
   git clone https://github.com/atifa1110/Dashboard-Bicycle.git
   cd Dashboard-Bicycle

## Setup Environment - Anaconda

- conda create --name main-ds python=3.9
- conda activate main-ds
- pip install -r requirements.txt

##  Setup Environment - Shell/Terminal

- mkdir create_streamlit
- cd create_streamlit
- pipenv install
- pipenv shell
- pip install -r requirements.txt

## 🧩 Dependencies

List of main Python libraries used:
- pandas  
- matplotlib  
- seaborn  
- streamlit  

## Run the Streamlit dashboard:

### Most common way
streamlit run app.py

### Safer for virtual environments
python -m streamlit run app.py