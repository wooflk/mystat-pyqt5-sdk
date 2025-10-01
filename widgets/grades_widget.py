from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

class GradesWidget(QWidget):
    
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.table = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("Оценки")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: 700; 
            color: #2c3e50;
            padding: 20px 0px;
        """)
        layout.addWidget(title)
        
        self.table = self.create_grades_table()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
    def create_grades_table(self):
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Дата", "Предмет", "Преподаватель", "Оценка"])
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
    
    def update_data(self, marks_data):
        if not marks_data or not self.table:
            return
        
        self.table.setRowCount(0)
        
        for i, mark in enumerate(marks_data):
            self.table.insertRow(i)
            if isinstance(mark, dict):
                self.table.setItem(i, 0, QTableWidgetItem(str(mark.get('mark_date', ''))))
                self.table.setItem(i, 1, QTableWidgetItem(str(mark.get('name_spec', ''))))
                self.table.setItem(i, 2, QTableWidgetItem(str(mark.get('fio_teach', ''))))
                self.table.setItem(i, 3, QTableWidgetItem(str(mark.get('mark', ''))))
        
        self.table.resizeColumnsToContents()
        
