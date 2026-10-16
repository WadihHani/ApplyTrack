
import pytest

import project


def test_validate_date():
    assert project.validate_date("2026-10-16")
    assert project.validate_date("2024-02-29")
    assert not project.validate_date("2025-02-29")
    assert not project.validate_date("16-10-2026")
    assert not project.validate_date("")


def test_add_application():
    applications = []

    application = project.add_application(
        applications,
        "Google",
        "Python Developer",
        "2026-10-16",
    )

    assert application["id"] == 1
    assert application["company"] == "Google"
    assert application["role"] == "Python Developer"
    assert application["status"] == "Applied"
    assert len(applications) == 1


def test_add_application_validation():
    applications = []

    with pytest.raises(ValueError):
        project.add_application(
            applications, "", "Developer", "2026-10-16"
        )

    with pytest.raises(ValueError):
        project.add_application(
            applications, "Google", "Developer", "invalid-date"
        )

    with pytest.raises(ValueError):
        project.add_application(
            applications, "Google", "Developer",
            "2026-10-16", "Unknown"
        )


def test_search_applications():
    applications = [
        {
            "id": 1,
            "company": "Google",
            "role": "Python Developer",
            "date_applied": "2026-10-16",
            "status": "Applied",
        },
        {
            "id": 2,
            "company": "Amazon",
            "role": "Data Analyst",
            "date_applied": "2026-10-15",
            "status": "Interview",
        },
    ]

    assert len(project.search_applications(applications, "google")) == 1
    assert len(project.search_applications(applications, "DATA")) == 1
    assert len(project.search_applications(applications, "unknown")) == 0


def test_calculate_statistics():
    applications = [
        {"id": 1, "company": "Google", "role": "Developer",
         "date_applied": "2026-10-16", "status": "Applied"},
        {"id": 2, "company": "Amazon", "role": "Analyst",
         "date_applied": "2026-10-15", "status": "Interview"},
        {"id": 3, "company": "Apple", "role": "Engineer",
         "date_applied": "2026-10-14", "status": "Applied"},
    ]

    statistics = project.calculate_statistics(applications)

    assert statistics["total"] == 3
    assert statistics["by_status"]["Applied"] == 2
    assert statistics["by_status"]["Interview"] == 1
    assert statistics["by_status"]["Offer"] == 0


def test_save_and_load_applications(tmp_path, monkeypatch):
    data_file = tmp_path / "applications.json"
    monkeypatch.setattr(project, "DATA_FILE", data_file)

    applications = []
    project.add_application(
        applications, "Google", "Developer", "2026-10-16"
    )

    project.save_applications(applications)
    loaded = project.load_applications()

    assert loaded == applications
