
# ApplyTrack
#### Video Demo: [ADD YOUR VIDEO LINK HERE]
#### Description:

ApplyTrack is a command-line job application tracker built with Python. It helps job seekers organize their applications, monitor recruitment progress, and keep track of important application details in one place.

When applying to multiple jobs, it can become difficult to remember which companies have been contacted, which positions are still under consideration, and which applications have progressed to interviews or offers. ApplyTrack addresses this problem by providing a simple, persistent system for managing job applications.

## Features

- **Add applications:** Record a company's name, job title, and application date.
- **View applications:** Display saved applications in a structured table.
- **Search applications:** Find applications by company name or job title. Searches are case-insensitive.
- **Update status:** Change an application's status as the recruitment process progresses.
- **Delete applications:** Remove an application after confirmation.
- **Application statistics:** View the total number of applications and a breakdown by status.
- **Persistent storage:** Save application records to a local JSON file so they remain available after restarting the program.
- **Input validation:** Check required fields, date formats, and valid application statuses.

## Application Statuses

Each application can have one of the following statuses:

- Wishlist
- Applied
- Interview
- Offer
- Rejected
- Withdrawn

## Files

- `project.py` contains the main application, data-management functions, validation, search, statistics, and interactive menu.
- `test_project.py` contains automated tests for the core functionality.
- `requirements.txt` lists the project's Python dependencies.
- `applications.json` stores application records locally and is created when the application saves data.

## Design Decisions

I chose Python's built-in `json` module for data persistence because ApplyTrack is a small, local application that does not require a database server. JSON keeps the stored data readable and easy to inspect without adding unnecessary dependencies.

The application separates core operations from user interaction. Functions such as `add_application`, `search_applications`, `validate_date`, and `calculate_statistics` handle specific responsibilities. This structure makes the program easier to understand, maintain, and test.

Application records use dictionaries containing an ID, company, role, application date, and status. IDs allow users to update or delete individual applications. The program validates user-provided dates using Python's `datetime.date` functionality and restricts statuses to a predefined list.

The test suite uses `pytest` to verify date validation, application creation, invalid input handling, case-insensitive searching, statistics, and saving and loading data. Temporary files are used when testing persistence so that tests do not need to modify the user's actual application data.

I deliberately kept the project lightweight: its core functionality uses Python's standard library, while `pytest` is used for development and testing. This keeps setup simple and allows the project to run in a standard Python environment.

## Requirements

- Python 3.10 or newer
- pytest for running the automated tests

## Installation and Usage

Clone or download the project and open a terminal in the project directory.

Create and activate a virtual environment if desired:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python project.py
```

Follow the numbered menu to add, view, search, update, or delete applications and display statistics.

Run the automated tests with:

```bash
python -m pytest -v
```

## Future Improvements

Possible future improvements include exporting applications to CSV, adding reminders for follow-ups, tracking interview dates, and replacing local JSON storage with a database for larger datasets.
