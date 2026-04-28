# services/validation_service.py

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import (
    VALID_USERS,
    ERROR_EMPTY_USERNAME,
    ERROR_EMPTY_PASSWORD,
    ERROR_INVALID_CREDENTIALS,
    ERROR_SHORT_USERNAME,
    ERROR_SHORT_PASSWORD
)
class CheckValid:

    
    def __init__(self):
        
        self.valid_users = VALID_USERS 
        self.error_message = ""
    
    def validate_username(self, username):
        # Bemty or n ot 
        if not username or username.strip() == "":
            self.error_message = ERROR_EMPTY_USERNAME
            return False
        
        # Minimum 3 kcharacter
        if len(username) < 3:
            self.error_message = ERROR_SHORT_USERNAME
            return False
        
        self.error_message = ""
        return True
    
    def validate_password(self, password):
        
        # emty or not
        if not password or password.strip() == "":
            self.error_message = ERROR_EMPTY_PASSWORD
            return False
        
        # Minimum 4 character
        if len(password) < 4:
            self.error_message = ERROR_SHORT_PASSWORD
            return False
        
        self.error_message = ""
        return True
    
    def check_credentials(self, username, password):
        
        # check name and password enterde inpıt 
        if not self.validate_username(username):
            return False
        
        if not self.validate_password(password):
            return False
        

        if username in self.valid_users:
            
            if self.valid_users[username] == password:
                
                self.error_message = ""
                return True
            else:
            
                self.error_message = ERROR_INVALID_CREDENTIALS
                return False
        else:
        
            self.error_message = ERROR_INVALID_CREDENTIALS
            return False
    
    def get_error_message(self):
    
        return self.error_message

