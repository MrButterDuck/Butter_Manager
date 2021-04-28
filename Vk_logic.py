import vk_api, time, random
from server_logout import Client_output, Logs
class Vk_accounts:

    def read_file_token(file_name):
        try:
            file = open(file_name, 'r')
        except:
            file.close()
            return None
        list = []
        for line in file.readlines():
            token = line.split()[0]
            try:
                autoris = vk_api.VkApi(token= token)
                vk = autoris.get_api()
                info = vk.account.getProfileInfo()
                list.append([token, info['first_name'], info['last_name'], info['id']])
                vk.account.setOnline(voip = 0)
            except:
                pass
        file.close()
        return list

    def write_file_token(file_name, token, list_adding, list, addr):
        try:
            file = open(file_name, 'a')
        except FileNotFoundError:
            file = open(file_name, 'w')
        try:
            for acc in list:
                if token == acc[0]:
                    Client_output.message('ACCOUNT HAD ALREADY ADDED')
                    return None
        except:
            pass
        try:
            autoris = vk_api.VkApi(token= token)
            vk = autoris.get_api()
            info = vk.account.getProfileInfo()
            vk.account.setOnline(voip = 0)
            file.write(token+'\n')
            file.close()
        except Exception as e:
            Logs.log_write('Got an error: '+str(e), ['Vk_logic', 'write_file_token'])
        if list_adding:
            list.append([token, info['first_name'], info['last_name'], info['id']])
            return list

    def accounts_messages(account_list, num_of_messages, is_user_only, message_list):
        for acc in account_list:
            autoris = vk_api.VkApi(token= acc[0])
            vk = autoris.get_api()
            vk.account.setOnline(voip = 0)
            messages = vk.messages.getConversations(count = num_of_messages)
            message_list = []
            if is_user_only:
                for message in messages.get('items'):
                    if message.get('conversation').get('peer').get('type') == 'user':
                        message_list.append(message.get('conversation').get('peer').get('id'))
            else:
                for message in messages.get('items'):
                    message_list.append(message.get('conversation').get('peer').get('id'))

    def accounts_groups(account_list, num_of_groups, group_list):
        #for acc in account_list:
        autoris = vk_api.VkApi(token= account_list[0][0])
        vk = autoris.get_api()
        vk.account.setOnline(voip = 0)
        groups = vk.groups.get(user_id = account_list[0][3], extended = 1, count = num_of_groups)
        group_list =[]
        for group in groups.get('items'):
            group_list.append([group.get('id'),group.get('name')])
        return group_list

    def group_posts(account_list, group_ids, num_of_posts, post_list, newest = False):
        for id in group_ids:
            autoris = vk_api.VkApi(token= account_list[0][0])
            vk = autoris.get_api()
            vk.account.setOnline(voip = 0)
            posts = vk.wall.get(owner_id = '-'+str(id), count = num_of_posts, filter = 'owner')
            buffer_post = []
            post_list = []
            if newest:
                buffer_post = [posts.get('items')[0].get('id'), posts.get('items')[0].get('date')]
                if buffer_post[0][1] < posts.get('items')[1].get('date') and num_of_posts > 1:
                    buffer_post = [posts.get('items')[1].get('id'), posts.get('items')[1].get('date')]
            else:
                for post in posts.get('items'):
                    buffer_post.append([post.get('id'),post.get('date')])
            post_list.append([buffer_post, id])
        return post_list

    def likes(account_list, post_list, user_id, unquie_users = True, protected_id = 0):
        for posts in post_list:
            for post in posts[0]:
                autoris = vk_api.VkApi(token= account_list[0][0])
                vk = autoris.get_api()
                vk.account.setOnline(voip = 0)
                likes = vk.likes.getList(type = 'post', owner_id = '-'+str(posts[1]), item_id = post[0], extended = 0, count = 1000, skip_own = 1)
                user_id = []
                try:
                    if unquie_users:
                        user_id.append(likes.get('items')[0])
                        for like in likes.get('items'):
                            if like in user_id:
                                pass
                            else:
                                user_id.append(like)
                        try:
                            for id in user_id:
                                if vk.groups.isMember(group_id = '-'+str(protected_id), user_id = str(id)):
                                    user_id.remove(id)
                        except:
                            pass
                    else:
                        for like in likes.get('items'):
                            user_id.append(like)
                except:
                    pass

        return user_id

    def send_messages(account_list, like_list, message, count, sleep_time = 5, only_new = True, message_list = list()):
        if only_new :
            for like in like_list:
                if like in message_list:
                    like_list.remove(like)
        mes = 0
        send_mes = 0
        while send_mes < count:
            for acc in account_list:
                autoris = vk_api.VkApi(token= acc[0])
                vk = autoris.get_api()
                try:
                    vk.account.setOnline(voip = 0)
                    vk.messages.setActivity(user_id = like_list[mes], type = 'typing')
                    time.sleep(random.randint(0,10))
                    vk.messages.send(user_id = like_list[mes], message = message, random_id = random.randint(1, 32000))
                    send_mes += 1
                    Logs.user_list(like_list[mes])
                except Exception as e:
                    Logs.user_list(like_list[mes], Succes = False, error = e)
                time.sleep(sleep_time)
                mes += 1
                if send_mes == count:
                    break
            if(send_mes >= 20 * len(account_list)):
                break

    def post_on_wall(account_info, group_id):
        autoris = vk_api.VkApi(token = account_info[0])
        vk = autoris.get_api()
        try:
            vk.account.setOnline(voip = 0)
            group_posts = vk.wall.get(owner_id = '-'+str(group_id), count = 10, filter = 'owner')
            posts_ids = []
            for id in group_posts.get('items'):
                posts_ids.append(id.get('id'))
            user_posts = vk.wall.get(owner_id = str(account_info[3]), count = 100)
            for id in user_posts.get('items'):
                if id.get('id') in posts_ids:
                    posts_ids.remove(id.get('id'))
            vk.wall.repost(object = 'wall-{0}_{1}'.format(str(group_id), str(posts_ids[random.randint(0,len(posts_ids))])))
        except Exception as e:
            Logs.log_write('Got an error: '+str(e), ['Vk_logic', 'post_on_wall'])

    def send_to_friend(account_list, account_info, send_post = False, message = '', group_id = 0 ):
        autoris = vk_api.VkApi(token = account_info[0])
        vk = autoris.get_api()
        if send_post:
            vk.account.setOnline(voip = 0)
            group_posts = vk.wall.get(owner_id = '-'+str(group_id), count = 10, filter = 'owner')
            posts_ids = []
            for id in group_posts.get('items'):
                posts_ids.append(id.get('id'))
        while True:
            friend_id = account_list[random.randint(0, len(account_list)-1)][3]
            if friend_id == account_info[3]:
                pass
            else:
                vk.account.setOnline(voip = 0)
                if send_post:
                    print(str(friend_id))
                    vk.messages.setActivity(user_id = str(friend_id), type = 'typing')
                    time.sleep(random.randint(0,10))
                    vk.messages.send(user_id = str(friend_id), message = message, attachment = 'wall-{0}_{1}'.format(str(group_id), str(posts_ids[random.randint(0,len(posts_ids))])), random_id = random.randint(1, 32000))
                else:
                    vk.messages.send(user_id = str(friend_id), message = message, random_id = random.randint(1, 32000))
                break

    def set_like(account_info, group_id , post_id):
        try:
            autoris = vk_api.VkApi(token = account_info[0])
            vk = autoris.get_api()
            vk.account.setOnline(voip = 0)
            vk.likes.add(owner_id = '-'+str(group_id), item_id = str(post_id), type = 'post')
        except Exception as e:
            Logs.log_write('Got an error: '+str(e), ['Vk_logic', 'set_like'])

    def answer_on_message(account_list, account_info, latency = 5, message = ''):
        #try:
        autoris = vk_api.VkApi(token = account_info[0])
        vk = autoris.get_api()
        vk.account.setOnline(voip = 0)
        messages = vk.messages.getConversations(count = 25, filter = 'unread', extended = 1)
        for mes in messages.get('items'):
            try:
                if mes.get('last_message').get('attachments')[0].get('type') != 'wall':
                     messages.get('items').remove(mes)
            except:
                messages.get('items').remove(mes)
        for mes in messages.get('items'):
            for acc in account_list:
                if acc[3] == mes.get('conversation').get('peer').get('id'):
                    time.sleep(latency)
                    vk.account.setOnline(voip = 0)
                    vk.messages.markAsRead(start_message_id = mes.get('conversation').get('last_message_id'))
                    vk.messages.setActivity(user_id = acc[3], type = 'typing')
                    time.sleep(random.randint(0,10))
                    vk.messages.send(user_id = acc[3], message = message, random_id = random.randint(1, 500000))
        if messages == [] or messages == None:
            Client_output.message("THERE IS NO ANY MESSAGE")
        #except Exception as e:
        #    Logs.log_write('Got an error: '+str(e), ['Vk_logic', 'answer_on_message'])
