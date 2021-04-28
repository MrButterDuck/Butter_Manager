from Vk_logic import Vk_accounts
from server_logout import Client_output, Logs
from settings import settings
import sys, os, random, datetime, time

class command_list:
    commands = [['add_acc', 'делает запрос на добавление нового аккаунта через токен'],
                ['acc_list', 'возвращает список добавленных аккаунтов'],
                ['acc_main', 'делает запрос на выбор главного аккаунта'],
                ['get_msg', 'возвращает id последних 200 людей, которым писал аккаунт'],
                ['get_grp', 'возвращает id групп, на которые подписан главный аккаунт'],
                ['get_pst', 'возвращает id постов, выбранных групп главного аккаунта'],
                ['get_lks', 'возвращает id людей, которые поставили лайк на посты'],
                ['send_msg', 'запускает отправку сообщений людям, которые поставили лайк на посты'],
                ['auto_send', 'автоматически находит людей для отправки в выбранных группах'],
                ['auto_send_srt', 'автоматически находит людей для отправки в выбранных группах, которым сообщение еще не отправлялось'],
                ['stop', 'останавливает сервер'],
                ['life_emit', 'пытается эмитировать "живой" аккаунт, путем лайков, репостов и сообщений'],
                ['new_port', 'позволяет выбрать новый порт для сервера, необходим пароль, изменения после рестарта'],
                ['help', 'показывает все достпуные команды'],
                ['choose_grp', 'позволяет выбрать группы для поиска людей'],
                ['choose_prot_grp', 'позволяет выбрать группу, в которую будут искать людей'],
                ['repost', 'позволяет сделать репост рандомной одной из последних записей на выбрраный аккаунт'],
                ['send_to_friend', 'позволяет отправить что-то другому боту'],
                ['set_like', 'ставит отментку "нравится" к рандомному посту'],
                ['answer_msg', 'поиск и ответ на сообщения'],
                ['msg_num', 'задает колличество отправляемых сообщений'],
                ['set_timer', 'задает промежуток дней для автоматической отправки'],
                ['timer_send', 'включает функцию автоматической рассылки'],
                ['status', 'выводит обратный счетчик до нового заупска расслыки'],
                ['msg_write', 'позволяет ввести сообщение для рассылки'],
                ]

