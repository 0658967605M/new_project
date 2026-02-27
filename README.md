# New Project

A Django-based news publishing platform with role-based functionality. Users can register as Readers, Journalists, or Editors, create and manage articles, and view dashboards. This project is containerized with Docker and includes Sphinx documentation.

---

## Features

- Role-based authentication: Reader, Journalist, Editor  
- Article management: create, edit, delete  
- Subscription system for readers to follow journalists  
- Dashboard views for different roles  
- Email login and registration  
- Docker-ready for easy deployment  
- Full Sphinx documentation

---

## Installation & Setup (Steps 1–7)

### Step 1: Clone the Repository
```bash
git clone https://github.com/0658967605M/new_project.git
cd new_project

# New Project

A Django-based news publishing platform with role-based functionality. Users can register as Readers, Journalists, or Editors, create and manage articles, and view dashboards. This project is containerized with Docker and includes Sphinx documentation.

---

## Features

- Role-based authentication: Reader, Journalist, Editor  
- Article management: create, edit, delete  
- Subscription system for readers to follow journalists  
- Dashboard views for different roles  
- Email login and registration  
- Docker-ready for easy deployment  
- Full Sphinx documentation

---

## Installation & Setup (Steps 1–7)

### Step 1: Clone the Repository
```bash
git clone https://github.com/0658967605M/new_project.git
cd new_project

### Step 2: Create and Activate a Virtual Environment
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux / Mac


###Step 3: Install Dependencies
pip install --upgrade pip
pip install -r requirements.txt


### Step 4: Database Setup (SQLite)

Ensure your new_project/settings.py uses SQLite:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

Apply migrations and create a superuser:

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # optional


### Step 5: Running the Project Locally
python manage.py runserver

Visit http://127.0.0.1:8000
 in your browser.


### Step 6: Docker Setup

1.Build the Docker image:

docker build --no-cache -t new_project .

2.Run the container:


docker run -p 8000:8000 new_project

Visit http://localhost:8000
 to access the app inside Docker.

⚠️ Use SQLite in Docker to avoid MySQL errors.


### Step 7: Sphinx Documentation

1.Install Sphinx:

pip install sphinx

2.Initialize Sphinx (if not done):

cd docs
sphinx-quickstart

3.Generate API documentation from apps:

# From project root
python -m sphinx.ext.apidoc -o docs news
python -m sphinx.ext.apidoc -o docs new_project

4.Build HTML docs:

cd docs
.\make.bat html    # Windows
# make html        # Linux / Mac

5.Open docs/_build/html/index.html in your browser to view docs.