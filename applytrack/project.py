
import json
from datetime import date
from pathlib import Path

DATA_FILE = Path("applications.json")

STATUSES = [
    "Wishlist",
    "Applied",
    "Interview",
    "Offer",
    "Rejected",
    "Withdrawn",
]


def load_applications():
    """Load applications from JSON, or return an empty list."""
    if not DATA_FILE.exists():
        return []

    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            applications = json.load(file)
    except (json.JSONDecodeError, OSError):
        return []

    return applications if isinstance(applications, list) else []


def save_applications(applications):
    """Save applications to JSON."""
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(applications, file, indent=4)


def validate_date(date_text):
    """Check whether a date follows YYYY-MM-DD format."""
    try:
        return date.fromisoformat(date_text).isoformat() == date_text
    except (ValueError, TypeError):
        return False


def add_application(applications, company, role, date_applied,
                    status="Applied"):
    """Validate and add a job application."""
    company = company.strip()
    role = role.strip()

    if not company or not role:
        raise ValueError("Company and role are required.")

    if not validate_date(date_applied):
        raise ValueError("Date must use YYYY-MM-DD format.")

    if status not in STATUSES:
        raise ValueError("Invalid application status.")

    application = {
        "id": max((item["id"] for item in applications), default=0) + 1,
        "company": company,
        "role": role,
        "date_applied": date_applied,
        "status": status,
    }

    applications.append(application)
    return application


def search_applications(applications, query):
    """Search applications by company or job title."""
    query = query.strip().casefold()

    if not query:
        return applications.copy()

    return [
        application
        for application in applications
        if query in application["company"].casefold()
        or query in application["role"].casefold()
    ]


def calculate_statistics(applications):
    """Calculate the total and number of applications per status."""
    statistics = {
        "total": len(applications),
        "by_status": {status: 0 for status in STATUSES},
    }

    for application in applications:
        status = application["status"]
        if status in statistics["by_status"]:
            statistics["by_status"][status] += 1

    return statistics


def display_applications(applications):
    """Print applications in a readable format."""
    if not applications:
        print("\nNo applications found.")
        return

    print("\n" + "-" * 75)
    print(f"{'ID':<5}{'Company':<20}{'Role':<25}{'Date':<15}{'Status'}")
    print("-" * 75)

    for application in applications:
        print(
            f"{application['id']:<5}"
            f"{application['company'][:19]:<20}"
            f"{application['role'][:24]:<25}"
            f"{application['date_applied']:<15}"
            f"{application['status']}"
        )

    print("-" * 75)


def choose_status():
    """Ask the user to choose a valid application status."""
    print("\nAvailable statuses:")

    for number, status in enumerate(STATUSES, start=1):
        print(f"{number}. {status}")

    while True:
        choice = input("Choose a status number: ").strip()

        if choice.isdigit() and 1 <= int(choice) <= len(STATUSES):
            return STATUSES[int(choice) - 1]

        print("Invalid choice. Try again.")


def add_application_menu(applications):
    """Collect information and create an application."""
    print("\n--- Add Application ---")

    company = input("Company: ")
    role = input("Job title: ")
    date_applied = input("Application date (YYYY-MM-DD): ")

    try:
        application = add_application(
            applications, company, role, date_applied
        )
    except ValueError as error:
        print(f"Error: {error}")
        return

    save_applications(applications)
    print(f"Application #{application['id']} added successfully.")


def update_application_menu(applications):
    """Update the status of an existing application."""
    if not applications:
        print("\nNo applications to update.")
        return

    display_applications(applications)
    choice = input("Enter the application ID to update: ").strip()

    if not choice.isdigit():
        print("Please enter a numeric ID.")
        return

    application_id = int(choice)

    for application in applications:
        if application["id"] == application_id:
            application["status"] = choose_status()
            save_applications(applications)
            print("Application status updated.")
            return

    print("Application ID not found.")


def delete_application_menu(applications):
    """Delete an application after confirmation."""
    if not applications:
        print("\nNo applications to delete.")
        return

    display_applications(applications)
    choice = input("Enter the application ID to delete: ").strip()

    if not choice.isdigit():
        print("Please enter a numeric ID.")
        return

    application_id = int(choice)

    for application in applications:
        if application["id"] == application_id:
            confirmation = input(
                f"Delete the application for {application['company']}? (y/n): "
            ).strip().lower()

            if confirmation == "y":
                applications.remove(application)
                save_applications(applications)
                print("Application deleted.")
            else:
                print("Deletion cancelled.")

            return

    print("Application ID not found.")


def show_statistics(applications):
    """Display application totals grouped by status."""
    statistics = calculate_statistics(applications)

    print(f"\nTotal applications: {statistics['total']}")

    for status, count in statistics["by_status"].items():
        print(f"{status}: {count}")


def main():
    """Run the ApplyTrack command-line application."""
    applications = load_applications()

    while True:
        print("\n=== ApplyTrack: Job Application Tracker ===")
        print("1. Add application")
        print("2. View all applications")
        print("3. Search applications")
        print("4. Update application status")
        print("5. Delete application")
        print("6. View statistics")
        print("7. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_application_menu(applications)

        elif choice == "2":
            display_applications(applications)

        elif choice == "3":
            query = input("Search company or job title: ")
            results = search_applications(applications, query)
            display_applications(results)

        elif choice == "4":
            update_application_menu(applications)

        elif choice == "5":
            delete_application_menu(applications)

        elif choice == "6":
            show_statistics(applications)

        elif choice == "7":
            save_applications(applications)
            print("Applications saved. Goodbye!")
            break

        else:
            print("Invalid option. Choose a number from 1 to 7.")


if __name__ == "__main__":
    main()
