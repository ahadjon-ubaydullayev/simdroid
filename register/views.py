from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telethon import TelegramClient, sync
from pyrogram import *
from telebot import *
import telebot
from .models import SimCardOption, Gift, Client, SimOrder
from django.core.files.base import ContentFile


bot = TeleBot("5051960822:AAFyFKJFrybdVmRsrG3E1k3rCz3bVXFEYPo")


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return HttpResponse("Bot Url Page")
    if request.method == 'POST':
        bot.process_new_updates([
            telebot.types.Update.de_json(
                request.body.decode("utf-8")
            )
        ])
        return HttpResponse(status=200)


@bot.message_handler(commands=['start'])
def greeting(message):
    active_users = Client.objects.filter(user_id=message.from_user.id, active=True)
    if len(active_users) == 0:
        bot.send_message(message.from_user.id, 'Botga Xush kelibsiz\n')
        client = Client.objects.filter(user_id=message.from_user.id)
        if len(client) == 0:
            client = Client.objects.create(
                user_id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                )
            client.save()
        else:
            client = Client.objects.get(user_id=message.chat.id)
            client.step = 0
            client.save()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Simkarta buyurtma berish')
    btn2 = types.KeyboardButton('Mening buyurtmalarim')
    btn3 = types.KeyboardButton('Linephone ')
    btn4 = types.KeyboardButton('Info📕')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.from_user.id,
                  'menyu:\n', reply_markup=markup)
    markup.add(btn1, btn2, btn3, btn4)
    

@bot.message_handler(commands=['info'])
def info(message):
    
    bot.send_message(message.from_user.id,
                     'Mavjud foydalanuvchilar haqida ma\'lumot')
    
 

