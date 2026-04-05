from customtkinter import *
from socket import*
import threading

class Window(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("400x600")
        self.title("LogiTalk")
        self.menu = CTkFrame(self)
        self.menu.place(x=0,y=0)
        self.menu.configure(width=0)
        self.menu.pack_propagate(False)
        self.show_menu = False
        self.width_menu = 0
        self.text_menu = CTkLabel(self.menu,text = "Ваше ім'я")
        self.text_menu.pack(pady = 30)
        self.name_menu = CTkEntry(self.menu)
        self.name_menu.pack()
        self.knopka = CTkButton(self.menu, text = "Підключитися",command = self.connect_to_serveer)
        self.knopka.pack()
        self.settings_menu = CTkButton(self,width = 30,height = 30,text = "⚙️", command = self.show_hide)
        self.settings_menu.place(x = 5, y = 5)
        self.chatik = CTkTextbox(self, state = "disable")
        self.chatik.place(x = 0, y = 150)
        self.massage = CTkEntry(self, placeholder_text= "Введіть повідомлення")
        self.massage.place(x = 0, y = 500)
        self.massage.bind("<Return>", self.send_by_Enter)
        self.send_massage = CTkButton(self, text = "➢", width = 30, height = 30, command = self.sand_msg)
        self.send_massage.place(x =200, y = 500)
        self.adaptive()  
    def send_by_Enter(self, event):
        self.sand_msg()


    def connect_to_serveer(self):
        self.name = self.name_menu.get()
        try:
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(('7.tcp.eu.ngrok.io', 17378))
            self.client_socket.send(self.name.encode("utf-8"))
            threading.Thread(target = self.receive_messages).start()
        except Exception as e:
            self.add_msg(f"помилка підключення: {e}")
    
    def add_msg(self, text):
        self.chatik.configure(state = "normal")
        self.chatik.insert("end", text + "\n")
        self.chatik.configure(state = "disable")
        self.chatik.see('end')

    def rozbor(self,line):
        if not line:
            return
        parts = line.split("@",3)  
        massage_type = parts[0]
        if massage_type == 'TEXT':
            if len(parts) >= 3:
                text_person = parts[1]
                text_msg = parts[2]
                self.add_msg(f"{text_person} : {text_msg}")

    def sand_msg(self):
        msg = self.massage.get()
        if msg:
            self.add_msg(f"{self.name}: {msg}")
            a = f"TEXT@{self.name}@{msg}\n"
            try:
                self.client_socket.send(a.encode('utf-8'))
            except:
                pass
        self.massage.delete(0, "end")

    def receive_messages(self):
        baza = ""
        while True:
            try:
                data = self.client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                baza += data
                while '\n' in baza:
                    line, baza = baza.split('\n', 1)
                    self.rozbor(line)

            except:
                break

        self.client_socket.close()

    def adaptive(self):
        self.menu.configure(height = self.winfo_height())
        self.chatik.configure(width = self.winfo_width() - self.menu.winfo_width(), height = self.winfo_height()  - self.massage.winfo_height() - 20)
        self.chatik.place(x = self.menu.winfo_width(), y = 25)
        self.massage.configure(width = self.winfo_width() - self.menu.winfo_width() - 35, height = 30)
        self.massage.place(x = self.menu.winfo_width(), y = self.winfo_height() - 100)
        self.send_massage.configure(width = self.massage.winfo_height(), height = self.massage.winfo_height())
        self.send_massage.place(x = self.menu.winfo_width() - 200, y = self.winfo_height() - 100)

        self.after(20,self.adaptive)


    def show_hide(self):
        if self.show_menu == True:
            self.show_menu = False
            self.close_menu()
    
        else:
            self.show_menu = True
            self.open_menu()

    def close_menu(self):
        if self.width_menu > 0 :
            self.width_menu -= 30
            self.menu.configure(width = self.width_menu)
            self.after(30,self.close_menu)

    def open_menu(self):
        if self.width_menu < 200 :
            self.width_menu += 30
            self.menu.configure(width = self.width_menu)
            self.after(30,self.open_menu)

window = Window()
window.mainloop()