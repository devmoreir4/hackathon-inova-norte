import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta, date

def test_create_event(client: TestClient, sample_user_data):
    # Create user first (as organizer)
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    event_data = {
        "title": "Test Event",
        "description": "This is a test event",
        "event_type": "lecture",
        "start_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "location": "Test Location",
        "max_capacity": 50,
        "organizer_id": user_id
    }
    
    response = client.post("/api/v1/events/", json=event_data)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == event_data["title"]
    assert data["organizer_id"] == user_id
    assert data["registrations_open"] == True

def test_get_event_by_id(client: TestClient, sample_user_data):
    # Create user and event
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    event_data = {
        "title": "Test Event",
        "description": "This is a test event",
        "event_type": "lecture",
        "start_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "location": "Test Location",
        "organizer_id": user_id
    }
    
    create_response = client.post("/api/v1/events/", json=event_data)
    event_id = create_response.json()["id"]
    
    # Get event by ID
    response = client.get(f"/api/v1/events/{event_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == event_id
    assert data["title"] == event_data["title"]

def test_get_event_not_found(client: TestClient):
    """Test get non-existent event"""
    response = client.get("/api/v1/events/99999")
    assert response.status_code == 404
    assert "Event not found" in response.json()["detail"]

def test_list_events(client: TestClient, sample_user_data):
    # Create user
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    # Create multiple events
    for i in range(3):
        event_data = {
            "title": f"Event {i}",
            "description": f"Description for event {i}",
            "event_type": "lecture",
            "start_date": (datetime.now() + timedelta(days=i+1)).isoformat(),
            "location": f"Location {i}",
            "organizer_id": user_id
        }
        client.post("/api/v1/events/", json=event_data)
    
    # List events
    response = client.get("/api/v1/events/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3

def test_update_event(client: TestClient, sample_user_data):
    # Create user and event
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    event_data = {
        "title": "Original Event",
        "description": "Original description",
        "event_type": "lecture",
        "start_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "location": "Original Location",
        "organizer_id": user_id
    }
    
    create_response = client.post("/api/v1/events/", json=event_data)
    event_id = create_response.json()["id"]
    
    # Update event
    update_data = {
        "title": "Updated Event",
        "location": "Updated Location",
        "registrations_open": False
    }
    
    response = client.put(f"/api/v1/events/{event_id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Event"
    assert data["location"] == "Updated Location"
    assert data["registrations_open"] == False

def test_delete_event(client: TestClient, sample_user_data):
    # Create user and event
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    event_data = {
        "title": "Event to Delete",
        "description": "This event will be deleted",
        "event_type": "lecture",
        "start_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "location": "Test Location",
        "organizer_id": user_id
    }
    
    create_response = client.post("/api/v1/events/", json=event_data)
    event_id = create_response.json()["id"]
    
    # Delete event
    response = client.delete(f"/api/v1/events/{event_id}")
    assert response.status_code == 204
    
    # Verify event is deleted
    get_response = client.get(f"/api/v1/events/{event_id}")
    assert get_response.status_code == 404

def test_register_for_event(client: TestClient, sample_user_data):
    # Create user and event
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    event_data = {
        "title": "Registration Test Event",
        "description": "Event for testing registration",
        "event_type": "lecture",
        "start_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "location": "Test Location",
        "max_capacity": 10,
        "organizer_id": user_id
    }
    
    create_response = client.post("/api/v1/events/", json=event_data)
    event_id = create_response.json()["id"]
    
    # Register for event
    registration_data = {
        "event_id": event_id
    }
    
    response = client.post(
        f"/api/v1/events/{event_id}/register?user_id={user_id}",
        json=registration_data
    )
    assert response.status_code == 201
    data = response.json()
    assert data["event_id"] == event_id
    assert data["user_id"] == user_id
    assert data["attended"] == False

def test_register_duplicate(client: TestClient, sample_user_data):
    # Create user and event
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    event_data = {
        "title": "Duplicate Test Event",
        "description": "Event for testing duplicate registration",
        "event_type": "lecture",
        "start_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "location": "Test Location",
        "organizer_id": user_id
    }
    
    create_response = client.post("/api/v1/events/", json=event_data)
    event_id = create_response.json()["id"]
    
    registration_data = {"event_id": event_id}
    
    # First registration
    response1 = client.post(
        f"/api/v1/events/{event_id}/register?user_id={user_id}",
        json=registration_data
    )
    assert response1.status_code == 201
    
    # Duplicate registration
    response2 = client.post(
        f"/api/v1/events/{event_id}/register?user_id={user_id}",
        json=registration_data
    )
    assert response2.status_code == 400
    assert "already registered" in response2.json()["detail"]

def test_list_event_registrations(client: TestClient, sample_user_data):
    # Create users and event
    user1_data = sample_user_data.copy()
    user1_response = client.post("/api/v1/users/", json=user1_data)
    user1_id = user1_response.json()["id"]
    
    user2_data = sample_user_data.copy()
    user2_data["email"] = "user2@example.com"
    user2_response = client.post("/api/v1/users/", json=user2_data)
    user2_id = user2_response.json()["id"]
    
    event_data = {
        "title": "Registration List Test",
        "description": "Event for testing registration list",
        "event_type": "lecture",
        "start_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "location": "Test Location",
        "organizer_id": user1_id
    }
    
    create_response = client.post("/api/v1/events/", json=event_data)
    event_id = create_response.json()["id"]
    
    # Register both users
    for user_id in [user1_id, user2_id]:
        client.post(
            f"/api/v1/events/{event_id}/register?user_id={user_id}",
            json={"event_id": event_id}
        )
    
    # List registrations
    response = client.get(f"/api/v1/events/{event_id}/registrations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2

def test_update_registration(client: TestClient, sample_user_data):
    # Create user and event
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    event_data = {
        "title": "Update Registration Test",
        "description": "Event for testing registration update",
        "event_type": "lecture",
        "start_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "location": "Test Location",
        "organizer_id": user_id
    }
    
    create_response = client.post("/api/v1/events/", json=event_data)
    event_id = create_response.json()["id"]
    
    # Register for event
    reg_response = client.post(
        f"/api/v1/events/{event_id}/register?user_id={user_id}",
        json={"event_id": event_id}
    )
    registration_id = reg_response.json()["id"]
    
    # Update registration
    response = client.put(
        f"/api/v1/events/{event_id}/registrations/{registration_id}?attended=true&feedback=Great event!"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["attended"] == True
    assert data["feedback"] == "Great event!"

def test_cancel_registration(client: TestClient, sample_user_data):
    # Create user and event
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    event_data = {
        "title": "Cancel Registration Test",
        "description": "Event for testing registration cancellation",
        "event_type": "lecture",
        "start_date": (datetime.now() + timedelta(days=7)).isoformat(),
        "location": "Test Location",
        "organizer_id": user_id
    }
    
    create_response = client.post("/api/v1/events/", json=event_data)
    event_id = create_response.json()["id"]
    
    # Register for event
    reg_response = client.post(
        f"/api/v1/events/{event_id}/register?user_id={user_id}",
        json={"event_id": event_id}
    )
    registration_id = reg_response.json()["id"]
    
    # Cancel registration
    response = client.delete(f"/api/v1/events/{event_id}/registrations/{registration_id}")
    assert response.status_code == 204
    
    # Verify registration is cancelled
    list_response = client.get(f"/api/v1/events/{event_id}/registrations")
    assert len(list_response.json()) == 0

# Calendar functionality tests
def test_get_events_by_date(client: TestClient, sample_user_data):
    # Create user
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    # Create events for different dates
    target_date = datetime.now() + timedelta(days=5)
    other_date = datetime.now() + timedelta(days=10)
    
    # Event on target date
    event_data_1 = {
        "title": "Event on Target Date",
        "description": "Event for specific date test",
        "event_type": "lecture",
        "start_date": target_date.isoformat(),
        "location": "Test Location",
        "organizer_id": user_id
    }
    
    # Event on different date
    event_data_2 = {
        "title": "Event on Other Date",
        "description": "Event for different date",
        "event_type": "lecture",
        "start_date": other_date.isoformat(),
        "location": "Test Location",
        "organizer_id": user_id
    }
    
    client.post("/api/v1/events/", json=event_data_1)
    client.post("/api/v1/events/", json=event_data_2)
    
    # Get events for target date
    target_date_str = target_date.strftime("%Y-%m-%d")
    response = client.get(f"/api/v1/events/calendar/{target_date_str}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Event on Target Date"

def test_get_events_by_range(client: TestClient, sample_user_data):
    # Create user
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    # Create events in different dates
    base_date = datetime.now() + timedelta(days=10)
    
    events_data = [
        {
            "title": "Event 1",
            "description": "First event",
            "event_type": "lecture",
            "start_date": base_date.isoformat(),
            "location": "Location 1",
            "organizer_id": user_id
        },
        {
            "title": "Event 2", 
            "description": "Second event",
            "event_type": "lecture",
            "start_date": (base_date + timedelta(days=2)).isoformat(),
            "location": "Location 2",
            "organizer_id": user_id
        },
        {
            "title": "Event 3",
            "description": "Third event",
            "event_type": "lecture", 
            "start_date": (base_date + timedelta(days=5)).isoformat(),
            "location": "Location 3",
            "organizer_id": user_id
        }
    ]
    
    for event_data in events_data:
        client.post("/api/v1/events/", json=event_data)
    
    # Get events in range (should include first 2 events)
    start_date = base_date.strftime("%Y-%m-%d")
    end_date = (base_date + timedelta(days=3)).strftime("%Y-%m-%d")
    
    response = client.get(f"/api/v1/events/calendar/range?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == "Event 1"
    assert data[1]["title"] == "Event 2"

def test_get_events_by_month(client: TestClient, sample_user_data):
    # Create user
    user_response = client.post("/api/v1/users/", json=sample_user_data)
    user_id = user_response.json()["id"]
    
    # Create events in specific month
    target_month = datetime.now().month + 1 if datetime.now().month < 12 else 1
    target_year = datetime.now().year if datetime.now().month < 12 else datetime.now().year + 1
    
    # Events in target month
    event_in_month = datetime(target_year, target_month, 15)
    event_outside_month = datetime(target_year, target_month + 1 if target_month < 12 else 1, 15)
    
    event_data_1 = {
        "title": "Event in Target Month",
        "description": "Event for month test",
        "event_type": "lecture",
        "start_date": event_in_month.isoformat(),
        "location": "Test Location",
        "organizer_id": user_id
    }
    
    event_data_2 = {
        "title": "Event Outside Month",
        "description": "Event outside target month",
        "event_type": "lecture", 
        "start_date": event_outside_month.isoformat(),
        "location": "Test Location",
        "organizer_id": user_id
    }
    
    client.post("/api/v1/events/", json=event_data_1)
    client.post("/api/v1/events/", json=event_data_2)
    
    # Get events for target month
    response = client.get(f"/api/v1/events/calendar/month/{target_year}/{target_month}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Event in Target Month"

def test_get_events_by_month_invalid(client: TestClient):
    response = client.get("/api/v1/events/calendar/month/2024/13")
    assert response.status_code == 400
    assert "Month must be between 1 and 12" in response.json()["detail"]

# User events tests
def test_get_user_events(client: TestClient, sample_user_data):
    # Create users
    user1_response = client.post("/api/v1/users/", json=sample_user_data)
    user1_id = user1_response.json()["id"]
    
    user2_data = sample_user_data.copy()
    user2_data["email"] = "user2@example.com"
    user2_response = client.post("/api/v1/users/", json=user2_data)
    user2_id = user2_response.json()["id"]
    
    # Create events for user1
    for i in range(2):
        event_data = {
            "title": f"User1 Event {i}",
            "description": f"Event organized by user1 - {i}",
            "event_type": "lecture",
            "start_date": (datetime.now() + timedelta(days=i+1)).isoformat(),
            "location": f"Location {i}",
            "organizer_id": user1_id
        }
        client.post("/api/v1/events/", json=event_data)
    
    # Create event for user2
    event_data = {
        "title": "User2 Event",
        "description": "Event organized by user2",
        "event_type": "lecture",
        "start_date": (datetime.now() + timedelta(days=5)).isoformat(),
        "location": "User2 Location",
        "organizer_id": user2_id
    }
    client.post("/api/v1/events/", json=event_data)
    
    # Get user1's events
    response = client.get(f"/api/v1/events/user/{user1_id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for event in data:
        assert event["organizer_id"] == user1_id
        assert "User1 Event" in event["title"]

def test_get_user_events_not_found(client: TestClient):
    response = client.get("/api/v1/events/user/99999")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]

def test_get_user_registrations(client: TestClient, sample_user_data):
    # Create users
    user1_response = client.post("/api/v1/users/", json=sample_user_data)
    user1_id = user1_response.json()["id"]
    
    user2_data = sample_user_data.copy()
    user2_data["email"] = "organizer@example.com"
    user2_response = client.post("/api/v1/users/", json=user2_data)
    organizer_id = user2_response.json()["id"]
    
    # Create events
    events = []
    for i in range(3):
        event_data = {
            "title": f"Event {i}",
            "description": f"Event for registration test {i}",
            "event_type": "lecture",
            "start_date": (datetime.now() + timedelta(days=i+1)).isoformat(),
            "location": f"Location {i}",
            "organizer_id": organizer_id
        }
        event_response = client.post("/api/v1/events/", json=event_data)
        events.append(event_response.json()["id"])
    
    # Register user1 for first 2 events
    for event_id in events[:2]:
        client.post(
            f"/api/v1/events/{event_id}/register?user_id={user1_id}",
            json={"event_id": event_id}
        )
    
    # Get user1's registrations
    response = client.get(f"/api/v1/events/user/{user1_id}/registrations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    for registration in data:
        assert registration["user_id"] == user1_id
        assert registration["event_id"] in events[:2]

def test_get_user_registrations_not_found(client: TestClient):
    response = client.get("/api/v1/events/user/99999/registrations")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"]
