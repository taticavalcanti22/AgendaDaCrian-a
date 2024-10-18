import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import sqlite3
import datetime

class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda de Atividades e Recompensas")
        self.geometry("800x600")

        self.total_estrelas = 0
        self.atividades = []

        # Inicializando o banco de dados e o banco de estrelas
        self.inicializar_banco_estrelas()
        self.criar_tabela_atividades()
        self.carregar_total_estrelas()

        # Botão para mostrar o total de estrelas
        btn_mostrar_estrelas = tk.Button(self, text="Mostrar Estrelas", command=self.mostrar_estrelas)
        btn_mostrar_estrelas.pack(pady=10)

        # Botão para adicionar atividades
        btn_adicionar_atividade = tk.Button(self, text="Adicionar Atividade", command=self.adicionar_atividade)
        btn_adicionar_atividade.pack(pady=10)

        # Botão para mostrar o quadro de rotina
        btn_quadro_rotina = tk.Button(self, text="Mostrar Quadro de Rotina", command=self.mostrar_quadro_rotina)
        btn_quadro_rotina.pack(pady=10)

        # Lista de atividades
        self.lista_atividades = tk.Listbox(self)
        self.lista_atividades.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        # Carregar as atividades do banco de dados
        self.carregar_atividades()

    def adicionar_atividade(self):
        janela_adicionar = tk.Toplevel(self)
        janela_adicionar.title("Adicionar Atividade")

        lbl_nome = tk.Label(janela_adicionar, text="Nome da Atividade:")
        lbl_nome.pack()

        nome_entry = tk.Entry(janela_adicionar)
        nome_entry.pack()

        lbl_data = tk.Label(janela_adicionar, text="Data (DD/MM/AAAA):")
        lbl_data.pack()

        data_entry = tk.Entry(janela_adicionar)
        data_entry.pack()
        data_entry.bind("<KeyRelease>", self.formatar_data)

        lbl_hora = tk.Label(janela_adicionar, text="Hora (HH:MM):")
        lbl_hora.pack()

        hora_entry = tk.Entry(janela_adicionar)
        hora_entry.pack()
        hora_entry.bind("<KeyRelease>", self.formatar_hora)

        lbl_estrelas = tk.Label(janela_adicionar, text="Estrelas:")
        lbl_estrelas.pack()

        estrelas_entry = tk.Entry(janela_adicionar)
        estrelas_entry.pack()

        lbl_imagem = tk.Label(janela_adicionar, text="Imagem:")
        lbl_imagem.pack()

        self.imagem_entry = tk.Entry(janela_adicionar)
        self.imagem_entry.pack()

        btn_selecionar_imagem = tk.Button(janela_adicionar, text="Selecionar Imagem", command=self.selecionar_imagem)
        btn_selecionar_imagem.pack()

        def salvar_atividade():
            nome = nome_entry.get()
            data = data_entry.get()
            hora = hora_entry.get()
            estrelas = estrelas_entry.get()
            caminho_imagem = self.imagem_entry.get()

            if not nome or not data or not hora or not estrelas:
                messagebox.showerror("Erro", "Preencha todos os campos.")
                return

            if not self.validar_data(data):
                messagebox.showerror("Erro", "Data inválida. Use o formato DD/MM/AAAA.")
                return

            atividade = {
                'nome': nome,
                'data': data,
                'hora': hora,
                'estrelas': estrelas,
                'imagem': caminho_imagem
            }

            self.atividades.append(atividade)
            self.lista_atividades.insert(tk.END, nome)

            # Salvar a atividade no banco de dados
            self.salvar_atividade_db(atividade)

            messagebox.showinfo("Sucesso", "Atividade adicionada com sucesso!")
            janela_adicionar.destroy()

        btn_salvar = tk.Button(janela_adicionar, text="Salvar Atividade", command=salvar_atividade)
        btn_salvar.pack(pady=10)

    def salvar_atividade_db(self, atividade):
        with sqlite3.connect('atividades.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO atividades (nome, data, hora, imagem, estrelas)
                VALUES (?, ?, ?, ?, ?)
            """, (atividade['nome'], atividade['data'], atividade['hora'], atividade['imagem'], atividade['estrelas']))
            conn.commit()

    def carregar_atividades(self):
        with sqlite3.connect('atividades.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nome, data, hora, imagem, estrelas FROM atividades")
            atividades_db = cursor.fetchall()

            for atividade in atividades_db:
                atividade_dict = {
                    'nome': atividade[0],
                    'data': atividade[1],
                    'hora': atividade[2],
                    'imagem': atividade[3],
                    'estrelas': atividade[4]
                }
                self.atividades.append(atividade_dict)
                self.lista_atividades.insert(tk.END, atividade[0])

    def criar_tabela_atividades(self):
        with sqlite3.connect('atividades.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS atividades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT NOT NULL,
                    data TEXT NOT NULL,
                    hora TEXT NOT NULL,
                    imagem TEXT,
                    estrelas INTEGER
                )
            """)
            conn.commit()

    def formatar_data(self, event=None):
        entry_widget = event.widget
        texto = entry_widget.get()

        # Remove caracteres não numéricos
        texto = texto.replace("/", "")

        # Formata conforme o número de dígitos inseridos
        if len(texto) > 2:
            texto = texto[:2] + "/" + texto[2:]
        if len(texto) > 5:
            texto = texto[:5] + "/" + texto[5:]

        # Limita a 10 caracteres (DD/MM/AAAA)
        if len(texto) > 10:
            texto = texto[:10]

        # Atualiza o campo de entrada
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, texto)

    def formatar_hora(self, event=None):
        entry_widget = event.widget
        texto = entry_widget.get()

        # Remove caracteres não numéricos
        texto = texto.replace(":", "")

        # Insere os dois pontos depois de dois dígitos
        if len(texto) > 2:
            texto = texto[:2] + ":" + texto[2:]

        # Limita a 5 caracteres (HH:MM)
        if len(texto) > 5:
            texto = texto[:5]

        # Atualiza o campo de entrada
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, texto)

    def selecionar_imagem(self):
        caminho_imagem = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        print(caminho_imagem)
        if caminho_imagem:
            self.imagem_entry.delete(0, tk.END)
            self.imagem_entry.insert(0, caminho_imagem)

    def mostrar_quadro_rotina(self):
        quadro_janela = tk.Toplevel(self)
        quadro_janela.title("Quadro de Rotina")
        quadro_janela.geometry("800x600")
        quadro_janela.configure(bg="#FFDEAD")

        for atividade in self.atividades:
            frame_atividade = tk.Frame(quadro_janela, bg="#FFFACD")
            frame_atividade.pack(pady=5, padx=10, fill=tk.X)

            nome_label = tk.Label(frame_atividade, text=f"Nome: {atividade['nome']}", font=("Arial", 12), bg="#FFFACD")
            nome_label.pack(anchor="w")

            data_label = tk.Label(frame_atividade, text=f"Data: {atividade['data']}", font=("Arial", 12), bg="#FFFACD")
            data_label.pack(anchor="w")

            hora_label = tk.Label(frame_atividade, text=f"Hora: {atividade['hora']}", font=("Arial", 12), bg="#FFFACD")
            hora_label.pack(anchor="w")

            estrelas_label = tk.Label(frame_atividade, text=f"Estrelas: {atividade['estrelas']}", font=("Arial", 12), bg="#FFFACD")
            estrelas_label.pack(anchor="w")

            if atividade['imagem']:
                try:
                    imagem = Image.open(atividade['imagem'])
                    imagem = imagem.resize((100, 100))
                    imagem_tk = ImageTk.PhotoImage(imagem)
                    img_label = tk.Label(frame_atividade, image=imagem_tk, bg="#FFFACD")
                    img_label.image = imagem_tk
                    img_label.pack(anchor="e")
                except Exception as e:
                    print(f"Erro ao carregar imagem: {e}")

    def mostrar_estrelas(self):
        messagebox.showinfo("Total de Estrelas", f"Você tem {self.total_estrelas} estrelas.")

    def inicializar_banco_estrelas(self):
        with sqlite3.connect('atividades.db') as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS banco_estrelas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    total_estrelas INTEGER
                )
            """)
            conn.commit()

            # Verifica se existe um registro no banco de estrelas
            cursor.execute("SELECT total_estrelas FROM banco_estrelas")
            row = cursor.fetchone()
            if row is None:
                cursor.execute("INSERT INTO banco_estrelas (total_estrelas) VALUES (0)")
                conn.commit()

    def carregar_total_estrelas(self):
        with sqlite3.connect('atividades.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT total_estrelas FROM banco_estrelas")
            row = cursor.fetchone()
            if row:
                self.total_estrelas = row[0]

    def validar_data(self, data):
        try:
            datetime.datetime.strptime(data, '%d/%m/%Y')
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    app = AgendaApp()
    app.mainloop()
