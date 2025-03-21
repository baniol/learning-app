"""
Scores module for saving and retrieving quiz scores.
"""
from datetime import datetime
from typing import List, Dict, Any, Optional
from .db import get_connection

def save_score(quiz_type: str, score: int, total_questions: int, player_name: str = "Anonymous") -> int:
    """
    Save a quiz score to the database.
    
    Args:
        quiz_type: The type of quiz (e.g., 'MultiplicationQuiz')
        score: The score achieved (number of correct answers)
        total_questions: The total number of questions in the quiz
        player_name: The name of the player (defaults to 'Anonymous')
        
    Returns:
        The ID of the newly inserted score record
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    percentage = (score / total_questions) * 100 if total_questions > 0 else 0
    
    cursor.execute('''
    INSERT INTO scores (quiz_type, player_name, score, total_questions, percentage)
    VALUES (?, ?, ?, ?, ?)
    ''', (quiz_type, player_name, score, total_questions, percentage))
    
    score_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return score_id

def get_top_scores(quiz_type: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Get the top scores from the database.
    
    Args:
        quiz_type: Optional filter by quiz type
        limit: Maximum number of scores to return
        
    Returns:
        A list of dictionaries containing score data, ordered by percentage (highest first)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    if quiz_type:
        cursor.execute('''
        SELECT * FROM scores
        WHERE quiz_type = ?
        ORDER BY percentage DESC, timestamp DESC
        LIMIT ?
        ''', (quiz_type, limit))
    else:
        cursor.execute('''
        SELECT * FROM scores
        ORDER BY percentage DESC, timestamp DESC
        LIMIT ?
        ''', (limit,))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to dictionaries
    return [dict(row) for row in rows]

def get_player_history(player_name: str, limit: int = 20) -> List[Dict[str, Any]]:
    """
    Get the score history for a specific player.
    
    Args:
        player_name: The name of the player
        limit: Maximum number of scores to return
        
    Returns:
        A list of dictionaries containing score data, ordered by timestamp (most recent first)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
    SELECT * FROM scores
    WHERE player_name = ?
    ORDER BY timestamp DESC
    LIMIT ?
    ''', (player_name, limit))
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to dictionaries
    return [dict(row) for row in rows]

def get_score_statistics(quiz_type: Optional[str] = None) -> Dict[str, Any]:
    """
    Get statistics about scores.
    
    Args:
        quiz_type: Optional filter by quiz type
        
    Returns:
        A dictionary containing statistics (average score, total quizzes taken, etc.)
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    query_params = []
    where_clause = ""
    
    if quiz_type:
        where_clause = "WHERE quiz_type = ?"
        query_params.append(quiz_type)
    
    cursor.execute(f'''
    SELECT 
        COUNT(*) as total_quizzes,
        AVG(percentage) as avg_percentage,
        MAX(percentage) as max_percentage,
        MIN(percentage) as min_percentage,
        AVG(score) as avg_score,
        SUM(score) as total_correct_answers,
        SUM(total_questions) as total_questions_asked
    FROM scores
    {where_clause}
    ''', query_params)
    
    result = dict(cursor.fetchone())
    conn.close()
    
    return result 