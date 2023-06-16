# Online Learning Platform

This is a Flask-based online learning platform that allows users to authenticate, manage courses, and retrieve course information. It provides a set of APIs for various functionalities.

## Prerequisites

Before running the application, make sure you have the following:

- Python installed on your system.
- Required packages installed (`Flask`, `Flask-JWT-Extended`, `Flask-Admin`, `Authlib`, `SQLAlchemy`, `python-dotenv`).

## Installation

1. Clone the repository:

   ```shell
   git clone <repository_url>

2. Navigate to the project directory:

    ```shell
    cd <project_directory>

3. Install the required packages:
    ```shell
    pip install -r requirements.txt

4. Set up the environment variables:
    - Create a `.env` file in the project directory.
    - Add the following environment variables to the `.env` file:
        - `SQLALCHEMY_DATABASE_URI`: The URI for the SQLAlchemy database.
        - `GOOGLE_CLIENT_ID`: The client ID for Google OAuth.
        - `GOOGLE_CLIENT_SECRET`: The client secret for Google OAuth.

## Usage
To run the application, execute the following command in the project directory:

    python app.py

The application will be accessible at http://localhost:5000/.


# API Endpoints
The application provides the following API endpoints:

1. User Authentication
    - `Endpoint`: /login/
    - `Method`: GET
    - `Description`: Initiates the Google OAuth login process.
    - `Returns`: Redirects the user to the Google login page.
2. Google Authorization
    - `Endpoint`: /google_authorization/
    - `Method`: GET
    - `Description`: Handles the callback from the Google OAuth process and stores the user data in the session.
    - `Returns`: Redirects the user to the home page.
3. Logout
    - `Endpoint`: /logout
    - `Method`: GET
    - `Description`: Logs out the user by removing the user data from the session.
    - `Returns`: Redirects the user to the home page.
4. Course Master Authentication
    - `Endpoint`: /api/course_master_authentication/
    - `Method`: POST
    - `Description`: Authenticates the course master (user) by checking their email and password.
    - `Parameters`:
        - `email` (string): The email of the course master.
        - `password` (string): The password of the course master.
    - `Returns`:
        - If the authentication is successful:
access_token (string): The access token for the course master. Status code 200
        - If the authentication fails:
message (string): "Invalid credentials". Status code 401
5. Get All Courses
    - `Endpoint`: /api/get_courses/
    - `Method`: GET
    - `Description`: Retrieves all courses associated with the authenticated course master.
    = `Authentication`: JWT token required (obtained from Course Master Authentication).
    - `Returns`:
        - `courses` (list): A list of course objects.
            - `id` (int): The ID of the course.
            - `course_name` (string): The name of the course.
            - `course_description` (string): The description of the course.
            - `course_duration` (string): The duration of the course.
            - `course_master_name` (string): The name of the course master.
            - `price` (float): The price of the course.
        - Status code 200
6. Add Course
    - `Endpoint`: /api/add_course/
    - `Method`: POST
    - `Description`: Adds a new course associated with the authenticated course master.
    - `Authentication`: JWT token required (obtained from Course Master Authentication).
    - `Parameters`:
        - `course_name` (string): The name of the course.
        - `course_description` (string): The description of the course.
        - `course_duration` (string): The duration of the course.
        - `course_author_name` (string): The name of the course author.
        - `price` (float): The price of the course.
    - `Returns`:
        - If the course is added successfully:
message (string): "New course added successfully". Status code 201
        - If the course already exists:
message (string): "User already exists". Status code 409
7. Update Course
    - `Endpoint`: /api/update_course/<int:course_id>/
    - `Method`: POST
    - `Description`: Updates an existing course.
    - `Authentication`: JWT token required (obtained from Course Master Authentication).
    - `Parameters`:
        - `course_name` (string, optional): The updated name of the course.
        - `course_description` (string, optional): The updated description of the course.
        - `course_duration` (string, optional): The updated duration of the course.
        - `course_author_name` (string, optional): The updated name of the course author.
        - `price` (float, optional): The updated price of the course.
    - `Returns`:
        - If the course exists and is updated successfully:
message (string): "Course updated successfully." Status code 200
        - If the course does not exist:
message (string): "Course not found.", Status code 404

## Database
The application uses a SQLite database to store user and course information. The database is created automatically if it does not exist.

## User Interface
The application includes some HTML templates for user interface rendering. The following templates are used:

- `login.html`: The login page.
- `courses.html`: The page displaying all available courses.

You can customize these templates or add additional templates as per your requirements.

## Admin Interface
- The application provides an admin interface using Flask-Admin. You can access it at `/admin/` URL. 
- Admin `insert, update, delete` course master using admin panel. 
- The admin interface allows you to manage the User and Course models.