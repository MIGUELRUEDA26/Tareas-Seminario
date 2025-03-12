import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
import threading

API_KEY = "sk-53751d5c6f344a5dbc0571de9f51313e"
API_URL = "https://api.deepseek.com/v1/chat/completions"

animacion_activa = False

def enviar_mensaje():
    global animacion_activa
    mensaje_usuario = entrada_texto.get()
    if not mensaje_usuario:
        return
    
    mostrar_mensaje_usuario(mensaje_usuario)
    entrada_texto.delete(0, tk.END)
    
    animacion_activa = True
    mostrar_mensaje_cargando()
    
    threading.Thread(target=obtener_respuesta_api_y_mostrar, args=(mensaje_usuario,)).start()

def mostrar_mensaje_usuario(mensaje):
    cuadro_chat.config(state=tk.NORMAL)
    cuadro_chat.insert(tk.END, f"\nUsuario:\n", "usuario")
    cuadro_chat.insert(tk.END, f"{mensaje}\n", "usuario_texto")
    cuadro_chat.insert(tk.END, "\n", "espacio")
    cuadro_chat.config(state=tk.DISABLED)
    cuadro_chat.yview(tk.END)

def animar_mensaje_cargando(index=0):
    global animacion_activa
    mensaje = "Buscando películas y series..."
    if animacion_activa:
        if index < len(mensaje):
            cuadro_chat.config(state=tk.NORMAL)
            cuadro_chat.insert(tk.END, mensaje[index], "cargando")
            cuadro_chat.config(state=tk.DISABLED)
            cuadro_chat.yview(tk.END)
            root.after(50, animar_mensaje_cargando, index + 1)
        else:
            cuadro_chat.config(state=tk.NORMAL)
            cuadro_chat.delete("cargando.first", "cargando.last")
            cuadro_chat.config(state=tk.DISABLED)
            root.after(50, animar_mensaje_cargando)

def mostrar_mensaje_cargando():
    cuadro_chat.config(state=tk.NORMAL)
    cuadro_chat.insert(tk.END, f"\nChatbot:\n", "chatbot")
    cuadro_chat.config(state=tk.DISABLED)
    animar_mensaje_cargando()

def obtener_respuesta_api_y_mostrar(mensaje):
    global animacion_activa
    respuesta_chatbot = obtener_respuesta_api(mensaje)
    
    animacion_activa = False
    
    cuadro_chat.config(state=tk.NORMAL)
    cuadro_chat.delete("cargando.first", "cargando.last")
    cuadro_chat.config(state=tk.DISABLED)
    
    respuesta_formateada = formatear_respuesta(respuesta_chatbot)
    mostrar_mensaje_chatbot(respuesta_formateada)

def obtener_respuesta_api(mensaje):
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'deepseek-chat',
        'messages': [
            {'role': 'system', 'content': 'Eres un experto en recomendaciones de películas y series. Proporciona respuestas detalladas que incluyan el título, año de publicación, género, actores principales y un resumen extenso.'},
            {'role': 'user', 'content': mensaje}
        ]
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        respuesta_chatbot = response.json()['choices'][0]['message']['content']
        return respuesta_chatbot
    except Exception as e:
        messagebox.showerror("Error", "Hubo un problema al conectarse con el servidor.")
        return "Error al obtener respuesta. Por favor, intenta de nuevo más tarde."

def formatear_respuesta(respuesta):
    respuesta = respuesta.replace("**", "").replace("##", "").replace("###", "")
    
    lineas = respuesta.split("\n")
    
    respuesta_formateada = ""
    for linea in lineas:
        if linea.strip().startswith("Título:"):
            respuesta_formateada += f"\n🎬 {linea.strip()}\n"
        elif linea.strip().startswith("Año:"):
            respuesta_formateada += f"📅 {linea.strip()}\n"
        elif linea.strip().startswith("Género:"):
            respuesta_formateada += f"🎭 {linea.strip()}\n"
        elif linea.strip().startswith("Actores:"):
            respuesta_formateada += f"🌟 {linea.strip()}\n"
        elif linea.strip().startswith("Resumen:"):
            respuesta_formateada += f"\n📖 {linea.strip()}\n"
        else:
            respuesta_formateada += f"{linea.strip()}\n"
    
    return respuesta_formateada

