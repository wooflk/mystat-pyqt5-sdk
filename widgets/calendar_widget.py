from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QCalendarWidget, QListWidget, 
                             QListWidgetItem, QFrame, QScrollArea)
from PyQt5.QtCore import Qt, QDate, QTimer
from PyQt5.QtGui import QFont, QPalette, QColor
from datetime import datetime, timedelta
import json

class CalendarWidget(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.schedule_data = []
        self.homework_data = []
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("Календарь")
        title.setStyleSheet("""
            font-size: 28px; 
            font-weight: 700; 
            color: #2c3e50;
            padding: 10px 0px;
            margin-bottom: 10px;
        """)
        layout.addWidget(title)
        
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)
        
        calendar_section = self.create_calendar_section()
        content_layout.addWidget(calendar_section, 2)
        
        events_section = self.create_events_section()
        content_layout.addWidget(events_section, 1)
        
        layout.addLayout(content_layout)
        self.setLayout(layout)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_current_date)
        self.timer.start(60000) 
        
    def create_calendar_section(self):
        calendar_frame = QFrame()
        calendar_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e1e8ed;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        self.calendar = QCalendarWidget()
        self.calendar.setStyleSheet("""
            QCalendarWidget {
                background-color: white;
                border: 1px solid #e1e8ed;
                border-radius: 8px;
            }
            QCalendarWidget QWidget {
                alternate-background-color: #f8f9fa;
            }
            QCalendarWidget QAbstractItemView:enabled {
                background-color: white;
                selection-background-color: #6C59F5;
                selection-color: white;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #bdc3c7;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #6C59F5;
                border-radius: 8px 8px 0px 0px;
            }
            QCalendarWidget QToolButton {
                background-color: transparent;
                color: white;
                font-weight: bold;
                font-size: 14px;
                padding: 8px;
                border: none;
            }
            QCalendarWidget QToolButton:hover {
                background-color: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
            }
            QCalendarWidget QToolButton:pressed {
                background-color: rgba(255, 255, 255, 0.3);
            }
            QCalendarWidget QSpinBox {
                background-color: transparent;
                color: white;
                font-weight: bold;
                font-size: 16px;
                border: none;
                padding: 4px;
            }
            QCalendarWidget QSpinBox::up-button, QCalendarWidget QSpinBox::down-button {
                background-color: transparent;
                border: none;
                width: 0px;
            }
            QCalendarWidget QWidget#qt_calendar_calendarview {
                background-color: white;
            }
            QCalendarWidget QAbstractItemView {
                selection-background-color: #6C59F5;
                selection-color: white;
                border: none;
            }
            QCalendarWidget QAbstractItemView:item {
                padding: 8px;
                border: none;
            }
            QCalendarWidget QAbstractItemView:item:selected {
                background-color: #6C59F5;
                color: white;
                border-radius: 4px;
            }
            QCalendarWidget QAbstractItemView:item:hover {
                background-color: #ecf0f1;
                border-radius: 4px;
            }
        """)
        
        self.calendar.selectionChanged.connect(self.on_date_selected)
        
        layout.addWidget(self.calendar)
        
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(10)
        
        self.today_btn = QPushButton("Сегодня")
        self.today_btn.setStyleSheet("""
            QPushButton {
                background-color: #6C59F5;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 600;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #5A4AE8;
            }
        """)
        self.today_btn.clicked.connect(self.go_to_today)
        
        self.prev_week_btn = QPushButton("◀ Неделя")
        self.next_week_btn = QPushButton("Неделя ▶")
        
        for btn in [self.prev_week_btn, self.next_week_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #ecf0f1;
                    color: #2c3e50;
                    border: none;
                    border-radius: 6px;
                    padding: 8px 12px;
                    font-weight: 600;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #bdc3c7;
                }
            """)
        
        self.prev_week_btn.clicked.connect(self.go_to_previous_week)
        self.next_week_btn.clicked.connect(self.go_to_next_week)
        
        nav_layout.addWidget(self.today_btn)
        nav_layout.addStretch()
        nav_layout.addWidget(self.prev_week_btn)
        nav_layout.addWidget(self.next_week_btn)
        
        layout.addLayout(nav_layout)
        calendar_frame.setLayout(layout)
        
        return calendar_frame
        
    def create_events_section(self):
        events_frame = QFrame()
        events_frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e1e8ed;
                border-radius: 12px;
                padding: 20px;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        events_title = QLabel("События дня")
        events_title.setStyleSheet("""
            font-size: 18px; 
            font-weight: 600; 
            color: #2c3e50;
            padding: 5px 0px;
        """)
        layout.addWidget(events_title)
        
        self.selected_date_label = QLabel()
        self.selected_date_label.setStyleSheet("""
            font-size: 14px; 
            color: #7f8c8d;
            padding: 5px 0px;
        """)
        layout.addWidget(self.selected_date_label)
        
        self.events_list = QListWidget()
        self.events_list.setStyleSheet("""
            QListWidget {
                background-color: #f8f9fa;
                border: 1px solid #e1e8ed;
                border-radius: 8px;
                padding: 10px;
            }
            QListWidget::item {
                background-color: white;
                border: 1px solid #e1e8ed;
                border-radius: 6px;
                padding: 12px;
                margin: 4px 0px;
            }
            QListWidget::item:hover {
                background-color: #ecf0f1;
                border-color: #6C59F5;
            }
            QListWidget::item:selected {
                background-color: #6C59F5;
                color: white;
                border-color: #5A4AE8;
            }
        """)
        layout.addWidget(self.events_list)
        
        self.stats_label = QLabel()
        self.stats_label.setStyleSheet("""
            font-size: 12px; 
            color: #7f8c8d;
            padding: 10px 0px;
        """)
        layout.addWidget(self.stats_label)
        
        events_frame.setLayout(layout)
        
        self.on_date_selected()
        
        return events_frame
        
    def on_date_selected(self):
        selected_date = self.calendar.selectedDate()
        self.selected_date_label.setText(selected_date.toString("dddd, dd MMMM yyyy"))
        self.update_events_for_date(selected_date)
        
    def update_events_for_date(self, date):
        self.events_list.clear()
        
        date_str = date.toString("yyyy-MM-dd")
        events_count = 0
        
        if self.schedule_data:
            for schedule in self.schedule_data:
                if isinstance(schedule, dict) and schedule.get('date') == date_str:
                    events_count += 1
                    self.add_schedule_event(schedule)
        
        if self.homework_data and isinstance(self.homework_data, dict) and 'data' in self.homework_data:
            for homework in self.homework_data['data']:
                if isinstance(homework, dict):
                    due_date = homework.get('due_date', '')
                    if due_date and due_date.startswith(date_str):
                        events_count += 1
                        self.add_homework_event(homework)
        
        self.stats_label.setText(f"Найдено событий: {events_count}")
        
        if events_count == 0:
            no_events_item = QListWidgetItem("Нет событий на этот день")
            self.events_list.addItem(no_events_item)
            
    def add_schedule_event(self, schedule):
        item = QListWidgetItem()
        
        started_at = schedule.get('started_at', '')
        finished_at = schedule.get('finished_at', '')
        time_str = f"{started_at} - {finished_at}" if started_at and finished_at else "Время не указано"
        
        subject = schedule.get('subject_name', 'Неизвестный предмет')
        teacher = schedule.get('teacher_name', 'Преподаватель не указан')
        
        item.setText(f"📚 {subject}\n⏰ {time_str}\n👨‍🏫 {teacher}")
        item.setData(Qt.UserRole, {'type': 'schedule', 'data': schedule})
        
        self.events_list.addItem(item)
        
    def add_homework_event(self, homework):
        item = QListWidgetItem()
        
        title = homework.get('title', 'Без названия')
        status = homework.get('status', '')
        
        if 'просрочено' in status.lower() or 'overdue' in status.lower():
            icon = "[ПРОСРОЧЕНО]"
        elif 'выполнено' in status.lower() or 'completed' in status.lower():
            icon = "[ВЫПОЛНЕНО]"
        else:
            icon = "[ЗАДАНИЕ]"
        
        item.setText(f"{icon} {title}\nДомашнее задание")
        item.setData(Qt.UserRole, {'type': 'homework', 'data': homework})
        
        self.events_list.addItem(item)
        
    def go_to_today(self):
        self.calendar.setSelectedDate(QDate.currentDate())
        
    def go_to_previous_week(self):
        current_date = self.calendar.selectedDate()
        new_date = current_date.addDays(-7)
        self.calendar.setSelectedDate(new_date)
        
    def go_to_next_week(self):
        current_date = self.calendar.selectedDate()
        new_date = current_date.addDays(7)
        self.calendar.setSelectedDate(new_date)
        
    def update_current_date(self):
        today = QDate.currentDate()
        if self.calendar.selectedDate() == today:
            self.on_date_selected()
            
    def update_data(self, schedule_data=None, homework_data=None):
        if schedule_data:
            self.schedule_data = schedule_data
        if homework_data:
            self.homework_data = homework_data
         
        self.on_date_selected()