class commands:

    #settings
    launch = True
    accounts = Vk_accounts.read_file_token('accounts.json')
    messages = []
    groups = []
    protected_group = settings.read_groups('protected_group_id', prot = True)
    message_quantity = settings.get_settings('message_quantity', int_ = True)
    posts = []
    user_id = []
    group_ids = settings.read_groups('search_group_ids')
    group_names = settings.read_groups('search_group_names')
    prot_name = settings.read_groups('protected_group_name', prot = True)
    addr = []
    port = 0
    start_time = ''
    owner_ids = []
    message = settings.read_msg()
    timer = settings.get_settings('auto_timer', int_ = True)
    last_launch = None
    password = 'nfvfhf5230' #главный пароль, недоступный для изменения, требуемый для смены настроек и входа
    auto_sending = settings.get_settings('auto_sending', bool_ = True)
    life_emit = settings.get_settings('life_emitting', bool_ = True)

    life_timer = settings.get_settings('life_timer', int_ = True)
    send_timer = settings.get_settings('send_timer', int_ = True)

    choosen_grp = False
    choosen_prot_grp = False
    choosen_main = False
    choosen_msg = False
    choosen_port = False
    choosen_timer = False
    choosen_timer_send = False
    choosen_life_emit = False
    choose_msg = False
    status = False

    buffer = ''

    def command_processing(input_ask, addr = None, secsion = None):

        cmd_list = command_list.commands
        acc = commands.accounts
        Client_output.addr = addr

        try:
            Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message )
        except:
            Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, ' ', ' ', commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit )

        if commands.choosen_grp:
            Logs.log_write('Got a message: '+str(input_ask), addr)
            try:
                id = input_ask.split()
                commands.group_ids = []; commands.protected_group = 0; commands.group_names = []; commands.prot_name = ''
                for i in range(len(id)):
                    commands.group_ids.append(commands.groups[int(id[i])-1][0])
                    commands.group_names.append(commands.groups[int(id[i])-1][1])
                Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message )
                Client_output.message('SUCCESFULL')
                Logs.log_write('; '.join(commands.group_names), addr)
                commands.choosen_grp = False
                settings.write_groups('search_group_ids',commands.group_ids )
                settings.write_groups('search_group_names',commands.group_names )
                return None
            except Exception as e:
                Logs.log_write('Got an error: '+str(e), addr)
                Client_output.message('GOT AN ERROR, PLEASE TRY AGAIN')
                commands.choosen_grp = False
                return None

        if commands.choosen_prot_grp:
            Logs.log_write('Got a message: '+str(input_ask), addr)
            try:
                id = input_ask.split()
                if not(commands.groups[int(id[0])-1][0] in commands.group_ids):
                    commands.protected_group = commands.groups[int(id[0])-1][0]
                    commands.prot_name = commands.groups[int(id[0])-1][1]
                    Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message  )
                    Client_output.message('SUCCESFULL')
                    Logs.log_write(commands.prot_name, addr)
                    commands.choosen_prot_grp = False
                    settings.write_groups('protected_group_id', [commands.protected_group] )
                    settings.write_groups('protected_group_name', [commands.prot_name] )
                    return None
                else:
                    Client_output.message("THIS GROUP IS ALREADY IN SERACH LIST")
                    return None
            except Exception as e:
                Logs.log_write('Got an error: '+str(e), addr)
                Client_output.message('GOT AN ERROR, PLEASE TRY AGAIN')
                commands.choosen_prot_grp = False
                return None

        if commands.choosen_main:
            Logs.log_write('Got a message: '+str(input_ask), addr)
            id = input_ask.split()
            try:
                buffer = commands.accounts
                commands.accounts = []
                commands.accounts.append(buffer.pop(int(id[0])-1))
                for i in range(len(buffer)):
                    commands.accounts.append(buffer[i])
                Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message  )
                Client_output.message('SUCCESFULL')
                commands.choosen_main = False
                return commands.accounts
            except Exception as e:
                Logs.log_write('Got an error: '+str(e), addr)
                Client_output.message('GOT AN ERROR, PLEASE TRY AGAIN')
                commands.choosen_main = False
                return commands.choosen_main

        if commands.choosen_msg:
            Logs.log_write('Got a message: '+str(input_ask), addr)
            try:
                num = input_ask.split()
                if int(num[0]) > len(commands.accounts) * 20:
                    Client_output.message('TO MANY FOR '+str(len(commands.accounts))+' ACCOUNTS')
                    commands.choosen_msg = False
                    return commands.choosen_msg
                else:
                    commands.message_quantity = int(num[0])
                    Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message  )
                    Client_output.message('SUCCESFULL')
                    commands.choosen_msg = False
                    settings.set_settings('message_quantity', commands.message_quantity)
                    return commands.message_quantity
            except Exception as e:
                Logs.log_write('Got an error: '+str(e), addr)
                Client_output.message('GOT AN ERROR, PLEASE TRY AGAIN')
                commands.choosen_msg = False
                return commands.choosen_msg

        if commands.choosen_port:
            try:
                new_port = input_ask.split()
                if len(new_port[0]) <= 6 and len(new_port[0]) >= 4:
                    settings.set_settings('port', new_port[0])
                    Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message  )
                    Client_output.message('SUCCESFULL')
                    commands.choosen_port = False
                    return commands.choosen_port
                else:
                    Client_output.message("INCORRECT PORT INDEX, PORT HADN'T CHANGED")
                    commands.choosen_port = False
                    return commands.choosen_port
            except Exception as e:
                Logs.log_write('Got an error: '+str(e), addr)
                Client_output.message('GOT AN ERROR, PLEASE TRY AGAIN')
                commands.choosen_port = False
                return commands.choosen_port

        if commands.choosen_timer:
            Logs.log_write('Got a message: '+str(input_ask), addr)
            try:
                days = input_ask.split()
                if int(days[0]) < 1:
                    Client_output.message('MINIMAL DAYS - 1')
                    commands.choosen_timer = False
                    return commands.choosen_timer
                else:
                    commands.timer = int(days[0])
                    Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message  )
                    Client_output.message('SUCCESFULL')
                    settings.set_settings('auto_timer', days[0])
                    commands.choosen_timer = False
                    return commands.timer
            except Exception as e:
                Logs.log_write('Got an error: '+str(e), addr)
                Client_output.message('GOT AN ERROR, PLEASE TRY AGAIN')
                commands.choosen_timer = False
                return commands.choosen_timer

        if commands.choosen_timer_send:
            Logs.log_write('Got a message: '+str(input_ask), addr)
            try:
                answer = input_ask.split()
                if answer[0].upper() == 'Y' or answer[0].upper() == 'YES':
                    commands.auto_sending = True
                    Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message  )
                    Client_output.message('SUCCESFULL TOGGLED ON')
                    commands.choosen_timer_send = False
                    settings.set_settings('auto_sending', 1)
                    return None
                elif answer[0].upper() == 'N' or answer[0].upper() == 'NO':
                    commands.auto_sending = False
                    Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message  )
                    Client_output.message('SUCCESFULL TOGGLED OFF')
                    commands.choosen_timer_send = False
                    settings.set_settings('auto_sending', 0)
                    return None
                else:
                    Client_output.message("CAN NOT READ THE ANSWER, PLEASE TRY AGAIN")
                    commands.choosen_timer_send = False
                    return None
            except Exception as e:
                Logs.log_write('Got an error: '+str(e), addr)
                Client_output.message('GOT AN ERROR, PLEASE TRY AGAIN')
                commands.choosen_timer_send = False
                return None

        if commands.choosen_life_emit:
            Logs.log_write('Got a message: '+str(input_ask), addr)
            try:
                answer = input_ask.split()
                if answer[0].upper() == 'Y' or answer[0].upper() == 'YES':
                    commands.life_emit = True
                    Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message  )
                    Client_output.message('SUCCESFULL TOGGLED ON')
                    commands.choosen_life_emit = False
                    settings.set_settings('life_emitting', 1)
                    return None
                elif answer[0].upper() == 'N' or answer[0].upper() == 'NO':
                    commands.life_emit = False
                    Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message  )
                    Client_output.message('SUCCESFULL TOGGLED OFF')
                    commands.choosen_life_emit = False
                    settings.set_settings('life_emitting', 0)
                    return None
                else:
                    Client_output.message("CAN NOT READ THE ANSWER, PLEASE TRY AGAIN")
                    commands.choosen_life_emit = False
                    return None
            except Exception as e:
                Logs.log_write('Got an error: '+str(e), addr)
                Client_output.message('GOT AN ERROR, PLEASE TRY AGAIN')
                commands.choosen_life_emit = False
                return None

        if commands.choose_msg:
            Logs.log_write('Got a message: '+str(input_ask), addr)
            try:
                if input_ask.split()[0].upper() == 'S' or input_ask.split()[0].upper() == 'STOP':
                    file = open('message.txt', 'w', encoding='utf8')
                    file.write(commands.buffer)
                    file.close()
                    commands.message = commands.buffer
                    Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message  )
                    Client_output.message('SUCCESFULL')
                    commands.choose_msg = False
                    commands.buffer = None
                    return commands.message
                else:
                    msg = input_ask
                    commands.buffer += msg +'\n'
                    Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message  )
                    Client_output.message(commands.buffer)
                    return None
            except Exception as e:
                Logs.log_write('Got an error: '+str(e), addr)
                Client_output.message('GOT AN ERROR, PLEASE TRY AGAIN')
                commands.choose_msg = False
                return None

        if secsion == None: #основной цикл с командами
            if input_ask == cmd_list[0][0]: #запрос на ввод токена
                Logs.log_write('Got a command: '+str(input_ask), addr)
                Client_output.message('PLEASE, WRITE A TOKEN: ')
                token = input()
                Vk_accounts.write_file_token('accounts.json', token, True, acc, addr)
                return None

            if input_ask == cmd_list[1][0]: # вывод всех аккаунтов
                Logs.log_write('Got a command: '+str(input_ask), addr)
                Client_output.accout_list(commands.accounts)
                return None

            if input_ask == cmd_list[2][0]:  #делает выбранный аккаунт в списке первым
                Logs.log_write('Got a command: '+str(input_ask), addr)
                Client_output.accout_list(commands.accounts)
                Client_output.message('PLEASE, INPUT ACCOUNT INDEX: ')
                commands.choosen_main = True
                return commands.choosen_main

            if input_ask == cmd_list[3][0]: #собирает id сообщения аккаунтов
                Logs.log_write('Got a command: '+str(input_ask), addr)
                Vk_accounts.accounts_messages(commands.accounts, 200, True, commands.messages)
                Client_output.message('SUCCESFULL')
                return None

            if input_ask == cmd_list[4][0]: #cобирает группы
                Logs.log_write('Got a command: '+str(input_ask), addr)
                commands.groups = []
                commands.groups = Vk_accounts.accounts_groups(commands.accounts, 100, commands.groups)
                Client_output.message('SUCCESFULL')
                return None

            if input_ask == cmd_list[5][0]: #cобирает посты
                Logs.log_write('Got a command: '+str(input_ask), addr)
                if commands.group_ids == None or commands.protected_group == 0:
                    Client_output.message("YOU DIDN'T CHOSE A SEARCH GROUPS OR PROTECTED GROUP")
                    return None
                else:
                    commands.posts = Vk_accounts.group_posts(commands.accounts, commands.group_ids, 10, commands.posts)
                    Client_output.message('SUCCESFULL')
                    return None

            if input_ask == cmd_list[6][0]: #cобирает лайки
                Logs.log_write('Got a command: '+str(input_ask))
                commands.user_id = Vk_accounts.likes(commands.accounts, commands.posts, commands.user_id, protected_id = commands.protected_group)
                Client_output.message('SUCCESFULL')
                return None

            if input_ask == cmd_list[7][0]: #отправляет сообщения
                Logs.log_write('Got a command: '+str(input_ask), addr)
                if commands.group_ids == None or commands.protected_group == 0 or  commands.message_quantity == 0:
                    Client_output.message("YOU DIDN'T CHOSE A PROTECTED GROUP, GROUPS FOR SEARCH OR MESSAGE QUANTITY")
                    return None
                else:
                    Vk_accounts.send_messages(commands.accounts, commands.user_id, commands.message,  commands.message_quantity, message_list = commands.messages, sleep_time = commands.send_timer)
                    Client_output.message('SUCCESFULL')
                    return None

            if input_ask == cmd_list[8][0]: #автоматичский процесс поиска людей и рассылки
                Logs.log_write('Got a command: '+str(input_ask), addr)
                Vk_accounts.accounts_messages(commands.accounts, 200, True, commands.messages)
                if commands.group_ids == None or commands.protected_group == 0 or  commands.message_quantity == 0:
                    Client_output.message("YOU DIDN'T CHOSE A PROTECTED GROUP, GROUPS FOR SEARCH OR MESSAGE QUANTITY")
                    return None
                else:
                    commands.posts = Vk_accounts.group_posts(commands.accounts, commands.group_ids, 10, commands.posts)
                    commands.user_id = Vk_accounts.likes(commands.accounts, commands.posts, commands.user_id)
                    Vk_accounts.send_messages(commands.accounts, commands.user_id, commands.message,  commands.message_quantity, only_new = False, sleep_time = commands.send_timer)
                    Client_output.message('SUCCESFULL')
                    return None

            if input_ask == cmd_list[9][0]: #автоматичский процесс поиска людей и рассылки c фильтром тех, кому не было отправлений
                Logs.log_write('Got a command: '+str(input_ask), addr)
                Vk_accounts.accounts_messages(commands.accounts, 200, True, commands.messages)
                if commands.group_ids == None or commands.protected_group == 0 or  commands.message_quantity == 0:
                    Client_output.message("YOU DIDN'T CHOSE A PROTECTED GROUP, GROUPS FOR SEARCH OR MESSAGE QUANTITY")
                    return None
                else:
                    commands.posts = Vk_accounts.group_posts(commands.accounts, commands.group_ids, 10, commands.posts)
                    commands.user_id = Vk_accounts.likes(commands.accounts, commands.posts, commands.user_id)
                    Vk_accounts.send_messages(commands.accounts, commands.user_id, commands.message, commands.message_quantity, message_list = commands.messages, sleep_time = commands.send_timer)
                    Client_output.message('SUCCESFULL')
                    return None

            if input_ask == cmd_list[10][0]: #остановка сервера
                Logs.log_write('Got a command: '+str(input_ask), addr)
                Client_output.message('SERVER HAS BEEN STOPPED')
                commands.launch = False
                return commands.launch

            if input_ask == cmd_list[11][0]: #эмитация жизни
                Logs.log_write('Got a command: '+str(input_ask), addr)
                #if commands.protected_group == 0:
                #    Client_output.message("YOU DIDN'T CHOSE A PROTECTED GROUP")
                #    return None
                #else:
                Client_output.message('ARE YOU WANT TO TOGGLE AUTO SENDING ON? Y(YES)/N(NO)')
                commands.choosen_life_emit = True
                return commands.choosen_life_emit

            if input_ask == cmd_list[12][0]: #смена порта сервера
                Logs.log_write('Got a command: '+str(input_ask), addr)
                #Client_output.message('PLEASE, WRITE ADMIN PASSWORD ')
                #inp = input()
                #if commands.password == inp:
                Client_output.message('PLEASE, WRITE NEW PORT(FROM 4 TO 6 NUMBERS) ')
                commands.choosen_port = True
                #else:
                #    Client_output.message("WRONG PASSWORD")
                return commands.choosen_port

            if input_ask == cmd_list[13][0]: #выодит список всех команд
                Logs.log_write('Got a command: '+str(input_ask), addr)
                Client_output.help_list(cmd_list)
                return None

            if input_ask == cmd_list[14][0]: #выбор групп для поиска
                Logs.log_write('Got a command: '+str(input_ask), addr)
                if commands.groups != []:
                    Client_output.group_list(commands.groups)
                    Client_output.message('PLEASE, INPUT GROUP INDEXS WITH SPACE ')
                    commands.choosen_grp = True
                    return commands.choosen_grp
                else:
                    Client_output.message("ACCOUNT GROUPS INFORMATION IS ABSENT")
                    return None

            if input_ask == cmd_list[15][0]: #выбор группы, для которой ищут
                Logs.log_write('Got a command: '+str(input_ask), addr)
                if commands.groups != [] and commands.group_ids != []:
                    Client_output.group_list(commands.groups)
                    Client_output.message('PLEASE, INPUT PROTECTED GROUP INDEX ')
                    commands.choosen_prot_grp = True
                    return commands.choosen_prot_grp
                else:
                    Client_output.message("YOU DIDN'T CHOSE A SEARCH GROUPS OR PROTECTED GROUP")
                    return None

            if input_ask == cmd_list[16][0]: #делает репост
                Logs.log_write('Got a command: '+str(input_ask), addr)
                if commands.protected_group != 0:
                    try:
                        Vk_accounts.post_on_wall(commands.accounts[0], commands.protected_group)
                        Client_output.message('SUCCESFULL')
                        return None
                    except Exception as e:
                        Logs.log_write('Got an error: '+str(e), addr)
                        return None
                else:
                    Client_output.message("PROTECTED GROUP INFORMATION IS ABSENT")
                    return None

            if input_ask == cmd_list[17][0]: #отсылает что-тo другу
                Logs.log_write('Got a command: '+str(input_ask), addr)
                if commands.protected_group != 0:
                    Vk_accounts.send_to_friend(commands.accounts, commands.accounts[0], send_post = True, group_id = commands.protected_group)
                    Client_output.message('SUCCESFULL')
                    return None
                else:
                    Client_output.message("PROTECTED GROUP INFORMATION IS ABSENT")
                    return None

            if input_ask == cmd_list[18][0]: #ставит лайк
                Logs.log_write('Got a command: '+str(input_ask), addr)
                if commands.posts != []:
                    rand_group = commands.posts[random.randint(0, len(commands.posts)-1)]
                    Vk_accounts.set_like(commands.accounts[0], rand_group[-1], rand_group[0][random.randint(0, len(rand_group[0])-2)][0] )
                    Client_output.message('SUCCESFULL')
                    return None

            if input_ask == cmd_list[19][0]: #ответ на сообщения
                Logs.log_write('Got a command: '+str(input_ask), addr)
                Vk_accounts.answer_on_message(commands.accounts, commands.accounts[0], latency = 3, message = 'лол :)')
                Client_output.message('SUCCESFULL')
                return None

            if input_ask == cmd_list[20][0]: #кол-во сообщений
                Logs.log_write('Got a command: '+str(input_ask), addr)
                Client_output.message('PLEASE, WRITE A MESSAGE QUANTITY')
                commands.choosen_msg = True
                return commands.choosen_msg

            if input_ask == cmd_list[21][0]: #кол-во дней
                Logs.log_write('Got a command: '+str(input_ask), addr)
                if commands.auto_sending:
                    Client_output.message('YOU NEED TO TOGGLE OFF AUTO SENDING FIRSTLY')
                    return None
                else:
                    Client_output.message('PLEASE, WRITE A DAY QUANTITY')
                    commands.choosen_timer = True
                    return commands.choosen_timer

            if input_ask == cmd_list[22][0]: #автоматическая рассылка
                Logs.log_write('Got a command: '+str(input_ask), addr)
                if commands.group_ids == None or commands.protected_group == 0 or  commands.message_quantity == 0:
                    Client_output.message("YOU DIDN'T CHOSE A PROTECTED GROUP, GROUPS FOR SEARCH OR MESSAGE QUANTITY")
                    return None
                elif commands.timer == 0:
                    Client_output.message("YOU DIDN'T SET A TIMER")
                    return None
                else:
                    Client_output.message('ARE YOU WANT TO TOGGLE AUTO SENDING ON? Y(YES)/N(NO)')
                    commands.choosen_timer_send = True
                return commands.choosen_timer_send

            if input_ask == cmd_list[23][0]: #статус
                Logs.log_write('Got a command: '+str(input_ask), addr)
                Client_output.message('SUCCESFULL')
                commands.status = not(commands.status)
                return commands.status

            if input_ask == cmd_list[24][0]: #ввод сообщения
                Logs.log_write('Got a command: '+str(input_ask), addr)
                Client_output.message('PLEASE, INPUT MESSAGE LINE BY LINE, TO STOP MESSAGE INPUT WTIRE "STOP" OR "S"')
                commands.choose_msg = True
                return commands.choose_msg

            if input == 'start':
                return None

            elif input not in cmd_list and not(commands.choose_msg):
                Logs.log_write('Unknow command: '+str(input_ask), addr)
                Client_output.message('UNKNOW COMMAND')


