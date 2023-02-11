from datetime import datetime
import time
import socket
import threading
from tkinter import *
from PIL.Image import init 
import requests 
import json
from tkinter import messagebox

HostName = socket.gethostname()
HOST = socket.gethostbyname(HostName)
#HOST = "127.0.0.1"
class server:
    def __init__(self):
        update=threading.Thread(target=self.updateData,daemon=TRUE)
        update.start()
        self.Window = Tk()
        self.Window.iconbitmap('c.ico')
        self.Window.withdraw()
        self.InputPort()
        self.Window.mainloop()
    def InputPort(self):
        self.login = Toplevel()
        self.login.iconbitmap('c.ico')
        self.login.title("OPEN PORT")
        self.login.resizable(width=False,
                             height=False)
        self.login.configure(width=400,
                             height=300)
        self.pls = Label(self.login,
                         text="NHẬP PORT MỞ",
                         justify=CENTER,
                         font="Helvetica 14 bold")

        self.pls.place(x=140, y=30)
        # create a Label
        self.labelName = Label(self.login,
                               text="PORT: ",
                               font="Helvetica 12")

        self.labelName.place(relheight=0.2,
                             relx=0.2,
                             rely=0.15)

        self.entryName = Entry(self.login,
                               font="Helvetica 14")

        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)

        self.entryName.focus()

        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Calibri 14",
                         command=lambda: self.goAhead(self.entryName.get()), bg='#154c79', fg='white')

        self.go.place(relx=0.42,
                      rely=0.4)

        self.login.protocol("WM_DELETE_WINDOW", self.Quit) 
        self.login.mainloop()
    def goAhead(self, name):
        try:
            if int(name) <= 1024:
                messagebox.showerror('ERROR','cannot open this port')
            else:
                global PORT
                PORT =int(name)
                self.login.destroy()

                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((HOST, PORT))
                self.s.listen()

                self.dateTime=datetime.today().strftime('%Y-%m-%d')
                self.fileName=f'{self.dateTime}.json'
                f=open(self.fileName)
                self.dataToday=json.load(f)

                self.running = True
                self.layout()

        except:
            messagebox.showinfo('ERROR', 'cannot open this port')

    def check_ClientLogin(self,data):
        with open('ClientData.json','r') as f:
            UserData = json.loads(f.read())
        f.close()
        for item in Live_user:
            if(data[0]==item):
                return 0
        for user in UserData['UserAccount']:
            if(user['Username']==data[0] and user['Password']==data[1]):
                return 1
                break
        return 2

    def check_ClientRegister(self,data):
        with open('ClientData.json','r') as f:
            UserData = json.loads(f.read())
        f.close()
        for user in UserData['UserAccount']:
            if(user['Username']==data[0] ):
                return 0
            
        Info = {
            "Username": data[0],
            "Password": data[1]
        }
        UserData['UserAccount'].append(Info)
        js_string = json.dumps(UserData,indent = 2)
        with open('ClientData.json','w') as w:
            w.write(js_string)
        w.close()
        return 1

    def recvData(self,data):
        temp=data.replace("]","").replace("[","").replace("'","").replace(" ","")
        Data= list(temp.split(","))
        return Data

    def clientLogin(self,conn,data,addr):
        accept = self.check_ClientLogin(data)
        conn.send(str.encode(str(accept)))
        if accept==1:
            name=data[0]
            ID.append(name)
            Live_user.append(name)
            self.count+=1
            conn.send(str.encode(name))
            self.handle(conn,addr,name)

    def ClientRegister(self,sck,data):
        accept = self.check_ClientRegister(data)
        msg = str(accept)
        sck.send(str.encode(msg))
        return

    def layout(self):
        self.Window.deiconify()
        self.Window.title("SERVER")
        self.Window.configure(width=520,
                              height=550,
                              bg="#7E9DC2")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=rf'SERVER COVID-19 Ở VIỆT NAM''\n'
                               rf'HOST : {HOST} '
                               rf'PORT {PORT}',
                               font="Helvetica 13 bold")
            
        self.labelHead.place(relwidth=1)

        self.textCons = Text(self.Window,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Calibri 13",
                            )
        self.labelBottom = Label(self.Window,
                                 bg="#17202A",
                                 height=80)

        self.labelBottom.place(relwidth=1,
                               rely=0.825)

        self.buttonMsg = Button(self.labelBottom,
                                text="STOP SERVER",
                                font="Calibri 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=self.Quit)
        self.countActive = Label(self.labelBottom,
                               bg="#17202A",
                               fg="#EAECEE", 
                               text='ĐANG HOẠT ĐỘNG: 0\n' 
                               'SỐ LƯỢT TRUY CẬP HÔM NAY: 0 ',
                               font="Helvetica 13 bold")
        self.countActive.place(relx=0.01,
                             rely=0.008)
        
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)

        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)

        scrollbar = Scrollbar(self.textCons)

        scrollbar.place(relheight=1,
                        relx=0.974)

        scrollbar.config(command=self.textCons.yview)

        self.textCons.config(state=DISABLED)
        gui = threading.Thread(target=self.main,daemon=True)
        gui.start()
        self.Window.protocol("WM_DELETE_WINDOW", self.Quit) 
    def Quit(self):
        try:
            if messagebox.askokcancel("Quit", "Do you want to quit?"):
                self.running = False
                self.login.destroy()
                self.Window.destroy()
        except:
            pass
    def searchCovid(self,name):
        temp=name.split(',')
        self.fileName=f'{temp[1]}.json'
        try:
            self.data=json.load(open(self.fileName))
        except:
            return "Khong co DL"
        if(temp[0]==""): #search by day
            return self.data
        else: #search by day and name
            for location in self.data['locations']:
                if(temp[0]==location['name']):
                    return location
    def handle(self,conn,addr,cus):
        conn.send(str.encode(str(self.dataToday)))
        nowTime=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
        message=f'{cus}: {addr} connected at {nowTime}'
        self.print(message)
        self.countActive.config(text=f'ACTIVE CONNECTED: {threading.activeCount() - 3 }\n'
                                    f'SỐ LƯỢT TRUY CẬP HÔM NAY: {self.count} ')
        while True:
            try:
                data=conn.recv(2048)
                name=data.decode('utf-8')
                if(name=="logout"):
                    Live_user.remove(cus)
                    conn.send(str.encode("ok"))
                    nowTime=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
                    message=f'{cus}: {addr} disconnected at {nowTime}'
                    self.print(message)
                    self.countActive.config(text=f'ACTIVE CONNECTED: {threading.activeCount() - 4} \n'
                                            f'SỐ LƯỢT TRUY CẬP HÔM NAY: {self.count} ')
                    return
                else:
                    rs = self.searchCovid(name)
                    msg=str(rs)
                    conn.send(str.encode(msg))
            except:
                nowTime=datetime.today().strftime('%Y-%m-%d-%H:%M:%S')
                message=f'{cus}: {addr} disconnected at {nowTime}'
                Live_user.remove(cus)
                self.print(message)
                self.countActive.config(text=f'ACTIVE CONNECTED: {threading.activeCount() - 4} \n'
                                        f'SỐ LƯỢT TRUY CẬP HÔM NAY: {self.count} ')
                # conn.close()
                break
    def updateData(self):
        while True:
            dateTime=datetime.today().strftime('%Y-%m-%d')
            data = requests.get('https://static.pipezero.com/covid/data.json').json()
            with open(f'{dateTime}.json', 'w') as myfile:
                json.dump(data,myfile, indent=1)
            time.sleep(60*60)
    def print(self,message):
        self.textCons.config(state = NORMAL)
        self.textCons.insert(END,message+"\n")
        self.textCons.config(state = DISABLED)
    def Runserver(self,conn,addr):
        while True:
            try:
                inf=conn.recv(1024).decode('utf-8')
                data = self.recvData(inf)
                option = data[2]
                if option == LOGIN:
                    self.clientLogin(conn,data,addr)
                
                elif option == SIGNUP:
                    self.ClientRegister(conn,data)
            except:
                conn.close()
                break
    def main(self):
        self.count=0
        while self.running:
            conn,addr=self.s.accept()
            thread=threading.Thread(target=self.Runserver,args=(conn,addr))
            thread.start()


SIGNUP = "signup"
LOGIN = "login"
FORMAT="uft-8"
LARGE_FONT = ("verdana", 13,"bold")
Live_Account=[]
ID=[]
Live_user =[]
s = server() 
