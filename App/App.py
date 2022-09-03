import tkinter as tk
from tkinter.filedialog import askopenfile, asksaveasfilename

class Editor(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title('Analizador Léxico')
        #Tamaño fila
        self.rowconfigure(0,minsize=600,weight=1)
        #tamaño columna
        self.columnconfigure(1,minsize=600,weight=1)
        #Atributo de campo de texto
        self.campo_txt = tk.Text(self,wrap=tk.WORD)
        #Atributo de archivo
        self.archivo = None
        #Atributo para saber si ya se abrio un archivo
        self.archivo_abierto = False
        #Creacion de componentes
        self._crear_componentes()
        #Crear menu
        self._crear_menu()

    def _crear_componentes(self):
        frame_botones = tk.Frame(self,relief=tk.RAISED,bd=2)
        #botones
        boton_abrir = tk.Button(frame_botones,text='Abrir',command=self._abrir)
        boton_guardar = tk.Button(frame_botones,text='Guardar',command=self._guardar)
        boton_guardar_como = tk.Button(frame_botones,text='Guardar como...',command=self._guardar_como)
        #Expandir botones
        boton_abrir.grid(row=0,column=0,sticky='WE',padx=5,pady=5)
        boton_guardar.grid(row=1,column=0,sticky='WE',padx=5,pady=5)
        boton_guardar_como.grid(row=2,column=0,sticky='WE',padx=5,pady=5)
        #SE COLOCA EL FRAME vertical
        frame_botones.grid(row=0,column=0,sticky='NS')

        #Agregamos campo de texto se expandira por completo
        self.campo_txt.grid(row=0,column=1,sticky='NSWE')

    def _crear_menu(self):
        #Crear menu
        menu_app = tk.Menu(self)
        self.config(menu=menu_app)
        #Agregamos las opciones a nuestro menu
        menu_archivo = tk.Menu(menu_app,tearoff=0)
        menu_app.add_cascade(label='Archivo',menu=menu_archivo)
        #Agregamos las opciones del menu archivo
        menu_archivo.add_command(label='Abrir',command=self._abrir)
        menu_archivo.add_command(label='Guardar',command=self._guardar)
        menu_archivo.add_command(label='Guarar como...',command=self._guardar_como)
        menu_app.add_separator()
        menu_archivo.add_command(label='Salir',command=self.quit)

    def _abrir(self):
        #Abrimos el archivo para editar (lectura+escritura)
        self.archivo_abierto = askopenfile(mode='r+')
        #Eliminamos el texto anterior
        self.campo_txt.delete(1.0,tk.END)
        #Revisamos si hay un archivo,
        if not self.archivo_abierto:
            return
        #abrimos el archivo en modod lectura/escritura como rescurso
        with open(self.archivo_abierto.name,'r+') as self.archivo:
            #Leemos el contenido
            texto = self.archivo.read()
            #Insertamos todo el contenido en el campo de texto
            self.campo_txt.insert(1.0,texto)
            #Modifcamos el titulo de la aplicacion
            self.title(f'* Editor texto - {self.archivo.name} ')

    def _guardar(self):
        #Revisamos si ya se abrio un archivo
        if self.archivo_abierto:
            #Salvamos el archivo (arbimos en modo escritura)
            with open(self.archivo_abierto.name,'w') as self.archivo:
                #Leemos el contenido de la caja de texto
                texto = self.campo_txt.get(1.0,tk.END)
                #Escribimos todo el contenido al mismo archivo
                self.archivo.write(texto)
                #Cambiamos el nombre del titulo
                self.title(f'Editor texto - {self.archivo.name} ')

    def _guardar_como(self):
        #Salvar o guardar archivo
        self.archivo = asksaveasfilename(
            defaultextension='txt',
            filetypes=[('Archivos de Texto','*.txt'),('Todos los archivos','*.*')]
        )
        if not self.archivo:
            return
        #Abrimos el archivo en modo escritura
        with open(self.archivo,'w') as archivo:
            #Leemos el contendio
            texto = self.campo_txt.get(1.0,tk.END)
            #Escribimos 
            archivo.write(texto)
            #Cambiamos el nombre
            self.title(f'Editor texto - {archivo.name} ') 
            #Indicamos que ya hemos abierto un archivo
            self.archivo_abierto = archivo

if __name__ == '__main__':
    editor = Editor()
    editor.mainloop()

