import socket, threading, time, sys, datetime
from Vk_logic import Vk_accounts
from Commands import commands, Auto_send, Life_emitting
from settings import settings

class Sever:

    launch = commands.launch
    auto_send_launch = False
    life_launch = False
    port = settings.get_settings('port', int_ = True)
    last_launch = None
    s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    addr = []

    first_launch = True
    #choosen_grp = commands.choosen_grp
    #choosen_prot_grp = commands.choosen_prot_grp
    #choosen_main = commands.choosen_main

    def settings(self, file_name):
        #settings.new_settings()
        file = open(file_name, 'r', encoding='utf8')
        for line in file.readlines():
            try:
                name, value = line.split(' = ')
                if name == 'last_launch':
                    try:
                        time = value.split('\n')
                        Sever.last_launch = datetime.datetime.strptime(time[0], "%Y-%m-%d %H:%M:%S.%f")
                    except Exception as e:
                        print(str(e))
                        Sever.last_launch = datetime.datetime.now() - datetime.timedelta(days = 1)
            except:
                pass
        file.close()

    def Launch(self):
        host = socket.gethostbyname(socket.gethostname())
        port = Sever.port #port
        Sever.s.bind((host,port)) #connect host and port to socket
        Sever.addr = (host,port)
        #s.listen(1) #max conections
        print("\n[ Server Launched at " + socket.gethostbyname(socket.gethostname())+":"+str(port)+ "]")

    def Main_cycle(self):
        print("["+time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())+"]")
        commands.port = Sever.port
        commands.last_launch = Sever.last_launch
        print(Sever.last_launch)
        commands.start_time = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S.%f")
        while  Sever.launch == True:
            Sever.launch = commands.launch
            commands.port = Sever.port
            commands.addr = Sever.addr
            if not(commands.auto_sending):
                Sever.auto_send_launch = False
            if not(commands.life_emit):
                Sever.life_launch = False
            a_send = threading.Thread(target = Auto_send.timer_sending , daemon=True, args = ('auto_send',commands.timer))
            life = threading.Thread(target = Life_emitting.main_life_cycle , daemon=True, args = ('life_emmiting', commands.accounts))
            if commands.auto_sending and not(Sever.auto_send_launch):
                Sever.auto_send_launch = True
                a_send.start()
            if commands.life_emit and not(Sever.life_launch):
                Sever.life_launch = True
                life.start()
            time.sleep(1) #раз в 1 секундy получает значения их другого файла

    def input_keyboard(self): #local input
        while Sever.launch == True:
            try:
                addr = (socket.gethostbyname(socket.gethostname()), Sever.port)
                if Sever.first_launch:
                    commands.command_processing('start', addr)
                    Sever.first_launch = False
                inp = input()
                commands.command_processing(inp, addr)
            except:
                pass

    #def input_online(self, soc): #online input
    #    while Sever.launch == True:
    #        data, Sever.addr = soc.recvfrom(1024)
    #        if data.decode("utf-8") == 'con':
    #            Sever.s.sendto('suc'.encode("utf-8"), Sever.addr)
    #            time.sleep(1)
    #            commands.command_processing("acc_list", Sever.addr)
    #        else:
    #            commands.command_processing(data.decode("utf-8"), Sever.addr)

def main():
    Sever.settings('self', 'settings.json')
    Sever.Launch("Starting Server")
    rT1 = threading.Thread(target = Sever.input_keyboard, daemon=True, args = ('s')).start()
    #rT2 = threading.Thread(target = Sever.input_online,daemon=True, args = ('s', Sever.s)).start()
    Sever.Main_cycle("self")
    if not(Sever.launch):
        print("\n[ Server Stopped ]")
        try:
            Sever.s.sendto(("\n[ Server Lost Connection ]").encode("utf-8") ,Sever.addr)
        except:
            pass
        Sever.s.close()
        raise SystemExit

if __name__ == "__main__":
    main()
