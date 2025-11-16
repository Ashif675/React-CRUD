# Flask + React Task Manager

## How to Run the Project

### Prerequisites
- Python 3.8+
- Node.js 14+ and npm

### Backend Setup

1. Create a virtual environment:
   python -m venv venv

2. Activate the virtual environment:
   - Windows: venv\Scripts\activate
   - Mac/Linux: source venv/bin/activate

3. Install dependencies:
   pip install -r requirements.txt

4. Run the Flask app:
   python backend/app.py
   
   The API will be available at http://localhost:5000

### Frontend Setup

1. Navigate to the frontend directory:
   cd frontend

2. Install dependencies:
   npm install

3. Run the React app:
   npm start
   
   The app will open at http://localhost:3000

### Running Tests

To run the backend tests:
pytest
