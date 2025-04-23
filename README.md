# Quiz knowledge

## Description
Built a simple **Quiz** application using **Python** and **Flask** for development.

Deployed on a **Hetzner VPS** using **Docker** for deployment.

## Features

### Feature List
- **Answer Questions**: Accessible through a web interface.
- **Public Availability**: [http://37.27.8.233:5001](http://37.27.8.233:5001).
- **Result Display**: Shows score at the end with option to restart.

## Technologies

### Technology Stack
- **Backend**: **Python** with **Flask** for web requests.
- **Frontend**: **HTML** with **Jinja2** for the user interface.
- **Deployment**: **Docker** for containerization, **Gunicorn** as WSGI server.
- **Hosting**: **Hetzner Cloud VPS** (**CAX11**), Specs: **2 vCPU**, **4 GB RAM**, **40 GB** disk.

## Project Setup from Scratch

### 1. Local Setup of the Application

#### 1.1. Project Creation
Created a project directory and set up a virtual environment:

```bash
mkdir kvizprojekt
cd kvizprojekt
python3 -m venv venv
source venv/bin/activate