def mostrar_mensaje_chatbot(mensaje):
    cuadro_chat.config(state=tk.NORMAL)
    cuadro_chat.insert(tk.END, f"\nChatbot:\n", "chatbot")
    cuadro_chat.insert(tk.END, f"{mensaje}\n", "chatbot_texto")
    cuadro_chat.insert(tk.END, "\n", "espacio")
    cuadro_chat.config(state=tk.DISABLED)
    cuadro_chat.yview(tk.END)

def mostrar_mensaje_bienvenida():
    mensaje_bienvenida = (
        "¡Bienvenido! 🎬\n\n"
        "Aquí podrás buscar películas y series según:\n"
        "- Género\n"
        "- Año de lanzamiento\n"
        "- Actores\n"
        "- Resumen\n\n"
        "¡Comienza a escribir tus preferencias y te ayudaré a encontrar algo increíble! 😊"
    )
    
    cuadro_chat.config(state=tk.NORMAL)
    cuadro_chat.insert(tk.END, f"Chatbot:\n", "chatbot")
    cuadro_chat.insert(tk.END, f"{mensaje_bienvenida}\n", "chatbot_texto")
    cuadro_chat.insert(tk.END, "\n", "espacio")
    cuadro_chat.config(state=tk.DISABLED)
    cuadro_chat.yview(tk.END)

root = tk.Tk()
root.title("Chatbot de Películas y Series")
root.configure(bg="#f0f0f0")

header = tk.Frame(root, bg="#2196f3", height=80)
header.pack(fill="x")

title = tk.Label(header, text="ChatBot", font=("Arial", 18, "bold"), fg="white", bg="#2196f3")
title.pack(pady=(10, 0))

subtitle = tk.Label(header, text="Seminario de Actualización", font=("Arial", 12), fg="white", bg="#2196f3")
subtitle.pack()

author = tk.Label(header, text="Por Luis Miguel Rueda Galindo", font=("Arial", 10), fg="white", bg="#2196f3")
author.pack(pady=(0, 10))

chat_frame = tk.Frame(root, bg="#ffffff", bd=0, relief="flat")
chat_frame.pack(padx=10, pady=10, fill="both", expand=True)

cuadro_chat = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state=tk.DISABLED, width=60, height=25, bg="#ffffff", font=("Arial", 12))
cuadro_chat.pack(padx=10, pady=10, fill="both", expand=True)

cuadro_chat.tag_configure("usuario", foreground="#333333", font=("Arial", 12, "bold"))
cuadro_chat.tag_configure("usuario_texto", foreground="#333333", background="#e3f2fd", borderwidth=0, relief="flat", font=("Arial", 12), lmargin1=10, lmargin2=10, rmargin=10, spacing3=10)
cuadro_chat.tag_configure("chatbot", foreground="#333333", font=("Arial", 12, "bold"))
cuadro_chat.tag_configure("chatbot_texto", foreground="#333333", background="#f5f5f5", borderwidth=0, relief="flat", font=("Arial", 12), lmargin1=10, lmargin2=10, rmargin=10, spacing3=10)
cuadro_chat.tag_configure("espacio", font=("Arial", 4))
cuadro_chat.tag_configure("cargando", foreground="#333333", font=("Arial", 12, "italic"))

input_frame = tk.Frame(root, bg="#f0f0f0")
input_frame.pack(padx=10, pady=10, fill="x")

entrada_texto = tk.Entry(input_frame, width=50, font=("Arial", 12))
entrada_texto.pack(side="left", padx=(0, 10), fill="x", expand=True)

boton_enviar = tk.Button(input_frame, text="Enviar", command=enviar_mensaje, font=("Arial", 12), bg="#2196f3", fg="white", borderwidth=0, relief="flat")
boton_enviar.pack(side="right")

def on_enter(e):
    boton_enviar.config(bg="#1976d2")

def on_leave(e):
    boton_enviar.config(bg="#2196f3")

boton_enviar.bind("<Enter>", on_enter)
boton_enviar.bind("<Leave>", on_leave)

mostrar_mensaje_bienvenida()

root.mainloop()