import tkinter as tk
from tkinter import messagebox
from collections import deque

# =====================================================================
# 1. BASE DE DATOS AMPLIADA (Troncales Suba, Norte, Caracas y Calle 26)
# =====================================================================
mapa_transmilenio = {
    # Troncal Suba
    "Portal Suba": ["La Campiña"],
    "La Campiña": ["Portal Suba", "Suba - Calle 100"],
    "Suba - Calle 100": ["La Campiña", "Escuela Militar"],
    "Escuela Militar": ["Suba - Calle 100", "Calle 76"],
    
    # Troncal Norte y Caracas Alta
    "Portal Norte": ["Héroes"],
    "Héroes": ["Portal Norte", "Calle 76"],
    "Calle 76": ["Escuela Militar", "Héroes", "Marly", "Ricaurte"],
    "Marly": ["Calle 76", "Calle 26 (Caracas)"],
    "Calle 26 (Caracas)": ["Marly", "Centro Memoria"],
    
    # Troncal Calle 26 (Aeropuerto / El Dorado)
    "Portal Eldorado": ["Modelia"],
    "Modelia": ["Portal Eldorado", "Normandía"],
    "Normandía": ["Modelia", "Avenida Rojas"],
    "Avenida Rojas": ["Normandía", "El Tiempo - Maloka"],
    "El Tiempo - Maloka": ["Avenida Rojas", "Quinta Paredes"],
    "Quinta Paredes": ["El Tiempo - Maloka", "Corferias"],
    "Corferias": ["Quinta Paredes", "Ciudad Universitaria"],
    "Ciudad Universitaria": ["Corferias", "Centro Memoria"],
    "Centro Memoria": ["Ciudad Universitaria", "Calle 26 (Caracas)", "Ricaurte"],
    
    # Interconexión / Intercambiador Clave
    "Ricaurte": ["Calle 76", "Centro Memoria", "Paloquemao"],
    "Paloquemao": ["Ricaurte"]
}

# =====================================================================
# 2. CEREBRO BFS (ALGORITMO DE OPTIMIZACIÓN)
# =====================================================================
def buscar_ruta_optima(mapa, inicio, fin):
    if inicio not in mapa or fin not in mapa:
        return None
    fila_de_espera = deque([(inicio, [inicio])])
    estaciones_visitadas = set([inicio])
    
    while fila_de_espera:
        estacion_actual, camino_hasta_ahora = fila_de_espera.popleft()
        if estacion_actual == fin:
            return camino_hasta_ahora
        for vecina in mapa[estacion_actual]:
            if vecina not in estaciones_visitadas:
                estaciones_visitadas.add(vecina)
                fila_de_espera.append((vecina, camino_hasta_ahora + [vecina]))
    return None

# =====================================================================
# 3. ACCIÓN DEL BOTÓN EN LA INTERFAZ
# =====================================================================
def calcular_ruta():
    origen = combo_origen.get()
    destino = combo_destino.get()
    
    if origen == destino:
        messagebox.showwarning("Atención", "¡Ya estás en la estación de destino!")
        return
        
    ruta = buscar_ruta_optima(mapa_transmilenio, origen, destino)
    
    if ruta:
        txt_resultado.config(state="normal")
        txt_resultado.delete("1.0", tk.END)
        # Mostrar la ruta limpia separada por flechas
        txt_resultado.insert(tk.END, " -> \n".join(ruta))
        txt_resultado.config(state="disabled")
        lbl_total.config(text=f"Estaciones totales: {len(ruta)}")
    else:
        messagebox.showerror("Error", "No se pudo calcular la ruta.")

# =====================================================================
# 4. DISEÑO DE LA VENTANA GRÁFICA (INTERFAZ)
# =====================================================================
ventana = tk.Tk()
ventana.title("Optimizar TransMilenio (BFS)")
ventana.geometry("480x450")
ventana.configure(bg="#E53935") # Rojo TransMilenio

lbl_titulo = tk.Label(ventana, text="SISTEMA DE RUTAS BFS", font=("Arial", 16, "bold"), bg="#E53935", fg="white")
lbl_titulo.pack(pady=15)

frame_campos = tk.Frame(ventana, bg="#E53935")
frame_campos.pack(pady=10)

lbl_origen = tk.Label(frame_campos, text="Estación Origen:", font=("Arial", 11), bg="#E53935", fg="white")
lbl_origen.grid(row=0, column=0, padx=10, pady=5, sticky="e")

lista_estaciones = sorted(list(mapa_transmilenio.keys()))
combo_origen = tk.StringVar(ventana)
combo_origen.set(lista_estaciones[0])
menu_origen = tk.OptionMenu(frame_campos, combo_origen, *lista_estaciones)
menu_origen.grid(row=0, column=1, pady=5)

lbl_destino = tk.Label(frame_campos, text="Estación Destino:", font=("Arial", 11), bg="#E53935", fg="white")
lbl_destino.grid(row=1, column=0, padx=10, pady=5, sticky="e")

combo_destino = tk.StringVar(ventana)
combo_destino.set(lista_estaciones[1])
menu_destino = tk.OptionMenu(frame_campos, combo_destino, *lista_estaciones)
menu_destino.grid(row=1, column=1, pady=5)

btn_calcular = tk.Button(ventana, text="CALCULAR RUTA ÓPTIMA", font=("Arial", 11, "bold"), bg="#FFD54F", fg="black", command=calcular_ruta)
btn_calcular.pack(pady=15)

lbl_ruta = tk.Label(ventana, text="Tu ruta recomendada es:", font=("Arial", 11, "bold"), bg="#E53935", fg="white")
lbl_ruta.pack()

txt_resultado = tk.Text(ventana, height=5, width=50, font=("Arial", 10), wrap="word", state="disabled")
txt_resultado.pack(pady=5)

lbl_total = tk.Label(ventana, text="", font=("Arial", 10, "italic"), bg="#E53935", fg="white")
lbl_total.pack(pady=5)

ventana.mainloop()