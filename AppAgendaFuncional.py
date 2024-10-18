import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import Calendar
from PIL import Image, ImageTk
import datetime
import sqlite3
import json
import os
import locale


class AgendaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Agenda da Criança")
        self.geometry("800x800")
        self.configure(bg="#f1be40")
        self.nome_crianca = "Nome da Criança"
        self.caminho_foto_crianca = None

            # Definindo o local para Português
        locale.setlocale(locale.LC_ALL, 'pt_BR')

        self.atividades = []
        self.carregar_atividades_db()
        self.lista_atividade_db = ()

        self.total_estrelas = 0  # Iniciar com zero estrelas
        self.criar_tabelas()  # Garantir que as tabelas existam
        self.carregar_total_estrelas()  # Carregar as estrelas do banco de dados ao iniciar
        self.carregar_dados_crianca()

        # Botão para mostrar estrelas
        btn_mostrar_estrelas = tk.Button(self, text="Ver Total de Estrelas", command=self.mostrar_estrelas)
        btn_mostrar_estrelas.pack(pady=10)

        # Frame para os botões de definir nome e foto
        self.frame_botoes = tk.Frame(self, bg="#f1be40")
        self.frame_botoes.pack(pady=20)

        # Criando botões para definir o nome e a foto
        self.btn_definir_nome = tk.Button(self.frame_botoes, text="Lugar do meu lindo nome",
                                    command=self.definir_nome, bg="#aabe1a", fg="white", font=("Arial", 10))
        self.btn_definir_nome.pack(side="left", padx=5, pady=5)

        self.btn_definir_foto = tk.Button(self.frame_botoes,
                                        text="Lugar da minha linda foto",
                                        command=self.definir_foto_crianca,
                                        bg="#ff7828",
                                        fg="white",
                                        font=("Arial", 10))
        self.btn_definir_foto.pack(side="left", padx=5, pady=5)

        # Frame para a foto da criança
        self.frame_foto = tk.Frame(self, bg="#f1be40")
        self.frame_foto.pack(pady=10)

        self.label_foto_crianca = tk.Label(self.frame_foto, bg="#f1be40")
        self.label_foto_crianca.pack(side=tk.TOP)

        # Criar a label para a mensagem de boas-vindas
        self.label_frase_boas_vindas = tk.Label(self, text=f"O que vamos fazer hoje?", 
                                        font=("Arial", 22, "bold"), fg="#aa6925", bg="#f1be40")
        self.label_frase_boas_vindas.pack(pady=5)

        # Criando o atributo data_atual
        self.data_atual = datetime.date.today()
        data_formatada = self.data_atual.strftime("%A, %d/%m/%Y")

        # Exibindo a data atual em um label
        label_data = tk.Label(self, text=f"Hoje é {data_formatada}. Que dia incrível!", 
                            bg="#f1be40",
                            fg="#aa6925",
                            font=("Arial", 22, "bold"))
        label_data.pack(pady=(10, 20))

        # Inicializando a variável da imagem como None
        self.imagem_botao_foto = None
        self.atualizar_foto_crianca()

        # Carregar a imagem da capa

        self.capa = Image.open(r"C:\Users\tatic\myenv\agenda5.JPG")
        self.capa = self.capa.resize((800, 250), Image.LANCZOS)
        self.capa_imagem = ImageTk.PhotoImage(self.capa)

        self.label_capa = tk.Label(self, image=self.capa_imagem)
        self.label_capa.image = self.capa_imagem
        self.label_capa.pack(pady=0)

        self.frame_lista = tk.Frame(self, bg="#ADD8E6")
        self.frame_lista.pack(pady=10)

        self.lista_atividades = tk.Listbox(self.frame_lista, width=60, height=4, font=("Arial", 12), bg="#ffffff")
        self.lista_atividades.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.frame_lista, orient=tk.VERTICAL)
        self.scrollbar.config(command=self.lista_atividades.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lista_atividades.config(yscrollcommand=self.scrollbar.set)

        self.frame_botoes = tk.Frame(self, bg="#f1be40")
        self.frame_botoes.pack(pady=10)

        self.btn_adicionar = tk.Button(self.frame_botoes, text="Adicionar Atividades", command=self.adicionar_atividade, bg="#4CAF50", fg="white", font=("Arial", 10))
        self.btn_adicionar.pack(side=tk.LEFT, padx=4)

        self.btn_remover = tk.Button(self.frame_botoes, text="Remover Atividades", command=self.remover_atividade, bg="#F44336", fg="white", font=("Arial", 10))
        self.btn_remover.pack(side=tk.LEFT, padx=4)

        self.btn_calendario = tk.Button(self.frame_botoes, text="Calendário do mês", command=self.mostrar_calendario, bg="#aa6925", fg="white", font=("Arial", 10))
        self.btn_calendario.pack(side=tk.LEFT, padx=4)

        self.btn_quadro_rotina = tk.Button(self.frame_botoes, text="Quadro de Rotina", command=self.mostrar_quadro_rotina, bg="#3F51B5", fg="white", font=("Arial", 10))
        self.btn_quadro_rotina.pack(side=tk.LEFT, padx=4)

        self.btn_ver_estrelas = tk.Button(self.frame_botoes, text="Cofrinho de Estrelas",
            command=self.mostrar_estrelas, bg="#FF9800", fg="white", font=("Arial", 10))
        self.btn_ver_estrelas.pack(side=tk.LEFT, padx=4)

    def atualizar_lista_atividades(self):
        # Limpa a lista atual na interface (Listbox)
        self.lista_atividades.delete(0, tk.END)

        # Verifica se há atividades
        if self.atividades:  # Garantir que a lista de atividades não seja None e que contenha atividades
            for atividade in self.atividades:
                # Adiciona as atividades no formato desejado na lista
                self.lista_atividades.insert(
                    tk.END, f"{atividade['nome']} - {atividade['data']} - {atividade['hora']} - {atividade['estrelas']} estrelas"
                )
        else:
            # Se não houver atividades, exibe uma mensagem informando que não há atividades
            self.lista_atividades.insert(tk.END, "Nenhuma atividade adicionada.")

    def salvar_dados_crianca(self):
        dados = {
            "nome": self.nome_crianca,
            "foto": self.caminho_foto_crianca
        }
        with open("dados_crianca.json", "w") as file:
            json.dump(dados, file)

    def carregar_dados_crianca(self):
        if os.path.exists("dados_crianca.json"):
            with open("dados_crianca.json", "r") as file:
                dados = json.load(file)
                self.nome_crianca = dados.get("nome", "Nome da Criança")
                self.caminho_foto_crianca = dados.get("foto", None)

    def definir_nome(self):
        nome_janela = tk.Toplevel(self)
        nome_janela.title("Definir Nome")
        nome_janela.geometry("200x100")
        nome_janela.configure(bg="#FFCCCB")

        nome_label = tk.Label(nome_janela, text="Digite o nome da criança:", font=("Arial", 12), bg="#FFCCCB")
        nome_label.pack(pady=10)

        nome_entry = tk.Entry(nome_janela, font=("Arial", 12))
        nome_entry.pack(pady=5)

        def salvar_nome():
            self.nome_crianca = nome_entry.get() or "Nome da Criança"
            self.label_frase_boas_vindas.config(text=f"Olá, {self.nome_crianca}. O que vamos fazer hoje?")
            self.salvar_dados_crianca()  # Salvar dados ao definir nome
            nome_janela.destroy()

        btn_confirmar = tk.Button(nome_janela, text="Confirmar", command=salvar_nome, bg="#4CAF50", fg="white", font=("Arial", 12))
        btn_confirmar.pack(pady=20)

    def definir_foto_crianca(self):
        caminho_foto = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
        if caminho_foto:
            self.caminho_foto_crianca = caminho_foto
            self.salvar_dados_crianca()  # Salvar dados ao definir foto
            self.atualizar_foto_crianca()  # Atualiza a foto exibida

    def atualizar_foto_crianca(self):
        if self.caminho_foto_crianca:
            foto_crianca = Image.open(self.caminho_foto_crianca)
            foto_crianca = foto_crianca.resize((200, 100), Image.LANCZOS)
            self.foto_crianca_imagem = ImageTk.PhotoImage(foto_crianca)
            self.label_foto_crianca.config(image=self.foto_crianca_imagem)
            self.label_foto_crianca.image = self.foto_crianca_imagem
            self.label_frase_boas_vindas.config(text=f"Olá, {self.nome_crianca}. O que vamos fazer hoje?")
        else:
            self.label_frase_boas_vindas.config(text=f"O que vamos fazer hoje?")

    def criar_tabelas(self):
        # Conectar ao banco de dados
        conn = sqlite3.connect('atividades.db')
        cursor = conn.cursor()

        # Cria a tabela de atividades se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS atividades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                data TEXT,
                hora TEXT,
                imagem TEXT,
                estrelas INTEGER
            )
        ''')

        # Cria a tabela para o banco de estrelas se não existir
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS banco_estrelas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_estrelas INTEGER
            )
        ''')

        # Inicializa o banco de estrelas, se necessário
        cursor.execute("SELECT total_estrelas FROM banco_estrelas LIMIT 1")
        if cursor.fetchone() is None:
            cursor.execute("INSERT INTO banco_estrelas (total_estrelas) VALUES (0)")

        conn.commit()
        conn.close()

    def carregar_atividades_db(self):
        with sqlite3.connect('atividades.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nome, data, hora, imagem, estrelas FROM atividades")
            for row in cursor.fetchall():
                atividade = {
                    'nome': row[0],
                    'data': row[1],
                    'hora': row[2],
                    'imagem': row[3],
                    'estrelas': row[4]
                }
                self.atividades.append(atividade)  # Adiciona à lista de atividades
                #self.lista_atividades.insert(tk.END, f"{atividade['nome']} - {atividade['data']} às {atividade['hora']}")

    def salvar_atividade_db(self, atividade):
        conn = sqlite3.connect('atividades.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO atividades (nome, data, hora, imagem, estrelas) VALUES (?, ?, ?, ?, ?)''',
                       (atividade['nome'], atividade['data'], atividade['hora'], atividade['imagem'], atividade['estrelas']))
        conn.commit()
        conn.close()

    def mostrar_calendario(self):
        print("Tentando abrir o calendário...")  # Mensagem de depuração

        # Criar uma nova janela Toplevel para o calendário
        calendario_janela = tk.Toplevel(self)
        calendario_janela.title("Calendário de Atividades")
        calendario_janela.geometry("800x800")
        calendario_janela.configure(bg="#FFD700")

        # Criar um frame dentro da nova janela
        cal_frame = tk.Frame(calendario_janela, bg="#FFD700")
        cal_frame.pack(fill=tk.BOTH, expand=True)  # Preencher a janela

        # Criar o calendário
        self.calendario_selecionado = Calendar(
        cal_frame,
        firstweekday="sunday",
        locale='pt_BR',
        selectmode='day',
        year=self.data_atual.year,
        month=self.data_atual.month,
        day=self.data_atual.day,
        showweeknumbers=False,
        background="lightblue",
        foreground="black",
        selectbackground="purple",
        font=("Arial", 14)
    )

        # Empacotar o widget do calendário
        self.calendario_selecionado.pack(pady=20)

    # Função para mostrar as atividades do dia selecionado
    def ver_atividades():
        data_selecionada = self.calendario_selecionado.get_date()
        atividades_do_dia = self.carregar_atividades_do_dia(data_selecionada)

        if atividades_do_dia:
            atividades_texto = "\n".join(atividades_do_dia)
        else:
            atividades_texto = "Nenhuma atividade para este dia."

        messagebox.showinfo("Atividades do Dia", atividades_texto)

        # Botão para ver atividades do dia selecionado
        btn_ver_atividades = tk.Button(cal_frame, text="Ver Atividades do Dia", command=ver_atividades, bg="#4CAF50", fg="white")
        btn_ver_atividades.pack(pady=10)

        # Mensagem de depuração para verificar se o calendário foi criado
        print("Calendário criado na nova janela.")

    def mostrar_quadro_verAtividades(self):
        data_selecionada = self.calendario_selecionado.get_date()
        atividades_do_dia = [a for a in self.atividades if a['data'] == datetime.datetime.strptime(data_selecionada, '%m/%d/%y').strftime('%d/%m/%Y')]
        if atividades_do_dia:
            atividades_texto = "\n".join([f"{a['nome']} {a['hora']}" for a in atividades_do_dia])
            messagebox.showinfo("Atividades", atividades_texto)
        else:
            messagebox.showinfo("Sem atividades", "Nenhuma atividade para o dia selecionado.")

    def adicionar_atividade(self):
        self.janela_nova_atividade = tk.Toplevel(self)
        self.janela_nova_atividade.title("Nova Atividade")
        self.janela_nova_atividade.geometry("300x500")
        self.janela_nova_atividade.configure(bg="#FFCCCB")

        nome_label = tk.Label(self.janela_nova_atividade, text="Nome:", font=("Arial", 12), bg="#FFCCCB")
        nome_label.pack(pady=5)
        nome_entry = tk.Entry(self.janela_nova_atividade, font=("Arial", 12))
        nome_entry.pack(pady=5)

        estrelas_label = tk.Label(self.janela_nova_atividade, text="Estrelas:", font=("Arial", 12), bg="#FFCCCB")
        estrelas_label.pack(pady=5)
        estrelas_entry = tk.Entry(self.janela_nova_atividade, font=("Arial", 12))
        estrelas_entry.pack(pady=5)

        data_label = tk.Label(self.janela_nova_atividade, text="Data (DD/MM/AAAA):", font=("Arial", 12), bg="#FFCCCB")
        data_label.pack(pady=5)
        data_entry = tk.Entry(self.janela_nova_atividade, font=("Arial", 12))
        data_entry.pack(pady=5)
        # Vincula a função formatar_data ao campo de data
        data_entry.bind("<KeyRelease>", self.formatar_data)

        hora_label = tk.Label(self.janela_nova_atividade, text="Hora (HH:MM):", font=("Arial", 12), bg="#FFCCCB")
        hora_label.pack(pady=5)
        hora_entry = tk.Entry(self.janela_nova_atividade, font=("Arial", 12))
        hora_entry.pack(pady=5)
        # Vincula a função formatar_hora ao campo de hora
        hora_entry.bind("<KeyRelease>", self.formatar_hora)

        # Label para o campo de imagem
        imagem_label = tk.Label(self.janela_nova_atividade, text="Imagem:", font=("Arial", 12), bg="#FFCCCB")
        imagem_label.pack(pady=5)

        # Campo de entrada para o caminho da imagem
        self.imagem_entry = tk.Entry(self.janela_nova_atividade, font=("Arial", 12))
        self.imagem_entry.pack(pady=5)

        # Botão para selecionar a imagem
        btn_selecionar_imagem = tk.Button(self.janela_nova_atividade, text="Selecionar Imagem", command=self.selecionar_imagem, bg="#2196F3", fg="white")
        btn_selecionar_imagem.pack(pady=5)

        # Adicionar o botão de confirmar
        btn_confirmar = tk.Button(
            self.janela_nova_atividade,
            text="Confirmar",
            command=lambda: self.confirmar_atividade(
                nome_entry.get(),
                data_entry.get(),
                hora_entry.get(),
                self.imagem_entry.get(),
                estrelas_entry.get()
            ),
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        )
        btn_confirmar.pack(pady=10)

    def confirmar_atividade(self, nome, data, hora, imagem, estrelas):
        # Cria o dicionário da nova atividade
        nova_atividade = {
            'nome': nome,
            'data': data,
            'hora': hora,
            'imagem': imagem,
            'estrelas': estrelas
        }

        # Adiciona a nova atividade à lista de atividades
        self.atividades.append(nova_atividade)

        # Atualiza a lista de atividades na interface
        self.atualizar_lista_atividades()

        # Fecha a janela de nova atividade após a confirmação
        self.janela_nova_atividade.destroy()

    def selecionar_imagem(self):
        # Abre o diálogo para selecionar a imagem e insere o caminho no campo de entrada
        caminho_imagem = filedialog.askopenfilename(title="Selecione a imagem", filetypes=[("Imagens", "*.png;*.jpg;*.jpeg")])
        if caminho_imagem:
            self.imagem_entry.delete(0, tk.END)
            self.imagem_entry.insert(0, caminho_imagem)

    def salvar_atividade_db(self, atividade):
        conn = sqlite3.connect('atividades.db')
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO atividades (nome, data, hora, imagem, estrelas) 
            VALUES (?, ?, ?, ?, ?)
        ''', (atividade['nome'], atividade['data'], atividade['hora'], atividade['imagem'], atividade['estrelas']))

        conn.commit()
        conn.close()

        # Atualiza a interface após salvar no banco de dados
        self.lista_atividades.insert(tk.END, f"{atividade['nome']} - {atividade['data']} às {atividade['hora']}")

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

    def remover_atividade(self):
        selection = self.lista_atividades.curselection()
        if selection:
            indice = selection[0]
            atividade = self.atividades[indice]
            if atividade:
                # Remove do banco de dados
                self.remover_atividade_db(atividade)
                # Remove da lista de atividades
                self.atividades.remove(atividade)
                # Remove da interface
                self.lista_atividades.delete(indice)
                messagebox.showinfo("Removido", f"Atividade '{atividade['nome']}' removida com sucesso.")
            else:
                messagebox.showerror("Erro", "Atividade não encontrada na lista.")
        else:
            messagebox.showwarning("Atenção", "Selecione uma atividade para remover.")

    def remover_atividade_db(self, atividade):
        with sqlite3.connect('atividades.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM atividades WHERE nome = ?", (atividade['nome'],))
            conn.commit()

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

            check_var = tk.BooleanVar()
            check_button = tk.Checkbutton(frame_atividade, text="Tarefa cumprida", variable=check_var, 
            command=lambda a=atividade: self.completar_atividade(a))
            check_button.pack(anchor="w")

            caminho_imagem = atividade['imagem']
            if caminho_imagem is not None:
                try:
                    imagem_original = Image.open(caminho_imagem)
                    imagem = imagem_original.resize((200, 200), Image.LANCZOS)
                    imagem_tk = ImageTk.PhotoImage(imagem)
                    imagem_label = tk.Label(frame_atividade, image=imagem_tk, bg="#FFFACD")
                    imagem_label.image = imagem_tk  # manter uma referência
                    imagem_label.pack(side=tk.RIGHT)
                    imagem_original.close()
                except Exception as e:
                    print(e)

    def completar_atividade(self, atividade):
        try:
            estrelas = int(atividade['estrelas'])
        except ValueError:
            messagebox.showerror("Erro", "O valor de estrelas deve ser um número.")
            return

        # Incrementa as estrelas no total
        self.total_estrelas += estrelas
        self.atualizar_total_estrelas()  # Atualiza e salva o novo total de estrelas no banco

        messagebox.showinfo("Parabéns!", f"Você ganhou {estrelas} estrelas!")

        # Remover a atividade completada da lista de atividades
        indice = self.atividades.index(atividade)
        self.atividades.remove(atividade)
        self.lista_atividades.delete(indice)

        # Remove a atividade completada do banco de dados
        with sqlite3.connect('atividades.db') as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM atividades WHERE nome = ?", (atividade['nome'],))
            conn.commit()

    # def criar_tabelas(self):
    #     # Abre a conexão com o banco de dados
    #     conn = sqlite3.connect('atividades.db')
    #     cursor = conn.cursor()

    #     # Cria a tabela de atividades se não existir
    #     cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS atividades (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             nome TEXT,
    #             data TEXT,
    #             hora TEXT,
    #             imagem TEXT,
    #             estrelas INTEGER
    #         )
    #     ''')

    #     # Cria a tabela para o banco de estrelas se não existir
    #     cursor.execute('''
    #         CREATE TABLE IF NOT EXISTS banco_estrelas (
    #             id INTEGER PRIMARY KEY AUTOINCREMENT,
    #             total_estrelas INTEGER
    #         )
    #     ''')

    #     # Verifica se já existe um registro de estrelas, caso contrário, inicializa com 0
    #     cursor.execute("SELECT total_estrelas FROM banco_estrelas LIMIT 1")
    #     if cursor.fetchone() is None:
    #         cursor.execute("INSERT INTO banco_estrelas (total_estrelas) VALUES (0)")

    #     # Confirma as alterações e fecha a conexão
    #     conn.commit()
    #     conn.close()

    def carregar_total_estrelas(self):
        try:
            conn = sqlite3.connect('atividades.db')
            cursor = conn.cursor()

            # Carrega o total de estrelas do banco de dados
            cursor.execute("SELECT total_estrelas FROM banco_estrelas LIMIT 1")
            resultado = cursor.fetchone()

            if resultado:
                self.total_estrelas = resultado[0]
            else:
                self.total_estrelas = 0  # Caso não haja nenhum valor, inicialize com 0

        except Exception as e:
            print(f"Erro ao carregar total de estrelas: {e}")

        finally:
            conn.close()

    def atualizar_total_estrelas(self):
        with sqlite3.connect('atividades.db') as conn:
            cursor = conn.cursor()

            # Atualiza o total de estrelas no banco de dados
            cursor.execute("UPDATE banco_estrelas SET total_estrelas = ? WHERE id = 1", (self.total_estrelas,))

            conn.commit()

    def mostrar_estrelas(self):
        # Mostra o total de estrelas acumuladas
        messagebox.showinfo("Total de Estrelas", f"Você tem um total de {self.total_estrelas} estrelas.")

    def inicializar_banco_estrelas(self):
        # Inicializa o banco de estrelas, garantindo que haja um registro inicial
        with sqlite3.connect('atividades.db') as conn:
            cursor = conn.cursor()

            # Verifica se o banco de estrelas já tem um registro
            cursor.execute("SELECT COUNT(*) FROM banco_estrelas")
            if cursor.fetchone()[0] == 0:
                cursor.execute("INSERT INTO banco_estrelas (total_estrelas) VALUES (0)")
                conn.commit()

    def validar_data(self,data):
        try:
            datetime.datetime.strptime(data, '%d/%m/%Y')
            return True
        except ValueError:
            return False

if __name__ == "__main__":
    app = AgendaApp()
    app.mainloop()