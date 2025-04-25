import tkinter as tk
from tkinter import ttk
import os

# Secuencia de referencia
referencia = "ATGCTAGGCTAAT"

# Leer el archivo con las secuencias
def leer_secuencias_desde_archivo(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print("Archivo no encontrado")
        return []
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
        return [linea.strip().upper() for linea in lineas if linea.strip()]

# Comparar dos secuencias y detectar mutaciones
def comparar_con_referencia(ref, secuencia):
    mutaciones = []
    if len(ref) != len(secuencia):
        return ("longitud_invalida", [])
    else:
        for i, (a, b) in enumerate(zip(ref, secuencia)):
            if a != b:
                mutaciones.append((i, b))
    if not mutaciones:
        return ("correcta", [])
    else:
        return ("mutada", mutaciones)

# Interfaz gráfica 
ventana = tk.Tk()
ventana.title("Verificador de Secuencias de ADN")
ventana.geometry("800x600")
ventana.config(bg="#f0f0f0")

canvas = tk.Canvas(ventana, bg="#f0f0f0")
scroll_y = tk.Scrollbar(ventana, orient="vertical", command=canvas.yview)
frame_con_scroll = ttk.Frame(canvas)

frame_con_scroll.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=frame_con_scroll, anchor="nw")
canvas.configure(yscrollcommand=scroll_y.set)

canvas.pack(side="left", fill="both", expand=True)
scroll_y.pack(side="right", fill="y")

# Título
titulo = ttk.Label(frame_con_scroll, text="Resultado del Análisis de Secuencias de ADN", font=("Arial", 18, "bold"))
titulo.pack(pady=10)

# Ruta del archivo
ruta_archivo = "C:/Users/User/Desktop/tarea8/secuencias_ADN.txt"

# Leer y procesar las secuencias
secuencias = leer_secuencias_desde_archivo(ruta_archivo)

for i, secuencia in enumerate(secuencias, 1):
    estado, mutaciones = comparar_con_referencia(referencia, secuencia)

    bloque = ttk.LabelFrame(frame_con_scroll, text=f"Secuencia {i}", padding=10)
    bloque.pack(fill='x', pady=10, padx=20)

    ref_label = ttk.Label(bloque, text=f"Referencia:  {referencia}", font=("Courier", 12))
    ref_label.pack(anchor='w')

    if estado == "correcta":
        resultado = ttk.Label(bloque, text="✔ Secuencia Correcta (0 mutaciones)", foreground="green", font=("Arial", 12, "bold"))
        resultado.pack(anchor='w')
        seq_label = ttk.Label(bloque, text=f"Secuencia:   {secuencia}", font=("Courier", 12))
        seq_label.pack(anchor='w')

    elif estado == "longitud_invalida":
        resultado = ttk.Label(bloque, text="✖ Longitud inválida (No se puede analizar)", foreground="orange", font=("Arial", 12, "bold"))
        resultado.pack(anchor='w')
        seq_label = ttk.Label(bloque, text=f"Secuencia:   {secuencia}", font=("Courier", 12))
        seq_label.pack(anchor='w')

    elif estado == "mutada":
        cantidad = len(mutaciones)
        resultado = ttk.Label(bloque, text=f"✖ {cantidad} Mutación(es) Detectadas", foreground="red", font=("Arial", 12, "bold"))
        resultado.pack(anchor='w')

        mut_label = tk.Text(bloque, height=1, font=("Courier", 12), borderwidth=0)
        mut_label.insert("1.0", secuencia)

        for idx, letra in mutaciones:
            start = f"1.{idx}"
            end = f"1.{idx+1}"
            mut_label.tag_add(f"mutacion{idx}", start, end)
            mut_label.tag_config(f"mutacion{idx}", foreground="white", background="red")

        mut_label.config(state="disabled")
        mut_label.pack(anchor='w')

ventana.mainloop()
