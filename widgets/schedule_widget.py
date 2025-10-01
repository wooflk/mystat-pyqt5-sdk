from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

class ScheduleWidget(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("Расписание")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: 700; 
            color: #2c3e50;
            padding: 20px 0px;
        """)
        layout.addWidget(title)
        
        self.table = self.create_schedule_table()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
    def create_schedule_table(self):
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Время", "Предмет", "Преподаватель", "Аудитория"])
        table.setRowCount(0)
        table.horizontalHeader().setStretchLastSection(True)
        
        table.setStyleSheet("""
            QTableWidget {
                background-color: white;
                border: 1px solid #e1e8ed;
                border-radius: 8px;
                gridline-color: #ecf0f1;
                selection-background-color: #6C59F5;
            }
            QTableWidget::item {
                padding: 12px;
                border-bottom: 1px solid #ecf0f1;
            }
            QTableWidget::item:selected {
                background-color: #6C59F5;
                color: white;
            }
            QHeaderView::section {
                background-color: #6C59F5;
                color: white;
                padding: 12px;
                border: none;
                font-weight: 600;
                font-size: 13px;
            }
        """)
        
        return table
    
    def update_data(self, schedule_data):
        if not schedule_data or not self.table:
            return
        
        self.table.setRowCount(0)
        
        if isinstance(schedule_data, list):
            for i, schedule in enumerate(schedule_data):
                self.table.insertRow(i)
                
                started_at = schedule.get('started_at', '')
                finished_at = schedule.get('finished_at', '')
                time_str = f"{started_at} - {finished_at}" if started_at and finished_at else ""
                
                self.table.setItem(i, 0, QTableWidgetItem(str(time_str)))
                self.table.setItem(i, 1, QTableWidgetItem(str(schedule.get('subject_name', ''))))
                self.table.setItem(i, 2, QTableWidgetItem(str(schedule.get('teacher_name', ''))))
                self.table.setItem(i, 3, QTableWidgetItem(""))
        
        self.table.resizeColumnsToContents()
        
