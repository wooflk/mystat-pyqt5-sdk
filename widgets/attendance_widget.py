from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

class AttendanceWidget(QWidget):
    
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.table = None
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        title = QLabel("Посещаемость")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: 700; 
            color: #2c3e50;
            padding: 20px 0px;
        """)
        layout.addWidget(title)
        
        self.table = self.create_attendance_table()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
    def create_attendance_table(self):
        table = QTableWidget()
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Дата", "Предмет", "Был", "Тема"])
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
    
    def update_data(self, attendance_data):
        if not attendance_data or not self.table:
            return
        
        self.table.setRowCount(0)
        
        if isinstance(attendance_data, dict) and "data" in attendance_data:
            data = attendance_data["data"]
            row_count = 0
            
            for year, months in data.items():
                for month, days in months.items():
                    for day, info in days.items():
                        for visit in info.get("visits", []):
                            self.table.insertRow(row_count)
                            
                            date = visit.get("date_vizit", f"{year}-{month.zfill(2)}-{day.zfill(2)}")
                            was = visit.get("was", "-")
                            theme = visit.get("theme", "")
                            spec_name = visit.get("spec", {}).get("name_spec", "")
                            
                            self.table.setItem(row_count, 0, QTableWidgetItem(str(date)))
                            self.table.setItem(row_count, 1, QTableWidgetItem(str(spec_name)))
                            self.table.setItem(row_count, 2, QTableWidgetItem(str(was)))
                            self.table.setItem(row_count, 3, QTableWidgetItem(str(theme)))
                            
                            row_count += 1
        
        self.table.resizeColumnsToContents()
        
