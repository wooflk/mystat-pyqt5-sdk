# главное окно PyQt5: сборка интерфейса, логика UIs

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QStackedWidget, 
                             QFrame, QLineEdit, QMessageBox, QTableWidget, QTableWidgetItem,
                             QCalendarWidget)
from PyQt5.QtCore import Qt

from core import SessionLocal
from models import User
from interface.mystat_interface import MystatInterface
from widgets.grades_widget import GradesWidget
from widgets.attendance_widget import AttendanceWidget
from widgets.schedule_widget import ScheduleWidget
from widgets.homework_widget import HomeworkWidget
from widgets.calendar_widget import CalendarWidget

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MyStat - Вход")
        self.setFixedSize(520, 450)
        
        self.setStyleSheet("""
            QWidget { 
                background-color: white;
                color: #333; 
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLineEdit { 
                background-color: white;
                border: 2px solid #ddd;
                border-radius: 8px;
                padding: 12px 16px;
                font-size: 14px;
                color: #333;
                min-height: 20px;
            }
            QLineEdit:focus {
                border: 2px solid #6C59F5;
                background-color: white;
            }
            QPushButton { 
                background-color: #6C59F5;
                color: white; 
                border: none;
                border-radius: 8px;
                padding: 12px 24px; 
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover { 
                background-color: #5A4AE8;
            }
            QPushButton:pressed {
                background-color: #4A3BD1;
            }
        """)
        
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(25)
        layout.setContentsMargins(50, 50, 50, 50)
        
        title = QLabel("MyStat")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 32px; 
            font-weight: bold; 
            color: #2c3e50;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        self.login_input = QLineEdit()
        self.login_input.setPlaceholderText("Логин")
        layout.addWidget(self.login_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Пароль")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)
        
        self.toggle_password_btn = QPushButton("👁 Показать пароль")
        self.toggle_password_btn.setStyleSheet("""
            QPushButton {
                background-color: #f8f9fa;
                border: 2px solid #ddd;
                border-radius: 8px;
                font-size: 14px;
                color: #666;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #e9ecef;
                color: #333;
            }
            QPushButton:pressed {
                background-color: #dee2e6;
            }
        """)
        self.toggle_password_btn.clicked.connect(self.toggle_password_visibility)
        layout.addWidget(self.toggle_password_btn)
        
        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)
        
        self.setLayout(layout)
        
    def toggle_password_visibility(self):
        if self.password_input.echoMode() == QLineEdit.Password:
            self.password_input.setEchoMode(QLineEdit.Normal)
            self.toggle_password_btn.setText("👁 Скрыть пароль")
        else:
            self.password_input.setEchoMode(QLineEdit.Password)
            self.toggle_password_btn.setText("👁 Показать пароль")
        
    def login(self):
        login = self.login_input.text()
        password = self.password_input.text()
        
        if not login or not password:
            QMessageBox.warning(self, "Ошибка", "Введите логин и пароль")
            return
            
        client = MystatInterface(login, password)
        
        if client.authenticate():
            self.save_user_to_db(login, password)
            
            self.main_window = MainWindow(client)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.critical(self, "Ошибка", "Неверный логин или пароль")
    
    def save_user_to_db(self, login, password):
        db = SessionLocal()
        try:
            user = db.query(User).filter_by(login=login).first()
            if not user:
                user = User(login=login, password=password, role="student")
                db.add(user)
                db.commit()
        finally:
            db.close()

class SidebarButton(QPushButton):
    def __init__(self, text, is_active=False):
        super().__init__()
        self.setText(text)
        self.is_active = is_active
        self.setCheckable(True)
        self.setChecked(is_active)
        self.setFixedHeight(50)
        
        self.setStyleSheet("""
            QPushButton { 
                background-color: transparent; 
                border: none; 
                text-align: left; 
                padding: 15px 20px; 
                color: #ecf0f1; 
                font-size: 15px;
                font-weight: 600;
                border-radius: 8px;
                margin: 2px 0px;
            }
            QPushButton:hover { 
                background-color: rgba(255, 255, 255, 0.15);
                color: white;
            }
            QPushButton:checked { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #6C59F5, stop:1 #5A4AE8);
                color: white;
            }
        """)

