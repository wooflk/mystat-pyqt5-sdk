from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QTableWidget, QTableWidgetItem

class LeaderboardWidget(QWidget):
    def __init__(self, client):
        super().__init__()
        self.client = client
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        title = QLabel("Таблица лидеров")
        title.setStyleSheet("""
            font-size: 24px; 
            font-weight: 700; 
            color: #2c3e50;
            padding: 20px 0px;
        """)
        layout.addWidget(title)
        
        self.table = self.create_leaderboard_table()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
        
    def create_leaderboard_table(self):
        table = QTableWidget()
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Место", "Имя", "Баллы"])
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
    
    def update_data(self, leaderboard_data):
        if not leaderboard_data or not self.table:
            return
        
        self.table.setRowCount(0)
        
        if isinstance(leaderboard_data, dict) and "group" in leaderboard_data and "top" in leaderboard_data["group"]:
            for i, leader in enumerate(leaderboard_data["group"]["top"]):
                self.table.insertRow(i)
                
                self.table.setItem(i, 0, QTableWidgetItem(str(leader.get('position', ''))))
                self.table.setItem(i, 1, QTableWidgetItem(str(leader.get('fio_stud', '-'))))
                self.table.setItem(i, 2, QTableWidgetItem(str(leader.get('amount', 0))))
        
        self.table.resizeColumnsToContents()
        
