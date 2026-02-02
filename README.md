# Task Manager API

A robust, RESTful API for managing tasks with Role-Based Access Control (RBAC), built using **Django** and **PostgreSQL**.

## Tech Stack

*   **Framework**: Django 6.0, Django REST Framework (DRF)
*   **Database**: PostgreSQL 15
*   **Authentication**: JWT (JSON Web Tokens)
*   **Containerization**: Docker & Docker Compose
*   **Documentation**: Swagger/OpenAPI (via `drf-yasg`)

## Key Features 🚀

-   **Modular Architecture**: Split into `core`, `authentication`, and `tasks` apps for scalability.
-   **Security**:
    -   JWT Authentication with **Role-Based Access Control (RBAC)**.
    -   Secure credential management via `.env`.
    -   Safe from SQL Injection (parameterized queries) and XSS (Django defaults).
-   **Performance**:
    -   **Zero-DB Auth**: Validates tokens purely via crypto signature & JWT payload (User ID + Role), avoiding DB hits on every request.
    -   **Connection Pooling**: Persistent DB connections enabled for high throughput.
    -   **Cursor Pagination**: Efficient pagination for large datasets.
-   **Developer Experience**:
    -   Dockerized setup.
    -   Swagger UI with "Try it out" feature.
    -   Comprehensive Test Suite (11 Tests).

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

3.  **Environment Setup**:
    Create a `.env` file in the root directory (see `.env.example` or use defaults below):
    ```ini
    SECRET_KEY='your-secret-key'
    DEBUG=True
    DB_NAME=taskmanager
    DB_USER=postgres
    DB_PASSWORD=postgrespassword
    DB_HOST=127.0.0.1
    DB_PORT=5432
    ```

4.  **Database Config**:
    Ensure PostgreSQL is running. Update `.env` with your credentials.

5.  **Run Migrations**:
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

*   **`taskmanager/`**: Project settings and main URL routing.

---

## Troubleshooting

### Q: Login fails with "Internal Server Error"?
**A**: Ensure your PostgreSQL container is running (`docker compose ps`) and your `.env` credentials match.

### Q: Swagger "Authorize" button doesn't work?
**A**: We support **Bearer Token**.
1. Login via `POST /auth/login`.
2. Copy the `token` from the response.
3. Click "Authorize" at the top of Swagger.
4. Paste the token. (No need to type "Bearer ", just the token).

### Q: "Relation does not exist" error?
**A**: You might need to run migrations inside the container:
```bash
docker compose exec web python manage.py migrate
```

## License
MIT License. Free to use!