class Auto_send:

    def timer_sending(self, wait_time, latency = commands.send_timer):
        while commands.auto_sending:
            if datetime.datetime.now() >= commands.last_launch + datetime.timedelta(days = wait_time):
                try:
                    if commands.life_emit == True:
                        life_was = True
                        commands.life_emit = False
                        time.sleep(5)
                    Vk_accounts.accounts_messages(commands.accounts, 200, True, commands.messages)
                    Client_output.message('SUCCESFULL COLLECTED MESSAGES')
                    commands.posts = Vk_accounts.group_posts(commands.accounts, commands.group_ids, 10, commands.posts)
                    Client_output.message('SUCCESFULL COLLECTED POSTS')
                    commands.user_id = Vk_accounts.likes(commands.accounts, commands.posts, commands.user_id)
                    Client_output.message('SUCCESFULL COLLECTED USER IDS')
                    Vk_accounts.send_messages(commands.accounts, commands.user_id, commands.message,  (commands.message_quantity + len(acc_list)*10), only_new = False, sleep_time = latency)
                    Client_output.message('SUCCESFULL SENDED MESSAGES')
                    settings.set_time('last_launch')
                except Exception as e:
                    Logs.log_write('Got an error: '+str(e), ['Auto_send', 'timer_sending'])
            if commands.status:
                deff = commands.last_launch+ datetime.timedelta(days = wait_time) - datetime.datetime.now()
                days, seconds = deff.days, deff.seconds
                hours = days * 24 + seconds // 3600
                minutes = (seconds % 3600) // 60
                seconds = (seconds % 60)
                Client_output.information(commands.port, len(commands.accounts), commands.accounts[0], commands.start_time, '; '.join(commands.group_names), commands.prot_name, commands.message_quantity ,commands.auto_sending, commands.timer, commands.life_emit, message = commands.message  )
                Client_output.message('BEFORE NEW AUTO LAUNCH: '+"{0}:{1}:{2}".format(hours, minutes, seconds))
                time.sleep(1)

