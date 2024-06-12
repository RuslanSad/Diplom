import sys
from PyQt5.QtWidgets import (
    QApplication,
    QDateEdit,
    QComboBox,
    QMainWindow,
    QTabWidget,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
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
        self.setup_zakazi_tab(supplier_products_tab)

        our_products_tab = QWidget()
        self.setup_dostavki_tab(our_products_tab)

        workers = QWidget()
        self.setup_workers_tab(workers)

        dostavshiki = QWidget()
        self.setup_dostavshiki_tab(dostavshiki)

        self.tab_widget.addTab(suppliers_tab, "Склад")
        self.tab_widget.addTab(workers, "Сотрудники")
        self.tab_widget.addTab(dostavshiki, "Поставщики")
        self.tab_widget.addTab(our_products_tab, "Поставки")
        self.tab_widget.addTab(supplier_products_tab, "Заказы")

        self.setCentralWidget(self.tab_widget)

    def setup_suppliers_tab(self, tab):
        def add_item():
            row = suppliers_model.rowCount()
            suppliers_model.insertRow(row)

        def delete_item():
            selected_index = suppliers_table_view.selectedIndexes()
            if len(selected_index) > 0:
                row = selected_index[0].row()
                suppliers_model.removeRow(row)
                suppliers_model.select()

        def apply_filter():
            filter_text = filter_line_edit.text()
            suppliers_model.setFilter("наименование LIKE '%{}%'".format(filter_text))
            suppliers_model.select()

        layout = QVBoxLayout()
        suppliers_model = QSqlTableModel()
        suppliers_model.setTable("Товары")
        suppliers_model.select()

        suppliers_table_view = QTableView()
        suppliers_table_view.setModel(suppliers_model)

        username_label = QLabel("Введите название товара: ")
        filter_line_edit = QLineEdit()
        filter_button = QPushButton("Применить фильтр")

        layout.addWidget(username_label)
        layout.addWidget(filter_line_edit)
        layout.addWidget(filter_button)
        layout.addWidget(suppliers_table_view)

        add_button = QPushButton("Добавить")
        delete_button = QPushButton("Удалить")

        add_button.clicked.connect(add_item)
        delete_button.clicked.connect(delete_item)
        filter_button.clicked.connect(apply_filter)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)

        layout.addLayout(buttons_layout)
        tab.setLayout(layout)

    def setup_workers_tab(self, tab):
        def add_item():
            row = supplier_workers_model.rowCount()
            supplier_workers_model.insertRow(row)

        def delete_item():
            selected_index = supplier_workers_table_view.selectedIndexes()
            if len(selected_index) > 0:
                row = selected_index[0].row()
                supplier_workers_model.removeRow(row)
                supplier_workers_model.select()

        layout = QVBoxLayout()
        supplier_workers_model = QSqlTableModel()
        supplier_workers_model.setTable("Сотрудники")
        supplier_workers_model.select()

        supplier_workers_table_view = QTableView()
        supplier_workers_table_view.setModel(supplier_workers_model)

        layout.addWidget(supplier_workers_table_view)
        add_button = QPushButton("Добавить")
        delete_button = QPushButton("Удалить")

        add_button.clicked.connect(add_item)
        delete_button.clicked.connect(delete_item)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)

        layout.addLayout(buttons_layout)

        tab.setLayout(layout)

    def setup_dostavshiki_tab(self, tab):
        def add_item():
            row = supplier_posstavshiki_model.rowCount()
            supplier_posstavshiki_model.insertRow(row)

        def delete_item():
            selected_index = supplier_products_table_view.selectedIndexes()
            if len(selected_index) > 0:
                row = selected_index[0].row()
                supplier_posstavshiki_model.removeRow(row)
                supplier_posstavshiki_model.select()

        layout = QVBoxLayout()
        supplier_posstavshiki_model = QSqlTableModel()
        supplier_posstavshiki_model.setTable("Поставщики")
        supplier_posstavshiki_model.select()

        supplier_products_table_view = QTableView()
        supplier_products_table_view.setModel(supplier_posstavshiki_model)

        layout.addWidget(supplier_products_table_view)
        add_button = QPushButton("Добавить")
        delete_button = QPushButton("Удалить")

        add_button.clicked.connect(add_item)
        delete_button.clicked.connect(delete_item)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)

        layout.addLayout(buttons_layout)

        tab.setLayout(layout)

    def setup_dostavki_tab(self, tab):
        def add_item():
            row = supplier_products_model.rowCount()
            supplier_products_model.insertRow(row)

        def delete_item():
            selected_index = supplier_products_table_view.selectedIndexes()
            if len(selected_index) > 0:
                row = selected_index[0].row()
                supplier_products_model.removeRow(row)
                supplier_products_model.select()

        def filter_data():
            filter_date = date_edit.date().toPyDate()
            filter_status = status_combo.currentText()
            supplier_products_model.setFilter(
                f"дата_поставки = '{filter_date}' AND статус = '{filter_status}'"
            )
            supplier_products_model.select()

        layout = QVBoxLayout()

        supplier_products_model = QSqlTableModel()
        supplier_products_model.setTable("Поставки")
        supplier_products_model.select()

        supplier_products_table_view = QTableView()
        supplier_products_table_view.setModel(supplier_products_model)

        layout.addWidget(supplier_products_table_view)

        add_button = QPushButton("Добавить")
        delete_button = QPushButton("Удалить")
        filter_button = QPushButton("Фильтр")

        add_button.clicked.connect(add_item)
        delete_button.clicked.connect(delete_item)
        filter_button.clicked.connect(filter_data)

        date_edit = QDateEdit()
        status_combo = QComboBox()
        status_combo.addItems(["доставлено", "в пути", "отменено"])

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addWidget(date_edit)
        buttons_layout.addWidget(status_combo)
        buttons_layout.addWidget(filter_button)

        layout.addLayout(buttons_layout)
        tab.setLayout(layout)

    def setup_zakazi_tab(self, tab):
        def add_item():
            row = our_products_model.rowCount()
            our_products_model.insertRow(row)

        def delete_item():
            selected_index = our_our_products_table_view.selectedIndexes()
            if len(selected_index) > 0:
                row = selected_index[0].row()
                our_products_model.removeRow(row)
                our_products_model.select()

        def filter_data():
            filter_date = date_edit.date().toPyDate()
            our_products_model.setFilter(f"дата_заказа = '{filter_date}'")
            our_products_model.select()

        layout = QVBoxLayout()

        our_products_model = QSqlTableModel()
        our_products_model.setTable("Заказы")
        our_products_model.select()

        our_our_products_table_view = QTableView()
        our_our_products_table_view.setModel(our_products_model)

        layout.addWidget(our_our_products_table_view)
        add_button = QPushButton("Добавить")
        delete_button = QPushButton("Удалить")
        filter_button = QPushButton("Фильтр")

        add_button.clicked.connect(add_item)
        delete_button.clicked.connect(delete_item)
        filter_button.clicked.connect(filter_data)

        date_edit = QDateEdit()
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(add_button)
        buttons_layout.addWidget(delete_button)
        buttons_layout.addWidget(date_edit)
        buttons_layout.addWidget(filter_button)
        layout.addLayout(buttons_layout)
        tab.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("warehouse.db")
    if not db.open():
        print("Cannot open database")
        sys.exit(1)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
