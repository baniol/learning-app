"""
User management module for the quiz application.
This centralizes all user-related functionality in one place.
"""
from PySide6.QtWidgets import QMessageBox, QComboBox
from PySide6.QtCore import QObject, Signal
from .database.users import get_all_users, get_user
from .components.user_dialog import UserDialog
from .components.navigation_bar import NavigationBar
from .debug import is_debug_mode, log


class UserManager(QObject):
    """
    Manages user functionality for the quiz application.
    Handles user selection, creation, and the user dropdown UI.
    """
    # Signal emitted when the current user changes
    user_changed = Signal(dict)  # user_data
    
    def __init__(self, parent=None):
        """
        Initialize the user manager.
        
        Args:
            parent: Parent QObject
        """
        super().__init__(parent)
        
        # Set current user - default to Anonymous (ID 1)
        self.current_user_id = 1
        self.current_user = get_user(self.current_user_id) or {"id": 1, "username": "anonymous", "display_name": "Anonymous"}
        self.user_dropdown = None
        self.nav_bar = None
        
        log("UserManager", "Initialized")
    
    def setup_navigation_bar(self, return_callback=None):
        """
        Set up the navigation bar with user selection.
        
        Args:
            return_callback: Callback function for the Back button
            
        Returns:
            The created NavigationBar
        """
        # Create navigation bar
        self.nav_bar = NavigationBar(return_callback or (lambda: None))  # No return callback if not provided
        self.nav_bar.setFixedHeight(40)
        
        # Get users from database
        try:
            users = get_all_users()
            log("UserManager", f"Retrieved {len(users)} users from database")
        except Exception as e:
            error_msg = f"Failed to load users: {str(e)}"
            log("UserManager", f"Error: {error_msg}")
            if parent := self.parent():
                QMessageBox.warning(parent, "Database Error", error_msg)
            users = [{"id": 1, "display_name": "Anonymous"}]
        
        # Add user dropdown
        self.user_dropdown = self.nav_bar.add_user_dropdown(users, self.current_user_id)
        
        # Connect to our own handler instead of directly to the signal
        self.nav_bar.user_changed.connect(self.on_user_changed)
        
        return self.nav_bar
    
    def on_user_changed(self, user_id):
        """
        Handle user selection changes.
        
        Args:
            user_id: The ID of the selected user
        """
        log("UserManager", f"User changed to ID: {user_id}")
        
        # If it's the special "Add New User" option
        if user_id == -1:
            # Add new user was selected
            log("UserManager", "Add new user selected, opening dialog...")
            parent = self.parent()
            result = UserDialog.create_user(parent)
            log("UserManager", f"Dialog result: {result}")
            
            if result:
                # Dialog was accepted and user was created
                new_user_id, username, display_name = result
                log("UserManager", f"New user created: {new_user_id}, {username}, {display_name}")
                
                # Update the dropdown with the new user selected
                self.refresh_user_dropdown(new_user_id)
                
                # Set as current user
                self.current_user_id = new_user_id
                self.current_user = {
                    "id": new_user_id,
                    "username": username,
                    "display_name": display_name
                }
                
                # Emit signal
                self.user_changed.emit(self.current_user)
            else:
                # Dialog was canceled or failed
                log("UserManager", "User creation canceled or failed")
                # Reset to the previously selected user
                try:
                    # Find the index for the current user ID
                    for i in range(self.user_dropdown.count()):
                        if self.user_dropdown.itemData(i) == self.current_user_id:
                            self.user_dropdown.setCurrentIndex(i)
                            break
                except Exception as e:
                    log("UserManager", f"Error resetting user dropdown: {str(e)}")
                    # If all else fails, set to the first item
                    if self.user_dropdown.count() > 0:
                        self.user_dropdown.setCurrentIndex(0)
        else:
            # Regular user selection
            self.current_user_id = user_id
            self.current_user = get_user(user_id) or {"id": user_id}
            
            # Emit signal
            self.user_changed.emit(self.current_user)
    
    def refresh_user_dropdown(self, select_user_id=None):
        """
        Refresh the user dropdown with current users.
        
        Args:
            select_user_id: User ID to select after refresh
        """
        if not self.user_dropdown:
            log("UserManager", "Cannot refresh dropdown: dropdown not initialized")
            return
            
        try:
            users = get_all_users()
            log("UserManager", f"Refreshing dropdown with {len(users)} users")
            
            # Clear and repopulate dropdown
            current_index = 0
            self.user_dropdown.clear()
            
            for i, user in enumerate(users):
                self.user_dropdown.addItem(user['display_name'], user['id'])
                if select_user_id and user['id'] == select_user_id:
                    current_index = i
            
            # Add the "Add New User" option
            self.user_dropdown.addItem("+ Add New User", -1)
            
            # Set the selected index
            if select_user_id:
                self.user_dropdown.setCurrentIndex(current_index)
                log("UserManager", f"Selected user ID {select_user_id} at index {current_index}")
                
        except Exception as e:
            error_msg = f"Failed to refresh users: {str(e)}"
            log("UserManager", f"Error: {error_msg}")
            parent = self.parent()
            if parent:
                QMessageBox.warning(parent, "Database Error", error_msg)
    
    def get_current_user(self):
        """
        Get the current user data.
        
        Returns:
            Dict containing user data
        """
        return self.current_user 