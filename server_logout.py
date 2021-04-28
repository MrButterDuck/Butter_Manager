import os, time, socket
from clear_screen import clear

class Logs:

    def log_write(message, addr):
        try:
            os.mkdir('logs')
        except:
            pass
        name = time.strftime("%d-%m-%Y", time.localtime())
        try:
            file = open('logs/'+name+'.txt', 'a', encoding= "utf-8")
        except:
            file = open('logs/'+name+'.txt', 'w', encoding= "utf-8")
        file.write("["+addr[0]+"]=["+str(addr[1])+"]=["+time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())+"] = "+str(message)+'\n')
        print("["+addr[0]+"]=["+str(addr[1])+"]=["+time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())+"]  = "+str(message))
        file.close()

    def user_list(id, Succes = True, error = None):
        try:
            os.mkdir('users')
        except:
            pass
        name = time.strftime("%d-%m-%Y", time.localtime())
        try:
            file = open('users/'+name+'.txt', 'a')
        except:
            file = open('users/'+name+'.txt', 'w')
        if Succes:
            file.write("["+time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())+"] = "+"vk.com/id"+str(id)+' -  Succesfull'+'\n')
            print("["+time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())+"] = "+"vk.com/id"+str(id)+' -  Succesfull'+'\n')
        if not(Succes):
             file.write("["+time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())+"] = "+"vk.com/id"+str(id)+' -  Unsuccesfull: '+str(error)+'\n')
             print("["+time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())+"] = "+"vk.com/id"+str(id)+' -  Unsuccesfull: '+str(error)+'\n')

class Client_output:

    addr = []
    def sendto(message, addr):
        soc = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        if addr == [] or str(addr[0]) == socket.gethostbyname(socket.gethostname()):
            if message == 'clear':
                clear()
            else:
                print(str(message))
        else:
            soc.sendto((str(message)).encode("utf-8"), addr)

    def information(port, account_list_len, main_acc_list, launch_time, chosed_grp, choosed_prot_grp, mes_num, auto_send, time_intr, life_acc, ip = socket.gethostbyname(socket.gethostname()), message = ''  ):
        logo = ["______________________________________________________________________________________________________________________________________________",
                "#  ____            _     _                     __  __                                                                     ___         ___    #",
                "# |  _ \          | |   | |                   |  \/  |                                                                   |__ \       / _ \   #",
                "# | |_) |  _   _  | |_  | |_    ___   _ __    | \  / |   __ _   _ __     __ _    __ _    ___   _ __            __   __      ) |     | | | |  #",
                "# |  _ <  | | | | | __| | __|  / _ \ | '__|   | |\/| |  / _` | | '_ \   / _` |  / _` |  / _ \ | '__|           \ \ / /     / /      | | | |  #",
                "# | |_) | | |_| | | |_  | |_  |  __/ | |      | |  | | | (_| | | | | | | (_| | | (_| | |  __/ | |               \ V /     / /_   _  | |_| |  #",
                "# |____/   \__,_|  \__|  \__|  \___| |_|      |_|  |_|  \__,_| |_| |_|  \__,_|  \__, |  \___| |_|                \_/     |____| (_)  \___/   #",
                "#                                                                                __/ |                                                       #",
                "#                                                                               |___/                                                        #",
                "#____________________________________________________________________________________________________________________________________________#",
                "#                                                     MAIN INFORMATION AND SERVER STATUS                                                     #",
                "#____________________________________________________________________________________________________________________________________________#",
                ]
        logo.append("# SERVER IP: "+str(ip))
        logo.append("# SERVER PORT: "+str(port))
        logo.append("# SERVER WAS LAUNCHED: "+launch_time)
        logo.append("# ACCOUNTS ADDED: "+str(account_list_len))
        logo.append("# MAIN ACCOUNT: "+str(main_acc_list[1])+' '+str(main_acc_list[2]))
        logo.append("# CHOSED GROUPS: "+str(chosed_grp))
        logo.append("# CHOSED PROTECTED GROUP: "+str(choosed_prot_grp))
        logo.append("# MESSAGE QUANTITY: "+str(mes_num))
        logo.append('# MESSAGE: '+message[:20]+'...')
        logo.append("# AUTO SENDING MESSAGES: "+str(auto_send))
        logo.append("# SENDING TIME INTERVAL: "+str(time_intr)+' DAY(S)')
        logo.append("# SIMULATE A LIVE ACCOUNT: "+str(life_acc))
        logo.append("#_____________________________________________________________________________________________________________________________________________ \n")
        try:
            Client_output.sendto('clear', Client_output.addr)
            for i in range(len(logo)):
                Client_output.sendto(logo[i], Client_output.addr)
        except Exception as e:
            Logs.log_write('Got an error: '+str(e), ['server_logout', 'information'])

    def help_list(list):
        try:
            new_list = sorted(list, key= lambda cmd: cmd[0])
            Client_output.sendto("______________________________________________________________________________________________________________________________________________", Client_output.addr)
            for i in range(len(new_list)):
                Client_output.sendto("# "+str(i+1)+" "+new_list[i][0]+" = "+new_list[i][1], Client_output.addr)
            Client_output.sendto("#_____________________________________________________________________________________________________________________________________________ \n", Client_output.addr)
        except Exception as e:
            Logs.log_write('Got an error: '+str(e), ['server_logout', 'help_list'])

    def accout_list(list):
        try:
            Client_output.sendto("______________________________________________________________________________________________________________________________________________", Client_output.addr)
            for i in range(len(list)):
                if i == 0:
                    Client_output.sendto("# "+"\033[93m"+str(i+1)+"\033[0m "+list[i][1]+" "+list[i][2], Client_output.addr)
                else:
                    Client_output.sendto("# "+str(i+1)+" "+list[i][1]+" "+list[i][2], Client_output.addr)
            Client_output.sendto("#_____________________________________________________________________________________________________________________________________________ \n", Client_output.addr)
        except Exception as e:
            Logs.log_write('Got an error: '+str(e), ['server_logout', 'accout_list'])

    def group_list(list):
        try:
            Client_output.sendto("______________________________________________________________________________________________________________________________________________", Client_output.addr)
            for i in range(len(list)):
                Client_output.sendto("# "+str(i+1)+" "+str(list[i][1]), Client_output.addr)
            Client_output.sendto("#_____________________________________________________________________________________________________________________________________________", Client_output.addr)
        except Exception as e:
            Logs.log_write('Got an error: '+str(e), ['server_logout', 'group_list'])

    def message(message):
        try:
            Client_output.sendto("______________________________________________________________________________________________________________________________________________", Client_output.addr)
            Client_output.sendto("# "+str(message), Client_output.addr)
            Client_output.sendto("#_____________________________________________________________________________________________________________________________________________", Client_output.addr)
        except Exception as e:
            Logs.log_write('Got an error: '+str(e), ['server_logout', 'message'])
