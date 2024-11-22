import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Função para atualizar a quantidade no estoque
def update_stock(codigo, quantidade, operacao):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Verificar se o componente existe
        cursor.execute("SELECT quantidade FROM componentes WHERE codigo = ?", (codigo,))
        resultado = cursor.fetchone()

        if resultado is None:
            messagebox.showerror("Erro", "Componente não encontrado!")
            return False

        quantidade_atual = resultado[0]

        # Atualizar quantidade com base na operação (entrada ou saída)
        if operacao == "entrada":
            nova_quantidade = quantidade_atual + quantidade
        elif operacao == "saida":
            if quantidade_atual < quantidade:
                messagebox.showerror("Erro", "Quantidade insuficiente em estoque!")
                return False
            nova_quantidade = quantidade_atual - quantidade
        else:
            messagebox.showerror("Erro", "Operação inválida!")
            return False

        # Atualizar a quantidade no banco de dados
        cursor.execute("UPDATE componentes SET quantidade = ? WHERE codigo = ?", 
                       (nova_quantidade, codigo))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao atualizar estoque: {e}")
        return False

# Função para criar a interface de controle de estoque
def controle_estoque(content_frame):
    for widget in content_frame.winfo_children():
        widget.destroy()

    title = tk.Label(content_frame, text="Controle de Estoque", font=("Arial", 14))
    title.pack(pady=10)

    # Formulário para entrada/saída de estoque
    frame_codigo = tk.Frame(content_frame)
    frame_codigo.pack(pady=5)
    lbl_codigo = tk.Label(frame_codigo, text="Código do Componente:", width=20, anchor='w')
    lbl_codigo.pack(side=tk.LEFT)

    # Combobox para selecionar o código do componente
    codigo_var = tk.StringVar()
    codigo_combo = ttk.Combobox(frame_codigo, textvariable=codigo_var, width=40, state="readonly")
    codigo_combo.pack(side=tk.LEFT)

    # Preenchendo os códigos dos componentes cadastrados
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT codigo FROM componentes")
    codigos = [row[0] for row in cursor.fetchall()]
    conn.close()
    codigo_combo["values"] = codigos

    frame_quantidade = tk.Frame(content_frame)
    frame_quantidade.pack(pady=5)
    lbl_quantidade = tk.Label(frame_quantidade, text="Quantidade:", width=20, anchor='w')
    lbl_quantidade.pack(side=tk.LEFT)
    entry_quantidade = tk.Entry(frame_quantidade, width=40)
    entry_quantidade.pack(side=tk.LEFT)

    # Função de atualização de estoque
    def registrar_entrada():
        codigo = codigo_var.get()
        try:
            quantidade = int(entry_quantidade.get())
            if update_stock(codigo, quantidade, "entrada"):
                messagebox.showinfo("Sucesso", "Entrada registrada com sucesso!")
                entry_quantidade.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro!")

    def registrar_saida():
        codigo = codigo_var.get()
        try:
            quantidade = int(entry_quantidade.get())
            if update_stock(codigo, quantidade, "saida"):
                messagebox.showinfo("Sucesso", "Saída registrada com sucesso!")
                entry_quantidade.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro!")

    # Botões de ação
    btn_entrada = tk.Button(content_frame, text="Registrar Entrada", command=registrar_entrada)
    btn_entrada.pack(pady=5)

    btn_saida = tk.Button(content_frame, text="Registrar Saída", command=registrar_saida)
    btn_saida.pack(pady=5)

    # Botão para atualizar os códigos no combobox
    def atualizar_codigos():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("SELECT codigo FROM componentes")
        novos_codigos = [row[0] for row in cursor.fetchall()]
        conn.close()
        codigo_combo["values"] = novos_codigos
        messagebox.showinfo("Atualizado", "Lista de códigos atualizada!")

    btn_atualizar = tk.Button(content_frame, text="Atualizar Lista de Códigos", command=atualizar_codigos)
    btn_atualizar.pack(pady=5)
