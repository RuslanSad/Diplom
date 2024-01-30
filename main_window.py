import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QMessageBox,
)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("БытХимПром")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget()

        suppliers_tab = QWidget()
        self.setup_suppliers_tab(suppliers_tab)

        supplier_products_tab = QWidget()
        self.setup_supplier_products_tab(supplier_products_tab)

        our_products_tab = QWidget()
        self.setup_our_products_tab(our_products_tab)

        self.tab_widget.addTab(suppliers_tab, "Suppliers")
        self.tab_widget.addTab(supplier_products_tab, "Supplier Products")
        self.tab_widget.addTab(our_products_tab, "Our Products")

        self.setCentralWidget(self.tab_widget)

    def setup_suppliers_tab(self, tab):
        layout = QVBoxLayout()
        # Установка таблицы и модели для поставщиков
        suppliers_model = QSqlTableModel()
        suppliers_model.setTable("suppliers")
        suppliers_model.select()

        suppliers_table_view = QTableView()
        suppliers_table_view.setModel(suppliers_model)

        layout.addWidget(suppliers_table_view)

        tab.setLayout(layout)

    def setup_supplier_products_tab(self, tab):
        layout = QVBoxLayout()
        # Установка таблицы и модели для товаров поставщиков
        supplier_products_model = QSqlTableModel()
        supplier_products_model.setTable("supplier_products")
        supplier_products_model.select()

        supplier_products_table_view = QTableView()
        supplier_products_table_view.setModel(supplier_products_model)

        layout.addWidget(supplier_products_table_view)

        tab.setLayout(layout)

    def setup_our_products_tab(self, tab):
        layout = QVBoxLayout()
        # Установка таблицы и модели для наших товаров
        our_products_model = QSqlTableModel()
        our_products_model.setTable("our_products")
        our_products_model.select()

        our_products_table_view = QTableView()
        our_products_table_view.setModel(our_products_model)

        layout.addWidget(our_products_table_view)

        tab.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Создание подключения к базе данных
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("warehouse.db")  # Укажите путь к вашей базе данных
    if not db.open():
        print("Cannot open database")
        sys.exit(1)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
