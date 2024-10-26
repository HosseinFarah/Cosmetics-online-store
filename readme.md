# Todo App

This is a Flask-based Todo application that allows users to manage their tasks. The application includes user authentication, profile management, and task management features.

## Features

- **User Authentication**: Login, Logout, Registration, Email Confirmation
- **Profile Management**: View and Update Profile
- **Task Management**: Create, Update, Delete, View Tasks
- **Error Handling**: Custom 404 and 500 error pages

## File Structure

### `__init__.py`

- Initializes the Flask application.
- Configures the application using settings from the `config` module.
- Sets up extensions such as SQLAlchemy, Flask-Migrate, Flask-Login, Flask-Mail, Flask-Bootstrap, and CSRF protection.
- Registers blueprints for different modules (authentication, main, errors, todos).

### `views.py`

- **User Authentication**: Handles user login, logout, registration, email confirmation, password reset, and resending confirmation emails.
- **Profile Management**: Allows users to view and update their profile information.
- **Task Management**: Provides functionality to create, update, delete, and view tasks.
- **Error Handling**: Defines custom error pages for 404 and 500 errors.

## Installation

1. Clone the repository:
    ```sh
    git clone git@github.com:HosseinFarah/flask-authentication-system.git
    cd todo-app
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    venv\Scripts\activate  # On Windows
    source venv/bin/activate  # On macOS/Linux
    ```

3. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set up the environment variables and configuration files as needed.

5. Run the application:
    ```sh
    flask run
    ```

## Usage

- Navigate to `http://127.0.0.1:5000/` to access the application.
- Register a new user, log in, and start managing your tasks.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.