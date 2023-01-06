# ValidAItor Model Validation Platform

We have attempted to build a platform where a user can 
1. upload their trained scikit-learn models (classifiers) 
2. visualise performance metrics

The platform is developed as standard [Django](https://www.djangoproject.com/) app

## Directory Structure

```
|-- pred_models                     # Separate Django app about a user's trained prediction models
|-- templates                       # Static files (HTML, JS, CSS)
    |-- pred_models                 # Static files specific to "pred_models"-app
    |-- registration                # Static files for user registration, password reset (pre-login)
    |-- user                        # Static files specific to "user"-app
|-- tests                           # App-wise Unit tests
    |-- pred_models                 # Unit tests for "pred_model"-app
|-- users                           # Separate Django app for user (leveraging Django users)
|-- validaitor                      # Main Django app/project
|-- manage.py                       # Django manager
|-- requirements.txt                # Packages required for the project
|-- README.md
```

### Setup 
1. Git clone
2. Create python3 [venv](https://docs.python.org/3/library/venv.html) `python3 -m venv /path/to/new/virtual/environment`
3. Install required packages `pip install -r requirement.txt`
4. Load environment variables with respective values (variables mentioned below)
5. Ensure database is created (Postgres is configured as of now)
6. Run migrations `python manage.py migrate`
7. Run django server `python manage.py runserver`

### Environment variables needed
- SECRET_KEY
- DB_HOST
- DB_PORT
- DB_USER
- DB_PASSWORD
- DB_NAME
- EMAIL_HOST
- EMAIL_PORT
- SRC_DIR

### Available Web Pages
1. Home `/` 
2. Account Management `/accounts` --> Django user management routes (login, reset password)
3. User registration `/register`
4. User's trained model related (required log-in, and user-specific)
   1. List all user's models `pred_models/`
   2. View a specific model `pred_models/<id>`
   3. Generate performance metrics for a model `pred_models/<id>/generate_report`