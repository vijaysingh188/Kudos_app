# Kudos Project

## Overview
The Kudos project is a web application designed to allow users to give and receive kudos within an organization. It consists of a backend built with Django and a frontend built with React.

## Project Structure

### Backend
The backend is located in the `kudos_pro` directory and is built using Django. It includes the following key components:
- **Models**: Define the database schema.
- **Views**: Handle the business logic.
- **Serializers**: Convert complex data types to JSON.
- **Management Commands**: Custom commands for tasks like generating demo data.

### Frontend
The frontend is located in the `kudos-frontend` directory and is built using React. It includes the following key components:
- **Components**: Reusable UI components.
- **Pages**: Represent different views in the application.
- **Services**: Handle API calls and authentication.

## Setup Instructions

### Backend Setup
1. Navigate to the `kudos_pro` directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Apply migrations:
   ```bash
   python manage.py migrate
   ```
4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
5. Start the development server:
   ```bash
   python manage.py runserver
   ```

### Frontend Setup
1. Navigate to the `kudos-frontend` directory.
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm start
   ```

## Usage
- Access the application at `http://localhost:3000` for the frontend and `http://localhost:8000` for the backend.
- Login with your credentials to start giving and receiving kudos.

## License
This project is licensed under the MIT License.