# Urban Travel Assistant

An AI-powered travel planning assistant built using **Python, Streamlit, and Google Gemini API**.  
The application helps users plan trips through a guided workflow and provides intelligent travel recommendations, travel tips, and chatbot support.

---

## Features

- AI-powered travel recommendations
- Destination suggestions based on travel preferences
- Attractions, food, clothing, safety, and cultural tips
- Interactive travel checklist for packing essentials
- AI chatbot for travel-related questions
- Clean and interactive Streamlit interface

---

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- JSON
- Session State Management

---

## Project Structure

```
travel-chatbot
│
├── app.py
├── auth.py
├── ai_services.py
├── travel_flow.py
├── ui_styles.py
├── users.json
├── requirements.txt
│
├── templates
│   └── chat.html
│
└── .streamlit
    └── config.toml
```

---

## Installation

### Clone the repository

```
git clone https://github.com/yourusername/travel-chatbot.git
```

### Navigate to the project folder

```
cd travel-chatbot
```

### Install dependencies

```
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file and add your Gemini API key.

```
GEMINI_API_KEY=your_api_key_here
```

---

## Run the Application

```
streamlit run app.py
```

The application will run at:

```
http://localhost:8501
```

---

## Future Improvements

- Google Maps integration
- Hotel and transport suggestions
- Save travel itineraries
- Online deployment

---

## Author

**Chetana Korivi**  
B.Tech – Artificial Intelligence & Data Science