class CardWidget(QFrame):
    def __init__(self, title, content_widget=None, card_type="default"):
        super().__init__()
        self.setFrameStyle(QFrame.StyledPanel)
        self.card_type = card_type
        self.apply_card_style()
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            font-size: 16px; 
            font-weight: 700; 
            color: #2c3e50;
            padding: 0px;
            margin-bottom: 5px;
        """)
        layout.addWidget(title_label)
        
        if content_widget:
            layout.addWidget(content_widget)
        
        self.setLayout(layout)
        
    def apply_card_style(self):
        base_style = """
            QFrame { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #ffffff, stop:1 #f8f9fa); 
                border: 2px solid #e1e8ed; 
                border-radius: 12px;
            }
        """
        
        if self.card_type == "stat":
            hover_style = """
                QFrame:hover {
                    border: 2px solid #6C59F5;
                }
            """
            self.setStyleSheet(base_style + hover_style)
        else:
            self.setStyleSheet(base_style)

class DashboardWidget(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(25)
        
        header_layout = QHBoxLayout()
        welcome_label = QLabel("Добро пожаловать в MyStat!")
        welcome_label.setStyleSheet("""
            font-size: 28px; 
            font-weight: 700; 
            color: #2c3e50;
            padding: 10px 0px;
        """)
        header_layout.addWidget(welcome_label)
        header_layout.addStretch()
        
        refresh_btn = QPushButton("🔄 Обновить")
        refresh_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C59F5;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: 600;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #5A4AE8;
            }
        """)
        refresh_btn.clicked.connect(self.refresh_data)
        header_layout.addWidget(refresh_btn)
        
        layout.addLayout(header_layout)
        
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(20)
        
        self.tasks_label = QLabel("-")
        self.overdue_label = QLabel("-")
        self.avg_grade_label = QLabel("-")
        self.attendance_label = QLabel("-")
        
        tasks_card = self.create_stat_card("Задания к выполнению", self.tasks_label, "#6C59F5")
        overdue_card = self.create_stat_card("Просрочено", self.overdue_label, "#F75325")
        avg_grade_card = self.create_stat_card("Средний балл", self.avg_grade_label, "#27ae60")
        attendance_card = self.create_stat_card("Посещаемость", self.attendance_label, "#f39c12")
        
        stats_layout.addWidget(tasks_card)
        stats_layout.addWidget(overdue_card)
        stats_layout.addWidget(avg_grade_card)
        stats_layout.addWidget(attendance_card)
        
        layout.addLayout(stats_layout)
        
        content_layout = QHBoxLayout()
        content_layout.setSpacing(25)
        
        left_column = QVBoxLayout()
        left_column.setSpacing(20)
        
        calendar_card = self.create_calendar_card()
        left_column.addWidget(calendar_card)
        
        content_layout.addLayout(left_column, 1)
        
        center_column = QVBoxLayout()
        center_column.setSpacing(20)
        
        leaderboard_card = self.create_table_card("Таблица лидеров", ["Место", "Имя", "Баллы"], "dashboard_leaderboard_table")
        center_column.addWidget(leaderboard_card)
        
        content_layout.addLayout(center_column, 2)
        
        right_column = QVBoxLayout()
        right_column.setSpacing(20)
        
        schedule_card = self.create_schedule_dashboard_card()
        right_column.addWidget(schedule_card)
        
        grades_card = self.create_grades_card()
        right_column.addWidget(grades_card)
        
        content_layout.addLayout(right_column, 2)
        
        layout.addLayout(content_layout)
        self.setLayout(layout)
        
    def create_stat_card(self, title, value_label, color="#6C59F5"):
        card = CardWidget(title, card_type="stat")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        value_label.setStyleSheet(f"""
            font-size: 48px; 
            font-weight: 800; 
            color: {color};
        """)
        value_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(value_label)

        subtitle = QLabel("за последний месяц")
        subtitle.setStyleSheet("""
            font-size: 12px; 
            color: #7f8c8d;
            font-weight: 500;
        """)
        subtitle.setAlignment(Qt.AlignCenter)
        layout.addWidget(subtitle)
        
        card.layout().addLayout(layout)
        return card
    
    
    def create_calendar_card(self):
        card = QFrame()
        card.setStyleSheet("""
            QFrame { 
                background: white; 
                border: 1px solid #e1e8ed; 
                border-radius: 8px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(5, 3, 5, 5)
        layout.setSpacing(0)
        
        
        self.mini_calendar = QCalendarWidget()
        self.mini_calendar.setFixedHeight(280)
        self.mini_calendar.setStyleSheet("""
            QCalendarWidget {
                background: white;
                border: none;
                border-radius: 6px;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background: #3498db;
                border-radius: 6px 6px 0px 0px;
            }
            QCalendarWidget QToolButton {
                background: transparent;
                color: white;
                font-size: 11px;
                padding: 4px;
                border: none;
            }
            QCalendarWidget QSpinBox {
                background: transparent;
                color: white;
                font-size: 12px;
                border: none;
            }
            QCalendarWidget QAbstractItemView:item {
                padding: 4px;
                border: none;
            }
            QCalendarWidget QAbstractItemView:item:selected {
                background: #3498db;
                color: white;
                border-radius: 3px;
            }
        """)
        
        layout.addWidget(self.mini_calendar)
        card.setLayout(layout)
        return card
        
    def create_grades_card(self):
        card = CardWidget("Последние оценки", card_type="default")
        
        self.dashboard_grades_table = QTableWidget()
        self.dashboard_grades_table.setColumnCount(3)
        self.dashboard_grades_table.setHorizontalHeaderLabels(["Предмет", "Оценка", "Дата"])
        self.dashboard_grades_table.setRowCount(0)
        self.dashboard_grades_table.setMaximumHeight(350)
        self.dashboard_grades_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e1e8ed;
                border-radius: 8px;
                gridline-color: #ecf0f1;
                selection-background-color: #3498db;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
                font-size: 13px;
            }
            QTableWidget::item:selected {
                background-color: #6C59F5;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #2c3e50;
                padding: 10px;
                border: none;
                font-weight: 600;
                font-size: 13px;
            }
        """)
        
        card.layout().addWidget(self.dashboard_grades_table)
        return card
        
    def create_schedule_dashboard_card(self):
        card = CardWidget("Ближайшие занятия", card_type="schedule")
        
        self.dashboard_schedule_table = QTableWidget()
        self.dashboard_schedule_table.setColumnCount(3)
        self.dashboard_schedule_table.setHorizontalHeaderLabels(["Время", "Предмет", "Преподаватель"])
        self.dashboard_schedule_table.setRowCount(0)
        self.dashboard_schedule_table.setMaximumHeight(400)
        self.dashboard_schedule_table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e1e8ed;
                border-radius: 8px;
                gridline-color: #ecf0f1;
                selection-background-color: #3498db;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
                font-size: 13px;
            }
            QTableWidget::item:selected {
                background-color: #6C59F5;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #2c3e50;
                padding: 10px;
                border: none;
                font-weight: 600;
                font-size: 13px;
            }
        """)
        
        card.layout().addWidget(self.dashboard_schedule_table)
        return card
        
    def create_table_card(self, title, columns, table_attr):
        card = CardWidget(title)
        card.setMaximumHeight(450)
        
        table = QTableWidget()
        table.setColumnCount(len(columns))
        table.setHorizontalHeaderLabels(columns)
        table.setRowCount(0)
        table.setMaximumHeight(400)
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e1e8ed;
                border-radius: 8px;
                gridline-color: #ecf0f1;
                selection-background-color: #3498db;
            }
            QTableWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ecf0f1;
                font-size: 13px;
            }
            QTableWidget::item:selected {
                background-color: #6C59F5;
                color: white;
            }
            QHeaderView::section {
                background-color: #f8f9fa;
                color: #2c3e50;
                padding: 10px;
                border: none;
                font-weight: 600;
                font-size: 13px;
            }
        """)
        card.layout().addWidget(table)
        
        setattr(self, table_attr, table)
        return card
    
    def update_data(self, dashboard_data):
        if hasattr(self, 'tasks_label'):
            tasks_count = self.count_tasks(dashboard_data.get('homework', []))
            self.tasks_label.setText(str(tasks_count))
        
        if hasattr(self, 'overdue_label'):
            overdue_count = self.count_overdue_tasks(dashboard_data.get('homework', []))
            self.overdue_label.setText(str(overdue_count))
            
        if hasattr(self, 'avg_grade_label'):
            avg_grade = self.calculate_average_grade(dashboard_data.get('grades', []))
            self.avg_grade_label.setText(f"{avg_grade:.1f}")
            
        if hasattr(self, 'attendance_label'):
            attendance = self.calculate_attendance(dashboard_data.get('attendance', []))
            self.attendance_label.setText(f"{attendance}%")
        
        if 'schedule' in dashboard_data:
            self.update_schedule_display(dashboard_data['schedule'])
        
        if hasattr(self, 'dashboard_leaderboard_table') and 'leaderboard' in dashboard_data:
            self.update_dashboard_leaderboard(dashboard_data['leaderboard'])
            
        if hasattr(self, 'dashboard_grades_table') and 'grades' in dashboard_data:
            self.update_dashboard_grades(dashboard_data['grades'])
    
    def update_dashboard_grades(self, grades_data):
        if not grades_data or not self.dashboard_grades_table:
            return
        
        self.dashboard_grades_table.setRowCount(0)
        
        for i, grade in enumerate(grades_data[:8]):
            self.dashboard_grades_table.insertRow(i)
            
            self.dashboard_grades_table.setItem(i, 0, QTableWidgetItem(str(grade.get('name_spec', ''))))
            self.dashboard_grades_table.setItem(i, 1, QTableWidgetItem(str(grade.get('mark', ''))))
            self.dashboard_grades_table.setItem(i, 2, QTableWidgetItem(str(grade.get('mark_date', ''))))
        
        self.dashboard_grades_table.resizeColumnsToContents()
    
    def update_dashboard_leaderboard(self, leaderboard_data):
        if not leaderboard_data or not self.dashboard_leaderboard_table:
            return
        
        self.dashboard_leaderboard_table.setRowCount(0)
        
        if "group" in leaderboard_data and "top" in leaderboard_data["group"]:
            for i, leader in enumerate(leaderboard_data["group"]["top"][:8]):
                self.dashboard_leaderboard_table.insertRow(i)
                
                self.dashboard_leaderboard_table.setItem(i, 0, QTableWidgetItem(str(leader.get('position', ''))))
                self.dashboard_leaderboard_table.setItem(i, 1, QTableWidgetItem(str(leader.get('fio_stud', '-'))))
                self.dashboard_leaderboard_table.setItem(i, 2, QTableWidgetItem(str(leader.get('amount', 0))))
        
        self.dashboard_leaderboard_table.resizeColumnsToContents()
    
    def count_tasks(self, homework_data):
        if not homework_data or not isinstance(homework_data, dict) or "data" not in homework_data:
            return 0
        return len(homework_data["data"])
    
    def count_overdue_tasks(self, homework_data):
        if not homework_data or not isinstance(homework_data, dict) or "data" not in homework_data:
            return 0
        
        overdue_count = 0
        for task in homework_data["data"]:
            status = str(task.get('status', '')).lower()
            if 'просрочено' in status or 'overdue' in status or 'expired' in status:
                overdue_count += 1
        
        return overdue_count
    
    
    
    def update_schedule_display(self, schedule_data):
        if not schedule_data or not hasattr(self, 'dashboard_schedule_table'):
            return
        
        self.dashboard_schedule_table.setRowCount(0)
        
        if isinstance(schedule_data, list):
            for i, schedule in enumerate(schedule_data[:10]):
                self.dashboard_schedule_table.insertRow(i)
                
                started_at = schedule.get('started_at', '')
                finished_at = schedule.get('finished_at', '')
                time_str = f"{started_at} - {finished_at}" if started_at and finished_at else ""
                
                self.dashboard_schedule_table.setItem(i, 0, QTableWidgetItem(str(schedule.get('date', ''))))
                self.dashboard_schedule_table.setItem(i, 1, QTableWidgetItem(str(time_str)))
                self.dashboard_schedule_table.setItem(i, 2, QTableWidgetItem(str(schedule.get('subject_name', ''))))
                self.dashboard_schedule_table.setItem(i, 3, QTableWidgetItem(str(schedule.get('teacher_name', ''))))
        
        self.dashboard_schedule_table.resizeColumnsToContents()
        
    def calculate_average_grade(self, grades_data):
        if not grades_data or not isinstance(grades_data, list):
            return 0.0
            
        total_marks = 0
        count = 0
        
        for grade in grades_data:
            if isinstance(grade, dict) and 'mark' in grade:
                try:
                    mark = float(grade['mark'])
                    if mark > 0:
                        total_marks += mark
                        count += 1
                except (ValueError, TypeError):
                    continue
                    
        return total_marks / count if count > 0 else 0.0
        
    def calculate_attendance(self, attendance_data):
        if not attendance_data or not isinstance(attendance_data, dict):
            return 0
            
        total_classes = attendance_data.get('total_classes', 0)
        attended_classes = attendance_data.get('attended_classes', 0)
        
        if total_classes > 0:
            return int((attended_classes / total_classes) * 100)
        return 0
        
    def refresh_data(self):
        try:
            self.load_dashboard_data()
        except Exception as e:
            print(f"Ошибка обновления данных: {e}")

