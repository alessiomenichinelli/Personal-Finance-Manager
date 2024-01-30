import telebot
import requests
from base64 import b64encode
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

TOKEN = ''
BAL_URL = 'http://hostname/api/balances/'
PM_URL = 'http://hostname/api/pm/'
PROF_URL = 'http://hostname/api/profiles/'
PROF_NEW_URL = 'http://hostname/api/profiles/new/'
USERS_URL = 'http://hostname/api/users/'

bot = telebot.TeleBot(TOKEN, parse_mode=None)

message_list = []
user_occ = {}

def clear_markup():
     if len(message_list) != 0:
          for mes in message_list:
               bot.edit_message_reply_markup(chat_id = mes.chat.id, message_id = mes.message_id)
               message_list.remove(mes)

def gen_markup(dict, n):
     markup = InlineKeyboardMarkup()
     markup.row_width = n
     for key in dict:
        markup.add(InlineKeyboardButton(key, callback_data=dict[key]))
     return markup

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "blc":
        clear_markup()
        send_balances(call.message)
    if call.data == "rgs":
        clear_markup()
        register(call.message)
    if call.data == "pm":
        clear_markup()
        send_pm(call.message)
    else:
        clear_markup()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    ids = []
    headers = {'X-CHAT-ID':''}
    r = requests.get(PROF_URL, headers=headers)
    datas = r.json()
    for profile in datas:
         ids.append(profile['chat_id'])

    if(message.chat.id in ids):
        string = "Ciao " + message.chat.first_name + "!\nCosa vuoi fare?"
        markup = gen_markup({"Bilanci":"blc", "Metodi di Pagamento":"pm"}, 2)
    else:
        string = "Benvenuto " + message.chat.first_name +"!\n"
        markup = gen_markup({"Registrati":"rgs"}, 1)

    Message = bot.send_message(message.chat.id, string, reply_markup=markup)
    message_list.append(Message)

@bot.message_handler(commands=['register'])
def register(message):
    clear_markup()
    ids = []
    headers = {'X-CHAT-ID':''}
    r = requests.get(PROF_URL, headers=headers)
    datas = r.json()
    for profile in datas:
         ids.append(profile['chat_id'])

    if(message.chat.id in ids):
        string = "Utente già registrato"
        bot.send_message(message.chat.id, string)
    else:
        string = "Non sei registrato?\nhttp://hostname\nSei già registrato?\nUsername:"
        bot.send_message(message.chat.id, string)

        @bot.message_handler(func=lambda m: True)
        def register_u(message):
            global user_occ
            user_occ['username'] = str(message.text)
            string = "Password:"
            bot.send_message(message.chat.id, string)

            @bot.message_handler(func=lambda m: True)
            def register_p(message):
                global user_occ
                user_occ['password']= str(message.text)
                mess = user_occ['username']+":"+user_occ['password']
                mess_bytes = mess.encode('ascii')
                base64_bytes = b64encode(mess_bytes)
                mess = base64_bytes.decode('ascii')
                headers = {'Authorization':'Basic '+mess}
                data = {"chat_id": message.chat.id, "name": message.chat.first_name}
                r = requests.post(PROF_NEW_URL, headers=headers, data=data)
                data = {}
                if ((r.status_code == requests.codes.created) == True):
                    string = "Aggiunto!"
                else:
                    string = "Errore, Riprova!"

                bot.send_message(message.chat.id, string)
            
            bot.register_next_step_handler(message, register_p)
        
        bot.register_next_step_handler(message, register_u)

@bot.message_handler(commands=['balances'])
def send_balances(message):
    clear_markup()
    ids = []
    headers = {'X-CHAT-ID':''}
    r = requests.get(PROF_URL, headers=headers)
    datas = r.json()
    for profile in datas:
         ids.append(profile['chat_id'])

    if(message.chat.id not in ids):
        string = "Utente non registrato"
        bot.send_message(message.chat.id, string)
    else:
        string = "I tuoi bilanci:\n\n"
        headers = {'X-CHAT-ID':str(message.chat.id)}
        r = requests.get(BAL_URL, headers=headers)
        datas = r.json()
        for bal in datas:
            string += str(bal['name'])+": "+str(bal['amount'])+"\n"
        bot.send_message(message.chat.id, string)

@bot.message_handler(commands=['payment_methods'])
def send_pm(message):
    clear_markup()
    ids = []
    headers = {'X-CHAT-ID':''}
    r = requests.get(PROF_URL, headers=headers)
    datas = r.json()
    for profile in datas:
         ids.append(profile['chat_id'])

    if(message.chat.id not in ids):
        string = "Utente non registrato"
        bot.send_message(message.chat.id, string)
    else:
        string = "I tuoi metodi di pagamento:\n\n"
        headers = {'X-CHAT-ID':str(message.chat.id)}
        r = requests.get(PM_URL, headers=headers)
        datas = r.json()
        for bal in datas:
            string += str(bal['name'])+": "+str(bal['amount'])+"\n"
        bot.send_message(message.chat.id, string)

@bot.message_handler(func=lambda message: True)
def unknown(message):
        bot.reply_to(message, "Sorry, I didn't understand that command.")
        
bot.infinity_polling()
