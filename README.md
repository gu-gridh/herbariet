# Herbariet

A simple web application for managing a collection of plants.

# Django backend with wagtail cms and Template frontend.

For this project we used wagtail cms as a backend solution to give the user the ability to add their data easily through a user friendly interface.

# Install podman and podman-compose on your machine
To install podman and podman-compose, follow the instructions for your operating system:

- For Windows, you can use the Windows Subsystem for Linux (WSL) and install podman and podman-compose using the package manager for your chosen Linux distribution.
- For macOS, you can use Homebrew:
  ```bash
  brew install podman podman-compose
  ```
- For Linux, you can use your distribution's package manager. For example, on Ubuntu:
  ```bash
  sudo apt update
  sudo apt install podman podman-compose
  ```
- intial setup of podman
    ```bash
    podman machine init
    podman machine start
    ```

# How to run the project

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/herbariet.git
   ```
2. Use podman-compose to build and run the containers:
    ```bash
    podman-compose -f podman-compose.yml up --build
    ```
3. Access the application at `http://localhost:8000`.
4. To stop the application, run:
    ```bash
   podman-compose -f podman-compose.yml down
   podman-compose down
   ```
