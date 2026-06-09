import customtkinter as ctk
from tkinter import messagebox, filedialog
from PIL import Image, ImageFilter, ImageEnhance, ImageOps

# 🎨 COLORES: TODO MORADO CLARITO / LILA (SIN NEGRO, SIN ERRORES)
ctk.set_appearance_mode("light")

FONDO_PRINCIPAL = "#E8D9FF"       # Morado clarito fondo
PANEL_LATERAL = "#D4BFFF"         # Morado medio panel
BOTON_AZUL = "#4169E1"            # Azul morado
BOTON_VERDE = "#32CD32"           # Verde guardar
BOTON_MORADO = "#9932CC"          # Morado filtros
TEXTO = "#4B0082"                 # Texto oscuro

class GlowStudio(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("GLOW STUDIO PRO - EDICIÓN TOTAL")
        self.geometry("1200x800")
        self.state("zoomed")
        self.configure(fg_color=FONDO_PRINCIPAL)

        # Variables imagen
        self.img_original = None
        self.img_procesada = None
        self.historial = []

        # 📌 PANEL IZQUIERDO
        self.sidebar = ctk.CTkFrame(self, width=220, fg_color=PANEL_LATERAL, corner_radius=12)
        self.sidebar.pack(side="left", fill="y", padx=15, pady=15)
        self.sidebar.pack_propagate(False)

        # Botones principales
        ctk.CTkButton(self.sidebar, text="Abrir Imagen", command=self.cargar_foto,
                      fg_color=BOTON_AZUL, hover_color="#6495ED", text_color="white",
                      font=("Arial",12,"bold"), corner_radius=8).pack(pady=8, padx=12, fill="x")

        ctk.CTkButton(self.sidebar, text="Guardar Imagen", command=self.guardar_foto,
                      fg_color=BOTON_VERDE, hover_color="#228B22", text_color="white",
                      font=("Arial",12,"bold"), corner_radius=8).pack(pady=5, padx=12, fill="x")

        ctk.CTkButton(self.sidebar, text="Deshacer", command=self.deshacer,
                      fg_color=BOTON_AZUL, hover_color="#6495ED", text_color="white",
                      font=("Arial",12,"bold"), corner_radius=8).pack(pady=5, padx=12, fill="x")

        # 🔘 BARRAS DE AJUSTE - ✅ ARREGLADAS PARA QUE FUNCIONEN YA
        # Brillo
        ctk.CTkLabel(self.sidebar, text="Brillo", text_color=TEXTO, font=("Arial",12,"bold")).pack(pady=(15,2))
        self.s_brillo = ctk.CTkSlider(self.sidebar, from_=0.1, to=3.0, command=self.actualizar_en_vivo,
                                       fg_color="#D8BFD8", progress_color=BOTON_MORADO,
                                       button_color=BOTON_MORADO, button_hover_color="#BA55D3")
        self.s_brillo.set(1.0)
        self.s_brillo.pack(pady=5, padx=12, fill="x")

        # Contraste
        ctk.CTkLabel(self.sidebar, text="Contraste", text_color=TEXTO, font=("Arial",12,"bold")).pack(pady=(10,2))
        self.s_contraste = ctk.CTkSlider(self.sidebar, from_=0.1, to=3.0, command=self.actualizar_en_vivo,
                                          fg_color="#D8BFD8", progress_color=BOTON_MORADO,
                                          button_color=BOTON_MORADO, button_hover_color="#BA55D3")
        self.s_contraste.set(1.0)
        self.s_contraste.pack(pady=5, padx=12, fill="x")

        # Saturación
        ctk.CTkLabel(self.sidebar, text="Saturación", text_color=TEXTO, font=("Arial",12,"bold")).pack(pady=(10,2))
        self.s_saturacion = ctk.CTkSlider(self.sidebar, from_=0.0, to=5.0, command=self.actualizar_en_vivo,
                                           fg_color="#D8BFD8", progress_color=BOTON_MORADO,
                                           button_color=BOTON_MORADO, button_hover_color="#BA55D3")
        self.s_saturacion.set(1.0)
        self.s_saturacion.pack(pady=5, padx=12, fill="x")

        # Botón aplicar
        ctk.CTkButton(self.sidebar, text="Aplicar Ajustes", command=self.guardar_ajustes,
                      fg_color=BOTON_AZUL, hover_color="#6495ED", text_color="white",
                      font=("Arial",12,"bold"), corner_radius=8).pack(pady=15, padx=12, fill="x")

        # 🎨 FILTROS
        filtros = [("Filtro Belleza", self.f_belleza), ("Glow", self.f_glow),
                   ("B/N", self.f_bn), ("Vintage", self.f_vintage)]
        for txt, cmd in filtros:
            ctk.CTkButton(self.sidebar, text=txt, command=cmd,
                          fg_color=BOTON_MORADO, hover_color="#DA70D6", text_color="white",
                          font=("Arial",11), corner_radius=8).pack(pady=4, padx=12, fill="x")

        # 🔄 ROTACIÓN
        ctk.CTkButton(self.sidebar, text="Rotar Derecha", command=lambda: self.rotar(-90),
                      fg_color=BOTON_AZUL, hover_color="#6495ED", text_color="white",
                      font=("Arial",11), corner_radius=8).pack(pady=8, padx=12, fill="x")

        ctk.CTkButton(self.sidebar, text="Rotar Izquierda", command=lambda: self.rotar(90),
                      fg_color=BOTON_AZUL, hover_color="#6495ED", text_color="white",
                      font=("Arial",11), corner_radius=8).pack(pady=4, padx=12, fill="x")

        # 🖼️ AREA IMAGEN
        self.lbl_canvas = ctk.CTkLabel(self, text="✨ Esperando imagen... ✨",
                                       fg_color=FONDO_PRINCIPAL, text_color=TEXTO,
                                       font=("Arial",16,"bold"))
        self.lbl_canvas.pack(expand=True, fill="both", padx=20, pady=20)


    # 📌 FUNCIÓN PRINCIPAL: ✅ BRILLO, CONTRASTE, SATURACIÓN FUNCIONAN YA AL 100%
    def actualizar_en_vivo(self, valor):
        if self.img_original:
            # Tomamos la imagen original y aplicamos los cambios AL INSTANTE
            img = self.img_original.copy()

            # ✅ EFECTOS REALES Y FUERTES
            img = ImageEnhance.Brightness(img).enhance(self.s_brillo.get())   # Brillo
            img = ImageEnhance.Contrast(img).enhance(self.s_contraste.get()) # Contraste
            img = ImageEnhance.Color(img).enhance(self.s_saturacion.get())    # Saturación

            # Actualizamos vista
            self.img_procesada = img
            self.renderizar()

    def guardar_ajustes(self):
        if self.img_procesada:
            self.historial.append(self.img_procesada.copy())
            messagebox.showinfo("✅ Guardado", "Ajustes aplicados correctamente")

    def cargar_foto(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp")])
        if ruta:
            self.img_original = Image.open(ruta).convert("RGB")
            self.img_procesada = self.img_original.copy()
            self.historial.clear()
            self.renderizar()

    def guardar_foto(self):
        if self.img_procesada:
            ruta = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG", "*.png"), ("JPG", "*.jpg")])
            if ruta:
                self.img_procesada.save(ruta)
                messagebox.showinfo("✅ Éxito", "Imagen guardada correctamente")
        else:
            messagebox.showwarning("⚠️ Atención", "No hay imagen para guardar")

    # ✅ FILTROS
    def f_belleza(self):
        if self.img_procesada:
            self.historial.append(self.img_procesada.copy())
            img = self.img_procesada.filter(ImageFilter.SMOOTH_MORE)
            img = ImageEnhance.Brightness(img).enhance(1.2)
            self.img_procesada = img
            self.renderizar()

    def f_glow(self):
        if self.img_procesada:
            self.historial.append(self.img_procesada.copy())
            img = self.img_procesada.filter(ImageFilter.GaussianBlur(3))
            img = ImageEnhance.Brightness(img).enhance(1.4)
            self.img_procesada = img
            self.renderizar()

    def f_bn(self):
        if self.img_procesada:
            self.historial.append(self.img_procesada.copy())
            self.img_procesada = ImageOps.grayscale(self.img_procesada).convert("RGB")
            self.renderizar()

    def f_vintage(self):
        if self.img_procesada:
            self.historial.append(self.img_procesada.copy())
            gris = ImageOps.grayscale(self.img_procesada)
            self.img_procesada = ImageOps.colorize(gris, "#704214", "#FFE4B5")
            self.renderizar()

    def rotar(self, grados):
        if self.img_procesada:
            self.historial.append(self.img_procesada.copy())
            self.img_procesada = self.img_procesada.rotate(grados, expand=True)
            self.renderizar()

    def deshacer(self):
        if self.historial:
            self.img_procesada = self.historial.pop()
            self.renderizar()
        else:
            messagebox.showinfo("ℹ️ Info", "No hay cambios para deshacer")

    def renderizar(self):
        # Imagen grande y centrada
        if self.img_procesada:
            ancho, alto = self.img_procesada.size
            max_w, max_h = 900, 700
            relacion = min(max_w/ancho, max_h/alto)
            nuevo_tam = (int(ancho * relacion), int(alto * relacion))

            self.imagen_render = ctk.CTkImage(light_image=self.img_procesada,
                                             dark_image=self.img_procesada,
                                             size=nuevo_tam)
            self.lbl_canvas.configure(image=self.imagen_render, text="")


# --- 🔐 LOGIN ---
def verificar_login():
    if entry_user.get().strip() == "Tatiana" and entry_pass.get().strip() == "123456":
        login_window.destroy()
        app = GlowStudio()
        app.mainloop()
    else:
        mensaje_error.configure(text="❌ Usuario o contraseña incorrectos")

login_window = ctk.CTk()
login_window.geometry("400x480")
login_window.title("Login | Glow Studio")
login_window.configure(fg_color="#D4BFFF")
login_window.resizable(False, False)

ctk.CTkLabel(login_window, text="✨ GLOW STUDIO ✨",
             text_color="#4B0082", font=("Arial", 24, "bold")).pack(pady=40)

entry_user = ctk.CTkEntry(login_window, placeholder_text="👤 Usuario",
                          fg_color="#E6E6FA", border_color="#9370DB",
                          text_color="#4B0082", font=("Arial",14), height=45)
entry_user.pack(pady=10, padx=40, fill="x")

entry_pass = ctk.CTkEntry(login_window, placeholder_text="🔑 Contraseña", show="*",
                          fg_color="#E6E6FA", border_color="#9370DB",
                          text_color="#4B0082", font=("Arial",14), height=45)
entry_pass.pack(pady=10, padx=40, fill="x")

mensaje_error = ctk.CTkLabel(login_window, text="", text_color="#C71585", font=("Arial",12))
mensaje_error.pack()

ctk.CTkButton(login_window, text="✨ INGRESAR ✨", command=verificar_login,
              fg_color="#9370DB", hover_color="#7B68EE",
              text_color="white", font=("Arial",16,"bold"), height=50).pack(pady=30, padx=40, fill="x")

login_window.mainloop()