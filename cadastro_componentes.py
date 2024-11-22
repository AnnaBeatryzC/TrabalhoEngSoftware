import tkinter as tk
from tkinter import ttk, messagebox
from utils import save_component
import sqlite3

def cadastro_componentes(content_frame):
    # Limpa o frame de conteúdo
    for widget in content_frame.winfo_children():
        widget.destroy()

    title = tk.Label(content_frame, text="Cadastro de Componentes", font=("Arial", 14))
    title.pack(pady=10)

    # Labels dos campos
    labels = ["Nome", "Código", "Fabricante", "Categoria", "Subcategoria", 
              "Especificações Técnicas", "Fornecedor", "Preço de Custo", "Preço de Venda"]

    # Dicionário para armazenar entradas
    entries = {}
    for label in labels:
        if label in ["Fabricante", "Fornecedor"]:
            frame = tk.Frame(content_frame)
            frame.pack(pady=5)
            lbl = tk.Label(frame, text=label, width=20, anchor='w')
            lbl.pack(side=tk.LEFT)
            
            var = tk.StringVar()
            combo = ttk.Combobox(frame, textvariable=var, width=40, state="normal")
            combo.pack(side=tk.LEFT)

            # Preenchendo valores já cadastrados no banco de dados
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()
            if label == "Fabricante":
                cursor.execute("SELECT DISTINCT fabricante FROM componentes WHERE fabricante IS NOT NULL")
            elif label == "Fornecedor":
                cursor.execute("SELECT DISTINCT nome FROM fornecedores WHERE nome IS NOT NULL")
            
            valores = [row[0] for row in cursor.fetchall()]
            conn.close()
            
            combo["values"] = valores
            entries[label] = var
        else:
            frame = tk.Frame(content_frame)
            frame.pack(pady=5)
            lbl = tk.Label(frame, text=label, width=20, anchor='w')
            lbl.pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=40)
            entry.pack(side=tk.LEFT)
            entries[label] = entry

    # Função para salvar o componente
    def submit():
        try:
            preco_custo = float(entries["Preço de Custo"].get())
            preco_venda = float(entries["Preço de Venda"].get())
        except ValueError:
            messagebox.showerror("Erro", "Preço de custo e venda devem ser numéricos.")
            return

        data = (
            entries["Nome"].get(),
            entries["Código"].get(),
            entries["Fabricante"].get(),
            entries["Categoria"].get(),
            entries["Subcategoria"].get(),
            entries["Especificações Técnicas"].get(),
            entries["Fornecedor"].get(),
            preco_custo,
            preco_venda
        )

        if save_component(data):
            messagebox.showinfo("Sucesso", "Componente cadastrado com sucesso!")
            for entry in entries.values():
                if isinstance(entry, tk.StringVar):
                    entry.set("")  # Limpa combobox
                else:
                    entry.delete(0, tk.END)

    # Botão para salvar componente
    submit_button = tk.Button(content_frame, text="Salvar Componente", command=submit)
    submit_button.pack(pady=10)

    # Botão para atualizar listas de Fabricantes e Fornecedores
    def atualizar_listas():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Atualizar fabricantes
        cursor.execute("SELECT DISTINCT fabricante FROM componentes WHERE fabricante IS NOT NULL")
        novos_fabricantes = [row[0] for row in cursor.fetchall()]
        entries["Fabricante"].set("")
        entries["Fabricante"].trace_vdelete("w", entries["Fabricante"].trace_vinfo()[0])
        ttk.Combobox(content_frame, textvariable=entries["Fabricante"], values=novos_fabricantes)

        # Atualizar fornecedores
        cursor.execute("SELECT DISTINCT nome FROM fornecedores WHERE nome IS NOT NULL")
        novos_fornecedores = [row[0] for row in cursor.fetchall()]
        entries["Fornecedor"].set("")
        entries["Fornecedor"].trace_vdelete("w", entries["Fornecedor"].trace_vinfo()[0])
        ttk.Combobox(content_frame, textvariable=entries["Fornecedor"], values=novos_fornecedores)

        conn.close()
        messagebox.showinfo("Atualizado", "Listas de Fabricantes e Fornecedores atualizadas!")

    atualizar_button = tk.Button(content_frame, text="Atualizar Listas", command=atualizar_listas)
    atualizar_button.pack(pady=10)
