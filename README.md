# 📚 Books Service CI/CD  

This repository is part of a **university assignment** and is not a fully developed production service. It demonstrates the implementation of **CI/CD pipelines** for a books-related microservice using **Flask, MongoDB, and Docker**.

## 📚 Table of Contents  
- [Project Overview](#project-overview)  
- [Technologies Used](#technologies-used)  
- [Project Structure](#project-structure)  
- [Getting Started](#getting-started)  
  - [Prerequisites](#prerequisites)  
  - [Installation](#installation)  
- [Usage](#usage)  
- [Testing](#testing)  
- [CI/CD Pipeline](#cicd-pipeline)  
- [Contributing](#contributing)  
- [License](#license)  

## 🔍 Project Overview  

The **Books Service** is a simple **Flask API** that allows users to **add, update, delete, and retrieve books**, as well as manage ratings. It fetches book metadata from the **Google Books API** and stores data in **MongoDB**.  

This project is **not a production-ready service** but rather a demonstration of:  
✅ **Microservice architecture** using Flask & MongoDB  
✅ **Containerization** with Docker  
✅ **Automated deployment** via GitHub Actions  
✅ **CI/CD best practices**  

## 🛠️ Technologies Used  

This project is built using:  

| Technology  | Description |
|-------------|------------|
| **Python**  | Main programming language |
| **Flask**  | Web framework for building REST API |
| **MongoDB**  | NoSQL database for book and rating storage |
| **Docker & Docker Compose** | Containerization and service orchestration |
| **GitHub Actions** | Automates testing and deployment |
| **Nginx** | Reverse proxy configuration for the backend |
| **JWT Authentication** | Secure API authentication |
| **Google Books API** | Fetches book metadata |

## 📂 Project Structure  

```
books-service-ci-cd/
├── .github/workflows/     # CI/CD workflow definitions
├── books_service/         # Flask service source code
│   ├── controllers/       # API controllers for books & ratings
│   ├── models/            # Book and Rating models
│   ├── routes/            # API route definitions
│   ├── util/              # Helper functions (e.g., JSON handling)
│   ├── app.py             # Main Flask application entry point
│   ├── requirements.txt   # Python dependencies
│   ├── Dockerfile         # Docker build instructions
│   └── query.txt          # Sample query file for testing
├── tests/                 # Unit & integration tests
├── docker-compose.yml     # Docker Compose setup
├── .gitignore             # Git ignore rules
└── README.md              # Project documentation
```

## 🚀 Getting Started  

### ✅ Prerequisites  

Ensure you have the following installed:  
- [Docker](https://www.docker.com/get-started)  
- [Docker Compose](https://docs.docker.com/compose/install/)  
- [Python 3.9+](https://www.python.org/downloads/)  
- [Flask](https://flask.palletsprojects.com/)  
- [MongoDB](https://www.mongodb.com/)  

### 🔧 Installation  

1. **Clone the repository:**  

   ```bash
   git clone https://github.com/ronsalomon97/books-service-ci-cd.git
   cd books-service-ci-cd
   ```

2. **Build and start the services:**  

   ```bash
   docker-compose up --build
   ```

## 📌 Usage  

### 🎯 Running the Flask API  

Once the service is running, you can access the API:  

- **Health Check:**  
  ```bash
  curl http://localhost:5001/health
  ```

- **Add a Book:**  
  ```bash
  curl -X POST http://localhost:5001/books \
       -H "Content-Type: application/json" \
       -d '{"title": "Example Book", "ISBN": "123456789", "genre": "Fiction"}'
  ```

- **Retrieve a Book by ID:**  
  ```bash
  curl -X GET http://localhost:5001/books/{book_id}
  ```

- **Delete a Book:**  
  ```bash
  curl -X DELETE http://localhost:5001/books/{book_id}
  ```

- **Retrieve Top Rated Books:**  
  ```bash
  curl -X GET http://localhost:5001/top
  ```

## 🤖 Testing  

To run unit tests inside the Docker container:  

```bash
docker-compose run books_service pytest
```

Or locally:  

```bash
pytest -v tests/assn3_tests.py
```

## ⚙️ CI/CD Pipeline  

This project uses **GitHub Actions** to automate:  

1. **Build & Test:**  
   - Checks out the repository  
   - Builds the Docker image  
   - Runs unit and integration tests  

2. **Deployment:**  
   - Pushes the Docker image to **Docker Hub**  
   - Deploys the service to **AWS EC2**  

📌 **Workflow File Location:** `.github/workflows/assignment3.yml`  

## 🤝 Contributing  

This repository is part of a **university assignment**, so external contributions are not expected. However, feel free to open an issue if you have suggestions.  

## 📝 License  

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

