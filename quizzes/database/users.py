"""
User management module for quiz application.
"""
from typing import List, Dict, Any, Optional
from .db import get_connection

def get_all_users() -> List[Dict[str, Any]]:
    """
    Get all users from the database.
    
    Returns:
        A list of dictionaries containing user data
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM users ORDER BY display_name')
        
        rows = cursor.fetchall()
        conn.close()
        
        # Convert rows to dictionaries
        users = [dict(row) for row in rows]
        print(f"Retrieved {len(users)} users from database")
        return users
    except Exception as e:
        print(f"Error getting users: {str(e)}")
        # Return at least the anonymous user
        return [{"id": 1, "username": "anonymous", "display_name": "Anonymous"}]

def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """
    Get a user by ID.
    
    Args:
        user_id: The ID of the user to retrieve
        
    Returns:
        User data as a dictionary, or None if not found
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None

def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """
    Get a user by username.
    
    Args:
        username: The username to look up
        
    Returns:
        User data as a dictionary, or None if not found
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    
    row = cursor.fetchone()
    conn.close()
    
    return dict(row) if row else None

def create_user(username: str, display_name: str = None) -> int:
    """
    Create a new user.
    
    Args:
        username: The unique username
        display_name: The display name (defaults to username if not provided)
        
    Returns:
        The ID of the newly created user
    """
    print(f"Creating user: username='{username}', display_name='{display_name}'")
    if display_name is None:
        display_name = username
        
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            'INSERT INTO users (username, display_name) VALUES (?, ?)',
            (username, display_name)
        )
        user_id = cursor.lastrowid
        print(f"User created with ID: {user_id}")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error creating user in database: {str(e)}")
        raise e
    finally:
        conn.close()
        
    return user_id

def update_user(user_id: int, display_name: str) -> bool:
    """
    Update a user's display name.
    
    Args:
        user_id: The ID of the user to update
        display_name: The new display name
        
    Returns:
        True if successful, False otherwise
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            'UPDATE users SET display_name = ? WHERE id = ?',
            (display_name, user_id)
        )
        success = cursor.rowcount > 0
        conn.commit()
    except Exception as e:
        conn.rollback()
        success = False
    finally:
        conn.close()
        
    return success

def delete_user(user_id: int) -> bool:
    """
    Delete a user.
    
    Args:
        user_id: The ID of the user to delete
        
    Returns:
        True if successful, False otherwise
    """
    # Don't allow deleting the anonymous user
    if user_id == 1:
        return False
        
    conn = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        success = cursor.rowcount > 0
        conn.commit()
    except Exception as e:
        conn.rollback()
        success = False
    finally:
        conn.close()
        
    return success 