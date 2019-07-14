import vk_api as vka
import requests
import json
import random

token = "c1b7dfddca48fa79c144af2e8f12352d5f65ba28d6f29ab27a2108453b23e760739757894a69323419381"

vk = vka.VkApi(token=token)

i = 0
group_id = 179062716  # ID вашей группы
count = 0
err = 0
own = 215776978
send_ids = ""
add_id = ""

users = []

with open("users.txt") as f:
    for line in f:
        users.append([int(x) for x in line.split()])
    f.close()

try:
    userids = users[0]
except IndexError:
    users.append([])
    userids = users[0]

print("Bot Online")
print("Users count: " + str(len(userids)))
print("====================================")
print("Users: " + str(userids))

data = requests.get('https://api.vk.com/method/groups.getLongPollServer?group_id=' + str(group_id) + '&access_token=' +
                    token + '&v=5.95').json()['response']
key = str(data['key'])
server = str(data['server'])
ts = str(data['ts'])

while True:
    update = json.loads(requests.get(server + "?act=a_check&key=" + key + "&ts=" + ts + "&wait=25").content)
    ts = update['ts']
    if update['updates'] == []:
        continue
    elif update['updates'][0]['type'] == 'wall_post_new':
        with open("users.txt") as f:
            users = []
            for line in f:
                users.append([int(x) for x in line.split()])
            f.close()
        try:
            userids = users[0]
        except IndexError:
            users.append([])
            userids = users[0]
        if update['updates'][0]['object']['marked_as_ads'] == 0:
            if not 'copy_history' in update['updates'][0]['object']:
                type = update['updates'][0]['object']['attachments'][0]['type']
                own_id = str(update['updates'][0]['object']['attachments'][0][type]['owner_id'])
                id = str(update['updates'][0]['object']['attachments'][0][type]['id'])
                attach = type + own_id + '_' + id
                for ids in userids:
                    vk.method('messages.send', {'user_id': ids, 'random_id': random.randint(1, 999999999999),
                                                'message': update['updates'][0]['object']['text'],
                                                'dont_parse_links': 1, 'attachment': attach})
            elif 'copy_history' in update['updates'][0]['object']:
                with open("users.txt") as f:
                    users = []
                    for line in f:
                        users.append([int(x) for x in line.split()])
                    f.close()
                try:
                    userids = users[0]
                except IndexError:
                    users.append([])
                    userids = users[0]
                type = update['updates'][0]['object']['copy_history'][0]['attachments'][0]['type']
                own_id = str(update['updates'][0]['object']['copy_history'][0]['attachments'][0][type]['owner_id'])
                id = str(update['updates'][0]['object']['copy_history'][0]['attachments'][0][type]['id'])
                attach = type + own_id + '_' + id
                for ids in userids:
                    vk.method('messages.send', {'user_id': ids, 'random_id': random.randint(1, 999999999999),
                                                'message': update['updates'][0]['object']['copy_history'][0]['text'],
                                                'dont_parse_links': 1, 'attachment': attach})
    elif update['updates'][0]['type'] == 'message_new':
        with open("users.txt") as f:
            users = []
            for line in f:
                users.append([int(x) for x in line.split()])
            f.close()
        try:
            userids = users[0]
        except IndexError:
            users.append([])
            userids = users[0]
        request = update['updates'][0]['object']['text']
        from_id = update['updates'][0]['object']['from_id']
        if str.lower(request) == "!рассылка":
            if from_id not in userids:
                vk.method('messages.send', {'user_id': from_id, 'random_id': random.randint(1, 999999999999),
                                            'message': 'Вы подписались на рассылку'})
                userids.append(from_id)
                with open('users.txt', 'w+') as usr:
                    for ids in userids:
                        usr.write(str(ids) + " ")
                    usr.close()
                print("Нa рассылку подписался " + str(from_id))
                continue
            if from_id in userids:
                vk.method('messages.send', {'user_id': from_id, 'random_id': random.randint(1, 999999999999),
                                            'message': 'Вы уже подписанны на рассылку'})
                continue
        if str.lower(request) == "!отписка":
            if from_id not in userids:
                vk.method('messages.send', {'user_id': from_id, 'random_id': random.randint(1, 999999999999),
                                            'message': 'Вы не были подписаны на рассылку'})
                continue
            if from_id in userids:
                vk.method('messages.send', {'user_id': from_id, 'random_id': random.randint(1, 999999999999),
                                            'message': 'Вы отписались от рассылки'})
                userids.remove(from_id)
                with open('users.txt', 'w+') as usr:
                    for ids in userids:
                        usr.write(str(ids) + " ")
                    usr.close()
                print("От рассылки отписался " + str(from_id))
                continue
        if str.lower(request) == "!bot_users" and from_id == own:
            vk.method('messages.send', {'user_id': own, 'random_id': random.randint(1, 999999999999),
                                        'message': len(userids)})
            if len(userids) == 0:
                continue
            elif len(userids) != 0:
                for sids in userids:
                    send_ids = send_ids + str(sids) + "\n"
                vk.method('messages.send', {'user_id': own, 'random_id': random.randint(1, 999999999999),
                                            'message': send_ids})
            continue
        if str.lower(request) == "!bot_save" and from_id == own:
            with open('users.txt', 'w+') as usr:
                for ids in userids:
                    usr.write(str(ids) + " ")
                usr.close()
            vk.method('messages.send', {'user_id': own, 'random_id': random.randint(1, 999999999999),
                                        'message': 'Данные сохранены'})
        if str.lower(request).startswith("!kick_user") and from_id == own:
            try:
                kid = int(request.replace("!kick_user ", ""))
            except ValueError:
                vk.method('messages.send', {'user_id': own, 'random_id': random.randint(1, 999999999999),
                                            'message': 'ID введён неверно'})
                continue
            if kid in userids:
                userids.remove(kid)
                with open('users.txt', 'w+') as usr:
                    for ids in userids:
                        usr.write(str(ids) + " ")
                    usr.close()
                vk.method('messages.send', {'user_id': own, 'random_id': random.randint(1, 999999999999),
                                            'message': 'Данный пользователь успешно удалён'})
                print("Пользователь " + str(kid) + " успешно удалён")
            elif kid not in userids:
                vk.method('messages.send', {'user_id': own, 'random_id': random.randint(1, 999999999999),
                                            'message': 'Данного пользователя нету в списке'})
        if str.lower(request).startswith("!sub") and from_id == own:
            try:
                add_id = int(request.replace("!sub ", ""))
            except ValueError:
                vk.method('messages.send', {'user_id': own, 'random_id': random.randint(1, 999999999999),
                                            'message': 'ID введён неверно'})
            if add_id in userids:
                vk.method('messages.send', {'user_id': own, 'random_id': random.randint(1, 999999999999),
                                            'message': 'Данный пользователь уже подписан на рассылку'})
                continue
            elif add_id not in userids:
                with open('users.txt', 'w+') as usr:
                    for ids in userids:
                        usr.write(str(add_id) + " ")
                    usr.close()
                vk.method('messages.send', {'user_id': own, 'random_id': random.randint(1, 999999999999),
                                            'message': 'Пользователь успешно добавлен'})
                print("Пользователь " + str(add_id) + " успешно добавлен")
        else:
            continue
