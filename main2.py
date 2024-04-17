#posso tappare una cella sola oppure premo il tasto sinistro poi premo quello destro e mantenendo quello sinistro premuto coloro tutto

from tkinter import *
import tkinter.colorchooser
from PIL import ImageGrab
from datetime import datetime
from tkinter import filedialog
from tkinter import simpledialog


import json
class PixelApp:
    def __init__(self,root):

        #*variabili
        self.root = root
        self.root.title("Pixel Art")
        # self.root.resizable(False,False)
        self.root.geometry("1500x732")
        self.cell_lenght= 25
        self.grid_width = 60
        self.grid_height= 27
        self.my_font = ('Verdana', 10, 'normal')

        self.colour_chooser = tkinter.colorchooser.Chooser(self.root) #per selezionare i colori
        #nessun colore o strumento selezionato
        self.chosen_colour = None
        self.is_pen_selected = False
        self.is_eraser_selected = False

        self.is_mouse_held = False
        self.cells_being_colored = []
        
        #*Main Canvas
        self.drawing_grid = Canvas(self.root) #creo una griglia che sarà un canvas
        self.drawing_grid.grid(column=0, row=1, sticky=(N,E,S,W))

        # Pannello di controllo
        control_frame = Frame(self.root, height=self.cell_lenght)
        control_frame.grid(column=0, row=0, sticky=(N, E, S, W))
        control_frame.pack_propagate(0) 
        control_frame.configure(background= '#4687ff')

        #Creare la griglia
        self.cells= []
        for i in range(0,self.grid_height): 
            for j in range(0,self.grid_width):
                cell = Frame(self.drawing_grid, width=self.cell_lenght, height=self.cell_lenght, bg="white", highlightbackground="black",highlightcolor="black", highlightthickness=1) #creiamo una cella esempio
                cell.grid(column=j,row=i) 
                cell.bind('<Button-1>', self.press_mouse_button)
                cell.bind('<B1-Motion>', self.move_mouse)
                self.cells.append(cell)

        #*Pannello di controllo
        self.control_frame = Frame(self.root, height= self.cell_lenght, bg='#a3d7f0', borderwidth=2, relief='solid')
        self.control_frame.grid(column=0, row=0, sticky=(N,E,S,W))

        #save button
        save_button = Button(self.control_frame, text="Save png",  relief="groove", font=self.my_font, cursor='hand2', command=self.press_save_button)
        save_button.grid(column=0,row=0,columnspan=3, sticky=(N,E,S,W), padx= 5,pady=5)

        #matita
        self.pencil_image = PhotoImage(file="./assets/pen.png").subsample(10,12) #importiamo la foto e la mettiamo in una variabile
        pen_button = Button(self.control_frame, text="Pen", image=self.pencil_image, cursor='hand2', relief="groove", command=self.press_pen_button) #mettiamo come immagine la variabile sopra
        pen_button.grid(column=11, row=0,columnspan=2, sticky=(N,E,S,W), padx= 5,pady=5)

        #gomma
        self.erase_image = PhotoImage(file="./assets/rubber.png").subsample(10,12) #subsample serve a ridimensionare
        erase_button = Button(self.control_frame, text="Erase", relief="groove", cursor='hand2', image= self.erase_image, command=self.press_erase_button)
        erase_button.grid(column=13,row=0,columnspan=2, sticky=(N,E,S,W), padx= 5,pady=5)

        #colore selezionato
        self.selected_color_box = Frame(self.control_frame, borderwidth=2, relief="raised", bg="white")
        self.selected_color_box.grid(column=43, row=0, columnspan=3, sticky=(N, E, S, W), padx= 7,pady=7)

        #selezione colore
        pick_color_button = Button(self.control_frame, text="Pick colour", font=self.my_font, relief="groove", cursor='hand2', command=self.press_pick_color_button)
        pick_color_button.grid(column=47, row=0,columnspan=3, sticky=(N,E,S,W), padx= 5,pady=5)

        #buttons per le dimensioni delle griglie
        
        #misura delle celle
        self.cells_button = Button(self.control_frame, relief="groove", text="Change cells' dimensions: <15-60>", font=self.my_font, cursor='hand2', command=self.change_cells_dimensions)
        self.cells_button.grid(column=25, row=0, columnspan=3, sticky=(N, E, S, W), padx= 5,pady=5)
        
        #input
        self.cells_entry = Entry(self.control_frame, width=5, font=self.my_font, justify=CENTER)
        self.cells_entry.grid(column=28, row=0, columnspan=2, sticky=(N, E, S, W), padx=5, pady=5)        

        #sistemare i buttons del pannello 
        cols, rows = self.control_frame.grid_size() 
        for col in range(cols):
            self.control_frame.columnconfigure(col, minsize=self.cell_lenght)
        self.control_frame.rowconfigure(0, minsize=self.cell_lenght) 

        #*menu

        my_menu = Menu(root)
        root.config(menu=my_menu)

        file_menu = Menu(my_menu, tearoff=False)
        my_menu.add_cascade(label='File', menu=file_menu)

        self.new_icon = PhotoImage(file="./assets/new-icon.png")
        self.open_icon = PhotoImage(file="./assets/open-icon.png")
        self.save_icon = PhotoImage(file="./assets/save-icon.png")
        self.exit_icon = PhotoImage(file="./assets/exit-icon.png")


        file_menu.add_command(label='New', image=self.new_icon, compound=LEFT, command=self.press_new_button) 
        file_menu.add_command(label='Open',image=self.open_icon, compound=LEFT, command=self.open_drawing)
        file_menu.add_command(label='Save',image=self.save_icon, compound=LEFT, command=self.save_drawing)
        
        file_menu.config(bg='white', fg='black')
        file_menu.add_command(label='Exit',image=self.exit_icon, compound=LEFT, command=root.quit)
        
        
        #file_menu.add_separator()


        #*Funzioni

    #salva il file in formato .dat per poi essere riaperto nell'app
    def save_drawing(self):
        file_name = filedialog.asksaveasfilename(
                initialdir='c:\\Users\costa\\OneDrive\\Desktop\\Python\\Pixel Art\\saved_drawings',  
                title='Save file',
                filetypes=(('Dat Files', '*.dat'),('All Files', '*.*'))
            )
        if file_name:
            if file_name.endswith('.dat'): 
                pass
            else:
                file_name = f'{file_name}.dat'
            
        cell_data = []  #salvo le informazioni di colonne, righe e bg color delle celle salvate
        for cell in self.cells:
            cell_data.append({
                'column': cell.grid_info()['column'],
                'row': cell.grid_info()['row'],
                'color': cell['bg'],
                'width': self.cell_lenght,
                'height': self.cell_lenght
            })
            
        #salvo il file
        with open(file_name, 'w') as file:  
            json.dump(cell_data, file)

    #riprendo un disegno salvato
    def open_drawing(self): 
        file_name = filedialog.askopenfilename(
            initialdir='c:\\Users\costa\\OneDrive\\Desktop\\Python\\Pixel Art\\saved_drawings',  
            title='Open file',
            filetypes=(('Dat Files', '*.dat'),('All Files', '*.*'))
        )

        #resetto
        if file_name:  
            for cell in self.cells:
                cell["bg"] = "white"
                self.chosen_colour = None
                self.is_pen_selected= False
                self.is_eraser_selected= False
                self.selected_color_box["bg"] = "white"
            
            #open file
            with open(file_name, 'r') as file:
                cell_data = json.load(file)

            
            #distruggo e ricreo la griglia
            for cell in self.cells:
                cell.destroy()
            self.cells = []
            for data in cell_data:  #per i dati che ho creo una nuova griglia che ha gli stessi dati di quella salvata

                cell = Frame(self.drawing_grid, width=data['width'], height=data['height'], bg=data['color'], highlightbackground="black",highlightcolor="black", highlightthickness=0.5)
                cell.grid(column=data['column'], row=data['row'])
                cell.bind('<Button-1>', self.press_mouse_button)
                cell.bind('<B1-Motion>', self.move_mouse)
                self.cells.append(cell)
            

    #colorare le celle o cancellarle
    def color_cell(self, cell_widget):
        if self.is_eraser_selected:
            cell_widget["bg"] = "white"
        elif self.is_pen_selected and self.chosen_colour is not None:
            cell_widget["bg"] = self.chosen_colour
        
    #event toccare la cella
    def tap_cell(self, event):
        widget = event.widget
        self.color_cell(widget)

    #colorare una ad una le celle
    def press_mouse_button(self, event):
        self.is_mouse_held = True
        self.cells_being_colored.append(event.widget)
        self.color_cell(event.widget)

    #rilasciare e smettere di colorare
    def release_mouse_button(self, event):
        self.is_mouse_held = False
        self.cells_being_colored = []

    #muovere il mouse e colorare nel passaggio
    def move_mouse(self, event):
        if self.is_mouse_held:
            widget = event.widget
            self.color_cell(widget)
            
        #creare le celle
    def create_cells(self):
        for cell in self.cells:
            cell.bind('<Button-1>', self.press_mouse_button)
            cell.bind('<ButtonRelease-1>', self.release_mouse_button)
            cell.bind('<B1-Motion>', self.move_mouse)
            cell.bind('<Button-1>', self.tap_cell)
            
        #resettare e pulire la griglia
    def press_new_button(self): 
        for cell in self.cells:
            cell["bg"] = "white"
            self.chosen_colour = None
            self.is_pen_selected= False
            self.is_eraser_selected= False
            self.selected_color_box["bg"] = "white"

    #fare uno screen del disegno
    def press_save_button(self):
        
        file_name = filedialog.asksaveasfilename(
            initialdir='c:\\Users\\costa\\OneDrive\\Desktop\\Python\\Pixel Art\\saved_screenshots',  # Initial directory
            title='Save Image',
            defaultextension=".png",
            filetypes=(('PNG Files', '*.png'), ('All Files', '*.*'))
        )
        if file_name:
            x = self.root.winfo_rootx() + self.drawing_grid.winfo_x() 
            y = self.root.winfo_rooty() + self.drawing_grid.winfo_y()  
            
            width = x+1125
            height = y+670

            _ = ImageGrab.grab(bbox=(x,y,width,height)).save(file_name)
        
    #selezionare la matita
    def press_pen_button(self):
        self.is_pen_selected = True
        self.is_eraser_selected= False

    #selezionare la gomma
    def press_erase_button(self):
        self.is_pen_selected = False
        self.is_eraser_selected= True

     #selezionare il colore
    def press_pick_color_button(self):
        colour_info = self.colour_chooser.show()#per mostrare la tavolozza colori
        chosen = colour_info[1]
        if chosen!= None: #se l'hex del colore non è nullo lo memorizzo in variabile e lo passo nel frame della box colorata
            self.chosen_colour = chosen
            self.selected_color_box["bg"] = self.chosen_colour

    #cambiare dimensioni griglia
    def change_cells_dimensions(self):
        self.new_dimension = int(self.cells_entry.get())  # prendo il valore dell'input

        if 15 <= self.new_dimension <= 20:
            self.update_grid_layout(45,100)
        elif 21 <= self.new_dimension <= 30:
            self.update_grid_layout(32,72)
        elif 31 <= self.new_dimension <= 40:
            self.update_grid_layout(22,49)
        elif 41 <= self.new_dimension <= 50:
            self.update_grid_layout(17,37)
        elif 51 <= self.new_dimension <= 60:
            self.update_grid_layout(14,30)
        else:
            print("You cannot enter a number less than 15 or more than 60")
            self.print_message()
            
    #validazione del cambio griglia
    def print_message(self):
        if self.new_dimension<15:
            message_label = Label(self.control_frame, text="You cannot enter a number less than 15", relief="flat")
            message_label.grid(column=29,row=0,columnspan=3, sticky=(N,E,S,W), padx= 5,pady=5)
            
            message_label.after(3000, message_label.destroy)

        elif self.new_dimension>60:
            message_label = Label(self.control_frame, text="You cannot enter a number more than 60", relief="flat")
            message_label.grid(column=29,row=0,columnspan=3, sticky=(N,E,S,W), padx= 5,pady=5)
            message_label.after(3000, message_label.destroy)
        else: 
            pass

    
    #aggiornare le dimensioni griglia
    def update_grid_layout(self, num_rows, num_cols):
        for cell in self.cells:
            cell.destroy()
        self.cells = []
        for i in range(num_rows):
            for j in range(num_cols):
                cell = Frame(self.drawing_grid, width=self.new_dimension, height=self.new_dimension, bg="white",
                            highlightbackground="black", highlightcolor="black", highlightthickness=0.5)
                self.cell_lenght = self.new_dimension
                cell.grid(column=j, row=i)
                cell.bind('<Button-1>', self.press_mouse_button)
                cell.bind('<B1-Motion>', self.move_mouse)
                self.cells.append(cell)

    
root = Tk()
PixelApp(root)
root.mainloop()


