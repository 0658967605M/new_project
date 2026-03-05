# New Project – Django News Publishing Platform

A **Django-based News Publishing Platform** that allows users to register and interact based on their assigned roles.

Users can register as:

- **Readers** – read articles and subscribe to journalists
- **Journalists** – create and manage articles
- **Editors** – review and manage publishing content

The project includes:

- Role-based dashboards
- Article creation and management
- Subscription system
- Docker containerization
- Sphinx documentation

---

# Features

- Role-based authentication (Reader, Journalist, Editor)
- User registration and login
- Article creation, editing, and deletion
- Reader subscription system
- Dashboard views per role
- Django Admin interface
- Docker support
- Sphinx documentation

---

# Technologies Used

- Python
- Django
- SQLite
- Docker
- Sphinx

---

# Project Structure

```
new_project/
│
├── news/                       # Main application
│   ├── migrations/
│   ├── templates/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── urls.py
│
├── new_project/                # Django project configuration
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── docs/                       # Sphinx documentation
│   ├── source/
│   └── build/
│
├── manage.py
├── requirements.txt
├── Dockerfile
└── README.md
```

---

# Installation and Setup

## Step 1: Clone the Repository

```bash
git clone https://github.com/0658967605M/new_project.git
cd new_project
```

---

# Step 2: Create a Virtual Environment

Create the environment:

```bash
python -m venv venv
```

Activate the environment.

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

# Step 3: Install Dependencies

Upgrade pip and install required packages.

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

# Step 4: Configure the Database

This project uses **SQLite** for simplicity.

Ensure the following configuration exists in  
`new_project/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

# Step 5: Apply Migrations

Run the following commands to create database tables.

```bash
python manage.py makemigrations
python manage.py migrate
```

(Optional) Create a superuser for the admin panel:

```bash
python manage.py createsuperuser
```

---

# Step 6: Run the Application Locally

Start the Django development server.

```bash
python manage.py runserver
```

Open the application in your browser:

```
http://127.0.0.1:8000
```

Admin dashboard:

```
http://127.0.0.1:8000/admin
```

---

# Running the Application with Docker

Make sure **Docker Desktop is installed and running**.

### Step 1: Navigate to the project root folder

```
new_project/
```

### Step 2: Build the Docker image

```bash
docker build --no-cache -t new_project .
```

### Step 3: Run the Docker container

```bash
docker run -p 8000:8000 new_project
```

Open the application in your browser:

```
http://localhost:8000
```

---

# Sphinx Documentation

The project includes **Sphinx documentation for developers**.

The documentation files are located in the `docs` directory.

After building the documentation, open the generated HTML file:

```
docs/_build/html/index.html
```

This documentation describes the project modules and code structure.

---

# Admin Login

After creating a superuser, access the Django admin panel:

```
http://127.0.0.1:8000/admin
```

Login using the credentials created with:

```
python manage.py createsuperuser
```

---

# Example User Roles

The system supports three roles:

### Reader
- View articles
- Subscribe to journalists

### Journalist
- Create and manage articles
- Publish content

### Editor
- Review and manage articles
- Oversee platform content

---

# Author

**Manqoba Manqoba**

---

# GitHub Repository

```
https://github.com/0658967605M/new_project
```

---
