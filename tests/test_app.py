import pytest
from app import app, init_db, get_db_connection
import os

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test_secret'
    
    with app.test_client() as client:
        # Create a fresh database for each test
        init_db()
        yield client
    
    # Cleanup after tests
    if os.path.exists("aceest_fitness.db"):
        os.remove("aceest_fitness.db")

def test_index_redirect(client):
    """Test that the index page redirects to login when not logged in."""
    rv = client.get('/', follow_redirects=True)
    assert b'Secure Login' in rv.data

def test_login_logout(client):
    """Test login and logout functionality."""
    # Test valid login
    rv = client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    assert b'Client Management' in rv.data
    
    # Test logout
    rv = client.get('/logout', follow_redirects=True)
    assert b'Secure Login' in rv.data

def test_add_client(client):
    """Test adding a new client."""
    # Login first
    client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    # Add client
    rv = client.post('/client/add', data=dict(
        name='Test User'
    ), follow_redirects=True)
    assert b'Test User' in rv.data
    assert b'added successfully' in rv.data

def test_generate_program(client):
    """Test AI program generation."""
    # Login first
    client.post('/login', data=dict(
        username='admin',
        password='admin'
    ), follow_redirects=True)
    
    # Add client
    client.post('/client/add', data=dict(
        name='Test User'
    ), follow_redirects=True)
    
    # Get client ID
    conn = get_db_connection()
    user = conn.execute("SELECT id FROM clients WHERE name='Test User'").fetchone()
    conn.close()
    
    client_id = user['id']
    
    # Generate program
    rv = client.get(f'/client/{client_id}/generate_program', follow_redirects=True)
    assert b'Generated' in rv.data
    assert b'program:' in rv.data

def test_database_persistence():
    """Test that data is correctly saved in the database."""
    init_db()
    conn = get_db_connection()
    conn.execute("INSERT INTO clients (name) VALUES (?)", ("Persistent User",))
    conn.commit()
    
    row = conn.execute("SELECT * FROM clients WHERE name='Persistent User'").fetchone()
    assert row['name'] == 'Persistent User'
    conn.close()
    
    if os.path.exists("aceest_fitness.db"):
        os.remove("aceest_fitness.db")
