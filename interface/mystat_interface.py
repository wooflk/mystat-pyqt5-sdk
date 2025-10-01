from core import (get_auth, get_marks, calc_avr_mark, get_attendance, get_leaderboard, 
                 get_homework, get_schedule, download_file, get_file_token, 
                 upload_file_to_storage, submit_homework, check_token_validity)

class MystatInterface:
    def __init__(self, login, password, campus='aqtobe'):
        self.login = login
        self.password = password
        self.campus = campus
        self.token = None

    def authenticate(self):
        success, token = get_auth(self.login, self.password)
        if success:
            self.token = token
            return True
        return False
    
    def get_user_info(self):
        if not self.token:
            return None
        
        try:
            import base64
            import json
            
            parts = self.token.split('.')
            if len(parts) != 3:
                return None
                
            payload = parts[1]
            padding = len(payload) % 4
            if padding:
                payload += '=' * (4 - padding)
                
            decoded = base64.urlsafe_b64decode(payload)
            user_data = json.loads(decoded)
            
            return user_data
        except Exception as e:
            print(f"Ошибка декодирования токена: {e}")
            return None

    def marks(self):
        return get_marks(self.token, self.campus) if self.token else None

    def average_mark(self):
        return calc_avr_mark(self.token, self.campus) if self.token else None

    def homework(self, status=3, limit=1000, sort='-hw.time'):
        return get_homework(self.token, self.campus, status, limit, sort) if self.token else None

    def attendance(self, period="month"):
        return get_attendance(self.token, self.campus, period) if self.token else None

    def leaderboard(self):
        return get_leaderboard(self.token, self.campus) if self.token else None

    def schedule(self, week=True, date=None):
        return get_schedule(self.token, week, date, self.campus) if self.token else None

    def download_homework_file(self, file_url, save_path):
        return download_file(file_url, save_path, self.token) if self.token else (False, "Нет токена авторизации")
    
    def check_token_validity(self):
        if not self.token:
            return False, "Нет токена авторизации"
        
        return check_token_validity(self.token, self.campus)
    
    def get_file_token(self):
        if not self.token:
            return False, "Нет токена авторизации"
        
        print(f"Основной токен для запроса create-token: {self.token}")
        return get_file_token(self.token, self.campus)
    
    def upload_file_to_storage(self, file_path, file_token, homework_dir_id):
        return upload_file_to_storage(file_path, file_token, homework_dir_id)
    
    def submit_homework(self, homework_id, file_url=None, answer_text=None):
        return submit_homework(self.token, self.campus, homework_id, file_url, answer_text) if self.token else (False, "Нет токена авторизации")
    