@bot.message_handler(func=lambda message: True, content_types=['photo', 'text'] )
def register_view(message):
    client = Client.objects.get(user_id=message.from_user.id)
    print('client: ', client)
    user_commands = ['Tasdiqlash✅', 'Orqaga ↩️', 'Mening buyurtmalarim', 'My orders', 'Orqaga', 'O\'chirish', 'Bekor qilish 🚫', 'Ma\'lumot olish📕', 'Simkarta buyurtma berish','Order simcard', 'Info📕', 'Cancel 🚫', 'Back ↩️', 'Confirm✅', 'Simkartani o\'chirish'] 
    if client.step == 0:   
        if message.text not in user_commands:
            bot.send_message(message.from_user.id, 'Iltimos kerakli buyruqni tanlang!')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Simkarta buyurtma berish')
    btn2 = types.KeyboardButton('Mening buyurtmalarim')
    btn3 = types.KeyboardButton('Linephone ')
    btn4 = types.KeyboardButton('Ma\'lumot olish📕')
    markup.add(btn1, btn2, btn3, btn4)

    if message.text == 'Simkarta buyurtma berish':  
        order = SimOrder.objects.create(
            owner=client,
            sim_type=SimCardOption.objects.first(),
            full_name=message.from_user.first_name,
            gift=Gift.objects.first(),
            address='unavailable',
            tel_number='9x xxx xx xx'
            )
        order.active_sim = True
        order.step = 1
        order.save()
        client.step = 1
        client.save()
        bot.send_message(message.from_user.id, 'Iltimos, simkarta buyurtma berish uchun quyidagi ma\'lumotlarni kiriting')   
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn2 = types.KeyboardButton('Bekor qilish 🚫')
        markup.add(btn2)
        
        bot.send_message(
            message.from_user.id, 'Ismingiz va familiyangizni kiriting:', reply_markup=markup)
    elif message.text == 'Order simcard':     
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        cancel = types.KeyboardButton('Cancel 🚫')
        markup.add(cancel)
        order.step = 1
        order.save()
        bot.send_message(
            message.from_user.id, 'Please enter your full name', reply_markup=markup)
    elif message.text == 'Ma\'lumot olish📕':
        clients = Client.objects.all()
        bot.send_message(message.from_user.id,
                         "Bot haqida ma\'lumot:")
        for u in clients:
            bot.send_message(message.from_user.id,
                             f"Ism Familiyasi👤 - {u.full_name}")

    elif message.text == 'Info📕':
        bot.send_message(message.from_user.id,
                         "Some text")
    
    elif message.text == 'Bekor qilish 🚫':
        order = SimOrder.objects.filter(owner=client, active_sim=True).first()
        order.delete()
        bot.send_message(message.from_user.id,
                         "Bekor qilindi\n", reply_markup=markup)
    
    elif message.text == 'Cancel 🚫':
        order = SimOrder.objects.filter(owner=client, active_sim=True).first()
        order.delete()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('Order simcard')
        btn2 = types.KeyboardButton('My orders')
        btn3 = types.KeyboardButton('Linephone ')
        btn4 = types.KeyboardButton('Info📕')
        markup.add(btn1, btn2, btn3, btn4)
        bot.send_message(message.from_user.id,
                         "Cancelled\n", reply_markup=markup)
    
    elif message.text == 'Orqaga ↩️':
        order = SimOrder.objects.filter(owner=client, active_sim=True).first()
        order.step -= 1
        order.save()
        cancel_func(message)
    
    elif message.text == 'Back ↩️':
        order = SimOrder.objects.filter(owner=client, active_sim=True).first()
        order.step -= 1
        order.save()
        cancel_func(message)

    elif message.text == 'Linephone':
        bot.send_message(message.from_user.id,
                          "Linephone\n")

    elif message.text == 'Tasdiqlash✅':
        order = SimOrder.objects.filter(owner=client, step=8).first()
        order.step = 9
        order.active_sim = False
        order.save()
        bot.send_message(message.from_user.id,
                         "Buyurtmangiz qabul qilindi!", reply_markup=markup)

    elif message.text == 'Confirm✅':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        btn1 = types.KeyboardButton('Order simcard')
        btn2 = types.KeyboardButton('My orders')
        btn3 = types.KeyboardButton('Linephone ')
        btn4 = types.KeyboardButton('Info📕')
        markup.add(btn1, btn2, btn3, btn4)
        order = SimOrder.objects.filter(owner=client, step=8).first()
        order.step = 9
        order.active_sim = False
        order.save()
        bot.send_message(message.from_user.id,
                         "Your order has been accepted!", reply_markup=markup)
    elif message.text == 'Mening buyurtmalarim': # use callback query use loops to retrieve objects from database
        markup = types.InlineKeyboardMarkup(row_width=2)
        orders = SimOrder.objects.filter(owner=client, active_sim=False)
        if len(orders) != 0:
            for order in orders:
                obj = order.sim_type
                markup.add(types.InlineKeyboardButton(f"{obj}", callback_data=f"{order.id}"),
                           types.InlineKeyboardButton("❌", callback_data=f"{order.id}")
                    )
            bot.send_message(message.from_user.id,
                          "Sizning buyurtmalaringiz:\n", reply_markup=markup)
        else:
            bot.send_message(message.from_user.id,
                          "Sizda hozircha buyurtmalar mavjud emas.\n", reply_markup=markup)
        
    elif message.text == 'O\'chirish':
        user_obj.delete()
        bot.send_message(message.from_user.id,
                             "Simkarta o\'chirildi", reply_markup=markup)
    elif message.text == 'Orqaga':
        bot.send_message(message.from_user.id,
                         "Bekor qilindi", reply_markup=markup)

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton('Orqaga ↩️')
        btn2 = types.KeyboardButton('Bekor qilish 🚫')
        markup.add(btn1, btn2)
        markup_r = types.ReplyKeyboardRemove(selective=False)
        order = SimOrder.objects.filter(owner=client, active_sim=True).first()
        if order.step == 1:
            if str(message.text).isdigit():
                bot.send_message(message.from_user.id,
                                 'Iltimos to\'g\'ri ma\'lumot kiriting🙅‍♂️')
                bot.send_message(
                    message.from_user.id, 'Ismingiz va familiyangizni kiriting:', reply_markup=markup)
            else:
                order.full_name = message.text
                client.first_name = message.text
                order.step += 1
                order.save()
                client.save()
                bot.send_message(
                    message.from_user.id, 'Telefon raqamingizni 9x xxx xx xx ko\'rinshda kiriting☎️:', reply_markup=markup)

        elif order.step == 2: # not working
            if str(message.text).isdigit():
                order.tel_number = message.text
                order.step += 1
                order.save()
                sim_options = SimCardOption.objects.all()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
                btn1 = types.KeyboardButton('Orqaga ↩️')
                btn2 = types.KeyboardButton('Bekor qilish 🚫')
                for s in sim_options:
                    markup.add(types.KeyboardButton(s.sim_type))
                markup.add(btn1, btn2)
                bot.send_message(message.from_user.id,
                                 'Sim karta turini tanlang', reply_markup=markup)
            else:
                bot.send_message(message.from_user.id,
                                 'Iltimos to\'g\'ri ma\'lumot kiriting🙅‍♂️')
                bot.send_message(
                    message.from_user.id, 'Telefon raqamingizni 9x xxx xx xx ko\'rinshda kiriting☎️:', reply_markup=markup)

        elif order.step == 3: 
            obj = SimCardOption.objects.filter(sim_type=message.text).first()
            order.sim_type = obj
            order.step += 1
            order.save()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            btn1 = types.KeyboardButton('Orqaga ↩️')
            btn2 = types.KeyboardButton('Bekor qilish 🚫')
            
            gifts = Gift.objects.all()
            for g in gifts:
                markup.add(types.KeyboardButton(g.name))
            markup.add(btn1, btn2)
            bot.send_message(
                message.from_user.id, 'Sovga turini tanlang:', reply_markup=markup)
    
        elif order.step == 4: 
            obj = Gift.objects.filter(name=message.text).first()
            order.user_gift = obj
            order.step += 1
            order.save()
            markup_d = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            btn1 = types.KeyboardButton('Orqaga ↩️')
            btn2 = types.KeyboardButton('Bekor qilish 🚫')
            markup_d.add(btn1, btn2)
            bot.send_message(message.from_user.id, "Passportingiz yoki ID kartangizning oldi qism rasmini jo'nating:", reply_markup=markup_d)
       
        elif order.step == 5:
            raw = message.photo[1].file_id
            path = raw + ".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            content = ContentFile(downloaded_file)
            order.id_picture.save(path, content, save=True)
            order.step += 1
            order.save()
            markup_d = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            btn1 = types.KeyboardButton('Orqaga ↩️')
            btn2 = types.KeyboardButton('Bekor qilish 🚫')
            markup_d.add(btn1, btn2)
            bot.send_message(
                message.from_user.id, 'Passportingiz yoki ID kartangizning orqa qism rasmini jo\'nating:', reply_markup=markup_d)

        elif order.step == 6:
            raw = message.photo[1].file_id
            path = raw + ".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            content = ContentFile(downloaded_file)
            order.id_picture2.save(path, content, save=True)
            order.step += 1
            order.save()
            bot.send_message(
                message.from_user.id, 'Manzilinginzi kiriting🏠:', reply_markup=markup)
        elif order.step == 7:
            order.address = message.text
            order.step += 1
            order.save()
            bot.send_message(message.from_user.id,
                         f"F I SH: {order.full_name}\nTelefon raqam: {order.tel_number}\nTanlangan sim karta turi:{order.sim_type}\nTanlangan sovg'a turi: {order.gift}\nYashash manzili: {order.address} " , reply_markup=markup)
            
            markup = types.ReplyKeyboardMarkup(
                resize_keyboard=True, row_width=2)
            btn1 = types.KeyboardButton('Orqaga ↩️')
            btn2 = types.KeyboardButton('Bekor qilish 🚫')
            btn3 = types.KeyboardButton('Tasdiqlash✅')
            markup.add(btn1, btn2, btn3)
            bot.send_message(message.from_user.id,
                         "Ma'lumotlar to'g'riligini tasdiqlang" , reply_markup=markup)



