import tkinter as tk
from tkinter import messagebox
import secrets
import string

# Função para gerar uma senha segura e aleatória
def gerar_senha():
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(secrets.choice(caracteres) for _ in range(12))
    return senha

# Função para gerar o código PowerShell
def gerar_codigo():
    nome_completo = entry_nome_completo.get()
    user_logon = entry_user_logon.get()
    cargo = entry_cargo.get()
    departamento = entry_departamento.get()
    empresa = entry_empresa.get()
    manager = entry_manager.get()

    # Verifica se todos os campos estão preenchidos
    if not (nome_completo and user_logon and cargo and departamento and empresa and manager):
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    senha = entry_senha.get()  # A senha agora é pega diretamente do campo da senha gerada

    # Gerar código PowerShell para criação do usuário no AD
    codigo_powershell = f"""
New-ADUser -Name "{nome_completo}" -GivenName "{nome_completo.split()[0]}" -Surname "{nome_completo.split()[-1]}" -SamAccountName "{user_logon}" -UserPrincipalName "{user_logon}@dominio.local" -Title "{cargo}" -Department "{departamento}" -Company "{empresa}" -Manager "{manager}" -AccountPassword (ConvertTo-SecureString "{senha}" -AsPlainText -Force) -Enabled $true
"""
    # Exibir o código gerado e a senha
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"Senha Gerada: {senha}\n\nCódigo PowerShell:\n{codigo_powershell}")

# Função para gerar e preencher a senha automaticamente
def preencher_senha(event):
    senha = gerar_senha()
    entry_senha.delete(0, tk.END)
    entry_senha.insert(0, senha)

# Função para preencher automaticamente o campo de User Logon Name com base no Nome Completo
def preencher_user_logon(event):
    nome_completo = entry_nome_completo.get()
    if nome_completo:
        # Supondo que o nome completo seja composto por nome e sobrenome
        nome_parts = nome_completo.split()
        if len(nome_parts) >= 2:
            user_logon = nome_parts[0][0].lower() + nome_parts[-1].lower()  # Primeira letra do primeiro nome + sobrenome
            entry_user_logon.delete(0, tk.END)
            entry_user_logon.insert(0, user_logon)

# Criação da interface gráfica
app = tk.Tk()
app.title("Elysium - Gerenciamento de Usuários")
app.geometry("600x750")  # Aumentando o tamanho da janela para dar mais espaço

# Configuração da cor de fundo
app.configure(bg="black")

# Nome do Projeto Elysium centralizado na parte superior
title_label = tk.Label(app, text="ELYSIUM", fg="white", bg="black", font=("Arial", 16, "bold"))
title_label.place(relx=0.5, y=20, anchor="center")

# Labels e Entradas
labels_text = ["Nome Completo", "Nome de Logon", "Cargo", "Departamento", "Empresa", "Gerente", "Senha"]
entries = []

# Definindo a distância entre os campos para evitar sobreposição
espaco_vertical = 60

for i, text in enumerate(labels_text):
    label = tk.Label(app, text=text, fg="white", bg="black", font=("Arial", 10, "bold"))
    label.place(relx=0.5, y=80 + (i * espaco_vertical), anchor="center")  # Centraliza os labels

    entry = tk.Entry(app, width=40, bg="#2b2b2b", fg="white")
    entry.place(relx=0.5, y=100 + (i * espaco_vertical), anchor="center")  # Centraliza os campos de entrada
    entries.append(entry)

entry_nome_completo, entry_user_logon, entry_cargo, entry_departamento, entry_empresa, entry_manager, entry_senha = entries

# Bind para gerar a senha automaticamente quando o campo "Manager" perder o foco
entry_manager.bind("<FocusOut>", preencher_senha)

# Bind para preencher o User Logon Name automaticamente ao digitar o Nome Completo
entry_nome_completo.bind("<KeyRelease>", preencher_user_logon)

# Botão para gerar o código PowerShell (ajustado para uma posição centralizada)
button_gerar = tk.Button(app, text="Gerar Código PowerShell", command=gerar_codigo, bg="#3498db", fg="white", font=("Arial", 10, "bold"))
button_gerar.place(relx=0.5, y=500, anchor="center")  # Colocando o botão em uma posição correta

# Textbox para mostrar a senha gerada e o código PowerShell (deslocado mais para baixo)
result_text = tk.Text(app, width=60, height=10, wrap="word", bg="#2b2b2b", fg="white")
result_text.place(relx=0.5, y=640, anchor="center")  # Abaixando a posição da caixa de resultado para ficar abaixo do botão

# Função para redimensionar a interface de forma responsiva
def on_resize(event):
    largura, altura = event.width, event.height
    # Reajustar a posição dos elementos com base no tamanho da janela
    title_label.place(relx=0.5, y=20)
    for i, label in enumerate(labels_text):
        label.place(relx=0.5, y=80 + (i * espaco_vertical), anchor="center")
        entries[i].place(relx=0.5, y=100 + (i * espaco_vertical), anchor="center")
    button_gerar.place(relx=0.5, y=500)
    result_text.place(relx=0.5, y=640)

# Conectar a função de redimensionamento
app.bind("<Configure>", on_resize)

# Executar a interface
app.mainloop()
