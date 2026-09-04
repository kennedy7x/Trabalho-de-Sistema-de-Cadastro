import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QComboBox, 
    QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout,
    QGroupBox, QMessageBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QGridLayout, QScrollArea, QFrame, QSizePolicy,
    QTabWidget, QSpacerItem
)
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont, QIcon, QColor, QPalette, QPixmap, QPainter, QBrush, QLinearGradient

from database import Database
from validators import Validators
from cep_service import CEPService

class PessoaForm(QWidget):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.cep_service = CEPService()
        self.modo_edicao = False
        self.id_editando = None
        self.tabela = None
        self.tabs = None  # <-- ADICIONE ESTA LINHA
        self.init_ui()
        # Carrega a lista APÓS a UI estar pronta
        QTimer.singleShot(100, self.carregar_lista_pessoas)
        
    def init_ui(self):
        self.setWindowTitle("🌟 Sistema de Cadastro de Pessoas")
        
        # Layout responsivo - ajusta tamanho baseado na tela
        screen = QApplication.primaryScreen().availableGeometry()
        width = min(screen.width() - 50, 1200)
        height = min(screen.height() - 50, 800)
        self.resize(width, height)
        self.setMinimumSize(650, 550)
        
        # Aplica estilo global
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', 'Arial', sans-serif;
                background-color: #F0F4F8;
            }
            QTabWidget::pane {
                border: 2px solid #DCE4EC;
                border-radius: 10px;
                background-color: white;
            }
            QTabBar::tab {
                background: #E8EEF2;
                border: none;
                border-radius: 6px 6px 0 0;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 13px;
                color: #2C3E50;
                margin-right: 2px;
                min-width: 150px;
            }
            QTabBar::tab:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B9BD5, stop:1 #4A8BC2);
                color: white;
            }
            QTabBar::tab:hover:!selected {
                background: #D5DDE6;
            }
            QLabel {
                color: #2C3E50;
                font-weight: 500;
            }
            QLineEdit, QComboBox {
                border: 2px solid #DCE4EC;
                border-radius: 6px;
                padding: 6px 10px;
                background-color: white;
                color: #2C3E50;
                font-size: 12px;
                min-height: 20px;
                selection-background-color: #5B9BD5;
                selection-color: white;
            }
            QLineEdit:hover, QComboBox:hover {
                border: 2px solid #5B9BD5;
                background-color: #EBF5FB;
                color: #1A1A1A;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 2px solid #5B9BD5;
                background-color: #F8FBFF;
                color: #1A1A1A;
            }
            QLineEdit:disabled, QComboBox:disabled {
                background-color: #F0F0F0;
                color: #666666;
            }
            QGroupBox {
                border: 2px solid #DCE4EC;
                border-radius: 10px;
                margin-top: 12px;
                padding-top: 12px;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 15px;
                padding: 0 8px 0 8px;
                color: #2C3E50;
                font-weight: bold;
                font-size: 13px;
            }
            QTableWidget {
                border: 2px solid #DCE4EC;
                border-radius: 8px;
                background-color: white;
                gridline-color: #E8EEF2;
            }
            QTableWidget::item {
                padding: 12px 10px;
                color: #2C3E50;
            }
            QTableWidget::item:selected {
                background-color: #5B9BD5;
                color: white;
            }
            QTableWidget::item:hover {
                background-color: #EBF5FB;
                color: #1A1A1A;
            }
            QHeaderView::section {
                background-color: #E8EEF2;
                padding: 8px 10px;
                border: none;
                font-weight: bold;
                color: #2C3E50;
                min-height: 30px;
            }
            QPushButton {
                font-weight: bold;
            }
            QScrollArea {
                background: transparent;
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #2C3E50;
                selection-background-color: #5B9BD5;
                selection-color: white;
                border: 2px solid #DCE4EC;
                border-radius: 4px;
                padding: 4px;
            }
            QComboBox QAbstractItemView::item:hover {
                background-color: #EBF5FB;
                color: #1A1A1A;
            }
        """)
        
        # Layout principal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)
        
        # Cabeçalho
        header_widget = QWidget()
        header_widget.setMinimumHeight(65)
        header_widget.setMaximumHeight(90)
        header_widget.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #2C3E50, stop:0.5 #34495E, stop:1 #2C3E50);
            border-radius: 10px;
        """)
        
        header_layout = QHBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 5, 20, 5)
        
        title_label = QLabel("🌟 Sistema de Cadastro")
        title_label.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: white;")
        header_layout.addWidget(title_label)
        
        subtitle = QLabel("Gerenciamento de Pessoas")
        subtitle.setFont(QFont("Segoe UI", 10))
        subtitle.setStyleSheet("color: #BDC3C7;")
        header_layout.addWidget(subtitle)
        header_layout.addStretch()
        
        self.status_label = QLabel("✅ Pronto")
        self.status_label.setFont(QFont("Segoe UI", 9))
        self.status_label.setStyleSheet("color: #2ECC71; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 12px;")
        header_layout.addWidget(self.status_label)
        
        main_layout.addWidget(header_widget)
        
        # ==================== CRIAR AS ABAS PRIMEIRO ====================
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget {
                background: transparent;
                border: none;
            }
        """)
        
        # ==================== ABA 1: CADASTRO ====================
        tab_cadastro = QWidget()
        tab_cadastro.setStyleSheet("background: transparent;")
        layout_cadastro = QVBoxLayout(tab_cadastro)
        layout_cadastro.setSpacing(12)
        layout_cadastro.setContentsMargins(0, 5, 0, 0)
        
        # DADOS PESSOAIS
        group_pessoal = QGroupBox("📋 Dados Pessoais")
        group_pessoal.setStyleSheet("""
            QGroupBox {
                background: white;
                border: 2px solid #E8EEF2;
                border-radius: 12px;
            }
        """)
        
        form_pessoal = QFormLayout()
        form_pessoal.setSpacing(12)
        form_pessoal.setContentsMargins(15, 20, 15, 20)
        form_pessoal.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        # Tipo de Pessoa
        self.tipo_pessoa_combo = QComboBox()
        self.tipo_pessoa_combo.addItems(["👤 Física", "🏢 Jurídica"])
        self.tipo_pessoa_combo.setFixedHeight(35)
        self.tipo_pessoa_combo.currentTextChanged.connect(self.on_tipo_pessoa_changed)
        form_pessoal.addRow("👤 Tipo:", self.tipo_pessoa_combo)
        
        # Nome Completo
        self.nome_input = QLineEdit()
        self.nome_input.setPlaceholderText("Ex: João Silva Santos")
        self.nome_input.setFixedHeight(35)
        self.nome_input.setStyleSheet("font-size: 13px;")
        form_pessoal.addRow("📝 Nome:*", self.nome_input)
        
        # CPF/CNPJ
        doc_widget = QWidget()
        doc_layout = QHBoxLayout(doc_widget)
        doc_layout.setContentsMargins(0, 0, 0, 0)
        doc_layout.setSpacing(8)
        
        self.documento_input = QLineEdit()
        self.documento_input.setPlaceholderText("Digite o CPF ou CNPJ")
        self.documento_input.setFixedHeight(35)
        self.documento_input.setMaxLength(18)
        self.documento_input.textChanged.connect(self.on_documento_changed)
        doc_layout.addWidget(self.documento_input)
        
        self.btn_validar_doc = QPushButton("✅ Validar")
        self.btn_validar_doc.setFixedHeight(35)
        self.btn_validar_doc.setFixedWidth(90)
        self.btn_validar_doc.clicked.connect(self.validar_documento)
        self.btn_validar_doc.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B9BD5, stop:1 #4A8BC2);
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4A8BC2, stop:1 #3A7BAF);
            }
        """)
        doc_layout.addWidget(self.btn_validar_doc)
        
        form_pessoal.addRow("🆔 CPF/CNPJ:*", doc_widget)
        
        # E-mail
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("exemplo@dominio.com")
        self.email_input.setFixedHeight(35)
        form_pessoal.addRow("📧 E-mail:*", self.email_input)
        
        # Celular
        self.celular_input = QLineEdit()
        self.celular_input.setPlaceholderText("(XX) XXXXX-XXXX")
        self.celular_input.setFixedHeight(35)
        self.celular_input.setMaxLength(15)
        self.celular_input.textChanged.connect(self.on_celular_changed)
        form_pessoal.addRow("📱 Celular:*", self.celular_input)
        
        group_pessoal.setLayout(form_pessoal)
        layout_cadastro.addWidget(group_pessoal)
        
        # ENDEREÇO
        group_endereco = QGroupBox("📍 Endereço")
        group_endereco.setStyleSheet("""
            QGroupBox {
                background: white;
                border: 2px solid #E8EEF2;
                border-radius: 12px;
            }
        """)
        
        form_endereco = QFormLayout()
        form_endereco.setSpacing(12)
        form_endereco.setContentsMargins(15, 20, 15, 20)
        form_endereco.setLabelAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
        
        # CEP
        cep_widget = QWidget()
        cep_layout = QHBoxLayout(cep_widget)
        cep_layout.setContentsMargins(0, 0, 0, 0)
        cep_layout.setSpacing(8)
        
        self.cep_input = QLineEdit()
        self.cep_input.setPlaceholderText("00000-000")
        self.cep_input.setFixedHeight(35)
        self.cep_input.textChanged.connect(self.on_cep_changed)
        cep_layout.addWidget(self.cep_input)
        
        self.btn_consultar_cep = QPushButton("🔍 Consultar")
        self.btn_consultar_cep.setFixedHeight(35)
        self.btn_consultar_cep.setFixedWidth(100)
        self.btn_consultar_cep.clicked.connect(self.consultar_cep)
        self.btn_consultar_cep.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #3498DB, stop:1 #2980B9);
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2980B9, stop:1 #2471A3);
            }
            QPushButton:disabled {
                background: #95A5A6;
            }
        """)
        cep_layout.addWidget(self.btn_consultar_cep)
        
        form_endereco.addRow("📮 CEP:*", cep_widget)
        
        # Logradouro
        self.logradouro_input = QLineEdit()
        self.logradouro_input.setPlaceholderText("Rua, Avenida, etc.")
        self.logradouro_input.setFixedHeight(35)
        form_endereco.addRow("🏠 Logradouro:*", self.logradouro_input)
        
        # Número e Complemento
        num_comp_widget = QWidget()
        num_comp_layout = QHBoxLayout(num_comp_widget)
        num_comp_layout.setContentsMargins(0, 0, 0, 0)
        num_comp_layout.setSpacing(8)
        
        self.numero_input = QLineEdit()
        self.numero_input.setPlaceholderText("Número")
        self.numero_input.setFixedHeight(35)
        num_comp_layout.addWidget(self.numero_input)
        
        self.complemento_input = QLineEdit()
        self.complemento_input.setPlaceholderText("Complemento")
        self.complemento_input.setFixedHeight(35)
        num_comp_layout.addWidget(self.complemento_input)
        
        form_endereco.addRow("🔢 Número:*", num_comp_widget)
        
        # Bairro
        self.bairro_input = QLineEdit()
        self.bairro_input.setPlaceholderText("Bairro")
        self.bairro_input.setFixedHeight(35)
        form_endereco.addRow("🏘️ Bairro:*", self.bairro_input)
        
        # Cidade e Estado
        cidade_estado_widget = QWidget()
        cidade_estado_layout = QHBoxLayout(cidade_estado_widget)
        cidade_estado_layout.setContentsMargins(0, 0, 0, 0)
        cidade_estado_layout.setSpacing(8)
        
        self.cidade_input = QLineEdit()
        self.cidade_input.setPlaceholderText("Cidade")
        self.cidade_input.setFixedHeight(35)
        cidade_estado_layout.addWidget(self.cidade_input)
        
        self.estado_combo = QComboBox()
        self.estado_combo.addItems([
            "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", 
            "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", 
            "RS", "RO", "RR", "SC", "SP", "SE", "TO"
        ])
        self.estado_combo.setFixedHeight(35)
        self.estado_combo.setFixedWidth(80)
        cidade_estado_layout.addWidget(self.estado_combo)
        
        form_endereco.addRow("🌆 Cidade:*", cidade_estado_widget)
        
        group_endereco.setLayout(form_endereco)
        layout_cadastro.addWidget(group_endereco)
        
        # BOTÕES
        layout_botoes = QHBoxLayout()
        layout_botoes.setSpacing(10)
        
        self.btn_limpar = QPushButton("🗑️ Limpar")
        self.btn_limpar.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.btn_limpar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_limpar.setFixedHeight(40)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.btn_limpar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_limpar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #95A5A6, stop:1 #7F8C8D);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7F8C8D, stop:1 #6B7A7B);
            }
        """)
        
        self.btn_salvar = QPushButton("💾 Salvar")
        self.btn_salvar.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.btn_salvar.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_salvar.setFixedHeight(40)
        self.btn_salvar.clicked.connect(self.salvar_pessoa)
        self.btn_salvar.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_salvar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #2ECC71, stop:1 #27AE60);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #27AE60, stop:1 #229954);
            }
        """)
        
        self.btn_cancelar_edicao = QPushButton("❌ Cancelar")
        self.btn_cancelar_edicao.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
        self.btn_cancelar_edicao.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancelar_edicao.setFixedHeight(40)
        self.btn_cancelar_edicao.clicked.connect(self.cancelar_edicao)
        self.btn_cancelar_edicao.setVisible(False)
        self.btn_cancelar_edicao.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.btn_cancelar_edicao.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E67E22, stop:1 #D35400);
                color: white;
                border: none;
                border-radius: 8px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #D35400, stop:1 #BA4A00);
            }
        """)
        
        layout_botoes.addWidget(self.btn_limpar)
        layout_botoes.addWidget(self.btn_salvar)
        layout_botoes.addWidget(self.btn_cancelar_edicao)
        
        layout_cadastro.addLayout(layout_botoes)
        layout_cadastro.addStretch()
        
        # ==================== ABA 2: LISTA DE CADASTRADOS ====================
        tab_lista = QWidget()
        tab_lista.setStyleSheet("background: transparent;")
        layout_lista = QVBoxLayout(tab_lista)
        layout_lista.setContentsMargins(10, 10, 10, 10)
        layout_lista.setSpacing(15)
        
        # Título da lista
        lista_title = QLabel("📋 Lista de Usuários Cadastrados")
        lista_title.setFont(QFont("Segoe UI", 15, QFont.Weight.Bold))
        lista_title.setStyleSheet("color: #2C3E50; margin-bottom: 8px;")
        layout_lista.addWidget(lista_title)
        
        # Barra de pesquisa
        layout_pesquisa = QHBoxLayout()
        layout_pesquisa.setSpacing(10)
        
        self.busca_input = QLineEdit()
        self.busca_input.setPlaceholderText("🔍 Pesquisar por nome ou CPF/CNPJ...")
        self.busca_input.setFixedHeight(38)
        self.busca_input.setStyleSheet("""
            QLineEdit {
                font-size: 12px; 
                padding: 4px 15px;
                border: 2px solid #DCE4EC;
                border-radius: 6px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #5B9BD5;
                background-color: #F8FBFF;
            }
        """)
        self.busca_input.textChanged.connect(self.pesquisar_pessoas)
        layout_pesquisa.addWidget(self.busca_input)
        
        self.btn_atualizar = QPushButton("🔄 Atualizar")
        self.btn_atualizar.setFixedHeight(38)
        self.btn_atualizar.setFixedWidth(110)
        self.btn_atualizar.clicked.connect(self.carregar_lista_pessoas)
        self.btn_atualizar.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B9BD5, stop:1 #4A8BC2);
                color: white;
                border: none;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4A8BC2, stop:1 #3A7BAF);
            }
        """)
        layout_pesquisa.addWidget(self.btn_atualizar)
        
        layout_lista.addLayout(layout_pesquisa)
        
        # TABELA
        self.tabela = QTableWidget()
        self.tabela.setColumnCount(8)
        self.tabela.setHorizontalHeaderLabels([
            "ID", "Nome", "CPF/CNPJ", "Email", "Celular", 
            "Cidade/UF", "Cadastro", "Ações"
        ])
        
        self.tabela.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.tabela.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tabela.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.tabela.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        self.tabela.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.tabela.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        self.tabela.horizontalHeader().setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        self.tabela.horizontalHeader().setSectionResizeMode(7, QHeaderView.ResizeMode.Fixed)
        self.tabela.setColumnWidth(7, 110)
        
        self.tabela.verticalHeader().setVisible(False)
        self.tabela.setAlternatingRowColors(True)
        self.tabela.setMinimumHeight(300)
        self.tabela.setStyleSheet("""
            QTableWidget {
                border: 2px solid #E8EEF2;
                border-radius: 8px;
                background-color: white;
                gridline-color: #E8EEF2;
            }
            QTableWidget::item {
                padding: 12px 10px;
            }
            QTableWidget::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #5B9BD5, stop:1 #4A8BC2);
                color: white;
            }
            QTableWidget::item:hover {
                background-color: #EBF5FB;
                color: #1A1A1A;
            }
        """)
        
        layout_lista.addWidget(self.tabela)
        
        # ==================== ADICIONAR AS ABAS AO TAB WIDGET ====================
        self.tabs.addTab(tab_cadastro, "📝 Cadastro")
        self.tabs.addTab(tab_lista, "📋 Lista de Usuários Cadastrados")
        
        # ==================== ADICIONAR O TAB WIDGET AO LAYOUT PRINCIPAL ====================
        main_layout.addWidget(self.tabs)
        
        self.setLayout(main_layout)
        
        # Carrega a lista APÓS a UI estar totalmente construída
        QTimer.singleShot(50, self.carregar_lista_pessoas)
    
    # ---------- MÉTODO PARA VALIDAR CELULAR (SOMENTE NÚMEROS) ----------
    def on_celular_changed(self, text):
        """Permite apenas números no campo celular e formata"""
        # Remove caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, text))
        
        # Limita a 11 dígitos
        if len(numeros) > 11:
            numeros = numeros[:11]
        
        # Formata
        if len(numeros) <= 2:
            self.celular_input.setText(numeros)
        elif len(numeros) <= 7:
            self.celular_input.setText(f"({numeros[:2]}) {numeros[2:]}")
        else:
            self.celular_input.setText(f"({numeros[:2]}) {numeros[2:7]}-{numeros[7:]}")
        
        # Coloca o cursor no final
        self.celular_input.setCursorPosition(len(self.celular_input.text()))
    
    # ---------- MÉTODO PARA VALIDAR CPF/CNPJ (MÁXIMO 15 DÍGITOS) ----------
    def on_documento_changed(self, text):
        """Auto formata o documento enquanto digita - máximo 14 dígitos"""
        # Remove caracteres não numéricos
        numeros = ''.join(filter(str.isdigit, text))
        
        # Limita a 14 dígitos (CNPJ) ou 11 (CPF)
        if len(numeros) > 14:
            numeros = numeros[:14]
        
        if len(numeros) <= 11:
            # CPF
            if len(numeros) <= 3:
                self.documento_input.setText(numeros)
            elif len(numeros) <= 6:
                self.documento_input.setText(f"{numeros[:3]}.{numeros[3:]}")
            elif len(numeros) <= 9:
                self.documento_input.setText(f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:]}")
            else:
                self.documento_input.setText(f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}")
        elif len(numeros) <= 14:
            # CNPJ
            if len(numeros) <= 2:
                self.documento_input.setText(numeros)
            elif len(numeros) <= 5:
                self.documento_input.setText(f"{numeros[:2]}.{numeros[2:]}")
            elif len(numeros) <= 8:
                self.documento_input.setText(f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:]}")
            elif len(numeros) <= 12:
                self.documento_input.setText(f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:]}")
            else:
                self.documento_input.setText(f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:]}")
        
        # Coloca o cursor no final
        self.documento_input.setCursorPosition(len(self.documento_input.text()))
    
    # ---------- MÉTODO PARA VALIDAR CEP ----------
    def on_cep_changed(self, text):
        """Auto formata CEP e consulta quando 8 dígitos são digitados"""
        numeros = ''.join(filter(str.isdigit, text))
        
        if len(numeros) > 8:
            numeros = numeros[:8]
        
        if len(numeros) <= 5:
            self.cep_input.setText(numeros)
        else:
            self.cep_input.setText(f"{numeros[:5]}-{numeros[5:]}")
        
        self.cep_input.setCursorPosition(len(self.cep_input.text()))
        
        if len(numeros) == 8:
            self.consultar_cep()
    
    # NOTA: Os métodos abaixo são os mesmos da versão anterior, mantenha-os
    def validar_campos(self):
        """Valida todos os campos do formulário"""
        erros = []
        
        nome = self.nome_input.text().strip()
        if not nome:
            erros.append("Nome completo é obrigatório")
            self.nome_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        elif not Validators.validar_nome_completo(nome):
            erros.append("Digite o nome completo (mínimo: nome e sobrenome)")
            self.nome_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        else:
            self.nome_input.setStyleSheet("border: 2px solid #2ECC71; background: #F0FFF4;")
        
        documento = self.documento_input.text().strip()
        if not documento:
            erros.append("CPF/CNPJ é obrigatório")
            self.documento_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        else:
            tipo = Validators.identificar_tipo_documento(documento)
            if tipo == 'CPF':
                if not Validators.validar_cpf(documento):
                    erros.append("CPF inválido")
                    self.documento_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
                else:
                    self.documento_input.setStyleSheet("border: 2px solid #2ECC71; background: #F0FFF4;")
            elif tipo == 'CNPJ':
                if not Validators.validar_cnpj(documento):
                    erros.append("CNPJ inválido")
                    self.documento_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
                else:
                    self.documento_input.setStyleSheet("border: 2px solid #2ECC71; background: #F0FFF4;")
            else:
                erros.append("Documento inválido. Use CPF (11 dígitos) ou CNPJ (14 dígitos)")
                self.documento_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        
        email = self.email_input.text().strip()
        if not email:
            erros.append("E-mail é obrigatório")
            self.email_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        elif not Validators.validar_email(email):
            erros.append("E-mail inválido (ex: usuario@dominio.com)")
            self.email_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        else:
            self.email_input.setStyleSheet("border: 2px solid #2ECC71; background: #F0FFF4;")
        
        celular = self.celular_input.text().strip()
        if not celular:
            erros.append("Celular é obrigatório")
            self.celular_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        elif not Validators.validar_celular(celular):
            erros.append("Celular inválido. Use (XX) XXXXX-XXXX")
            self.celular_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        else:
            self.celular_input.setStyleSheet("border: 2px solid #2ECC71; background: #F0FFF4;")
        
        cep = self.cep_input.text().strip()
        if not cep:
            erros.append("CEP é obrigatório")
            self.cep_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        elif not Validators.validar_cep(cep):
            erros.append("CEP inválido (8 dígitos)")
            self.cep_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        else:
            self.cep_input.setStyleSheet("border: 2px solid #2ECC71; background: #F0FFF4;")
        
        if not self.logradouro_input.text().strip():
            erros.append("Logradouro é obrigatório")
            self.logradouro_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        else:
            self.logradouro_input.setStyleSheet("")
        
        if not self.numero_input.text().strip():
            erros.append("Número é obrigatório")
            self.numero_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        else:
            self.numero_input.setStyleSheet("")
        
        if not self.bairro_input.text().strip():
            erros.append("Bairro é obrigatório")
            self.bairro_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        else:
            self.bairro_input.setStyleSheet("")
        
        if not self.cidade_input.text().strip():
            erros.append("Cidade é obrigatória")
            self.cidade_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
        else:
            self.cidade_input.setStyleSheet("")
        
        return erros

    def validar_documento(self):
        """Valida o documento atual"""
        documento = self.documento_input.text().strip()
        if not documento:
            QMessageBox.warning(self, "⚠️ Aviso", "Digite um CPF ou CNPJ primeiro!")
            return
        
        tipo = Validators.identificar_tipo_documento(documento)
        
        if tipo == 'CPF':
            if Validators.validar_cpf(documento):
                doc_formatado = Validators.formatar_cpf_cnpj(documento)
                self.documento_input.setText(doc_formatado)
                self.documento_input.setStyleSheet("border: 2px solid #2ECC71; background: #F0FFF4;")
                QMessageBox.information(self, "✅ CPF Válido", f"CPF {doc_formatado} é válido!")
            else:
                self.documento_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
                QMessageBox.warning(self, "❌ CPF Inválido", "O CPF informado é inválido!")
        elif tipo == 'CNPJ':
            if Validators.validar_cnpj(documento):
                doc_formatado = Validators.formatar_cpf_cnpj(documento)
                self.documento_input.setText(doc_formatado)
                self.documento_input.setStyleSheet("border: 2px solid #2ECC71; background: #F0FFF4;")
                QMessageBox.information(self, "✅ CNPJ Válido", f"CNPJ {doc_formatado} é válido!")
            else:
                self.documento_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
                QMessageBox.warning(self, "❌ CNPJ Inválido", "O CNPJ informado é inválido!")
        else:
            QMessageBox.warning(self, "❌ Documento Inválido", 
                              "Documento inválido. Use CPF (11 dígitos) ou CNPJ (14 dígitos)")

    def consultar_cep(self):
        """Consulta o CEP informado"""
        cep = self.cep_input.text().strip()
        
        if not Validators.validar_cep(cep):
            QMessageBox.warning(self, "⚠️ CEP Inválido", 
                              "CEP inválido. Digite 8 dígitos.")
            return
        
        self.btn_consultar_cep.setText("⏳ Buscando...")
        self.btn_consultar_cep.setEnabled(False)
        self.status_label.setText("⏳ Buscando CEP...")
        self.status_label.setStyleSheet("color: #F39C12; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 12px;")
        
        QTimer.singleShot(100, self._realizar_consulta_cep)

    def _realizar_consulta_cep(self):
        """Realiza a consulta do CEP de fato"""
        cep = self.cep_input.text().strip()
        resultado = self.cep_service.consultar_cep(cep)
        
        self.btn_consultar_cep.setText("🔍 Consultar")
        self.btn_consultar_cep.setEnabled(True)
        
        if resultado['success']:
            dados = resultado['data']
            self.logradouro_input.setText(dados['logradouro'])
            self.bairro_input.setText(dados['bairro'])
            self.cidade_input.setText(dados['cidade'])
            
            index = self.estado_combo.findText(dados['estado'])
            if index >= 0:
                self.estado_combo.setCurrentIndex(index)
            
            self.cep_input.setStyleSheet("border: 2px solid #2ECC71; background: #F0FFF4;")
            self.status_label.setText("✅ CEP Encontrado")
            self.status_label.setStyleSheet("color: #2ECC71; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 12px;")
            
            QMessageBox.information(self, "✅ CEP Encontrado", 
                                  "📍 Endereço preenchido com sucesso!")
        else:
            self.cep_input.setStyleSheet("border: 2px solid #E74C3C; background: #FFF5F5;")
            self.status_label.setText("❌ CEP Não Encontrado")
            self.status_label.setStyleSheet("color: #E74C3C; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 12px;")
            
            QMessageBox.warning(self, "❌ Erro na Consulta", resultado['error'])

    def on_tipo_pessoa_changed(self, tipo):
        """Muda o label do documento conforme o tipo de pessoa"""
        pass

    def carregar_lista_pessoas(self):
        """Carrega a lista de pessoas na tabela"""
        # Verifica se a tabela existe
        if self.tabela is None:
            QTimer.singleShot(100, self.carregar_lista_pessoas)
            return
        
        # Verifica se o tabs existe
        if self.tabs is None:
            QTimer.singleShot(100, self.carregar_lista_pessoas)
            return
        
        try:
            pessoas = self.db.get_all_pessoas()
            self._popular_tabela(pessoas)
            self.status_label.setText(f"✅ {len(pessoas)} registros")
            self.status_label.setStyleSheet("color: #2ECC71; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 12px;")
        except RuntimeError:
            QTimer.singleShot(100, self.carregar_lista_pessoas)

    def pesquisar_pessoas(self):
        """Pesquisa pessoas pelo nome ou CPF/CNPJ"""
        if self.tabela is None:
            return
        
        try:
            termo = self.busca_input.text().strip()
            if termo:
                pessoas = self.db.search_pessoas(termo)
                self.status_label.setText(f"🔍 {len(pessoas)} resultados")
                self.status_label.setStyleSheet("color: #F39C12; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 12px;")
            else:
                pessoas = self.db.get_all_pessoas()
                self.status_label.setText(f"✅ {len(pessoas)} registros")
                self.status_label.setStyleSheet("color: #2ECC71; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 12px;")
            self._popular_tabela(pessoas)
        except RuntimeError:
            pass

    def _popular_tabela(self, pessoas):
        """Popula a tabela com os dados das pessoas"""
        # Verifica se a tabela existe e não foi deletada
        if self.tabela is None:
            return
        
        try:
            self.tabela.setRowCount(len(pessoas))
        except RuntimeError:
            return
        
        for row, pessoa in enumerate(pessoas):
            try:
                # ID
                id_item = QTableWidgetItem(str(pessoa[0]))
                id_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabela.setItem(row, 0, id_item)
                
                # Nome
                nome_item = QTableWidgetItem(pessoa[1])
                self.tabela.setItem(row, 1, nome_item)
                
                # CPF/CNPJ
                doc_item = QTableWidgetItem(pessoa[2])
                doc_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabela.setItem(row, 2, doc_item)
                
                # Email
                email_item = QTableWidgetItem(pessoa[3])
                self.tabela.setItem(row, 3, email_item)
                
                # Celular
                cel_item = QTableWidgetItem(Validators.formatar_celular(pessoa[4]))
                cel_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabela.setItem(row, 4, cel_item)
                
                # Cidade/UF
                cidade_uf = f"{pessoa[10]}/{pessoa[11]}"
                cidade_item = QTableWidgetItem(cidade_uf)
                cidade_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabela.setItem(row, 5, cidade_item)
                
                # Data de Cadastro
                if len(pessoa) > 12:
                    data_cadastro = pessoa[12]
                    if len(data_cadastro) < 10:
                        data_cadastro = "N/A"
                else:
                    data_cadastro = "N/A"
                
                data_item = QTableWidgetItem(data_cadastro)
                data_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tabela.setItem(row, 6, data_item)
                
                # ========== BOTÕES DE AÇÃO - SOMENTE ÍCONES ==========
                widget_botoes = QWidget()
                widget_botoes.setStyleSheet("background: transparent;")
                
                # Layout vertical com centralização
                layout_botoes = QVBoxLayout(widget_botoes)
                layout_botoes.setContentsMargins(0, 0, 0, 0)
                layout_botoes.setSpacing(0)
                
                # Stretch em cima
                layout_botoes.addStretch(1)
                
                # Container horizontal para os botões
                container_botoes = QWidget()
                container_botoes.setStyleSheet("background: transparent;")
                container_layout = QHBoxLayout(container_botoes)
                container_layout.setContentsMargins(0, 0, 0, 0)
                container_layout.setSpacing(8)
                
                # Centraliza horizontalmente
                container_layout.addStretch()
                
                # Botão Editar - Somente ícone
                btn_editar = QPushButton("✏️")
                btn_editar.setFixedSize(34, 30)
                btn_editar.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_editar.setToolTip("Editar usuário")
                btn_editar.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 #5B9BD5, stop:1 #4A8BC2);
                        color: white;
                        border: none;
                        border-radius: 6px;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 #4A8BC2, stop:1 #3A7BAF);
                    }
                    QPushButton:pressed {
                        background: #3A7BAF;
                    }
                """)
                btn_editar.clicked.connect(lambda checked, r=row: self.editar_pessoa(r))
                container_layout.addWidget(btn_editar)
                
                # Botão Excluir - Somente ícone
                btn_excluir = QPushButton("🗑️")
                btn_excluir.setFixedSize(34, 30)
                btn_excluir.setCursor(Qt.CursorShape.PointingHandCursor)
                btn_excluir.setToolTip("Excluir usuário")
                btn_excluir.setStyleSheet("""
                    QPushButton {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 #E74C3C, stop:1 #C0392B);
                        color: white;
                        border: none;
                        border-radius: 6px;
                        font-size: 16px;
                    }
                    QPushButton:hover {
                        background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                            stop:0 #C0392B, stop:1 #A93226);
                    }
                    QPushButton:pressed {
                        background: #A93226;
                    }
                """)
                btn_excluir.clicked.connect(lambda checked, r=row: self.excluir_pessoa(r))
                container_layout.addWidget(btn_excluir)
                
                # Centraliza horizontalmente
                container_layout.addStretch()
                
                layout_botoes.addWidget(container_botoes)
                
                # Stretch embaixo
                layout_botoes.addStretch(2)
                
                self.tabela.setCellWidget(row, 7, widget_botoes)
                
            except RuntimeError as e:
                print(f"Erro ao popular linha {row}: {e}")
                continue
        
        # Ajusta altura das linhas
        try:
            for row in range(len(pessoas)):
                self.tabela.setRowHeight(row, 55)
        except RuntimeError:
            pass

    def salvar_pessoa(self):
        """Salva uma nova pessoa ou atualiza existente"""
        erros = self.validar_campos()
        
        if erros:
            QMessageBox.warning(self, "❌ Erros no Formulário", 
                              "Por favor, corrija os seguintes erros:\n\n" + 
                              "\n".join(f"• {erro}" for erro in erros))
            return
        
        dados = {
            'nome_completo': self.nome_input.text().strip(),
            'cpf_cnpj': ''.join(filter(str.isdigit, self.documento_input.text())),
            'email': self.email_input.text().strip(),
            'celular': ''.join(filter(str.isdigit, self.celular_input.text())),
            'cep': ''.join(filter(str.isdigit, self.cep_input.text())),
            'logradouro': self.logradouro_input.text().strip(),
            'numero': self.numero_input.text().strip(),
            'complemento': self.complemento_input.text().strip(),
            'bairro': self.bairro_input.text().strip(),
            'cidade': self.cidade_input.text().strip(),
            'estado': self.estado_combo.currentText(),
            'tipo_pessoa': self.tipo_pessoa_combo.currentText().replace("👤 ", "").replace("🏢 ", "")
        }
        
        if self.modo_edicao and self.id_editando:
            success, msg = self.db.update_pessoa(self.id_editando, dados)
        else:
            success, msg = self.db.insert_pessoa(dados)
        
        if success:
            QMessageBox.information(self, "✅ Sucesso!", msg)
            self.limpar_campos()
            self.carregar_lista_pessoas()
            self.status_label.setText("✅ Cadastro realizado!")
            self.status_label.setStyleSheet("color: #2ECC71; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 12px;")
        else:
            QMessageBox.critical(self, "❌ Erro!", msg)
            self.status_label.setText("❌ Erro ao salvar")
            self.status_label.setStyleSheet("color: #E74C3C; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 12px;")

    def editar_pessoa(self, row):
        """Carrega os dados de uma pessoa para edição"""
        id_item = self.tabela.item(row, 0)
        if not id_item:
            return
        
        pessoa_id = int(id_item.text())
        pessoa = self.db.get_pessoa_by_id(pessoa_id)
        
        if not pessoa:
            QMessageBox.warning(self, "❌ Erro", "Pessoa não encontrada!")
            return
        
        self.id_editando = pessoa[0]
        self.modo_edicao = True
        
        self.nome_input.setText(pessoa[1])
        self.documento_input.setText(Validators.formatar_cpf_cnpj(pessoa[2]))
        self.email_input.setText(pessoa[3])
        self.celular_input.setText(Validators.formatar_celular(pessoa[4]))
        self.cep_input.setText(Validators.formatar_cep(pessoa[5]))
        self.logradouro_input.setText(pessoa[6])
        self.numero_input.setText(pessoa[7])
        self.complemento_input.setText(pessoa[8] if pessoa[8] else "")
        self.bairro_input.setText(pessoa[9])
        self.cidade_input.setText(pessoa[10])
        
        index = self.estado_combo.findText(pessoa[11])
        if index >= 0:
            self.estado_combo.setCurrentIndex(index)
        
        tipo = "👤 Física" if pessoa[12] == "Física" else "🏢 Jurídica"
        index = self.tipo_pessoa_combo.findText(tipo)
        if index >= 0:
            self.tipo_pessoa_combo.setCurrentIndex(index)
        
        self.btn_salvar.setText("💾 Atualizar")
        self.btn_cancelar_edicao.setVisible(True)
        
        self.status_label.setText("✏️ Modo Edição")
        self.status_label.setStyleSheet("color: #F39C12; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 12px;")
        
        self.tabs.setCurrentIndex(0)
        
        QMessageBox.information(self, "✏️ Edição", "Dados carregados para edição!")

    def cancelar_edicao(self):
        """Cancela o modo de edição"""
        self.modo_edicao = False
        self.id_editando = None
        self.btn_salvar.setText("💾 Salvar")
        self.btn_cancelar_edicao.setVisible(False)
        self.limpar_campos()
        self.status_label.setText("✅ Edição cancelada")
        self.status_label.setStyleSheet("color: #2ECC71; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 12px;")

    def excluir_pessoa(self, row):
        """Exclui uma pessoa do banco de dados"""
        id_item = self.tabela.item(row, 0)
        if not id_item:
            return
        
        pessoa_id = int(id_item.text())
        nome = self.tabela.item(row, 1).text()
        
        reply = QMessageBox.question(
            self, "⚠️ Confirmar Exclusão",
            f"Tem certeza que deseja excluir a pessoa '{nome}'?\n\nEsta ação não pode ser desfeita.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success, msg = self.db.delete_pessoa(pessoa_id)
            if success:
                QMessageBox.information(self, "✅ Sucesso!", msg)
                self.carregar_lista_pessoas()
                self.status_label.setText("🗑️ Registro excluído")
                self.status_label.setStyleSheet("color: #E74C3C; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 12px;")
            else:
                QMessageBox.critical(self, "❌ Erro!", msg)

    def limpar_campos(self):
        """Limpa todos os campos do formulário"""
        self.nome_input.clear()
        self.documento_input.clear()
        self.email_input.clear()
        self.celular_input.clear()
        self.cep_input.clear()
        self.logradouro_input.clear()
        self.numero_input.clear()
        self.complemento_input.clear()
        self.bairro_input.clear()
        self.cidade_input.clear()
        self.estado_combo.setCurrentIndex(0)
        self.tipo_pessoa_combo.setCurrentIndex(0)
        
        for widget in [self.nome_input, self.documento_input, self.email_input, 
                      self.celular_input, self.cep_input]:
            widget.setStyleSheet("")
        
        self.nome_input.setFocus()
        
        if self.modo_edicao:
            self.cancelar_edicao()

    def closeEvent(self, event):
        """Evento chamado quando a janela é fechada"""
        self.db.close()
        event.accept()