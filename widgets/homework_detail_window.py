from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QTextEdit, QFrame, QFileDialog, 
                             QMessageBox, QScrollArea, QWidget)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QPixmap, QPainter, QColor
import os

class HomeworkDetailWindow(QDialog):
    homework_submitted = pyqtSignal(dict)
    
    def __init__(self, homework_data, parent=None):
        super().__init__(parent)
        self.homework_data = homework_data
        self.selected_file_path = None
        self.client = None
        self.setWindowTitle("Детали задания")
        self.setMinimumSize(600, 700)
        self.resize(800, 800)
        self.setModal(True)
        self.init_ui()
        
    def init_ui(self):
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        close_btn = QPushButton("✕")
        close_btn.setFixedSize(30, 30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 1px solid #e1e8ed;
                border-radius: 15px;
                font-size: 14px;
                color: #6c757d;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                color: #495057;
            }
        """)
        close_btn.clicked.connect(self.close)
        
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 20, 20, 10)
        header_layout.addStretch()
        header_layout.addWidget(close_btn)
        main_layout.addLayout(header_layout)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(20, 0, 20, 20)
        content_layout.setSpacing(20)
        
        self.create_homework_info(content_layout)
        
        self.create_open_task_button(content_layout)
        
        self.create_deadline_section(content_layout)
        
        self.create_submission_section(content_layout)
        
        content_widget.setLayout(content_layout)
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        self.setLayout(main_layout)
        
    def create_homework_info(self, parent_layout):
        date_subject_layout = QHBoxLayout()
        
        date = self.homework_data.get('completion_time', 'Не указан')
        date_label = QLabel(date)
        date_label.setStyleSheet("""
            color: #6c757d;
            font-size: 14px;
            font-weight: 500;
        """)
        date_subject_layout.addWidget(date_label)
        
        subject = self.homework_data.get('name_spec', 'Не указан')
        subject_label = QLabel(subject)
        subject_label.setStyleSheet("""
            color: #6c757d;
            font-size: 14px;
            font-weight: 500;
        """)
        date_subject_layout.addStretch()
        date_subject_layout.addWidget(subject_label)
        
        parent_layout.addLayout(date_subject_layout)
        
        theme = self.homework_data.get('theme', 'Без темы')
        title_label = QLabel(theme)
        title_label.setStyleSheet("""
            color: #2c3e50;
            font-size: 24px;
            font-weight: 700;
            margin: 10px 0px;
        """)
        title_label.setWordWrap(True)
        parent_layout.addWidget(title_label)
        
    def create_open_task_button(self, parent_layout):
        open_btn = QPushButton("Открыть задачу")
        open_btn.setFixedHeight(50)
        open_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C59F5;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
                padding: 0px 20px;
            }
            QPushButton:hover {
                background-color: #5A4AE8;
            }
            QPushButton:pressed {
                background-color: #4A3BD1;
            }
        """)
        open_btn.clicked.connect(self.open_task_file)
        parent_layout.addWidget(open_btn)
        
    def create_deadline_section(self, parent_layout):
        deadline_frame = QFrame()
        deadline_frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border: 1px solid #e9ecef;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        
        deadline_layout = QHBoxLayout()
        deadline_layout.setContentsMargins(0, 0, 0, 0)
        
        deadline_info_layout = QHBoxLayout()
        deadline_info_layout.setSpacing(10)
        
        deadline_date = self.homework_data.get('completion_time', 'Не указан')
        deadline_text = QLabel(f"Дедлайн: {deadline_date}")
        deadline_text.setStyleSheet("""
            color: #2c3e50;
            font-size: 14px;
            font-weight: 500;
        """)
        deadline_info_layout.addWidget(deadline_text)
        
        deadline_layout.addLayout(deadline_info_layout)
        deadline_layout.addStretch()
        
        days_left = self.calculate_days_left()
        days_label = QLabel(f"{days_left} дней")
        days_label.setStyleSheet("""
            color: #6c757d;
            font-size: 14px;
            font-weight: 500;
        """)
        deadline_layout.addWidget(days_label)
        
        deadline_frame.setLayout(deadline_layout)
        parent_layout.addWidget(deadline_frame)
        
    def create_submission_section(self, parent_layout):
        submission_title = QLabel("Отправить на проверку")
        submission_title.setStyleSheet("""
            color: #2c3e50;
            font-size: 18px;
            font-weight: 700;
            margin: 20px 0px 10px 0px;
        """)
        parent_layout.addWidget(submission_title)
        
        submission_frame = QFrame()
        submission_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 2px dashed #dee2e6;
                border-radius: 12px;
                padding: 15px;
            }
        """)
        submission_frame.setMinimumHeight(120)
        
        submission_layout = QVBoxLayout()
        submission_layout.setSpacing(15)
        
        file_upload_layout = QVBoxLayout()
        file_upload_layout.setSpacing(8)
        
        select_file_btn = QPushButton("Выбрать файл")
        select_file_btn.setFixedHeight(35)
        select_file_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                color: #495057;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                border-color: #adb5bd;
            }
        """)
        select_file_btn.clicked.connect(self.select_file)
        file_upload_layout.addWidget(select_file_btn)
        
        self.selected_file_label = QLabel("")
        self.selected_file_label.setStyleSheet("""
            color: #27ae60;
            font-size: 12px;
            font-weight: 500;
        """)
        self.selected_file_label.setAlignment(Qt.AlignCenter)
        file_upload_layout.addWidget(self.selected_file_label)
        
        submission_layout.addLayout(file_upload_layout)
        
        separator = QFrame()
        separator.setFrameShape(QFrame.HLine)
        separator.setStyleSheet("color: #dee2e6;")
        submission_layout.addWidget(separator)
        
        self.text_input = QTextEdit()
        self.text_input.setPlaceholderText("Введите текст")
        self.text_input.setMinimumHeight(100)
        self.text_input.setMaximumHeight(250)
        self.text_input.setStyleSheet("""
            QTextEdit {
                border: 1px solid #dee2e6;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                background-color: white;
            }
            QTextEdit:focus {
                border-color: #6C59F5;
            }
        """)
        submission_layout.addWidget(self.text_input)
        
        submission_frame.setLayout(submission_layout)
        parent_layout.addWidget(submission_frame)
        
        submit_btn = QPushButton("Отправить")
        submit_btn.setFixedHeight(50)
        submit_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C59F5;
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 16px;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #5A4AE8;
            }
            QPushButton:pressed {
                background-color: #4A3BD1;
            }
        """)
        submit_btn.clicked.connect(self.submit_homework)
        parent_layout.addWidget(submit_btn)
        
    def calculate_days_left(self):
        completion_time = self.homework_data.get('completion_time', '')
        
        if not completion_time:
            return "Не указан"
        
        try:
            from datetime import datetime

            date_formats = [
                '%d.%m.%Y',
                '%Y-%m-%d',
                '%d/%m/%Y',
            ]
            
            due_date = None
            for fmt in date_formats:
                try:
                    due_date = datetime.strptime(completion_time, fmt)
                    break
                except ValueError:
                    continue
            
            if due_date is None:
                if '.' in completion_time:
                    parts = completion_time.split('.')
                    if len(parts) == 3:
                        day, month, year = parts
                        due_date = datetime(int(year), int(month), int(day))
            
            if due_date:
                today = datetime.now()
                days_diff = (due_date - today).days
                
                if days_diff > 0:
                    return f"{days_diff} дней"
                elif days_diff == 0:
                    return "Сегодня"
                else:
                    return f"Просрочено на {abs(days_diff)} дней"
            else:
                return "Не указан"
                
        except Exception as e:
            print(f"Ошибка парсинга даты '{completion_time}': {e}")
            return "Не указан"
    
    
    def open_task_file(self):
        file_url = self.homework_data.get('file_path', '')
        if not file_url:
            QMessageBox.warning(self, "Предупреждение", "Файл задания не найден")
            return
        
        if not self.client:
            QMessageBox.warning(self, "Ошибка", "Нет подключения к API")
            return
        
        self.download_file(file_url, self.homework_data.get('theme', 'Задание'))
    
    def download_file(self, file_url, theme):
        save_dir = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения файла")
        if not save_dir:
            return
        
        safe_theme = "".join(c for c in theme if c.isalnum() or c in (' ', '-', '_')).rstrip()
        file_extension = self.get_file_extension(file_url)
        filename = f"{safe_theme}{file_extension}"
        save_path = os.path.join(save_dir, filename)
        
        success, message = self.client.download_homework_file(file_url, save_path)
        
        if success:
            QMessageBox.information(self, "Успех", message)
        else:
            QMessageBox.critical(self, "Ошибка", message)
    
    def get_file_extension(self, url):
        """Определяет расширение файла по URL"""
        try:
            if '.' in url:
                extension = url.split('.')[-1].split('?')[0]
                if len(extension) <= 5:
                    return f".{extension}"
        except:
            pass
        return ".pdf"
    
    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Выберите файл для отправки",
            "",
            "Все файлы (*.*)"
        )
        
        if file_path:
            self.selected_file_path = file_path
            file_name = os.path.basename(file_path)
            self.selected_file_label.setText(f"Выбран файл: {file_name}")
    
    def submit_homework(self):
        if not self.selected_file_path and not self.text_input.toPlainText().strip():
            QMessageBox.warning(self, "Предупреждение", "Выберите файл или введите текст")
            return
        
        if not self.client:
            QMessageBox.warning(self, "Ошибка", "Нет подключения к API")
            return
        
        homework_id = self.homework_data.get('id')
        if not homework_id:
            QMessageBox.warning(self, "Ошибка", "ID задания не найден")
            return
        
        try:
            file_url = None
            answer_text = self.text_input.toPlainText().strip() or None
            
            success, message = self.client.check_token_validity()
            if not success:
                QMessageBox.critical(self, "Ошибка авторизации", f"Токен недействителен: {message}")
                return
            
            if self.selected_file_path:
                success, token_data = self.client.get_file_token()
                if not success:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось получить create-token: {token_data}")
                    return
                
                file_token = token_data.get('token', '')
                homework_dir_id = token_data.get('homework_dir_id', '')
                
                if not file_token or not homework_dir_id:
                    QMessageBox.critical(self, "Ошибка", "Create-token или директория пусты")
                    return
                
                success, result = self.client.upload_file_to_storage(self.selected_file_path, file_token, homework_dir_id)
                if not success:
                    QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить файл: {result}")
                    return
                
                file_url = result
                print(f"Получен URL файла: {file_url}")
            
            success, message = self.client.submit_homework(homework_id, file_url, answer_text)
            
            if success:
                QMessageBox.information(self, "Успех", message)
                self.homework_submitted.emit(self.homework_data)
                self.close()
            else:
                QMessageBox.critical(self, "Ошибка", message)
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Произошла ошибка: {str(e)}")
