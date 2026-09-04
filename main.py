import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from pessoa_form import PessoaForm

def main():
    app = QApplication(sys.argv)
    
    # Configurações da aplicação
    app.setStyle("Fusion")
    
    # Cria e exibe a janela
    window = PessoaForm()
    window.show()
    
    sys.exit(app.exec())

if __name__ == "__main__":
    main()