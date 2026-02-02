# Task Manager API

A robust, RESTful API for managing tasks with Role-Based Access Control (RBAC), built using **Django** and **PostgreSQL**.

## Tech Stack

*   **Framework**: Django 6.0, Django REST Framework (DRF)
*   **Database**: PostgreSQL 15
*   **Authentication**: JWT (JSON Web Tokens)
*   **Containerization**: Docker & Docker Compose
*   **Documentation**: Swagger/OpenAPI (via `drf-yasg`)

---

## Setup & Installation

### Option 1: Docker (Recommended)

This comes with a pre-configured PostgreSQL database and Django backend.

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd zipee_backend_task
    ```

2.  **Build and Run**:
    ```bash
    docker compose up --build
    ```
    *   The API will be available at `http://localhost:8000`.
    *   Swagger Docs: `http://localhost:8000/swagger/`.

### Option 2: Local Development

**Prerequisites**: Python 3.11+, PostgreSQL.

1.  **Create Virtual Environment**:
    ```bash
    python -m venv venv
    # Windows
    .\venv\Scripts\activate
    # Linux/Mac
    source venv/bin/activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Database Config**:
    Ensure PostgreSQL is running. Update `taskmanager/settings.py` `DATABASES` config if needed (defaults to Docker values: user `postgres`, pass `postgrespassword`, port `5432`).

4.  **Run Migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Run Server**:
    ```bash
    python manage.py runserver
    ```

---

## Management Commands

We have custom scripts to help you get started quickly.

### 1. Create Admin User (`create_admin`)
Since we disabled public admin registration, use this command to create an Admin with full access.
```bash
python manage.py create_admin <username> <email> <password>
```
**Example**:
```bash
python manage.py create_admin admin admin@example.com admin123
```

### 2. Seed Database (`seed_tasks`)
Populate the database with dummy data for testing pagination and performance.
```bash
python manage.py seed_tasks
```
*   Creates a test user `seed_user` (if not exists).
*   Generates **1000 tasks** for that user.

---

## Testing

The project has comprehensive unit tests covering Authentication, Task Management, and RBAC.

### Run All Tests
```bash
python manage.py test tasks authentication
```

### Run Specific Apps
```bash
# Auth Tests (Register, Login)
python manage.py test authentication

# Task Tests (CRUD, RBAC)
python manage.py test tasks
```

---

## API Documentation

Interactive API documentation is available via Swagger UI.

*   **URL**: `http://localhost:8000/swagger/`
*   **Auth**: Click "Authorize" and enter `Bearer <your_token>` (get token from `/auth/login`).

### Key Endpoints

#### Authentication (`authentication` app)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/auth/register` | Register a new user (Role: 'user'). Returns user info. |
| `POST` | `/auth/login` | Login to get a JWT token. |

#### Tasks (`tasks` app)
| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/tasks` | List tasks. Supports Cursor Pagination. Admins see ALL tasks. |
| `POST` | `/tasks` | Create a new task. |
| `GET` | `/tasks/{id}` | Get task details. |
| `POST` | `/tasks/update` | Update task (RPC style). |
| `POST` | `/tasks/complete` | Mark task as complete/incomplete (RPC style). |
| `DELETE` | `/tasks/{id}` | Delete a task. |

---

## Project Structure (Modularized)

The codebase follows the Single Responsibility Principle (SRP) and is split into:

*   **`core/`**: Shared utilities (DB wrapper, API response helpers, Decorators).
*   **`authentication/`**: User models, Auth services (Register/Login), logic.
*   **`tasks/`**: Task business logic, specific Views, and Management commands.
*   **`taskmanager/`**: Project settings and main URL routing.
