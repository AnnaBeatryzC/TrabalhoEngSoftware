import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv

def relatorios(content_frame):
    # Limpa o frame de conteúdo
    for widget in content_frame.winfo_children():
        widget.destroy()

    title = tk.Label(content_frame, text="Relatórios", font=("Arial", 14))
    title.pack(pady=10)

    # Frame para opções de relatórios
    frame_opcoes = tk.Frame(content_frame)
    frame_opcoes.pack(pady=10)

    lbl_tipo_relatorio = tk.Label(frame_opcoes, text="Tipo de Relatório:", width=20, anchor='w')
    lbl_tipo_relatorio.pack(side=tk.LEFT)

    tipo_relatorio_var = tk.StringVar()
    tipo_relatorio_combo = ttk.Combobox(frame_opcoes, textvariable=tipo_relatorio_var, state="readonly", width=30)
    tipo_relatorio_combo["values"] = ["Estoque Atual", "Movimentações", "Componentes com Baixo Estoque"]
    tipo_relatorio_combo.pack(side=tk.LEFT, padx=5)
    tipo_relatorio_combo.current(0)

    btn_gerar = tk.Button(frame_opcoes, text="Gerar Relatório", command=lambda: gerar_relatorio(tipo_relatorio_var.get()))
    btn_gerar.pack(side=tk.LEFT, padx=10)

    # Frame para exibição dos dados
    frame_tabela = tk.Frame(content_frame)
    frame_tabela.pack(pady=20)

    colunas = []
    tree = ttk.Treeview(frame_tabela, columns=colunas, show="headings", height=15)
    tree.pack(side=tk.LEFT)

    scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=tree.yview)
    scrollbar.pack(side=tk.RIGHT, fill="y")
    tree.configure(yscrollcommand=scrollbar.set)

    # Função para gerar relatórios
    def gerar_relatorio(tipo_relatorio):
        # Limpar a tabela antes de gerar um novo relatório
        for col in tree["columns"]:
            tree.heading(col, text="")
            tree.column(col, width=0)
        tree.delete(*tree.get_children())

        if tipo_relatorio == "Estoque Atual":
            gerar_relatorio_estoque()
        elif tipo_relatorio == "Movimentações":
            gerar_relatorio_movimentacoes()
        elif tipo_relatorio == "Componentes com Baixo Estoque":
            gerar_relatorio_baixo_estoque()

    # Relatório de Estoque Atual
    def gerar_relatorio_estoque():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT nome, codigo, quantidade FROM componentes ORDER BY quantidade ASC")
        resultados = cursor.fetchall()
        conn.close()

        colunas_estoque = ["Nome", "Código", "Quantidade"]
        tree["columns"] = colunas_estoque
        for col in colunas_estoque:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for row in resultados:
            tree.insert("", tk.END, values=row)

        messagebox.showinfo("Relatório Gerado", "Relatório de Estoque Atual gerado com sucesso!")

    # Relatório de Movimentações
    def gerar_relatorio_movimentacoes():
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Exemplo de estrutura básica de movimentações (você pode ajustar a tabela de movimentações se necessário)
        cursor.execute("""
            SELECT data_movimentacao, codigo_componente, tipo_movimentacao, quantidade
            FROM movimentacoes
            ORDER BY data_movimentacao DESC
        """)
        resultados = cursor.fetchall()
        conn.close()

        colunas_movimentacoes = ["Data", "Código do Componente", "Tipo", "Quantidade"]
        tree["columns"] = colunas_movimentacoes
        for col in colunas_movimentacoes:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for row in resultados:
            tree.insert("", tk.END, values=row)

        messagebox.showinfo("Relatório Gerado", "Relatório de Movimentações gerado com sucesso!")

    # Relatório de Componentes com Baixo Estoque
    def gerar_relatorio_baixo_estoque():
        # Definir limite de baixo estoque
        limite = 25
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT nome, codigo, quantidade FROM componentes WHERE quantidade < ? ORDER BY quantidade ASC", (limite,))
        resultados = cursor.fetchall()
        conn.close()

        colunas_baixo_estoque = ["Nome", "Código", "Quantidade"]
        tree["columns"] = colunas_baixo_estoque
        for col in colunas_baixo_estoque:
            tree.heading(col, text=col)
            tree.column(col, width=150)

        for row in resultados:
            tree.insert("", tk.END, values=row)

        if resultados:
            messagebox.showinfo("Relatório Gerado", "Relatório de Componentes com Baixo Estoque gerado com sucesso!")
        else:
            messagebox.showinfo("Relatório Gerado", "Todos os componentes estão com estoque suficiente.")

    # Exportar relatório para CSV
    def exportar_csv():
        arquivo = filedialog.asksaveasfilename(defaultextension=".csv",
                                               filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                                               title="Salvar Relatório")
        if not arquivo:
            return

        with open(arquivo, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(tree["columns"])  # Escreve os cabeçalhos
            for row_id in tree.get_children():
                row = tree.item(row_id)["values"]
                writer.writerow(row)

        messagebox.showinfo("Exportação Concluída", f"Relatório exportado para {arquivo}")

    btn_exportar = tk.Button(content_frame, text="Exportar para CSV", command=exportar_csv)
    btn_exportar.pack(pady=10)

    
