# New Project – Django News Publishing Platform

A **Django-based News Publishing Platform** that allows users to register and interact based on their assigned roles.

Users can register as:

* **Readers** – read articles and subscribe to journalists
* **Journalists** – create and manage articles
* **Editors** – review and manage publishing content

The project includes role-based dashboards, article management, a subscription system, Docker containerization, and Sphinx documentation.

---

# Features

* Role-based authentication (Reader, Journalist, Editor)
* User registration and login
* Article creation, editing, and deletion
* Reader subscription system
* Dashboard views based on user roles
* Django Admin interface
* Docker support for containerized deployment
* Sphinx documentation for developers

---

# Technologies Used

* Python
* Django
* SQLite
* Docker
* Sphinx

---

# Project Structure

```
new_project/
│
├── news/                       # Main Django application
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

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment.

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

Upgrade pip and install the required packages.

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

Run the following commands to create the database tables.

```bash
python manage.py makemigrations
python manage.py migrate
```

(Optional) Create a superuser for the Django admin panel:

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

Ensure **Docker Desktop** is installed and running.

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

# Building the Documentation

This project uses **Sphinx** to generate documentation.

### Step 1: Navigate to the docs folder

```bash
cd docs
```

### Step 2: Build the documentation

```bash
make html
```

### Step 3: Open the generated documentation

After the build completes, open the following file in your browser:

```
docs/build/html/index.html
```

This documentation contains automatically generated information about the project modules and code.

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

## Reader

* View articles
* Subscribe to journalists

## Journalist

* Create and manage articles
* Publish content

## Editor

* Review and manage articles
* Oversee platform content

---

# Author

**Manqoba Hlongwane**

---

# GitHub Repository

https://github.com/0658967605M/new_project

---
