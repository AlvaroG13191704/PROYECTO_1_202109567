import tkinter as tk
from tkinter.filedialog import askopenfile, asksaveasfilename

# imports from components
from components.LexicalAnalyzer import LexicalAnalyzer

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
    
        # Main variables
        self.title('Analizador Léxico')
        # row size
        self.rowconfigure(0,minsize=400,weight=1)
        # col size
        self.columnconfigure(1,minsize=600,weight=1)
        # Atribute with the textarea
        self.txt_area = tk.Text(self,wrap=tk.WORD)
        
        # This variables manage the control of the opened files 
        self.file = None
        self.open_file = False

        # func to create the componentes
        self._create_components()

    def _create_components(self):
        btns_frame = tk.Frame(self,relief=tk.RAISED,bd=1)
        # first pair of buttons -> File
        btn_open = tk.Button(btns_frame,text='Abrir',command=self._open)
        btn_save = tk.Button(btns_frame,text='Guardar',command=self._save)
        btn_save_as = tk.Button(btns_frame,text='Guardar Como',command=self._save_as)
        btn_analyze = tk.Button(btns_frame,text='Ejecutar',command=self._analyze)
        # grid buttons
        btn_open.grid(row=0,column=0,sticky='WE',padx=5,pady=5)
        btn_save.grid(row=1,column=0,sticky='WE',padx=5,pady=5)
        btn_save_as.grid(row=2,column=0,sticky='WE',padx=5,pady=5)
        btn_analyze.grid(row=3,column=0,sticky='WE',padx=5,pady=5)

        # Second pair of buttons -> help
        btn_m_user = tk.Button(btns_frame,text='Manual de Usuario',command=self._manual_user)
        btn_m__tec = tk.Button(btns_frame,text='Manual Técnico',command=self._manual_tec)
        btn_help = tk.Button(btns_frame,text='Temas de ayuda',command=self._help)
        # grid
        btn_m_user.grid(row=6,column=0,sticky='WE',padx=5,pady=5)
        btn_m__tec.grid(row=7,column=0,sticky='WE',padx=5,pady=5)
        btn_help.grid(row=8,column=0,sticky='WE',padx=5,pady=5)
        # quit
        btn_exit = tk.Button(btns_frame,text='Salir',command= lambda: self.quit())
        btn_exit.grid(row=9,column=0,sticky='WE',padx=5,pady=5)

        # grid btns frame
        btns_frame.grid(row=0,column=0,sticky='NS')
        # add the textarea
        self.txt_area.grid(row=0,column=1,sticky='NSWE')

    # Func
    def _open(self):
        # Opend the file window
        self.open_file = askopenfile(mode='r+')
        self.txt_area.delete(1.0,tk.END) # remove any line 
        # Verified if ins´t a file already opened
        if not self.open_file: 
            return
        # Read the selected file
        with open(self.open_file.name, 'r+') as self.file:
            text = self.file.read() # read content
            self.txt_area.insert(1.0,text) # insert the text into the text area
            self.title(f'* Analizador Léxico - {self.file.name}') 
    
    def _save(self):
        # Verified if a file was already opened
        if self.open_file:
            with open(self.open_file.name,'w') as self.file:
                text = self.txt_area.get(1.0,tk.END) # read the content
                self.file.write(text) # write all the text in the textarea
                self.title(f'Analizador Léxico - {self.file.name}') # modified the title

    def _save_as(self):
        # save file
        self.file = asksaveasfilename(
            defaultextension='txt',
            filetypes=[('Archivos de Texto', '*.txt'), ('Todos los archivos', '*.*')]
        )
        #if the file isn't open
        if not self.file:
            return
        with open(self.file, 'w') as file:
            text = self.txt_area.get(1.0,tk.END) # get the content
            file.write(text) # write the content in the file
            self.title(f'Analizador Léxico - {file.name}')
            self.open_file = file #Indicate that the file was already open

    def _analyze(self):
        reader = LexicalAnalyzer()
        reader.compile(self.txt_area.get(1.0,tk.END))
    
    def _manual_user(self):
        pass

    def _manual_tec(self):
        pass
    
    def _help(self):
        pass


if __name__ == '__main__':
    editor = GUI()
    editor.mainloop()