class MainWindow(QMainWindow):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.setWindowTitle("MyStat")
        self.setMinimumSize(1600, 900)
        self.resize(1600, 900)
        self.setStyleSheet("""
            QMainWindow { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                font-family: 'Segoe UI', Arial, sans-serif;
            }
        """)
        self.init_ui()
        
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        self.content_area = QStackedWidget()
        self.content_area.setStyleSheet("""
            QStackedWidget { 
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                    stop:0 #f8f9fa, stop:1 #e9ecef);
                border-radius: 8px;
            }
        """)
        
        self.dashboard = DashboardWidget(self.client)
        self.grades_widget = GradesWidget(self.client)
        self.attendance_widget = AttendanceWidget(self.client)
        self.schedule_widget = ScheduleWidget(self.client)
        self.homework_widget = HomeworkWidget(self.client)
        self.calendar_widget = CalendarWidget(self.client)
        
        self.content_area.addWidget(self.dashboard)
        self.content_area.addWidget(self.grades_widget)
        self.content_area.addWidget(self.attendance_widget)
        self.content_area.addWidget(self.schedule_widget)
        self.content_area.addWidget(self.homework_widget)
        self.content_area.addWidget(self.calendar_widget)
        
        main_layout.addWidget(self.content_area, 1)
        
        self.setup_navigation(sidebar)
        
        central_widget.setLayout(main_layout)
        
        self.load_data()
    
    def setup_navigation(self, sidebar):
        self.sidebar_buttons = [
            sidebar.findChild(SidebarButton, "dashboard_btn"),
            sidebar.findChild(SidebarButton, "grades_btn"),
            sidebar.findChild(SidebarButton, "attendance_btn"),
            sidebar.findChild(SidebarButton, "schedule_btn"),
            sidebar.findChild(SidebarButton, "homework_btn"),
            sidebar.findChild(SidebarButton, "calendar_btn")
        ]
        
        for i, button in enumerate(self.sidebar_buttons):
            button.clicked.connect(lambda checked, idx=i: self.content_area.setCurrentIndex(idx))
            button.clicked.connect(lambda checked, btn=button: self.update_sidebar_selection(btn))
        
    def load_data(self):
        try:
            token_data = self.client.get_user_info()
            if token_data:
                self.load_dashboard_data()
                self.load_grades_data()
                self.load_attendance_data()
                self.load_schedule_data()
                self.load_homework_data()
                self.load_calendar_data()
                
                self.content_area.setCurrentIndex(0)
                
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
    
    def load_dashboard_data(self):
        try:
            dashboard_data = {}
            
            grades_data = self.client.marks()
            if grades_data:
                dashboard_data['grades'] = grades_data
            
            leaderboard_data = self.client.leaderboard()
            if leaderboard_data:
                dashboard_data['leaderboard'] = leaderboard_data
            
            homework_data = self.client.homework()
            if homework_data:
                dashboard_data['homework'] = homework_data
            
            schedule_data = self.client.schedule()
            if schedule_data:
                dashboard_data['schedule'] = schedule_data
                
            attendance_data = self.client.attendance()
            if attendance_data:
                dashboard_data['attendance'] = attendance_data
            
            self.dashboard.update_data(dashboard_data)
        except Exception as e:
            print(f"Ошибка загрузки дашборда: {e}")
    
    def load_grades_data(self):
        try:
            marks_data = self.client.marks()
            if marks_data:
                self.grades_widget.update_data(marks_data)
        except Exception as e:
            print(f"Ошибка загрузки оценок: {e}")
    
    def load_attendance_data(self):
        try:
            attendance_data = self.client.attendance()
            if attendance_data:
                self.attendance_widget.update_data(attendance_data)
        except Exception as e:
            print(f"Ошибка загрузки посещаемости: {e}")
    
    def load_schedule_data(self):
        try:
            schedule_data = self.client.schedule()
            if schedule_data:
                self.schedule_widget.update_data(schedule_data)
        except Exception as e:
            print(f"Ошибка загрузки расписания: {e}")
    
    def load_homework_data(self):
        try:
            homework_data = self.client.homework()
            if homework_data:
                self.homework_widget.update_data(homework_data)
        except Exception as e:
            print(f"Ошибка загрузки домашних заданий: {e}")
    
    def load_calendar_data(self):
        try:
            schedule_data = self.client.schedule()
            homework_data = self.client.homework()
            if schedule_data or homework_data:
                self.calendar_widget.update_data(schedule_data, homework_data)
        except Exception as e:
            print(f"Ошибка загрузки данных календаря: {e}")
        
    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet("""
            QFrame { 
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #2c3e50, stop:1 #34495e);
                border: none;
                border-right: 2px solid #34495e;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(5)
        
        buttons_data = [
            ("", "dashboard_btn", "Дашборд"),
            ("", "grades_btn", "Оценки"),
            ("", "attendance_btn", "Посещаемость"),
            ("", "schedule_btn", "Расписание"),
            ("", "homework_btn", "Задания"),
            ("", "calendar_btn", "Календарь")
        ]
        
        for icon, name, tooltip in buttons_data:
            btn = SidebarButton(tooltip, name == "dashboard_btn")
            btn.setObjectName(name)
            btn.setToolTip(tooltip)
            layout.addWidget(btn)
        
        layout.addStretch()
        
        logout_btn = QPushButton("Выход")
        logout_btn.setFixedHeight(45)
        logout_btn.setStyleSheet("""
            QPushButton { 
                background-color: #e74c3c;
                color: white; 
                border: none;
                border-radius: 8px;
                font-size: 14px;
                font-weight: 600;
            }
            QPushButton:hover { 
                background-color: #c0392b;
            }
        """)
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        sidebar.setLayout(layout)
        return sidebar
        
    def update_sidebar_selection(self, active_button):
        for button in self.sidebar_buttons:
            button.setChecked(button == active_button)
            
    def logout(self):
        self.close()
        self.login_window = LoginWindow()
        self.login_window.show()

def main():
    import os
    
    qt_plugin_path = r"C:\Users\лунара\AppData\Local\Programs\Python\Python313\Lib\site-packages\PyQt5\Qt5\plugins"
    os.environ["QT_PLUGIN_PATH"] = qt_plugin_path
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(qt_plugin_path, "platforms")
    os.environ["QT_MULTIMEDIA_PREFERRED_PLUGINS"] = "windowsmediafoundation"
    
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    login_window = LoginWindow()
    login_window.show()
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