class Life_emitting:

    def rand_choice(list, numbs):
        while True:
            new = True
            rand_choice = random.randint(0, len(list))
            if rand_choice in numbs or rand_choice == len(list):
                new = False
            if new:
                numbs.append(rand_choice)
                if len(numbs) > (len(list) // 2):
                    numbs.pop(0)
                break
        return rand_choice


    def main_life_cycle(self, account_list, latency = commands.life_timer):
        last_launch = settings.get_time('last_life_action')
        last_checking_msg = settings.get_time('last_check_message')
        last_post_on_wall = settings.get_time('last_repost')
        rand_choises_acc = []
        rand_choises_grp = []
        rand_answer = []
        rand_msg = []
        post_comments = ['']
        msg_answers = []

        try:
            file = open('post_comments.txt', 'r', encoding='utf8')
            for line in file.readlines():
                post_comments.append(line)
            file.close()

            file = open('msg_answers.txt', 'r', encoding='utf8')
            for line in file.readlines():
                msg_answers.append(line)
            file.close()
        except:
            pass
        while commands.life_emit:
            try:
                if datetime.datetime.now() >= last_launch + datetime.timedelta(minutes = latency):
                    acc = account_list[Life_emitting.rand_choice(account_list, rand_choises_acc)]
                    groups = []
                    groups = Vk_accounts.accounts_groups([acc, None], 100, groups)
                    case = round(random.uniform(0, 1), 1)
                    if case >= 0 and case < 0.1:
                        if datetime.datetime.now() >= last_post_on_wall + datetime.timedelta(minutes = latency*24):
                            Logs.log_write(acc[1]+' '+acc[2]+' posted something on wall', ['Life_emitting', 'main_life_cycle'])
                            Vk_accounts.post_on_wall(acc, groups[Life_emitting.rand_choice(groups, rand_choises_grp)][0])
                            last_post_on_wall = datetime.datetime.now()
                            settings.set_time('last_repost')
                            last_launch = datetime.datetime.now()
                            settings.set_time('last_life_action')
                            Client_output.message(acc[1].upper()+' '+acc[2].upper()+' POSTED SOMETHING ON WALL')
                    if case >= 0.1 and case < 0.6:
                        Logs.log_write(acc[1]+' '+acc[2]+' send something to friend', ['Life_emitting', 'main_life_cycle'])
                        Vk_accounts.send_to_friend(account_list, acc, send_post = True, group_id = groups[Life_emitting.rand_choice(groups, rand_choises_grp)][0], message = post_comments[Life_emitting.rand_choice(post_comments, rand_msg)] )
                        last_launch = datetime.datetime.now()
                        settings.set_time('last_life_action')
                        Client_output.message(acc[1].upper()+' '+acc[2].upper()+' SEND SOMETHING TO FRIEND')
                    if case >= 0.6 :
                        Logs.log_write(acc[1]+' '+acc[2]+' liked some post', ['Life_emitting', 'main_life_cycle'])
                        posts = []
                        posts = Vk_accounts.group_posts([acc, None], [groups[Life_emitting.rand_choice(groups, rand_choises_grp)][0]], 10, posts)
                        Vk_accounts.set_like(acc, posts[0][-1], posts[0][0][random.randint(0, len( posts[0][0]))][0])
                        last_launch = datetime.datetime.now()
                        settings.set_time('last_life_action')
                        Client_output.message(acc[1].upper()+' '+acc[2].upper()+' LIKED SOME POST')
                    groups = []; posts = []

                if datetime.datetime.now() >= last_checking_msg + datetime.timedelta(minutes = latency//2):
                    acc = account_list[Life_emitting.rand_choice(account_list, rand_choises_acc)]
                    Vk_accounts.answer_on_message(account_list, acc, latency = 3, message = msg_answers[Life_emitting.rand_choice(msg_answers, rand_answer)])
                    Logs.log_write(acc[1]+' '+acc[2]+' answered on message', ['Life_emitting', 'main_life_cycle'])
                    Client_output.message(acc[1].upper()+' '+acc[2].upper()+' ANSWERED ON MESSAGE')
                    last_checking_msg = datetime.datetime.now()
                    settings.set_time('last_check_message')

            except Exception as e:
                #last_launch = datetime.datetime.now()
                Logs.log_write('Got an error: '+str(e), ['Life_emitting', 'main_life_cycle'])
                Client_output.message('GOT AN ERROR: '+str(e))
