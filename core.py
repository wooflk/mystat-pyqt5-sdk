# работа с API сайта (MyStat)

import os
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///mystat.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

BASE_URL = "https://mapi.itstep.org"
LANGUAGE = "ru"

def _default_headers(token=None):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'content-type': 'application/json',
        'referer': 'https://mystat.itstep.org/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'x-language': LANGUAGE,
        'origin': 'https://mystat.itstep.org',
        'access-control-request-method': 'POST',
        'access-control-request-headers': 'content-type'
    }
    if token:
        headers['authorization'] = f'Bearer {token}'
    return headers

def handle_response(response):
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка {response.status_code}: {response.text}")
        return None

def get_auth(login, password):
    url = f'{BASE_URL}/v1/mystat/auth/login'
    payload = {"login": login, "password": password}
    
    print(f"Вход в систему: {login}")
    response = requests.post(url, json=payload, headers=_default_headers())
    
    if response.status_code == 200:
        print("Успешный вход в систему")
        return True, response.text
    else:
        print(f"Ошибка входа: {response.status_code}")
        return False, None

def get_marks(token, campus):
    url = f'{BASE_URL}/v1/mystat/{campus}/statistic/marks'
    return handle_response(requests.get(url, headers=_default_headers(token)))

def calc_avr_mark(token, campus):
    marks_data = get_marks(token, campus)
    if not marks_data:
        return None
    
    marks = []
    for item in marks_data:
        if isinstance(item, dict) and 'mark' in item:
            try:
                marks.append(float(item['mark']))
            except Exception:
                pass
    
    return sum(marks) / len(marks) if marks else None

def get_attendance(token, campus, period="month"):
    url = f"{BASE_URL}/v1/mystat/{campus}/statistic/attendance"
    params = {"period": period}
    response = requests.get(url, headers=_default_headers(token), params=params)
    return handle_response(response)

def get_leaderboard(token, campus):
    url = f'{BASE_URL}/v1/mystat/{campus}/progress/leader-table'
    return handle_response(requests.get(url, headers=_default_headers(token)))

def get_homework(token, campus, status=3, limit=1000, sort='-hw.time'):
    url = f'{BASE_URL}/v1/mystat/{campus}/homework/list'
    params = {
        'status': status,
        'limit': limit,
        'sort': sort
    }
    response = requests.get(url, headers=_default_headers(token), params=params)
    return handle_response(response)

def get_schedule(token, week=True, date=None, campus='aqtobe'):
    type_param = 'week' if week else 'month'
    date_filter = date or ''
    url = f"{BASE_URL}/v1/mystat/{campus}/schedule/get-month?type={type_param}&date_filter={date_filter}"
    data = handle_response(requests.get(url, headers=_default_headers(token)))
    if data:
        return data.get('data', data)
    return None

def download_file(file_url, save_path, token=None):
    try:
        headers = _default_headers(token) if token else {}
        response = requests.get(file_url, headers=headers, stream=True)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        return True, f"Файл успешно скачан: {save_path}"
    except Exception as e:
        return False, f"Ошибка скачивания файла: {str(e)}"

def check_token_validity(token, campus):
    if not token:
        return False, "Токен не предоставлен"
    
    url = f'{BASE_URL}/v1/mystat/{campus}/statistic/marks'
    headers = _default_headers(token)
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return True, "Токен действителен"
    elif response.status_code == 401:
        return False, "Токен авторизации недействителен или истек"
    else:
        return False, f"Ошибка проверки токена: {response.status_code}"

def get_file_token(token, campus):
    if not token:
        return False, "Токен не предоставлен"
    
    is_valid, message = check_token_validity(token, campus)
    if not is_valid:
        return False, message
    
    url = f'{BASE_URL}/v1/mystat/{campus}/user/file-token'
    headers = _default_headers(token)
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        file_token = result.get('token', '')
        directories = result.get('directories', {})
        homework_dir_id = directories.get('homeworkDirId', '')
        
        if file_token and homework_dir_id:
            return True, {
                'token': file_token,
                'homework_dir_id': homework_dir_id
            }
        else:
            return False, "Токен файла или директория не найдены в ответе"
    elif response.status_code == 401:
        return False, "Токен авторизации недействителен или истек. Попробуйте войти заново."
    else:
        return False, f"Ошибка получения токена: {response.status_code} - {response.text}"

def upload_file_to_storage(file_path, file_token, homework_dir_id):
    try:
        upload_url = "https://fsx3.itstep.org/api/v1/files"
        
        headers = {
            'Authorization': f'Bearer {file_token}',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

        with open(file_path, 'rb') as file:
            files = {'files[]': file}
            data = {'directory': homework_dir_id}
            
            response = requests.post(upload_url, files=files, data=data, headers=headers)
            
            if response.status_code == 200:
                result = response.json()
                if result and len(result) > 0:
                    file_url = result[0].get('link', '')
                    if file_url:
                        print(f"Файл успешно загружен: {file_url}")
                        return True, file_url
                    else:
                        return False, "URL файла не найден в ответе"
                else:
                    return False, "Неожиданный ответ от сервера"
            else:
                return False, f"Ошибка загрузки файла: {response.status_code} - {response.text}"
                
    except Exception as e:
        return False, f"Ошибка загрузки файла: {str(e)}"

def submit_homework(token, campus, homework_id, file_url=None, answer_text=None):
    try:
        url = f'{BASE_URL}/v1/mystat/{campus}/homework/create'
        
        payload = {
            'id': homework_id,
            'answerText': answer_text,
            'filename': file_url
        }
        
        response = requests.post(url, json=payload, headers=_default_headers(token))
        
        if response.status_code in [200, 201]:
            return True, "Задание успешно отправлено на проверку"
        else:
            return False, f"Ошибка отправки задания: {response.status_code} - {response.text}"
            
    except Exception as e:
        return False, f"Ошибка отправки задания: {str(e)}"
