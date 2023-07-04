import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem, QListView
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5 import QtCore


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SAMP ids")
        self.setMinimumSize(800, 600)
        layout = QVBoxLayout()
        search_layout = QHBoxLayout()

        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Digite o termo de pesquisa")
        self.search_field.returnPressed.connect(self.pesquisar_item)
        search_icon = QIcon("lupa.png")
        self.search_field.addAction(search_icon, QLineEdit.LeadingPosition)

        search_layout.addWidget(self.search_field)
        search_button = QPushButton("Pesquisar")
        search_button.clicked.connect(self.pesquisar_item)
        search_layout.addWidget(search_button)

        layout.addLayout(search_layout)
        self.sidebar = QListView()
        self.sidebar.setMaximumWidth(200)
        self.sidebar.clicked.connect(self.carregar_itens_categoria)
        layout.addWidget(self.sidebar)
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["ID", "Itens"])
        layout.addWidget(self.table)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.model = QStandardItemModel()
        self.sidebar.setModel(self.model)
        crawler_database_file = "dados_crawler.db"
        vehicles_database_file = "dados_crawler.db"
        self.crawler_conn = sqlite3.connect(crawler_database_file)
        self.crawler_cursor = self.crawler_conn.cursor()
        self.vehicles_conn = sqlite3.connect(vehicles_database_file)
        self.vehicles_cursor = self.vehicles_conn.cursor()
        self.preencher_sidebar()

    def preencher_sidebar(self):
        self.model.clear()
        categorias = ["Veículos", "Objetos", "Sons"]
        for categoria in categorias:
            item = QStandardItem(categoria)
            self.model.appendRow(item)

    def carregar_itens_categoria(self, index):
        categoria = self.model.itemFromIndex(index).text()
        if categoria == "Veículos":
            self.vehicles_cursor.execute("SELECT id, name FROM vehicles")
            resultados = self.vehicles_cursor.fetchall()
        elif categoria == "Objetos":
            self.crawler_cursor.execute("SELECT id, nome FROM objetos")
            resultados = self.crawler_cursor.fetchall()
        elif categoria == "Sons":
            self.crawler_cursor.execute("SELECT id, nome FROM sons")
            resultados = self.crawler_cursor.fetchall()

        self.exibir_resultados(resultados)

    def pesquisar_item(self):
        termo = self.search_field.text()

        self.vehicles_cursor.execute("SELECT id, name FROM vehicles WHERE name LIKE ?", ('%' + termo + '%',))
        resultados_veiculos = self.vehicles_cursor.fetchall()

        self.crawler_cursor.execute("SELECT id, nome FROM objetos WHERE nome LIKE ?", ('%' + termo + '%',))
        resultados_objetos = self.crawler_cursor.fetchall()

        self.crawler_cursor.execute("SELECT id, nome FROM sons WHERE nome LIKE ?", ('%' + termo + '%',))
        resultados_sons = self.crawler_cursor.fetchall()

        resultados = resultados_veiculos + resultados_objetos + resultados_sons
        self.exibir_resultados(resultados)

    def exibir_resultados(self, resultados):
        self.table.clearContents()

        total_linhas = len(resultados)
        total_colunas = len(resultados[0]) if resultados else 0
        self.table.setRowCount(total_linhas)
        self.table.setColumnCount(total_colunas)

        for i, resultado in enumerate(resultados):
            for j, valor in enumerate(resultado):
                item = QTableWidgetItem(str(valor))
                self.table.setItem(i, j, item)

    def closeEvent(self, event):
        self.crawler_conn.close()
        self.vehicles_conn.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
