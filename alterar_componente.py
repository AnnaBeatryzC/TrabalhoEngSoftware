import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def alterar_componente(content_frame):
    # Limpa o frame de conteúdo
    for widget in content_frame.winfo_children():
        widget.destroy()

    title = tk.Label(content_frame, text="Alterar Componente", font=("Arial", 14, "bold"), bg="#ffffff", fg="#4b6da1")
    title.pack(pady=(10, 20))

    # Selecionar o componente pelo código
    frame_codigo = tk.Frame(content_frame)
    frame_codigo.pack(pady=5)
    lbl_codigo = tk.Label(frame_codigo, text="Código do Componente:", width=20, anchor='w')
    lbl_codigo.pack(side=tk.LEFT)

    codigo_var = tk.StringVar()
    codigo_combo = ttk.Combobox(frame_codigo, textvariable=codigo_var, width=40, state="readonly")
    codigo_combo.pack(side=tk.LEFT)

    # Preencher os códigos dos componentes
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT codigo FROM componentes")
    codigos = [row[0] for row in cursor.fetchall()]
    conn.close()
    codigo_combo["values"] = codigos

    # Selecionar o campo a ser alterado
    frame_campo = tk.Frame(content_frame)
    frame_campo.pack(pady=5)
    lbl_campo = tk.Label(frame_campo, text="Campo a Alterar:", width=20, anchor='w')
    lbl_campo.pack(side=tk.LEFT)

    campo_var = tk.StringVar()
    campo_combo = ttk.Combobox(frame_campo, textvariable=campo_var, width=40, state="readonly")
    campo_combo["values"] = ["Nome", "Fabricante", "Categoria", "Subcategoria", 
                             "Especificações Técnicas", "Fornecedor", "Preço de Custo", "Preço de Venda"]
    campo_combo.pack(side=tk.LEFT)

    # Campo para inserir o novo valor
    frame_novo_valor = tk.Frame(content_frame)
    frame_novo_valor.pack(pady=5)
    lbl_novo_valor = tk.Label(frame_novo_valor, text="Novo Valor:", width=20, anchor='w')
    lbl_novo_valor.pack(side=tk.LEFT)

    novo_valor_entry = tk.Entry(frame_novo_valor, width=40)
    novo_valor_entry.pack(side=tk.LEFT)

    # Função para salvar a alteração
    def salvar_alteracao():
        codigo = codigo_var.get()
        campo = campo_var.get()
        novo_valor = novo_valor_entry.get()

        if not codigo or not campo or not novo_valor:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
            return

        try:
            # Mapear o campo escolhido para a coluna no banco de dados
            mapa_campos = {
                "Nome": "nome",
                "Fabricante": "fabricante",
                "Categoria": "categoria",
                "Subcategoria": "subcategoria",
                "Especificações Técnicas": "especificacoes",
                "Fornecedor": "fornecedor",
                "Preço de Custo": "preco_custo",
                "Preço de Venda": "preco_venda"
            }

            coluna = mapa_campos.get(campo)

            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            # Atualizar o valor no banco de dados
            if campo in ["Preço de Custo", "Preço de Venda"]:
                novo_valor = float(novo_valor)  # Validação para campos numéricos
                cursor.execute(f"UPDATE componentes SET {coluna} = ? WHERE codigo = ?", (novo_valor, codigo))
            else:
                cursor.execute(f"UPDATE componentes SET {coluna} = ? WHERE codigo = ?", (novo_valor, codigo))

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", f"{campo} atualizado com sucesso!")
            novo_valor_entry.delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Erro", "Preço de Custo e Preço de Venda devem ser valores numéricos!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro ao salvar: {e}")

    # Botão para salvar
    btn_salvar = tk.Button(content_frame, text="Salvar Alteração", command=salvar_alteracao)
    btn_salvar.pack(pady=10)

