# DevOps Knowledge Quiz

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3-green?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0-blue?logo=docker&logoColor=white)
![Traefik](https://img.shields.io/badge/Traefik-v3.0-orange?logo=traefik&logoColor=white)
![Status](https://img.shields.io/badge/Status-Live-success)

## 📖 Description

**DevOps Knowledge Quiz** is a web application designed to test your knowledge of DevOps concepts, including Linux, Docker, Kubernetes, and Terraform.

The application is built with **Python (Flask)** and serves a dynamic quiz interface. It is containerized using **Docker** and deployed on a **Hetzner VPS**, utilizing **Traefik** as a modern reverse proxy for automatic HTTPS management via Let's Encrypt.

👉 **Live Demo:** [https://kvizap.duckdns.org](https://kvizap.duckdns.org)

---

## ✨ Features

- **Interactive Quiz**: Randomly selected questions from a pool of DevOps topics.
- **Score Tracking**: Instant feedback and scoring at the end of the session.
- **Responsive Design**: Clean and simple UI accessible on desktop and mobile.
- **Secure**: Fully encrypted traffic (HTTPS) using automated TLS certificates.
- **Containerized**: Modular architecture with separate services for the app and proxy.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
|-----------|------------|-------------|
| **Backend** | Python, Flask | Handles quiz logic and session management. |
| **Frontend** | HTML, Jinja2, CSS | Renders the user interface. |
| **Server** | Gunicorn | WSGI HTTP Server for UNIX. |
| **Proxy** | Traefik v3.0 | Edge router, Load Balancer, and SSL manager. |
| **Container** | Docker & Compose | Orchestration of application services. |
| **Hosting** | Hetzner Cloud | CAX11 VPS (Ubuntu 24.04). |

---

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose installed on your machine.

### 1. Run Locally
Clone the repository and start the services:

```bash
git clone https://github.com/Tomo1912/kviz-app.git
cd kviz-app
docker compose up -d
```

The application will be available at:
- **HTTP**: `http://localhost`

### 2. Deployment (VPS)
This project is configured for easy deployment on any VPS with Docker installed.

1.  **SSH into your server**:
    ```bash
    ssh root@your-server-ip
    ```
2.  **Clone the repo**:
    ```bash
    git clone https://github.com/Tomo1912/kviz-app.git
    cd kviz-app
    ```
3.  **Start the stack**:
    ```bash
    docker compose up -d --build
    ```

Traefik will automatically:
- Detect the running containers.
- Acquire a Let's Encrypt SSL certificate for the domain defined in `docker-compose.yml`.
- Route traffic from port 80/443 to the application.

---

## 🚀 Automated CI/CD Deployment to AWS

This section details the modern, automated deployment pipeline built as an extension to this project, demonstrating best practices in cloud infrastructure and DevOps.

### Architecture Overview

The system is designed for zero-touch deployments, where a `git push` to the main branch triggers the entire process.

```
┌───────────────┐      ┌──────────────┐      ┌──────────────────────────┐
│   Developer   │──────│   Git Push   │──────│      GitHub Actions      │
└───────────────┘      └──────────────┘      └──────────────────────────┘
       │                      │                         │ 1. Connect to AWS (OIDC)
       │                      │                         │ 2. Package Application
       └──────────────────────┴─────────────────────────┘ 3. Deploy to AWS
                                                               │
                                                               ▼
                                                 ┌──────────────────────────┐
                                                 │ AWS Elastic Beanstalk    │
                                                 │ ------------------------ │
                                                 │ ∙ Runs docker-compose    │
                                                 │ ∙ Manages Nginx & App    │
                                                 └──────────────────────────┘
```

### Technology Stack (CI/CD & Cloud)

- **Cloud Platform:** AWS (Amazon Web Services)
- **Orchestration:** AWS Elastic Beanstalk (Docker Platform)
- **CI/CD:** GitHub Actions
- **Security & Identity:** AWS IAM (Identity and Access Management) with an **OIDC Connector**.

---

### Detailed Setup Guide

This guide outlines the key steps required to configure the AWS infrastructure and the GitHub Actions workflow.

#### Step 1: Setting Up the AWS Elastic Beanstalk Environment
1.  Navigate to the **AWS Elastic Beanstalk** service.
2.  Click **"Create application"** and configure the basics:
    -   **Application name:** `kviz-portfolio`
    -   **Platform:** Select **"Docker"**.
    -   **Application code:** Keep **"Sample application"** selected for the initial setup.
3.  If prompted, create and select the default service roles (`aws-elasticbeanstalk-service-role` and `aws-elasticbeanstalk-ec2-role`).
4.  Launch the environment and wait for its health status to become **Ok**.

#### Step 2: Configuring the Secure Bridge (IAM & OIDC)
This is the most critical part for security. We will allow GitHub Actions to securely connect to AWS without storing any long-term keys.

##### 2.1: Create the OIDC Identity Provider
1.  Navigate to the **IAM** service in the AWS Console.
2.  Go to **Identity providers** and click **"Add provider"**.
3.  Select **"OpenID Connect"**.
4.  For **Provider URL**, enter: `https://token.actions.githubusercontent.com`
5.  For **Audience**, enter: `sts.amazonaws.com`
6.  Click **"Add provider"**.

##### 2.2: Create the IAM Role for GitHub Actions
1.  In IAM, go to **Roles** and click **"Create role"**.
2.  For **Trusted entity type**, select **"Web identity"**.
3.  In the **Identity provider** dropdown, choose the `token.actions.githubusercontent.com` provider you just created.
4.  For **Audience**, choose `sts.amazonaws.com`.
5.  Fill in your GitHub details to restrict access:
    -   **GitHub organization:** Your GitHub username (e.g., `Tomo1912`).
    -   **GitHub repository:** The name of your repository (e.g., `kviz-app`).
    -   **GitHub branch:** `main`.
6.  Click **Next**.
7.  On the "Add permissions" screen, search for and attach the following two AWS Managed Policies:
    -   **`AdministratorAccess-AWSElasticBeanstalk`**: Allows GitHub Actions to create new application versions and update the Elastic Beanstalk environment.
    -   **`AmazonS3FullAccess`**: Required for the workflow to create a temporary S3 bucket, upload the application source bundle (`.zip`), and then clean it up.
8.  Click **Next**.
9.  Give the role a descriptive name, like `github-kvizapp-role`.
10. Click **"Create role"**.
11. **IMPORTANT:** Click on the newly created role and **copy its ARN**. You will need it for the workflow file.

#### Step 3: Creating the GitHub Actions Workflow
The final step is to create the `.github/workflows/deploy.yml` file in the repository. This file contains the instructions for the CI/CD process. The workflow performs the following actions:
- Authenticates with AWS using the OIDC role created above.
- Zips the application source code.
- Uploads the package to a temporary S3 bucket.
- Creates a new application version in Elastic Beanstalk from the S3 source.
- Deploys the new version to the environment.
- Cleans up the temporary S3 bucket.

### Result

The application was successfully deployed and is accessible on a public domain provided by Elastic Beanstalk.

<img width="1130" height="281" alt="Screenshot 2025-08-08 at 17 15 27" src="https://github.com/user-attachments/assets/87a416ab-ed48-40d1-87df-9989de8fa9c1" />

---

### ⚠️ AWS Resource Cleanup

As the AWS deployment is a portfolio project, it is crucial to **delete all created resources after the demonstration** to avoid unnecessary costs.

1.  Navigate to **AWS Elastic Beanstalk** in the AWS Console.
2.  Select the environment named `Kviz-portfolio-env`.
3.  In the top-right corner, click the **Actions** dropdown menu.
4.  Choose the **"Terminate Environment"** option.
5.  Confirm the termination by typing the environment's name.

This single step will automatically delete **all** associated resources that Elastic Beanstalk created (EC2 servers, Load Balancer, security groups, etc.), leaving your AWS account clean.
