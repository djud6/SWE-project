# Online Literary Club (OLC)

## DOWNLOAD THE PROJECT DEMO VIDEO IF IT'S TOO BIG TO BE VIEWED ON HERE, THE PROJECT REOPRT IS IN THE DISCBOARD/DEMO VIDEO AND PROJECT REPORT FOLDER.
## LINK: [https://github.com/djud6/SWE-project/tree/main/discboard/demo%20video%20and%20project%20report)

## Project Overview

The Online Literary Club (OLC) is a platform that connects book enthusiasts, enabling them to join themed book clubs, engage in discussions, and share recommendations.

## Prerequisites

- Python 3.10+
- Virtualenv
- Git
- Django


## Setup Instructions

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd <repository-folder>
```

### Step 2: Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv myenv

# Activate virtual environment
# On macOS/Linux:
source myenv/bin/activate

# On Windows:
myenv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install Django
pip install django
```

Install pillow
python -m pip install Pillow

### Step 4: Create a Superuser

Set up an admin user to access the Django admin panel:

```bash
python manage.py createsuperuser
```

## Running the Project

### Step 1: Navigate to Project Directory

```bash
cd bookclub_project
```

### Step 2: Start the Development Server

```bash
python manage.py runserver
```

### Step 3: Access the Application

Open your browser and navigate to:
- Application: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- Admin Panel: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

## Troubleshooting Common Issues

### Virtual Environment Activation

Ensure you activate the virtual environment before running any commands:

```bash
# On macOS/Linux:
source myenv/bin/activate

# On Windows:
myenv\Scripts\activate
```

### Dependency Installation

Ensure django is installed in the virtualenv:
pip i django

If you encounter issues installing dependencies:

```bash
# Upgrade pip
pip install --upgrade pip

# Reinstall dependencies
pip install -r requirements.txt  # If you have a requirements file
```

## Additional Notes

- Always work within the activated virtual environment
- Keep your Django installation up to date
- Refer to Django documentation for advanced configuration



