# NetworkProject

An educational social-network backend built with **Django REST Framework**.

The project includes API modules for user profiles, posts, comments,
likes, follows, saved posts and stories.

## Features

- User registration, login and logout
- JWT authentication with SimpleJWT
- User profiles
- Posts and hashtags
- Comments and likes
- Follow and unfollow actions
- Saved posts
- Stories and following-related feeds
- Filtering, search, ordering and pagination
- Custom owner and author permission classes

Features are described from the implementation.
Their presence does not imply that every scenario has been tested.

## Technology Stack

| Area | Technologies |
| --- | --- |
| Language | Python |
| Framework | Django |
| API | Django REST Framework |
| Authentication | SimpleJWT |
| Filtering | django-filter |
| Local database | SQLite |
| Deployment configuration | Docker, Docker Compose, gunicorn, nginx |

## Project Structure

```text
NetworkProject/
└── mysite/
    ├── manage.py
    ├── network_app/        # API and application logic
    ├── mysite/             # Django project configuration
    ├── nginx/              # Reverse proxy configuration
    ├── Dockerfile
    ├── docker-compose.yml
    └── req.txt             # Python dependencies
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/minbaevv/NetworkProject.git
cd NetworkProject
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Linux/macOS:

```bash
source .venv/bin/activate
```

Or on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
cd mysite
python -m pip install -r req.txt
```

### 4. Configure the environment

Review the Django settings and configure the required local
environment variables before startup.

Use a new local secret key. Do not commit working secrets,
real user data or private uploads.

### 5. Apply migrations and start the server

```bash
python manage.py migrate
python manage.py runserver
```

The default Django development address is:

```text
http://127.0.0.1:8000/
```

Use the URL configuration to identify the available API paths.
A frontend homepage is not required for an API-only project.

These setup instructions still need clean-environment verification.

## Authorization

The implementation references authenticated views and custom
owner/author permissions.

Before deployment, verify that:

- Anonymous users cannot perform protected actions
- Users cannot edit or delete another user's content
- Saved posts are isolated by owner
- Follow and unfollow actions behave consistently
- Story feeds return content from the intended users

## Development Priorities

- Document environment variables in a safe `.env.example`
- Add or extend authentication and ownership tests
- Verify the direction of follow relationships in story feeds
- Clarify the purpose of profile-list and current-user endpoints
- Check database query counts and optimize related-object loading
- Verify Docker startup in a clean environment
- Configure continuous integration

## Project Status

This repository is an educational backend project.

It demonstrates API implementation practice and is not presented
as a production-ready social network. Runtime behavior, permissions
and deployment configuration require further validation.

## Attribution and License

Retain attribution for any course, tutorial or external code used.
Document your own additions and changes.

Check the repository's licensing before reusing or redistributing code.

## Author

**Kubanychbek Duishekeev**

[GitHub](https://github.com/minbaevv) ·
[LinkedIn](https://www.linkedin.com/in/kubanychbek-duishekeev-7b9872427/) ·
[Telegram](https://t.me/d_kubanychbek) ·
[Gmail](mailto:duishekeevkubanychbek@gmail.com)
