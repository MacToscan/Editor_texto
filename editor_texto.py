from tkinter import *
from tkinter import filedialog, font, colorchooser
import os

class EditorTexto:
    def __init__(self, root):
        self.root = root
        self.ruta = ""
        self.seleccion = False
        self.etiqueta_contador = 0
        self.configurar_ventana()
        self.crear_menu()
        self.crear_botones()
        self.crear_monitor()

    def configurar_ventana(self):
        self.root.title("Editor de texto")
        self.root.geometry("640x490+0+0")

    def crear_menu(self):
        #--Menú de gestión de archivos.
        self.menubar = Menu(self.root)
        self.filemenu = Menu(self.menubar)
        #--Creamos el menú desplegable "cascade".
        self.filemenu.add_command(label="Nuevo", command=self.nuevo)      #-Vinculamos nuestros labels a las funciones correspondientes.
        self.filemenu.add_command(label="Abrir", command=self.abrir)
        self.filemenu.add_command(label="Guardar", command=self.guardar)
        self.filemenu.add_command(label="Guardar como", command=self.guardar_como)
        self.filemenu.add_separator()        #-Hacemos una linea separadora de nuestros labels anteriores.
        self.filemenu.add_command(label="Salir", command=self.root.quit)  #-Utilizamos la propia función .quit de root para salir de la ventana.
        self.menubar.add_cascade(menu = self.filemenu, label="Archivo")       #-Ponemos el nombre a la pestaña principal.
        #--Menú de edición de texto.
        self.editmenu = Menu(self.menubar)
        #--Creamos el menú desplegable "cascade".
        self.editmenu.add_command(label="Copiar      (Ctrl+c)", command=self.copiar)     #-Labels del menu Editar, vinculados a las funciones Copiar, Cortar y Pegar.
        self.editmenu.add_command(label="Cortar      (Ctrl+x)", command=self.cortar)
        self.editmenu.add_command(label="Pegar       (Ctrl+v)", command=self.pegar)
        self.menubar.add_cascade(menu = self.editmenu, label="Editar")
        #--Añadimos el menú editar "editmenu" en la pantalla al tocar botón derecho del ratón.
        self.root.bind("<2>", self.on_click)      #-<2> es el botón derecho del ratón, invocamos la función on_click que nos lleva al menú editar.
        #--Atajos de teclado para menú editar.
        self.root.bind("<Control-Key-x>", self.cortar)    #-Creamos los atajos de teclado para cortar, copiar y pegar, aunque no sería necesario porque vienen por default.
        self.root.bind("<Control-Key-c>", self.copiar)
        self.root.bind("<Control-Key-v>", self.pegar)
        #--Caja de texto central.
        self.texto = Text(self.root, undo = True, wrap=WORD)       #-Creamos el widget de texto, ponemos wrap=WORD para que al acabarse el ancho de la ventana salte de linea si la palabra no acaba.
        #texto.config(bg="white", fg="black",  )
        self.texto.pack(fill="both",  expand= 1)      #-Ocupamos todo el root
        #--Barra lateral de depslazamiento vertical.
        self.text_scroll = Scrollbar(self.texto)
        self.text_scroll.pack(side="right", fill=Y)
        self.text_scroll.config(command=self.texto.yview)     #-Configuramos la barra lateral a la variable texto con movimiento en Y.
        #-Configuramos el texto de nuestro editor.
        self.texto.config(bd=30, padx=6, pady=4,font=("Menlo"), selectbackground="rosy brown", yscrollcommand=self.text_scroll.set)
        self.root.config(menu=self.menubar)  #-Configuramos nuestro menú superior, Archivo y Editar, para que se haga presente.
        #--Label donde ubicar los botones.
        self.barra = Frame(self.root)
        self.barra.config(bg="black")
        self.barra.place(x=20, y=5)
    def crear_botones(self):
        #--Boton tipo de fuente.
        self.fuente_actual = font.Font(font=self.texto.cget("font"))                                  #-Obtenemos fuente actual.
        self.boton_fuente = Menubutton(self.barra, text = str(self.fuente_actual.actual()['family']))          #-Creamos MenuButton con el texto de la feunte actual.
        self.boton_fuente.config(fg="black", bg="gray", font=("Menlo", 12, "normal"))                 #-Configuarmos el tipo de botón que queremos.
        self.boton_fuente.pack(side="left")
        self.boton_fuente.menu = Menu(self.boton_fuente, tearoff=0)                            #-Creamos el menú depslegable del botón
        self.boton_fuente["menu"] = self.boton_fuente.menu
        self.boton_fuente.menu.add_radiobutton(label="Consolas", command=self.consolas)           #-Creamos RadioButtons para que solo se pueda quedar seleccionado uno de ellos.
        self.boton_fuente.menu.add_radiobutton(label="Arial", command=self.arial)
        self.boton_fuente.menu.add_radiobutton(label="Verdana", command=self.verdana)
        self.boton_fuente.menu.add_radiobutton(label="Times", command=self.times)
        self.boton_fuente.menu.add_radiobutton(label="Menlo", command=self.menlo)
        #--Definimos el tamaño de la feunte para poder poner el tamaño en el botón.
        self.tamaño_fuente = self.fuente_actual.cget("size")
        #--Botón tamaño fuente.
        self.boton_tamaño = Menubutton(self.barra, text = str(self.tamaño_fuente))
        self.boton_tamaño.config(fg="black", bg="gray", font=("Menlo", 12, "normal"))
        self.boton_tamaño.pack(side="left")
        self.boton_tamaño.menu = Menu(self.boton_tamaño, tearoff=0)                             #-Creamos el menú depslegable del botón
        self.boton_tamaño["menu"] = self.boton_tamaño.menu
        self.boton_tamaño.menu.add_radiobutton(label="10", command=self.tamaño_10)                 #-Creamos RadioButtons para que solo se pueda quedar seleccionado uno de ellos
        self.boton_tamaño.menu.add_radiobutton(label="12", command=self.tamaño_12)
        self.boton_tamaño.menu.add_radiobutton(label="14", command=self.tamaño_14)
        self.boton_tamaño.menu.add_radiobutton(label="16", command=self.tamaño_16)
        self.boton_tamaño.menu.add_radiobutton(label="20", command=self.tamaño_20)
        #--Botón color de texto.
        self.icono_color = "/Users/mactoscano/ConquerBlocks/Python/Ejercicios/Archivos/icon_color2.png"    #-Establecemos la variable icono_color, para que la ruta en otro dispositivo no falle.
        if os.path.exists(self.icono_color):
            self.imagen = PhotoImage(file = self.icono_color)     #-Cargamos la imagen desde su ruta.
            self.boton_color = Button(self.barra, image= self.imagen)      #-Creamos el botón, lo situamos en la barra y le damos la imagen anterior como objeto visible.
            self.boton_color.image = self.imagen                  #-Mantenemos una referéncia a la imagen
        else:
            self.boton_color = Button(self.barra, text="Color")       #-En caso de no encontrar la ruta de la imagen, establecemos un botón por defecto.
        self.boton_color.config(fg="black",bg="gray", font=("Menlo", 12, "bold"), command=self.color_fuente)
        self.boton_color.pack(side="right")
        #--Botón cursiva.
        self.boton_cursiva = Button(self.barra, text=("K"))           #-Creamos botón, lo situqamos en la barra y le damos el nombre.
        self.boton_cursiva.config(fg="black", bg="gray", font=("Menlo", 12, "italic"), command=self.cursiva)     #-Le ponemos sus características, en este caso ponemos letra en cursiva.
        self.boton_cursiva.pack(side="right")
        #--Botón negrita
        self.boton_negrita = Button(self.barra, text=("N"))           #-Creamos botón, lo situqamos en la barra y le damos el nombre.
        self.boton_negrita.config(fg="black", bg="gray", font=("Menlo", 12, "bold"), command=self.negrita)    #-Le ponemos sus características, en este caso ponemos letra en negrita.
        self.boton_negrita.pack(side="right")
    def crear_monitor(self):
        self.mensaje = StringVar()
        self.mensaje.set("Bienvenido al editor de texto del Sr. Toscano")
        self.monitor = Label(self.root, textvar=self.mensaje)
        self.monitor.config(fg="lightgray", font=("Menlo", 12, "normal"))
        self.monitor.pack(side="left", padx=10)
        self.actualizar_monitor()

    def actualizar_monitor(self):
        self.root.after(10000, self.actualizar_monitor)
        self.mensaje.set("Bienvenido al editor de texto del Sr. Toscano")

    #--///FUNCIONES PARA CREAR ARCHIVOS, NUEVO, ABRIR, GUARDAR Y GUARDAR COMO
    #--Función para crear un archivo nuevo y vacío.
    def nuevo(self):
        self.mensaje.set("Nuevo archivo")        #-Mensaje en monitor inferior.
        ruta = ""                               #-Establecemos la variable ruta sin nombre, por si queremos guardar en algún momento.
        self.texto.delete(0.0, END)                      #-Borramos todo el texto que se encuentre en el editor.
        self.root.title("Editor de texto")                   #-Ponemos el nombre de la ventana, cada vez que se inicie un archivo nuevo.
    #--Función para abrir un archivo guardado.
    def abrir(self):                                      
        self.ruta = filedialog.askopenfilename(initialdir=".",         #-Indicamos el directorio que abrirá inicialmente, con ".", indicamos que abrirá el directorio en el cual estamos.
                                        title="Abrir un archivo de texto",        #-Título de la ventana de los archivos a abrir.
                                        filetypes = (("Ficheros de texto", "*.txt"),),)   #-Indicamos el tipo de archivo que podemos abrir, todos los que sean .txt.
        if self.ruta != "":          #-Si la varible ruta tiene nombre entonces...
            with open(self.ruta, "r") as archivo: #-Abrimos el archivo en modo lectura y le damos el nombre a la variable.
                self.contenido = archivo.read()          #-Definimos la variable contenido con el archivo abierto anteriormente.
                self.texto.delete(0.0, END)                  #-Borramos todo el texto que se encuentre en nuestro editor, para dejar la página en blanco para nuestro archivo.
                self.texto.insert("insert", self.contenido)           #-Insertmaos nuestro archivo seleccionado anteriormente.
                self.root.title(self.ruta + " - Editor del Sr. Toscano")      #-Ponemos nombre en la ventana a nuestro archivo.
                self.mensaje.set("Archivo abierto correctamente")            #-Mensaje en nuestro monitor inferior.
    #-Función guardar.      
    def guardar(self):
        self.mensaje.set("Guardar archivo")          #-Mensaje en nuestro monitor inferior.
        if self.ruta != "":                  #-Si la variable ruta tiene nombre.
            self.contenido = self.texto.get(0.0, "end-1c")    #-Cogemos el texto del editor.
            with open(self.ruta, "w+") as fichero:                 #-Cogemos el fichero de dicha ruta y lo abrimos.
                self.fichero.write(self.contenido)                        #-Volveremos a guardar, esta vez, el contenido actual.
                self.mensaje.set("Archivo guardado correctamente")           #-Mensaje del monitor inferior.
        else:
            self.guardar_como()              #-Llamamos a la función guardar como en el caso que la variable ruta no tenga un nombre definido.
    #-Función guardar como.
    def guardar_como(self):
        self.mensaje.set("Guardar archivo como")
        self.fichero = filedialog.asksaveasfile(title="Guardar archivo", mode="w", defaultextension=".txt")  #-Creamos un fichero nuevo con filedialog.asksaveasfile()
        if self.fichero is not None:             #-Comprobamos que el fichero se ha creado correctamente.
            self.ruta = self.fichero.name                 #-Establecemos el nombre de la ruta con fichero.name, que nos dice la ruta exacta del fichero.
            self.contenido = self.texto.get(0.0, "end-1c")    #-Hacemos los mismo pasos que en la función anterior <guardar()>.
            with open(self.ruta, "w+") as self.fichero:
                self.fichero.write(self.contenido)
                self.mensaje.set("Archivo guardado correctamente")
        else:                                       #-Si el fichero no se ha creado correctamente, se ha cancelado o similar, entonces imprime mensaje de "guardado cancelado"
            self.mensaje.set("Guardado cancelado")
            ruta = ""
    #--///FUNCIONES DE CORTAR, COPIAR Y PEGAR///
    #--Función que nos permite cortar el texto seleccionado.
    def cortar(self):
        try:
            if self.texto.selection_get():               #-Si tenemos algo en seleccionado en nuestro editor, entonces...
                self.seleccion = self.texto.selection_get()       #-Creamos la variable selección con lo que tenemos seleccionado.
        except TclError:
                return
        self.texto.delete("sel.first", "sel.last")       #-Borramos toda la selección del texto.
        self.root.clipboard_clear()                          #-Eliminamos lo que pueda haber en el portapapeles.
        self.root.clipboard_append(self.seleccion)                    #-Añadimos nuestra selección al portapapeles, para futuras acciones.
    #--Función que nos permite copiar el texto seleccionado.
    def copiar(self):
        try:
            if self.texto.selection_get():       #-La misma lógica que en la función cortar exceptuando el borrado del texto seleccionado (selección).
                self.seleccion = self.texto.selection_get()       #-Creamos la variable selección con lo que tenemos seleccionado.
        except TclError:
                return
        self.root.clipboard_clear()
        self.root.clipboard_append(self.seleccion)
    #--Función que nos permite pegar el texto seleccionado.
    def pegar(self):                                   # Pegar el texto del portapapeles, .insert("donde esta el cursor", "lo que esta en el portapapeles")
        self.texto.insert(INSERT, root.clipboard_get())    #-Siempre que se guarde algo en el portapapeles o clipboard, con atajos de teclado o desde el menú editar, se pegará donde decimos.     
    #--Función que nos abre en el root el menú desplegable Editar, al clicar con el botón dercho del mouse.
    def on_click(self, event):
        self.editmenu.post(event.x_root, event.y_root)
    #--Función que actualiza el monitor inferior para que cambie el mensaje una vez se haya podido leer.
    def actualizar_monitor(self):
        self.root.after(10000, self.actualizar_monitor) 
        self.mensaje.set("Bienvenido al editor de texto del Sr. Toscano")
    #Función padre para cambiar el tipo de fuente, dando el parámetro de esta.
    def cambiar_fuente(self, fuente):
        self.tipo_fuente = font.Font(font=self.texto.cget("font"))        #-Establecemos el tipo de fuente para posteriormente sacar el tamaño de la fuente.
        self.tamaño_fuente = self.tipo_fuente.cget("size")                     #-Creamos la variable, del tamaño de la fuente.
        self.texto.config(bd=30, padx=6, pady=4, font=(fuente, str(self.tamaño_fuente)))     #-Actualizamos el texto del botón de tamaño, para que sea acorde al tamaño seleccionado
        self.actualizar_boton_fuente()                                             #-Actualizamos el texto del botón de tamaño, para que sea acorde al tamaño seleccionado
                                                
    #--Funciones que cambian la fuente mediante un botón desplegable.
    def consolas(self):
        self.cambiar_fuente("Consolas")
    def arial(self):
        self.cambiar_fuente("Arial")
    def verdana(self):
        self.cambiar_fuente("Verdana")
    def times(self):
        self.cambiar_fuente("Times")
    def menlo(self):
        self.cambiar_fuente("Menlo")
    #Función padre para cambiar el tamaño de la fuente, dando el parámetro de esta.
    def cambiar_tamaño(self, tamaño):
        self.fuente_actual = font.Font(font=self.texto.cget("font"))      #-Obtenemos la fuente actual.
        self.texto.config(font=(self.fuente_actual.actual()['family'], tamaño))   #-Cambiamos el tamaño de la fuente respetando esta.
        self.actualizar_boton_tamaño()                                           #-Actualizamos el texto del botón de tamaño, para que sea acorde al tamaño seleccionado
        self.actualizar_boton_fuente()                                                 #-Actualizamos el texto del botón de tipo de fuente, para que sea acorde a la fuente seleccionada.
    #--Funciones que cambian el tamaño de la fuente mediante un botón desplegable.
    def tamaño_10(self):
        self.cambiar_tamaño(10)
    def tamaño_12(self):
        self.cambiar_tamaño(12)
    def tamaño_14(self):
        self.cambiar_tamaño(14)
    def tamaño_16(self):
        self.cambiar_tamaño(16)
    def tamaño_20(self):
        self.cambiar_tamaño(20)
    #--Función que actualizaliza el texto del botón de tipo de fuente, para que esté acorde a la fuente seleccionada.
    def actualizar_boton_fuente(self):
        self.fuente_actual = font.Font(font=self.texto.cget("font"))  #-Obtenemos fuente actual.
        self.boton_fuente.config(text = self.fuente_actual.actual()['family']) #-Cambiamos texto del botón.
    #--Función que actualiza el texto del botón del tamaño de la feunte, para que esté acorde al tamaño seleccionado.
    def actualizar_boton_tamaño(self):
        self.fuente_actual = font.Font(font=self.texto.cget("font"))    #-Obtenemos fuente actual.
        self.tamaño_fuente = self.fuente_actual.cget("size")            #-Obtenemos el tamaño de la fuente.
        self.boton_tamaño.config(text = str(self.tamaño_fuente))   #-Cambiamos el texto del botón.
    #--Funciones que cambian el tipo de escritura, (negrita, cursiva) mediante un botón.
    def negrita(self):
        self.bold_font = font.Font(self.texto, self.texto.cget("font"))    
        self.bold_font.configure(weight="bold")                  #-Creamos nuestra fuente en negrita.
        self.texto.tag_configure("bold", font=self.bold_font)         #-Creamos una etiqueta llamada "bold", que coge como fuente la anterior creada.
        self.etiqueta_actual = self.texto.tag_names("sel.first")      #-Definimos la posición de la etiqueta.
        if "bold" in self.etiqueta_actual:
            self.texto.tag_remove("bold", "sel.first", "sel.last")   #-Si el texto seleccionado esta en negrita, entonces borrara el efecto, y volvera a su estado "normal"
        else:
            self.texto.tag_add("bold", "sel.first", "sel.last")      #-Si por el contrario "bold", no existe, convertira el texto seleccionado en negrita.
    #--Hacemos exactamente lo mismo que con la función anterior, para pasar el texto seleccionado a cursiva.
    def cursiva(self):
        self.italic_font = font.Font(self.texto, self.texto.cget("font"))
        self.italic_font.configure(slant="italic")           #-El único punto que cambia con respecto la función anterior es la manera de llamar a "italic", que es mediante "slant" y weight.
        self.texto.tag_configure("italic", font=self.italic_font)
        self.etiqueta_actual = self.texto.tag_names("sel.first")
        if "italic" in self.etiqueta_actual:
            self.texto.tag_remove("italic", "sel.first", "sel.last")
        else:
            self.texto.tag_add("italic", "sel.first", "sel.last")
    def color_fuente(self):
        self.fuente_actual = font.Font(font=self.texto.cget("font"))      #-Obtenemos fuente actual.
        self.tipo_fuente = font.Font(font=self.texto.cget("font"))            #-Establecemos el tipo de fuente para posteriormente sacar el tamaño de la fuente.
        self.tamaño_fuente = self.tipo_fuente.cget("size")                        #-Creamos la variable, del tamaño de la fuente.
        self.color = colorchooser.askcolor()[1]              #-Le asignamos a la variable color, la paleta de colores por default que viene con colorchooser.
        if self.color:
            self.etiqueta = f"select{self.etiqueta_contador}"       #-Variable etiqueta que va a ser el nombre que le damos al texto seleccionado, más un contador.
            self.texto.tag_add(self.etiqueta, "sel.first", "sel.last")   #-Agregamos la etiqueta en toda nuestra selección.     
            self.texto.tag_config(self.etiqueta, foreground=self.color)            #-Configuramos nuestra etiqueta para que el color sea el elegido en la paleta.
            self.texto.config(font=(self.fuente_actual.actual()['family'], self.tamaño_fuente))    #-Dejamos el texto con la misma fuente y el mismo tamaño
            self.etiqueta_contador += 1   #-Añadimos +1 en el contadoppr para que las etiiquetas sean diferentes y podamos tener más de un color dentro de nuestro edior.

if __name__ == "__main__":
    root = Tk()
    EditorTexto(root)
    root.mainloop()




