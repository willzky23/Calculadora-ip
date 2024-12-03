from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QMessageBox, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt
import ipaddress

class CalculadoraIP(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de IP")
        self.setGeometry(1, 200, 450, 600)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter) 

        self.titulo = QLabel("Calculadora")
        self.titulo.setAlignment(Qt.AlignCenter)  

        self.titulo.setObjectName("titulo")  
        layout.addWidget(self.titulo)

        self.texto_ip = QLabel("Escreva o número do IP:")
        layout.addWidget(self.texto_ip)

        self.campo_ip = QLineEdit()
        layout.addWidget(self.campo_ip)

        self.texto_mascara = QLabel("Escreva a máscara:")
        layout.addWidget(self.texto_mascara)
        
        self.campo_mascara = QLineEdit()
        layout.addWidget(self.campo_mascara)

        self.botao_ver = QPushButton("Calcular")
        self.botao_ver.clicked.connect(self.mostrar_resultado)
        layout.addWidget(self.botao_ver)

        tela = QWidget()
        tela.setLayout(layout)
        self.setCentralWidget(tela)


        # Aplicando estilo (QSS)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1E1E2F; 
            }
            QLabel {
                color: #EAEAEA; 
                font-size: 22px;
                font-family: Arial, sans-serif;
                margin-bottom: 0px; 
                font-family: Poppins, Bold;
            }

            QLabel#titulo {
                color: #FFFFFF;  
                font-size: 28px; 
                font-weight: bold; 
                font-family: Poppins, Bold; 
                margin-bottom: 30px; 
            }            
            
            QLineEdit {
                height: 60px;
                border: 2px solid #3E4451;
                border-radius: 8px;
                background-color: #2A2A40;
                color: #EAEAEA;
                font-size: 16px;
                padding-left: 10px;
                margin-bottom: 60px; 
            }

            QPushButton {
                font-size: 20px;
                height: 60px;
                font-family: Arial, sans-serif;
                color: #FFFFFF;
                background-color: #0078D7;
                border: none;
                border-radius: 6px;
                margin-bottom: 10px; 
                font-family: Poppins, Bold;
            }
            QPushButton:hover {
                background-color: #005FA1;
            }
            QPushButton:pressed {
                background-color: #004080; 
            }
            QMessageBox {
                background-color: #1E1E2F;
                color: #EAEAEA;
            }
                           
            """)

    def resizeEvent(self, event):
        largura = self.width()
        novo_tamanho = max(380, int(largura * 0.5))  # Não menos que 300px
        self.campo_ip.setFixedWidth(novo_tamanho)
        self.campo_mascara.setFixedWidth(novo_tamanho)

    def mostrar_resultado(self):
        numero_ip = self.campo_ip.text()
        mascara_ip = self.campo_mascara.text()

        try:
            rede = ipaddress.IPv4Network(f"{numero_ip}/{mascara_ip}", strict=False)

            octetos = numero_ip.split('.')
            primeiro_octeto = int(octetos[0])
            
            if 1 <= primeiro_octeto <= 126:
                classe = "A"

            elif 128 <= primeiro_octeto <= 191:
                classe = "B"

            elif 192 <= primeiro_octeto <= 223:
                classe = "C"

            else:
                classe = "Desconhecida"

            if primeiro_octeto == 10:
                tipo_ip = "Privado"

            elif primeiro_octeto == 172 and 16 <= int(octetos[1]) <= 31:
                tipo_ip = "Privado"

            elif primeiro_octeto == 192 and int(octetos[1]) == 168:
                tipo_ip = "Privado"

            else:
                tipo_ip = "Público"

            quantidade_hosts = rede.num_addresses - 2 
            numero_subredes = 2 ** (rede.prefixlen - 16) if classe == "B" else (2 ** (rede.prefixlen - 8) if classe == "A" else 1)
            primeiro_host = list(rede.hosts())[0]
            ultimo_host = list(rede.hosts())[-1]
            broadcast = rede.broadcast_address

            resultado = (
                f"Endereço ip: {numero_ip}\n"
                f"Mascara digitada: {mascara_ip}\n"
                f"Endereço de Rede: {rede.network_address}\n"
                f"Primeiro Host: {primeiro_host}\n"
                f"Último Host: {ultimo_host}\n"
                f"Endereço de Broadcast: {broadcast}\n"
                f"Classe do IP: {classe}\n"
                f"Número de Sub-redes: {numero_subredes}\n"
                f"Quantidade de Hosts: {quantidade_hosts}\n"
                f"Tipo do IP: {tipo_ip}"
            )

            msg = QMessageBox(self)
            msg.setWindowTitle("Resultado")
            msg.setText(resultado)
            msg.setStandardButtons(QMessageBox.Ok)

            ok_button = msg.button(QMessageBox.Ok)
            ok_button.setFixedSize(200, 60) 
            ok_button.setStyleSheet("""
                QPushButton {
                    font-size: 22px;
                    color: white;
                    border-radius: 8px;
                    height: 60px;
                    width: 200px;
                }
                QPushButton:hover {
                    color: #000000;
                    background-color: #FFFFFF;
                }
                QPushButton:pressed {
                    background-color: #388e3c;
                }
            """)

            msg.exec_()

            
        except ValueError:
            QMessageBox.critical(self, "Erro", "O número ou a máscara não estão certos!")

app = QApplication([])
calculadora = CalculadoraIP()
calculadora.show()
app.exec_()
