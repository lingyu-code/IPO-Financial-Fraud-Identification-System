# IPO-Financial-Fraud-Identification-System

This project aims to identify financial fraud in Initial Public Offerings (IPOs) using a combination of machine learning and data analysis techniques. It provides a comprehensive system for analyzing company data, detecting anomalies, and flagging potential fraudulent activities.

## Project Structure

The project is divided into two main parts:

- **`backend/`**: A Django-based backend API that handles data storage, processing, and serves the machine learning models.
- **`frontend/`**: A Vue.js-based frontend application that provides a user interface for interacting with the system, visualizing data, and managing IPO companies.

## Features

- User authentication and authorization.
- Management of IPO company data.
- Financial fraud detection and analytics.
- Data visualization for insights into company performance and potential risks.

## Setup and Installation

To set up and run the project locally, follow these steps:

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm or yarn
- pip

### Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
   (Note: A `requirements.txt` file will need to be created if it doesn't exist, containing all backend dependencies.)
4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser (optional, for admin access):
   ```bash
   python manage.py createsuperuser
   ```
6. Run the backend server:
   ```bash
   python manage.py runserver
   ```
   The backend API will be available at `http://127.0.0.1:8000/`.

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Install the Node.js dependencies:
   ```bash
   npm install
   ```
3. Run the frontend development server:
   ```bash
   npm run dev
   ```
   The frontend application will be available at `http://localhost:5173/` (or another port if 5173 is in use).

## Usage

- Access the frontend application in your browser (e.g., `http://localhost:5173/`).
- Register a new user or log in with existing credentials.
- Explore the dashboard, manage IPO companies, and view analytics related to financial fraud detection.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for any bugs or feature requests.

## License

This project is licensed under the MIT License.
