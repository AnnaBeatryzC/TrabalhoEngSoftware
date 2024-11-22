import sqlite3


def connect():
    return sqlite3.connect('database.db')

def initialize_db():
    # Conecta ao banco de dados
    conn = connect()
    cursor = conn.cursor()

    # Tabela de funcionários
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS funcionarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            usuario TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL,
            nivel INTEGER NOT NULL
        )
    """)

    # Criação da tabela de componentes
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS componentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            codigo TEXT UNIQUE,
            fabricante TEXT,
            categoria TEXT,
            subcategoria TEXT,
            especificacoes TEXT,
            fornecedor TEXT,
            preco_custo REAL,
            preco_venda REAL,
            quantidade INTEGER DEFAULT 0
        )
    ''')

    # Criação da tabela de fornecedores
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fornecedores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cnpj TEXT UNIQUE,
            email TEXT,
            telefone TEXT,
            endereco TEXT
        )
    ''')

    # Criação da tabela de movimentações
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimentacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_movimentacao TEXT,
            codigo_componente TEXT,
            tipo_movimentacao TEXT,
            quantidade INTEGER
        )
    ''')

    conn.commit()
    conn.close()

# Inicializar o banco de dados
if __name__ == "__main__":
    initialize_db()