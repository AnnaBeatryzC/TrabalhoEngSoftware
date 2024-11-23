import tkinter as tk
from tkinter import messagebox
from database import connect
from PIL import Image, ImageTk #Tem que instalar o Pillow apartir do pip install Pillow no terminal
import importlib

class SistemaLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - ElectroStore")
        self.root.geometry("400x400")
        self.root.minsize(400, 400) #Adicionar um limite minimo de tamanho para a janela
        self.root.configure(bg="#82a3db")  # Fundo azul claro

        # Adicionando o Ícone na Barra de Título
        try:
            icon_img = Image.open("logoElectostore.png").resize((16, 16))
            icon = ImageTk.PhotoImage(icon_img)
            self.root.iconphoto(False, icon)  # Ícone da barra de título
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")

        # Frame central para o conteúdo
        frame = tk.Frame(self.root, bg="#ffffff", relief="flat", bd=0)
        frame.place(relx=0.5, rely=0.5, anchor="center", width=320, height=350)

        # Adicionando a Logo
        try:
            logo_img = Image.open("logoElectostore.png").resize((100, 100))
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(frame, image=self.logo, bg="#ffffff")
            logo_label.image = self.logo  # Mantém a referência
            logo_label.pack(pady=(5, 10))  # Posiciona no topo do frame branco
        except Exception as e:
            print(f"Erro ao carregar logo: {e}")

        titulo = tk.Label(frame, text="LOGIN", font=("Arial", 14, "bold"), bg="#ffffff", fg="#4b6da1")
        titulo.pack(pady=(10, 20))

        # Campo Username com o texto "Usuário"
        username_frame = tk.Frame(frame, bg="#ffffff")
        username_frame.pack(fill="x", padx=20, pady=5)

        username_label = tk.Label(username_frame, text="Usuário", font=("Arial", 12), bg="#ffffff", fg="#4b6da1", width=8, anchor="w")
        username_label.pack(side="left")
        self.usuario_entry = tk.Entry(username_frame, font=("Arial", 12), relief="flat", bg="#f3f4f6", fg="#4b6da1")
        self.usuario_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))

        tk.Frame(username_frame, bg="#4b6da1", height=1).pack(fill="x", pady=(5, 0))

        # Campo Password com o texto "Senha"
        password_frame = tk.Frame(frame, bg="#ffffff")
        password_frame.pack(fill="x", padx=20, pady=10)

        password_label = tk.Label(password_frame, text="Senha", font=("Arial", 12), bg="#ffffff", fg="#4b6da1", width=8, anchor="w")
        password_label.pack(side="left")
        self.senha_entry = tk.Entry(password_frame, font=("Arial", 12), show="*", relief="flat", bg="#f3f4f6", fg="#4b6da1")
        self.senha_entry.pack(side="left", fill="x", expand=True, padx=(5, 0))

        tk.Frame(password_frame, bg="#4b6da1", height=1).pack(fill="x", pady=(5, 0))

        # Botão de Login
        botao_entrar = tk.Button(
            frame,
            text="LOGIN",
            font=("Arial", 12, "bold"),
            bg="#4b6da1",
            fg="white",
            activebackground="#365880",
            activeforeground="white",
            relief="flat",
            command=self.verificar_login
        )
        botao_entrar.pack(fill="x", padx=20, pady=20)

    def verificar_login(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        conexao = connect()
        cursor = conexao.cursor()
        cursor.execute(
            """
            SELECT * FROM funcionarios WHERE usuario = ? AND senha = ?
        """,
            (usuario, senha),
        )

        resultado = cursor.fetchone()
        conexao.close()

        if resultado:
            self.nivel_acesso = resultado[4]  # Nível do usuário
            messagebox.showinfo("Login Bem-Sucedido", f"Bem-vindo, {usuario}!")
            self.abrir_dashboard()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha incorretos!")

    def abrir_dashboard(self):
        # Fecha a tela de login
        self.root.destroy()

        # Usando importlib para importar e rodar o App de forma dinâmica
        app_module = importlib.import_module("main")  # Importa dinamicamente o módulo main
        app = app_module.App(nivel_acesso=self.nivel_acesso)  # Cria uma instância da classe App de main.py
        app.mainloop()  # Roda o loop principal da aplicação


if __name__ == "__main__":
    root = tk.Tk()
    SistemaLogin(root)
    root.mainloop()
