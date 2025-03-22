"""
User management dialog for adding and editing users.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
    QPushButton, QMessageBox
)
from PySide6.QtCore import Qt
from ..database.users import create_user, update_user, get_user_by_username

class UserDialog(QDialog):
    """Dialog for adding or editing a user."""
    
    def __init__(self, parent=None, user_id=None, user_data=None):
        super().__init__(parent)
        
        self.user_id = user_id
        self.user_data = user_data or {}
        self.is_edit_mode = user_id is not None
        
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the dialog UI."""
        # Set window properties
        title = "Edit User" if self.is_edit_mode else "Add New User"
        self.setWindowTitle(title)
        self.setMinimumWidth(400)
        
        # Main layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Username field (only editable in create mode)
        username_layout = QHBoxLayout()
        username_label = QLabel("Username:")
        username_label.setMinimumWidth(100)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username (letters and numbers only)")
        
        if self.is_edit_mode:
            self.username_input.setText(self.user_data.get('username', ''))
            self.username_input.setEnabled(False)
            
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Display name field
        display_name_layout = QHBoxLayout()
        display_name_label = QLabel("Display Name:")
        display_name_label.setMinimumWidth(100)
        self.display_name_input = QLineEdit()
        self.display_name_input.setPlaceholderText("Enter display name")
        
        if self.is_edit_mode:
            self.display_name_input.setText(self.user_data.get('display_name', ''))
            
        display_name_layout.addWidget(display_name_label)
        display_name_layout.addWidget(self.display_name_input)
        layout.addLayout(display_name_layout)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_user)
        self.save_button.setDefault(True)
        
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.save_button)
        layout.addLayout(buttons_layout)
        
    def save_user(self):
        """Validate and save the user."""
        username = self.username_input.text().strip()
        display_name = self.display_name_input.text().strip()
        
        print(f"Saving user: username='{username}', display_name='{display_name}'")
        
        # Validate inputs
        if not self.is_edit_mode and not username:
            print("Username is required")
            QMessageBox.warning(self, "Invalid Input", "Username is required")
            return
            
        if not display_name:
            display_name = username
        
        try:
            if self.is_edit_mode:
                # Update existing user
                success = update_user(self.user_id, display_name)
                print(f"Update user result: {success}")
                if success:
                    self.accept()
                else:
                    QMessageBox.warning(self, "Error", "Failed to update user")
            else:
                # Create new user
                # Check if username exists
                existing_user = get_user_by_username(username)
                print(f"Existing user check: {existing_user}")
                if existing_user:
                    QMessageBox.warning(self, "Username Exists", 
                                      "This username is already taken. Please choose another.")
                    return
                    
                # Create user
                try:
                    user_id = create_user(username, display_name)
                    print(f"Create user result: {user_id}")
                    if user_id:
                        self.user_id = user_id
                        self.accept()
                    else:
                        QMessageBox.warning(self, "Error", "Failed to create user")
                except Exception as e:
                    print(f"Error creating user: {str(e)}")
                    raise
        except Exception as e:
            print(f"Exception in save_user: {str(e)}")
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
    
    @staticmethod
    def create_user(parent=None):
        """
        Static method to create a new user.
        
        Returns:
            Tuple of (user_id, username, display_name) if successful, None otherwise
        """
        dialog = UserDialog(parent)
        try:
            # Use exec_ for PySide6 compatibility
            result = dialog.exec()
            print(f"Dialog exec result: {result}, QDialog.Accepted={QDialog.Accepted}")
            
            if result == QDialog.Accepted and dialog.user_id:
                return (dialog.user_id, 
                       dialog.username_input.text().strip(),
                       dialog.display_name_input.text().strip() or dialog.username_input.text().strip())
            return None
        except Exception as e:
            print(f"Exception in create_user: {str(e)}")
            return None
    
    @staticmethod
    def edit_user(user_id, user_data, parent=None):
        """
        Static method to edit an existing user.
        
        Returns:
            New display name if successful, None otherwise
        """
        dialog = UserDialog(parent, user_id, user_data)
        result = dialog.exec()
        
        if result == QDialog.Accepted:
            return dialog.display_name_input.text().strip() or user_data.get('username', '')
        return None 