def test_user_signup(test_client):
    """Test user sign up."""
    username = 'newuser'
    response = test_client.post('/register', json={
        'username': username,
        'password': 'newpassword',
        'email': 'newuser@example.com'
    })
    assert response.status_code == 201
    expected_message = f"User {username} was created"
    # Convert response data from bytes to dictionary for easy assertion
    response_data = response.get_json()
    assert response_data['message'] == expected_message


def test_user_login(test_client, signup_default_user):
    """Test user login."""
    # Since this test depends on signup_default_user fixture, the user will be signed up before login test
    response = test_client.post('/login', json={
        'username': 'default_user',
        'password': 'default_password',
        'email': 'default_user@example.com'
    })
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
    assert 'refresh_token' in data


def test_user_signup_existing_user(test_client, signup_default_user):
    """Test user sign up with an existing username."""
    response = test_client.post('/register', json={
        'username': 'default_user',  # Using the same username as before
        'password': 'anotherpassword',
        'email': 'default_user@example.com'
    })
    assert response.status_code == 400  # Or whatever your app returns in this case
    assert b"A user with that username already exists" in response.data
