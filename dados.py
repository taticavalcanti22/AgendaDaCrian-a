import sqlite3

class BancoDados:
    def __init__(self,):
        self.arquivo = 'atividades.db'
    
    def criar_tabelas(self):
        # Conectar ao banco de dados
        conn = sqlite3.connect(self.arquivo)
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
        atividades = []
        with sqlite3.connect(self.arquivo) as conn:
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
                atividades.append(atividade)
        return atividades
    
    def salvar_atividade_db(self, atividade):
        print("Função salvar_atividade_db foi chamada!")  # Diagnóstico inicial
        try:
            conn = sqlite3.connect(self.arquivo)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO atividades (nome, data, hora, imagem, estrelas)
                VALUES (?, ?, ?, ?, ?)
            ''', (atividade['nome'], atividade['data'], atividade['hora'], atividade['imagem'], atividade['estrelas']))

            conn.commit()
            conn.close()

            print(f"Atividade '{atividade['nome']}' salva com sucesso no banco de dados.")
            return True
        except Exception as e:
            print(f"Erro ao salvar atividade: {e}")
            return False
        
    def remover_atividade_db(self, atividade):
        with sqlite3.connect(self.arquivo) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM atividades WHERE nome = ?", (atividade['nome'],))
            conn.commit()

    def atualizar_total_estrelas(self, total_estrelas):
        with sqlite3.connect(self.arquivo) as conn:
            cursor = conn.cursor()

            # Atualiza o total de estrelas no banco de dados
            cursor.execute("UPDATE banco_estrelas SET total_estrelas = ? WHERE id = 1", (total_estrelas,))

            conn.commit()
    
    def carregar_total_estrelas(self):
        total_estrelas = -1
        try:
            conn = sqlite3.connect(self.arquivo)
            cursor = conn.cursor()

            # Carrega o total de estrelas do banco de dados
            cursor.execute("SELECT total_estrelas FROM banco_estrelas LIMIT 1")
            resultado = cursor.fetchone()

            if resultado:
                total_estrelas = resultado[0]
            else:
                total_estrelas = 0  # Caso não haja nenhum valor, inicialize com 0

        except Exception as e:
            print(f"Erro ao carregar total de estrelas: {e}")

        finally:
            conn.close()
            return total_estrelas