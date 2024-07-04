# GymTrack

GymTrack is a web application designed to support individuals in managing their fitness journey with a strong focus on organization.

- [About](#about)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

## About

GymTrack is a note-taking hub where users can create personalized workout sessions and add detailed notes for each section. It serves as a comprehensive tool for tracking and organizing fitness routines and progress.

## Features

- User registration and profile management
- Craft custom unique workout sections
- Create detailed notes to track progress.

## Technologies Used
- Flask (Backend framework)
- Bootstrap (CSS framework)
- MongoDB(Database)
- Flask-Bcrypt(Password hashing)

## Getting Started

To run GymTrack locally, follow these instructions:

### Prerequisites

- Python 3.x
- MongoDB

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/GymTrack.git

2. Install Python dependencies:
pip install -r project3requirements.txt

3. Set up the MongoDB database and configure the database URI in `project3config.py`.

4. Run the Flask backend:
   
## Usage

1. Open your web browser and go to `http://localhost:3000` to access the application.
2. Register as a patient or nurse and log in to your account.
3. Schedule vaccination appointments or record vaccinations as a nurse.
4. Manage your profile and view vaccination records.
flask run

## Usage

1. Open your web browser and go to `http://localhost:5000/home` to access the application.
2. Register as a user and log in to your account.
3. Create, delete, or update workout sections.
4. Add, delete or edit workout notes.


## API Endpoints

These are the following API endpoints:

- **GET /api**: Fetch all users
- **POST /api**: Create a user
- **GET /api/(idx)**: Fetch data for a certain user
- **PUT /api/(idx)**: Update data for a certain user
- **DELETE /api/(idx)**: Delete a user and related data.

## Contributing
Contributions are welcome! If you'd like to contribute to GymTrack, please fork the repository, make changes, and submit a pull request.

If you encounter any bugs or have suggestions for improvements, please open an issue on GitHub.

   


