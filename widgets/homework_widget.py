from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QScrollArea, 
                             QHBoxLayout, QMessageBox, QComboBox, QFrame, QGridLayout)
from PyQt5.QtCore import Qt
from datetime import datetime
from .homework_detail_window import HomeworkDetailWindow

class HomeworkWidget(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.homework_data = None
        self.subjects = set()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        title = QLabel("Домашние задания")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: 700; 
            color: #2c3e50;
            padding: 20px 0px;
        """)
        layout.addWidget(title)
        
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
        self.subject_filter = QComboBox()
        self.subject_filter.addItem("Предмет")
        self.subject_filter.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 1px solid #e1e8ed;
                border-radius: 8px;
                padding: 8px 12px;
                font-size: 14px;
                min-width: 150px;
                color: #2c3e50;
            }
            QComboBox:hover {
                background-color: white;
                border-color: #6C59F5;
                color: #2c3e50;
            }
            QComboBox::drop-down {
                border: none;
                width: 20px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #7f8c8d;
                margin-right: 5px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                border: 1px solid #e1e8ed;
                border-radius: 8px;
                selection-background-color: #6C59F5;
                color: #2c3e50;
            }
            QComboBox QAbstractItemView::item {
                color: #2c3e50;
                padding: 8px 12px;
                background-color: white;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #f8f9fa;
                color: #2c3e50;
            }
            QComboBox QAbstractItemView::item:selected {
                background-color: #6C59F5;
                color: white;
            }
        """)
        self.subject_filter.currentTextChanged.connect(self.filter_by_subject)
        filter_layout.addWidget(self.subject_filter)
        
        self.task_count_label = QLabel("Всего задач: 0")
        self.task_count_label.setStyleSheet("""
            font-size: 16px;
            color: #7f8c8d;
            font-weight: 500;
        """)
        filter_layout.addWidget(self.task_count_label)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        """)
        
        self.cards_container = QWidget()
        self.cards_layout = QVBoxLayout()
        self.cards_layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout.setSpacing(30)
        self.cards_container.setLayout(self.cards_layout)
        
        self.scroll_area.setWidget(self.cards_container)
        layout.addWidget(self.scroll_area)
        
        self.setLayout(layout)
        
    
    def create_homework_card(self, homework):
        card = QFrame()
        card.setMinimumHeight(120)
        card.setStyleSheet("""
            QFrame {
                background-color: white;
                border: 1px solid #e1e8ed;
                border-radius: 12px;
                margin: 5px;
            }
            QFrame:hover {
                border-color: #6C59F5;
                background-color: #f8f9fa;
            }
        """)
        
        card.setCursor(Qt.PointingHandCursor)
        
        card.mousePressEvent = lambda event: self.open_homework_detail(homework)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(8)
        
        task_type = QLabel("САМОСТОЯТЕЛЬНАЯ РАБОТА")
        task_type.setStyleSheet("""
            color: #7f8c8d;
            font-size: 11px;
            font-weight: 500;
            text-transform: uppercase;
        """)
        task_type.setWordWrap(True)
        layout.addWidget(task_type)
        
        subject = homework.get('name_spec', 'Не указан')
        subject_label = QLabel(subject)
        subject_label.setStyleSheet("""
            color: #2c3e50;
            font-size: 14px;
            font-weight: 600;
        """)
        subject_label.setWordWrap(True)
        subject_label.setMaximumHeight(35)
        subject_label.setAlignment(Qt.AlignTop)
        layout.addWidget(subject_label)
        
        theme = homework.get('theme', 'Без темы')
        title = QLabel(theme)
        title.setStyleSheet("""
            color: #2c3e50;
            font-size: 13px;
            font-weight: 500;
        """)
        title.setWordWrap(True)
        title.setMaximumHeight(50)
        title.setAlignment(Qt.AlignTop)
        layout.addWidget(title)
        
        date_status_layout = QHBoxLayout()
        date_status_layout.setSpacing(10)
        
        completion_time = homework.get('completion_time', '')
        date_text = completion_time if completion_time else 'Не указан'
        date_label = QLabel(date_text)
        date_label.setStyleSheet("""
            color: #7f8c8d;
            font-size: 12px;
        """)
        date_status_layout.addWidget(date_label)
 
        status_text, status_color = self.get_status_info(homework)
        status_label = QLabel(status_text)
        status_label.setStyleSheet(f"""
            color: {status_color};
            font-size: 12px;
            font-weight: 600;
        """)
        status_label.setWordWrap(True)
        date_status_layout.addWidget(status_label)
        
        date_status_layout.addStretch()
        layout.addLayout(date_status_layout)
        
        if homework.get('has_comments', False):
            notification_layout = QHBoxLayout()
            notification_layout.setAlignment(Qt.AlignRight)
            
            count_label = QLabel("1")
            count_label.setStyleSheet("""
                background-color: #6C59F5;
                color: white;
                border-radius: 8px;
                padding: 1px 4px;
                font-size: 10px;
                font-weight: 600;
                min-width: 12px;
                text-align: center;
        """)
            count_label.setAlignment(Qt.AlignCenter)
            notification_layout.addWidget(count_label)
            
            layout.addLayout(notification_layout)
        
        card.setLayout(layout)
        
        return card
    
    def update_data(self, homework_data):
        if not homework_data:
            return
        
        self.homework_data = homework_data
        
        for i in reversed(range(self.cards_layout.count())):
            self.cards_layout.itemAt(i).widget().setParent(None)
        
        self.subjects.clear()
        self.subject_filter.blockSignals(True)
        self.subject_filter.clear()
        self.subject_filter.addItem("Предмет")
        self.subject_filter.blockSignals(False)
        
        if isinstance(homework_data, dict) and "data" in homework_data:
            for homework in homework_data["data"]:
                subject = homework.get('name_spec', 'Не указан')
                if subject not in self.subjects:
                    self.subjects.add(subject)
                    self.subject_filter.addItem(subject)
            
            self.display_all_homework(homework_data["data"])
    
    
    def get_status_info(self, homework):
        completion_time = homework.get('completion_time', '')
        status = homework.get('status', 0)
        
        if not completion_time:
            return "Не указан", "#7f8c8d"
        
        try:
            if '.' in completion_time:
                day, month, year = completion_time.split('.')
                due_date = datetime(int(year), int(month), int(day))
                today = datetime.now()
                days_diff = (due_date - today).days
                
                if days_diff < 0:
                    return f"Просрочено: {abs(days_diff)} дней", "#F75325"
                elif days_diff == 0:
                    return "Сегодня", "#f39c12"
                else:
                    return f"В дедлайн: {days_diff} дней", "#27ae60"
            else:
                return "Не указан", "#7f8c8d"
        except:
            return "Не указан", "#7f8c8d"
    
    def filter_by_subject(self, subject):
        if subject == "Предмет" or not self.homework_data:
            if isinstance(self.homework_data, dict) and "data" in self.homework_data:
                self.display_all_homework(self.homework_data["data"])
            return
        
        if isinstance(self.homework_data, dict) and "data" in self.homework_data:
            filtered_homework = [hw for hw in self.homework_data["data"] 
                               if hw.get('name_spec', 'Не указан') == subject]
            self.display_all_homework(filtered_homework)
    
    def display_all_homework(self, homework_list):
        if not homework_list:
            return
        
        for i in reversed(range(self.cards_layout.count())):
            self.cards_layout.itemAt(i).widget().setParent(None)
        
        main_widget = QWidget()
        main_layout = QGridLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setRowMinimumHeight(0, 130)
        
        for i, homework in enumerate(homework_list):
            row = i // 4
            col = i % 4
            
            card = self.create_homework_card(homework)
            main_layout.addWidget(card, row, col)
        
        main_widget.setLayout(main_layout)
        self.cards_layout.addWidget(main_widget)
        
        self.task_count_label.setText(f"Всего задач: {len(homework_list)}")
    
    
    def open_homework_detail(self, homework_data):
        detail_window = HomeworkDetailWindow(homework_data, self)
        detail_window.client = self.client
        detail_window.homework_submitted.connect(self.on_homework_submitted)
        detail_window.exec_()
    
    def on_homework_submitted(self, homework_data):
        QMessageBox.information(self, "Успех", "Задание отправлено на проверку!")
    
    def refresh_data(self):
        try:
            homework_data = self.client.homework()
            if homework_data:
                self.update_data(homework_data)
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось обновить данные: {e}")