@bot.callback_query_handler(func=lambda call: True)
def call_data(call):
    client = Client.objects.get(user_id=call.from_user.id)
    order = SimOrder.objects.get(id=call.data)
    order.delete()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Simkarta buyurtma berish')
    btn2 = types.KeyboardButton('Mening buyurtmalarim')
    btn3 = types.KeyboardButton('Linephone ')
    btn4 = types.KeyboardButton('Ma\'lumot olish📕')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(call.from_user.id,
                         f"O'chirildi!", reply_markup=markup)

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def cancel_func(message):
    client = Client.objects.get(user_id=message.from_user.id)
    order = SimOrder.objects.filter(owner=client, active_sim=True).first()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Orqaga ↩️')
    btn2 = types.KeyboardButton('Bekor qilish 🚫')
    markup.add(btn1, btn2)
    
    if order.step == 1: 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) 
        btn2 = types.KeyboardButton('Bekor qilish 🚫')
        markup.add(btn2)
        bot.send_message(message.from_user.id, 'Ismingiz va familiyangizni kiriting:', reply_markup=markup)      
    
    elif order.step == 2: 
        bot.send_message(message.from_user.id, 'Telefon raqamingizni 9x xxx xx xx ko\'rinshda kiriting☎️:', reply_markup=markup)
    
    elif order.step == 3: 
        markup_t = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sim_options = SimCardOption.objects.all()
        for s in sim_options:
            markup_t.add(types.KeyboardButton(s.sim_type))
        markup_t.add(btn1, btn2)
        bot.send_message(message.from_user.id,
                                 'Sim karta turini tanlang', reply_markup=markup_t)      
      
    elif order.step == 4:
        markup_g = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        gifts = Gift.objects.all()
        for g in gifts:
            markup_g.add(types.KeyboardButton(g.name))
        markup_g.add(btn1, btn2)
        bot.send_message(
                message.from_user.id, 'Sovga turini tanlang:', reply_markup=markup_g)   
    elif order.step == 5:
        bot.send_message(message.from_user.id, "Passportingiz yoki ID kartangiz oldi qism rasmini jo'nating:", reply_markup=markup)

    elif order.step == 6:
        bot.send_message(message.from_user.id, "Passportingiz yoki ID kartangiz orqa qism rasmini jo'nating:", reply_markup=markup)

    elif order.step == 7:  
        bot.send_message(message.from_user.id, 'Manzilinginzi kiriting🏠:', reply_markup=markup)



bot.polling()


# check if the message in the given models gifts, sim types