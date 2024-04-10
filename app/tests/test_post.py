
def test_create_new_blog_post(test_client, auth_token):
    """Test creating a new blog post."""
    response = test_client.post('/posts', json={
        'title': 'New Blog Post',
        'body': 'This is a new blog post.'
    }, headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 201
    assert b'New Blog Post' in response.data


def test_retrieving_list_of_blog_posts(test_client, auth_token, create_default_posts):
    response = test_client.get('/posts', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert b'New Blog Post' in response.data

    # Parse the JSON response
    posts = response.get_json()
    assert len(posts) >= 3, f"Expected more than 3 posts, got {len(posts)}"


def test_retrieving_single_blog_post(test_client, auth_token, create_default_posts):
    """Test retrieving a single blog post by its ID."""
    # Assuming ID 1 exists and was created in a previous test
    response = test_client.get('/posts/1', headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert b'New Blog Post' in response.data


def test_update_existing_blog_post(test_client, auth_token, create_default_posts):
    """Test updating an existing blog post."""
    # Assuming ID 1 exists and was created in a previous test
    response = test_client.put('/posts/1', json={
        'title': 'Updated Blog Post',
        'body': 'This blog post has been updated.'
    }, headers={'Authorization': f'Bearer {auth_token}'})
    assert response.status_code == 200
    assert b'Updated Blog Post' in response.data


def test_create_new_blog_post_without_auth(test_client):
    """Test creating a new blog post without authentication."""
    response = test_client.post('/posts', json={
        'title': 'Unauthorized Post',
        'body': 'This should not be created.'
    })
    assert response.status_code == 401


def test_retrieving_single_blog_post_without_auth(test_client):
    """Test retrieving a single blog post by its ID without authentication."""
    # Assuming a post with ID 1 exists; adjust as needed.
    response = test_client.get('/posts/1')
    assert response.status_code == 401


def test_update_existing_blog_post_without_auth(test_client):
    """Test updating an existing blog post without authentication."""
    # Assuming a post with ID 1 exists; adjust as needed.
    response = test_client.put('/posts/1', json={
        'title': 'Unauthorized Update',
        'body': 'This update should not occur.'
    })
    assert response.status_code == 401
