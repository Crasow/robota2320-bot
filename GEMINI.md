# robota2320-bot Context

## Project Overview
`robota2320-bot` is a Telegram bot designed to facilitate job searching and posting. It allows users to post job offers ("Есть работа") and search for them ("Ищу работу"). The project is built using Python, specifically leveraging the `aiogram 3.x` framework for asynchronous Telegram bot development.

## Tech Stack
*   **Language:** Python >= 3.10
*   **Framework:** `aiogram 3.x` (Asynchronous Telegram Bot API)
*   **Database ORM:** `SQLAlchemy` (Async)
*   **Database Driver:** `aiosqlite` (implied for SQLite)
*   **Configuration:** `pydantic-settings`, `python-dotenv`
*   **Package Management:** `pip` / `uv` (implied by `uv.lock`)

## Architecture
The project follows a modular structure typical for `aiogram` bots:

*   **Entry Point (`main.py`):** Initializes the `Bot`, `Dispatcher`, and database connection. It aggregates routers from `bot.handlers`.
*   **Handlers (`bot/handlers/`):** Contains the business logic, organized by functionality:
    *   `common.py`: Handles basic commands like `/start`, `/cancel`, and history clearing.
    *   `creating.py`: Manages the job creation flow using FSM (Finite State Machine).
    *   `looking.py`: Handles job search functionality with pagination.
*   **Database (`bot/database/`):**
    *   `models.py`: Defines SQLAlchemy models (e.g., `Job`) and the async engine/session.
        *   `Job` table structure: `id`, `description`, `start_time`, `deadline`, `payment`, `people_count`, `location`, `user_id`.
*   **States (`bot/states/`):** Defines FSM states (e.g., `JobCreationState`) for multi-step user interactions.
*   **Keyboards (`bot/keyboards/`):** logic for inline and reply keyboards.
*   **Configuration (`bot/config.py`):** Loads environment variables (like `bot_token`) using Pydantic.

## Key Features & Flows

### Job Creation ("📢 Есть работа")
Implementation: `bot/handlers/creating.py`
1.  **Trigger:** User sends "📢 Есть работа".
2.  **Flow (FSM):**
    *   **Description:** "Опишите работу (кратко)"
    *   **Start Time:** "Когда приступить к работе?"
    *   **Deadline:** "Сроки выполнения?"
    *   **Payment:** "Какой бюджет на работу?"
    *   **People Count:** "Сколько человек нужно?"
    *   **Location:** "Адресс работы?"
3.  **Completion:** Data is saved to the `jobs` table in the database, linked to the user's ID.
4.  **Cancellation:** Users can send `/cancel` or "Отмена" at any step to abort the process.

### Job Search ("🔎 Ищу работу")
Implementation: `bot/handlers/looking.py`
1.  **Trigger:** User sends "🔎 Ищу работу".
2.  **Logic:** Fetches jobs from the database with pagination (10 items per page).
3.  **UI:** Displays a list of jobs with an inline keyboard for navigation (Previous/Next page).

## Setup & Running

1.  **Prerequisites:** Python 3.10+ installed.
2.  **Environment Variables:**
    Copy `.env.example` to `.env` and fill in the values:
    ```bash
    cp .env.example .env
    ```
    Your `.env` should contain:
    ```env
    BOT_TOKEN=your_telegram_bot_token
    # Optional, defaults to sqlite+aiosqlite:///./jobs.db
    DATABASE_URL=sqlite+aiosqlite:///db.sqlite3
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    # OR if using uv
    uv sync
    ```
4.  **Run the Bot:**
    ```bash
    python main.py
    ```

## Development Guidelines
*   **Database Schema Changes:** The project currently does not use migrations (e.g., Alembic). If you modify the `Job` model in `bot/database/models.py`, **you must manually delete the `jobs.db` file** (or your configured database file) for the changes to apply. The bot will recreate the database on the next run.
*   **Asynchronous Code:** All handlers and database operations are async (`async def`, `await`).
*   **Type Hinting:** The codebase uses strict type hinting, especially with SQLAlchemy `Mapped` types.
*   **Routers:** New functionality should be added via new Routers in `bot/handlers/` and registered in `main.py`.
