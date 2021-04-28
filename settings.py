import datetime

class settings:

    def new_settings():
        try:
            file = open('message.txt', 'r', encoding='utf8')
            file.close()
        except:
            file = open('message.txt', 'w', encoding='utf8')
            settings = ['port = 25565\n',
                        'life_timer = 30\n',
                        'send_timer = 10\n',
                        'auto_timer = 1\n',
                        'auto_sending = 0\n',
                        'life_emitting = 1\n',
                        'message_quantity = 20\n',
                        'search_group_ids = 19582;#;49439086;#;49468741;#;30096257;#;173925080;#;\n',
                        'search_group_names = Алан Рикман - профессор мечты;#;Дома не поймут;#;ты сохранишь;#;Алан Рикман / Alan Rickman. Золотое сердце.;#;пикчи с любовью;#;\n',
                        'protected_group_id = 185848867;#;\n',
                        'protected_group_name = Типичный Снейпоман | Северус Снейп | Алан Рикман;#;\n',
                        'last_launch = 2021-04-28 12:30:00.971916\n',
                        'last_repost = 2021-04-28 12:30:00.971916\n',
                        'last_check_message = 2021-04-28 12:30:00.971916\n',
                        'last_life_action = 2021-04-28 12:30:00.971916\n',]
            file.writelines(settings)
            file.close()

    def get_settings(name, int_ = False, bool_ = False):
        file = open('settings.json', 'r')
        for line in file.readlines():
            set, value = line.split(' = ')
            if set == name:
                if int_ :
                    return int(value)
                if bool_:
                    if value[0] == '1':
                        return True
                    else:
                        return False
                else:
                    return value

    def set_settings(name, num):
        file = open('settings.json', 'r')
        lines = file.readlines()
        file.close
        file = open('settings.json', 'w')
        for line in lines:
            set, value = line.split(' = ')
            if set == name:
                value = str(num)+'\n'
            file.write(set+' = '+value)
        file.close

    def read_msg():
        try:
            file = open('message.txt', 'r', encoding='utf8')
            msg = file.read()
            return msg
        except:
            return ''

    def read_groups(name, prot = False):
        file = open('settings.json', 'r',  encoding='utf8')
        lines = file.readlines()
        file.close()
        for line in lines:
            set, value = line.split(' = ')
            if set == name:
                if prot:
                    group_list = value.split(';#;')[:-1]
                    print(group_list)
                    return group_list[0]
                else:
                    group_list = value.split(';#;')[:-1]
                    print(group_list)
                    return group_list

    def write_groups(name ,num):
        file = open('settings.json', 'r',  encoding='utf8')
        lines = file.readlines()
        file.close
        file = open('settings.json', 'w',  encoding='utf8')
        for line in lines:
            set, value = line.split(' = ')
            if set == name:
                str_ = ''
                for i in range(len(num)):
                    str_ += str(num[i])+';#;'
                str_ += '\n'
                value = str_
            file.write(set+' = '+value)

    def get_time(name):
        file = open('settings.json', 'r',  encoding='utf8')
        for line in file.readlines():
            try:
                set, value = line.split(' = ')
                if set == name:
                    try:
                        time = value.split('\n')
                        return datetime.datetime.strptime(time[0], "%Y-%m-%d %H:%M:%S.%f")
                    except Exception as e:
                        print(str(e))
                        return datetime.datetime.now() - datetime.timedelta(days = 1)
            except:
                pass
        file.close()

    def set_time(name):
        file = open('settings.json', 'r', encoding='utf8')
        lines = file.readlines()
        file.close()
        file = open('settings.json', 'w', encoding='utf8')
        for line in lines:
            try:
                set , value = map(str, line.split(' = '))
                if set == name:
                    value = datetime.datetime.strftime(datetime.datetime.now(), "%Y-%m-%d %H:%M:%S.%f")
                    value += '\n'
                file.write(set+' = '+value)
            except Exception as e:
                Logs.log_write('Got an error: '+str(e), ['settings', 'timer_sending'])
        file.close()
