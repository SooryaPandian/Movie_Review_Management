# Movie Review System

This is a simple Movie Review System built using Flask, MySQL, and the TMDb API.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/SooryaPandian/Movie_Review_Management
    cd movie-review-system
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Setting Up the Database

1. Make sure you have MySQL installed on your system.

2. Create a new MySQL database and user:

    ```sql
    CREATE DATABASE movie_review_system;
    CREATE USER 'movie_user'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON movie_review_system.* TO 'movie_user'@'localhost';
    FLUSH PRIVILEGES;
    ```

4. Run the following SQL queries to create the required tables:

    ```sql
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    );

    CREATE TABLE reviews (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        movie_id INT,
        rating INT,
        comment TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id)
    );
    ```

## Usage

1. Start the Flask server:

    ```bash
    python app.py
    ```

2. Open your web browser and navigate to `http://localhost:5000` to access the application.
