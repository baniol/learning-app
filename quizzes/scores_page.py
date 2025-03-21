"""
Scores page for displaying and managing quiz scores.
"""
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView
from PySide6.QtCore import Signal, Qt
from typing import Dict, Any, List

# Create a new ScoresViewer class in this file to avoid import issues
class ScoresViewer(QWidget):
    """Widget for displaying quiz scores."""
    
    return_to_menu = Signal()
    
    def __init__(self):
        super().__init__()
        
        # Main layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        # Title
        self.title_label = QLabel("Quiz Scores")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 10px;")
        self.layout.addWidget(self.title_label)
        
        # Controls bar
        controls_layout = QHBoxLayout()
        
        # Quiz type filter
        self.filter_label = QLabel("Quiz Type:")
        controls_layout.addWidget(self.filter_label)
        
        self.quiz_filter = QComboBox()
        self.quiz_filter.addItem("All Quizzes", None)
        self.quiz_filter.currentIndexChanged.connect(self.update_scores)
        controls_layout.addWidget(self.quiz_filter)
        
        # Spacer
        controls_layout.addStretch()
        
        # Return button
        self.return_button = QPushButton("Return to Menu")
        self.return_button.clicked.connect(self.return_to_menu.emit)
        controls_layout.addWidget(self.return_button)
        
        self.layout.addLayout(controls_layout)
        
        # Statistics section
        self.stats_label = QLabel("Statistics")
        self.stats_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        self.layout.addWidget(self.stats_label)
        
        # Stats container
        self.stats_container = QWidget()
        stats_layout = QHBoxLayout()
        self.stats_container.setLayout(stats_layout)
        
        # Stats items
        self.total_quizzes = QLabel("Total Quizzes: 0")
        stats_layout.addWidget(self.total_quizzes)
        
        self.avg_score = QLabel("Average Score: 0%")
        stats_layout.addWidget(self.avg_score)
        
        self.high_score = QLabel("Highest Score: 0%")
        stats_layout.addWidget(self.high_score)
        
        self.layout.addWidget(self.stats_container)
        
        # Scores table
        self.scores_label = QLabel("Top Scores")
        self.scores_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-top: 10px;")
        self.layout.addWidget(self.scores_label)
        
        self.scores_table = QTableWidget()
        self.scores_table.setColumnCount(5)
        self.scores_table.setHorizontalHeaderLabels(["Quiz Type", "Player", "Score", "Percentage", "Date"])
        self.scores_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.layout.addWidget(self.scores_table)
        
        # Initialize the view
        self.populate_quiz_types()
        self.update_scores()
    
    def populate_quiz_types(self):
        """Populate the quiz type filter with available quiz types."""
        # This would typically query the database for all quiz types
        # For now, add some sample types
        quiz_types = [
            "MultiplicationQuiz",
            "AdditionQuiz",
            "SubtractionQuiz",
            "SmallMultiplicationQuiz"
        ]
        
        for quiz_type in quiz_types:
            self.quiz_filter.addItem(quiz_type, quiz_type)
    
    def update_scores(self):
        """Update the scores table and statistics based on the selected filter."""
        from .database.scores import get_top_scores, get_score_statistics
        
        quiz_type = self.quiz_filter.currentData()
        
        # Get scores from database
        scores = get_top_scores(quiz_type, limit=20)
        
        # Update statistics
        stats = get_score_statistics(quiz_type)
        self.update_statistics(stats)
        
        # Update scores table
        self.update_scores_table(scores)
    
    def update_statistics(self, stats: Dict[str, Any]):
        """Update the statistics display with the provided data."""
        total_quizzes = stats.get('total_quizzes', 0)
        avg_percentage = stats.get('avg_percentage', 0)
        max_percentage = stats.get('max_percentage', 0)
        
        self.total_quizzes.setText(f"Total Quizzes: {total_quizzes}")
        self.avg_score.setText(f"Average Score: {avg_percentage:.1f}%")
        self.high_score.setText(f"Highest Score: {max_percentage:.1f}%")
    
    def update_scores_table(self, scores: List[Dict[str, Any]]):
        """Update the scores table with the provided data."""
        self.scores_table.setRowCount(0)  # Clear the table
        
        for row_idx, score in enumerate(scores):
            self.scores_table.insertRow(row_idx)
            
            # Create table items
            quiz_type_item = QTableWidgetItem(score.get('quiz_type', 'Unknown'))
            player_item = QTableWidgetItem(score.get('player_name', 'Anonymous'))
            
            score_text = f"{score.get('score', 0)}/{score.get('total_questions', 0)}"
            score_item = QTableWidgetItem(score_text)
            
            percentage = score.get('percentage', 0)
            percentage_item = QTableWidgetItem(f"{percentage:.1f}%")
            
            # Format timestamp
            timestamp = score.get('timestamp', '')
            if timestamp:
                # SQLite timestamps are often strings, parse if needed
                if isinstance(timestamp, str):
                    try:
                        from datetime import datetime
                        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                        timestamp = dt.strftime('%Y-%m-%d %H:%M')
                    except ValueError:
                        pass
            
            date_item = QTableWidgetItem(str(timestamp))
            
            # Set items in the table
            self.scores_table.setItem(row_idx, 0, quiz_type_item)
            self.scores_table.setItem(row_idx, 1, player_item)
            self.scores_table.setItem(row_idx, 2, score_item)
            self.scores_table.setItem(row_idx, 3, percentage_item)
            self.scores_table.setItem(row_idx, 4, date_item)

class ScoresPage(QWidget):
    """Container for the scores viewer component."""
    
    return_to_menu = Signal()
    
    def __init__(self):
        super().__init__()
        
        # Main layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        
        # Scores viewer
        self.scores_viewer = ScoresViewer()
        self.scores_viewer.return_to_menu.connect(self.return_to_menu.emit)
        self.layout.addWidget(self.scores_viewer)
    
    def refresh(self):
        """Refresh the scores data."""
        self.scores_viewer.update_scores() 