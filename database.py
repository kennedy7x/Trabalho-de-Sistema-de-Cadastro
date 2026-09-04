import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()

    def connect(self):
        """Estabelece a conexão com o banco de dados"""
        try:
            self.conn = sqlite3.connect('cadastro.db')
            self.cursor = self.conn.cursor()
            print("Conectado ao banco de dados com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")

    def create_tables(self):
        """Cria as tabelas necessárias"""
        try:
            # Tabela de pessoas
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS pessoas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome_completo TEXT NOT NULL,
                    cpf_cnpj TEXT UNIQUE NOT NULL,
                    email TEXT NOT NULL,
                    celular TEXT NOT NULL,
                    cep TEXT NOT NULL,
                    logradouro TEXT NOT NULL,
                    numero TEXT NOT NULL,
                    complemento TEXT,
                    bairro TEXT NOT NULL,
                    cidade TEXT NOT NULL,
                    estado TEXT NOT NULL,
                    tipo_pessoa TEXT NOT NULL,
                    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.conn.commit()
            print("Tabela 'pessoas' criada/verificada com sucesso!")
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")

    def insert_pessoa(self, dados):
        """Insere uma nova pessoa no banco de dados"""
        try:
            self.cursor.execute('''
                INSERT INTO pessoas 
                (nome_completo, cpf_cnpj, email, celular, cep, logradouro, 
                 numero, complemento, bairro, cidade, estado, tipo_pessoa)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                dados['nome_completo'],
                dados['cpf_cnpj'],
                dados['email'],
                dados['celular'],
                dados['cep'],
                dados['logradouro'],
                dados['numero'],
                dados['complemento'],
                dados['bairro'],
                dados['cidade'],
                dados['estado'],
                dados['tipo_pessoa']
            ))
            self.conn.commit()
            return True, "Pessoa cadastrada com sucesso!"
        except sqlite3.IntegrityError:
            return False, "Erro: CPF/CNPJ já cadastrado!"
        except sqlite3.Error as e:
            return False, f"Erro ao salvar: {e}"

    def get_all_pessoas(self):
        """Retorna todas as pessoas cadastradas"""
        try:
            self.cursor.execute('''
                SELECT id, nome_completo, cpf_cnpj, email, celular, 
                       cep, logradouro, numero, complemento, bairro, 
                       cidade, estado, tipo_pessoa,
                       datetime(data_cadastro, 'localtime') as data_cadastro
                FROM pessoas 
                ORDER BY id DESC
            ''')
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar pessoas: {e}")
            return []

    def get_pessoa_by_cpf_cnpj(self, cpf_cnpj):
        """Busca uma pessoa pelo CPF/CNPJ"""
        try:
            self.cursor.execute('''
                SELECT * FROM pessoas WHERE cpf_cnpj = ?
            ''', (cpf_cnpj,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao buscar pessoa: {e}")
            return None

    def update_pessoa(self, id, dados):
        """Atualiza uma pessoa existente"""
        try:
            self.cursor.execute('''
                UPDATE pessoas 
                SET nome_completo = ?, email = ?, celular = ?, 
                    cep = ?, logradouro = ?, numero = ?, 
                    complemento = ?, bairro = ?, cidade = ?, 
                    estado = ?, tipo_pessoa = ?, data_atualizacao = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (
                dados['nome_completo'],
                dados['email'],
                dados['celular'],
                dados['cep'],
                dados['logradouro'],
                dados['numero'],
                dados['complemento'],
                dados['bairro'],
                dados['cidade'],
                dados['estado'],
                dados['tipo_pessoa'],
                id
            ))
            self.conn.commit()
            return True, "Pessoa atualizada com sucesso!"
        except sqlite3.Error as e:
            return False, f"Erro ao atualizar: {e}"

    def delete_pessoa(self, id):
        """Remove uma pessoa do banco de dados"""
        try:
            self.cursor.execute('DELETE FROM pessoas WHERE id = ?', (id,))
            self.conn.commit()
            return True, "Pessoa removida com sucesso!"
        except sqlite3.Error as e:
            return False, f"Erro ao remover: {e}"

    def search_pessoas(self, termo):
        """Busca pessoas por nome ou CPF/CNPJ"""
        try:
            self.cursor.execute('''
                SELECT id, nome_completo, cpf_cnpj, email, celular, 
                       cep, logradouro, numero, complemento, bairro, 
                       cidade, estado, tipo_pessoa
                FROM pessoas 
                WHERE nome_completo LIKE ? OR cpf_cnpj LIKE ?
                ORDER BY nome_completo
            ''', (f'%{termo}%', f'%{termo}%'))
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Erro ao buscar pessoas: {e}")
            return []

    def close(self):
        """Fecha a conexão com o banco de dados"""
        if self.conn:
            self.conn.close()
            print("Conexão com o banco de dados fechada.")

    def __del__(self):
        """Destrutor para garantir que a conexão seja fechada"""
        self.close()

    def get_pessoa_by_id(self, id):
        """Busca uma pessoa pelo ID"""
        try:
            self.cursor.execute('''
                SELECT * FROM pessoas WHERE id = ?
            ''', (id,))
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Erro ao buscar pessoa: {e}")
            return None