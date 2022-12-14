from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telethon import TelegramClient, sync
from pyrogram import *
from telebot import *
import telebot
from .models import SimCardOption, Gift, Client, SimOrder
from django.core.files.base import ContentFile


bot = telebot.TeleBot("5051960822:AAFyFKJFrybdVmRsrG3E1k3rCz3bVXFEYPo")

@csrf_exempt
def index(request):
    if request.method == 'GET':
        return HttpResponse("Bot Url Page")
    elif request.method == 'POST':
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

        if len(client) == 0: # creating user with active_sim has been modified
            if client.active_sim == False:
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
    language_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    uzbek = types.KeyboardButton("πΊπΏ O'zbek")
    english = types.KeyboardButton("π¬π§ English")
    russian = types.KeyboardButton("π·πΊ Russian")
    language_markup.add(uzbek, english, russian)
    bot.send_message(message.from_user.id,
                  'Iltimos kerakli tilni tanlang:\n', reply_markup=language_markup)
    
    

@bot.message_handler(commands=['info'])
def info(message):    
    bot.send_message(message.from_user.id,
                     'Mavjud foydalanuvchilar haqida ma\'lumot')


@bot.message_handler(func=lambda message: True, content_types=['photo', 'text'] )
def register_view(message):
    client = Client.objects.get(user_id=message.from_user.id)

    main_markup_uzbek = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1_u = types.KeyboardButton('Simkarta buyurtma berish')
    btn2_u = types.KeyboardButton('Mening buyurtmalarim')
    btn3_u = types.KeyboardButton('Linephone ')
    btn4_u = types.KeyboardButton('Ma\'lumot olishπ')
    main_markup_uzbek.add(btn1_u, btn2_u, btn3_u, btn4_u)

    main_markup_english = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1_e = types.KeyboardButton('Order simcard')
    btn2_e = types.KeyboardButton('My orders')
    btn3_e = types.KeyboardButton('Linephone ')
    btn4_e = types.KeyboardButton('Infoπ')
    main_markup_english.add(btn1_e, btn2_e, btn3_e, btn4_e)

    main_markup_russian = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1_r = types.KeyboardButton('ΠΠ°ΠΊΠ°Π·Π°ΡΡ ΡΠΈΠΌΠΊΠ°ΡΡΡ')
    btn2_r = types.KeyboardButton('ΠΠΎΠΈ Π·Π°ΠΊΠ°Π·Ρ')
    btn3_r = types.KeyboardButton('Linephone ')
    btn4_r = types.KeyboardButton('ΠΠ½ΡΠΎΡΠΌΠ°ΡΠΈΡπ')
    main_markup_russian.add(btn1_r, btn2_r, btn3_r, btn4_r)

    if message.text == "πΊπΏ O'zbek":
        client.language = 'uz'
        client.save()
        bot.send_message(message.from_user.id, 'Menyu:', reply_markup=main_markup_uzbek)
    elif message.text == "π¬π§ English":
        client.language = 'en'
        client.save()
        bot.send_message(message.from_user.id, 'Menu', reply_markup=main_markup_english)
    elif message.text == "π·πΊ Russian":
        client.language = 'ru'
        client.save()
        bot.send_message(message.from_user.id, 'ΠΠ΅Π½Ρ:', reply_markup=main_markup_russian)
    lan = client.language
    user_commands = ['Tasdiqlashβ', 'Orqaga β©οΈ', 'πΊπΏ O\'zbek', 'π¬π§ English', 'π·πΊ Russian', 'Mening buyurtmalarim', 'My orders', 'Orqaga', 'O\'chirish', 'Bekor qilish π«', 'Ma\'lumot olishπ', 'Simkarta buyurtma berish','Order simcard', 'Infoπ', 'Cancel π«', 'Back β©οΈ', 'Confirmβ', 'Simkartani o\'chirish'] 

    if (message.text == 'Simkarta buyurtma berish' or message.text == 'Order simcard' or message.text == 'ΠΠ°ΠΊΠ°Π·Π°ΡΡ ΡΠΈΠΌΠΊΠ°ΡΡΡ'):  
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
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        if lan == 'uz':
            bot.send_message(message.from_user.id, 'Iltimos, simkarta buyurtma berish uchun quyidagi ma\'lumotlarni kiriting:')   
            btn2 = types.KeyboardButton('Bekor qilish π«')
            markup.add(btn2)
            bot.send_message(
            message.from_user.id, 'Ismingiz va familiyangizni kiriting:', reply_markup=markup)
        elif lan == 'en':
            bot.send_message(message.from_user.id, 'Please, enter your credentials to order a simcard:')
            btn2 = types.KeyboardButton('Cancel π«')
            markup.add(btn2)
            bot.send_message(
            message.from_user.id, 'Enter your last and first name:', reply_markup=markup)
        elif lan == 'ru':
            bot.send_message(message.from_user.id, 'ΠΠΎΠΆΠ°Π»ΡΠΉΡΡΠ°, Π²Π²Π΅Π΄ΠΈΡΠ΅ ΡΠ²ΠΎΠΈ Π΄Π°Π½Π½ΡΠ΅, ΡΡΠΎΠ±Ρ Π·Π°ΠΊΠ°Π·Π°ΡΡ ΡΠΈΠΌ-ΠΊΠ°ΡΡΡ:')
            btn2 = types.KeyboardButton('ΠΡΠΌΠ΅Π½Π° π«')
            markup.add(btn2)
            bot.send_message(
            message.from_user.id, 'ΠΠ²Π΅Π΄ΠΈΡΠ΅ ΡΠ²ΠΎΡ ΡΠ°ΠΌΠΈΠ»ΠΈΡ ΠΈ ΠΈΠΌΡ:', reply_markup=markup)

    elif message.text == 'Ma\'lumot olishπ':
        bot.send_message(message.from_user.id,
                         "Bot haqida ma\'lumot:")

    elif message.text == 'Infoπ':
        bot.send_message(message.from_user.id,
                         "Some text")

    elif message.text == 'ΠΠ½ΡΠΎΡΠΌΠ°ΡΠΈΡπ':
        bot.send_message(message.from_user.id,
                         "ΠΠ½ΡΠΎΡΠΌΠ°ΡΠΈΡπ")
    
    elif message.text == 'Bekor qilish π«':
        order = SimOrder.objects.filter(owner=client, active_sim=True).last()
        print(order)
        order.delete()
        bot.send_message(message.from_user.id,
                         "Bekor qilindi\n", reply_markup=main_markup_uzbek)
    
    elif message.text == 'Cancel π«':
        order = SimOrder.objects.filter(owner=client, active_sim=True).last()
        print(order)
        order.delete()
        bot.send_message(message.from_user.id,
                         "Cancelled\n", reply_markup=main_markup_english)

    elif message.text == 'ΠΡΠΌΠ΅Π½Π° π«':
        order = SimOrder.objects.filter(owner=client, active_sim=True).last()
        print('order:', order.id)
        order.delete()
        bot.send_message(message.from_user.id,
                         "ΠΡΠΌΠ΅Π½Π΅Π½ΠΎ\n", reply_markup=main_markup_russian)
    
    elif message.text in ['Orqaga β©οΈ', 'Back β©οΈ', 'ΠΠ°Π·Π°Π΄ β©οΈ']:
        order = SimOrder.objects.filter(owner=client, active_sim=True).last()
        order.step -= 1
        order.save()
        cancel_func(message)
    
    elif message.text == 'Linephone':
        bot.send_message(message.from_user.id,
                          "Linephone\n")

    elif message.text in ['Tasdiqlashβ', 'Confirmβ', 'ΠΠΎΠ΄ΡΠ²Π΅ΡΠ΄ΠΈΡΡβ']:
        order = SimOrder.objects.filter(owner=client, step=8).first()
        order.step = 9
        order.active_sim = False
        order.save()
        if lan == 'uz':
            bot.send_message(message.from_user.id,
                         "Buyurtmangiz qabul qilindi!", reply_markup=main_markup_uzbek)
        elif lan == 'en':
            bot.send_message(message.from_user.id,
                         "Your order has been accepted!", reply_markup=main_markup_english)
        elif lan == 'ru':
            bot.send_message(message.from_user.id,
                         "ΠΠ°Ρ Π·Π°ΠΊΠ°Π· ΠΏΡΠΈΠ½ΡΡ!", reply_markup=main_markup_russian)
    
    elif (message.text == 'Mening buyurtmalarim' or message.text == 'My orders' or message.text == 'ΠΠΎΠΈ Π·Π°ΠΊΠ°Π·Ρ'): # use callback query use loops to retrieve objects from database
        markup = types.InlineKeyboardMarkup(row_width=2)
        orders = SimOrder.objects.filter(owner=client, active_sim=False)
        if len(orders) != 0:
            for order in orders:
                obj = order.sim_type
                markup.add(types.InlineKeyboardButton(f"{obj}", callback_data=f"{order.id}"),
                           types.InlineKeyboardButton("β", callback_data=f"{order.id}")
                    )
            if lan == 'uz':
                bot.send_message(message.from_user.id,
                              "Sizning buyurtmalaringiz:\n", reply_markup=markup)
            elif lan == 'en':
                bot.send_message(message.from_user.id,
                              "Your orders:\n", reply_markup=markup)
            elif lan == 'ru':
                bot.send_message(message.from_user.id,
                              "ΠΠ°ΡΠΈ Π·Π°ΠΊΠ°Π·Ρ:\n", reply_markup=markup)
        else:
            if lan == 'uz':
                bot.send_message(message.from_user.id,
                              "Sizda hozircha buyurtmalar mavjud emas.\n", reply_markup=markup)
            if lan == 'en':
                bot.send_message(message.from_user.id,
                              "You do not have any orders\n", reply_markup=markup)
            if lan == 'ru':
                bot.send_message(message.from_user.id,
                              "Π£ Π²Π°Ρ Π΅ΡΠ΅ Π½Π΅Ρ Π·Π°ΠΊΠ°Π·ΠΎΠ².\n", reply_markup=markup)

    else:
        order = SimOrder.objects.filter(owner=client, active_sim=True).first()
        
        secordary_markup_u = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_u = types.KeyboardButton('Orqaga β©οΈ')
        btn2_u = types.KeyboardButton('Bekor qilish π«')
        secordary_markup_u.add(btn1_u, btn2_u)

        secordary_markup_e = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_e = types.KeyboardButton('Back β©οΈ')
        btn2_e = types.KeyboardButton('Cancel π«')
        secordary_markup_e.add(btn1_e, btn2_e)

        secordary_markup_r = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1_r = types.KeyboardButton('ΠΠ°Π·Π°Π΄ β©οΈ')
        btn2_r = types.KeyboardButton('ΠΡΠΌΠ΅Π½Π° π«')
        secordary_markup_r.add(btn1_r, btn2_r)
        
        if order.step == 1:
        
            # if lan == 'uz': 
            #     bot.send_message(message.from_user.id,
            #                  'Iltimos to\'g\'ri ma\'lumot kiritingπββοΈ')
            #     bot.send_message(
            #         message.from_user.id, 'Ismingiz va familiyangizni kiriting:', reply_markup=secordary_markup_u)
            # if lan == 'en': 
            #     bot.send_message(message.from_user.id,
            #                  'Please, enter correct informationπββοΈ')
            #     bot.send_message(
            #         message.from_user.id, 'Enter your last and first name:', reply_markup=secordary_markup_e)
            # if lan == 'ru': 
            #     bot.send_message(message.from_user.id,
            #                  'ΠΠΎΠΆΠ°Π»ΡΠΉΡΡΠ°, Π²Π²Π΅Π΄ΠΈΡΠ΅ ΠΏΡΠ°Π²ΠΈΠ»ΡΠ½ΡΡ ΠΈΠ½ΡΠΎΡΠΌΠ°ΡΠΈΡπββοΈ')
            #     bot.send_message(
            #         message.from_user.id, 'ΠΠ²Π΅Π΄ΠΈΡΠ΅ ΡΠ²ΠΎΡ ΡΠ°ΠΌΠΈΠ»ΠΈΡ ΠΈ ΠΈΠΌΡ:', reply_markup=secordary_markup_r)
            order.full_name = message.text
            client.first_name = message.text
            order.step += 1
            order.save()
            client.save()
            if lan == 'uz':
                bot.send_message(
                    message.from_user.id, 'Telefon raqamingizni 9x xxx xx xx ko\'rinshda kiritingβοΈ:', reply_markup=secordary_markup_u)
            if lan == 'en':
                bot.send_message(
                    message.from_user.id, 'Enter your phone number as shown: 9x xxx xx xxβοΈ:', reply_markup=secordary_markup_e)
            if lan == 'ru':
                bot.send_message(
                    message.from_user.id, 'ΠΠ²Π΅Π΄ΠΈΡΠ΅ ΡΠ²ΠΎΠΉ Π½ΠΎΠΌΠ΅Ρ ΡΠ΅Π»Π΅ΡΠΎΠ½Π°, ΠΊΠ°ΠΊ ΠΏΠΎΠΊΠ°Π·Π°Π½ΠΎ: 9x xxx xx xxβοΈ:', reply_markup=secordary_markup_r)



        elif order.step == 2:
            if str(message.text).isdigit():
                order.tel_number = message.text
                order.step += 1
                order.save()
                sim_options = SimCardOption.objects.all()
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
                for s in sim_options:
                    markup.add(types.KeyboardButton(s.sim_option))
                if lan == 'uz':
                    markup.add(btn1_u, btn2_u)
                    bot.send_message(message.from_user.id,
                                     'Sim karta turini tanlang:', reply_markup=markup)
                if lan == 'en':
                    markup.add(btn1_e, btn2_e)
                    bot.send_message(message.from_user.id,
                                     'Choose the simcard type:', reply_markup=markup)
                if lan == 'ru':
                    markup.add(btn1_r, btn2_r)
                    bot.send_message(message.from_user.id,
                                     'ΠΡΠ±Π΅ΡΠΈΡΠ΅ ΡΠΈΠΏ ΡΠΈΠΌ-ΠΊΠ°ΡΡΡ', reply_markup=markup)
            else:
                if lan == 'uz':
                    bot.send_message(message.from_user.id,
                                     'Iltimos to\'g\'ri ma\'lumot kiritingπββοΈ')
                    bot.send_message(
                        message.from_user.id, 'Telefon raqamingizni 9x xxx xx xx ko\'rinshda kiritingβοΈ:', reply_markup=secordary_markup_u)
                if lan == 'en':
                    bot.send_message(message.from_user.id,
                                     'Please, enter correct informationπββοΈ')
                    bot.send_message(
                        message.from_user.id, 'Enter your phone number as shown: 9x xxx xx xxβοΈ:', reply_markup=secordary_markup_e)
                if lan == 'ru':
                    bot.send_message(message.from_user.id,
                                     'ΠΠΎΠΆΠ°Π»ΡΠΉΡΡΠ°, Π²Π²Π΅Π΄ΠΈΡΠ΅ ΠΏΡΠ°Π²ΠΈΠ»ΡΠ½ΡΡ ΠΈΠ½ΡΠΎΡΠΌΠ°ΡΠΈΡπββοΈ')
                    bot.send_message(
                        message.from_user.id, 'ΠΠ²Π΅Π΄ΠΈΡΠ΅ ΡΠ²ΠΎΠΉ Π½ΠΎΠΌΠ΅Ρ ΡΠ΅Π»Π΅ΡΠΎΠ½Π°, ΠΊΠ°ΠΊ ΠΏΠΎΠΊΠ°Π·Π°Π½ΠΎ: 9x xxx xx xxβοΈ:', reply_markup=secordary_markup_r)

        elif order.step == 3: 
            obj = SimCardOption.objects.filter(sim_option=message.text).first()
            order.sim_option = obj
            order.step += 1
            order.save()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
            gifts = Gift.objects.all()
            for g in gifts:
                markup.add(types.KeyboardButton(g.name))
            if lan == 'uz':
                markup.add(btn1_u, btn2_u)
                bot.send_message(
                    message.from_user.id, 'Sovga turini tanlang:', reply_markup=markup)
            if lan == 'en':
                markup.add(btn1_e, btn2_e)
                bot.send_message(
                    message.from_user.id, 'What do you want to get as a gift?\nChoose below:', reply_markup=markup)
            if lan == 'ru':
                markup.add(btn1_u, btn2_u)
                bot.send_message(
                    message.from_user.id, 'Π§ΡΠΎ Π²Ρ ΡΠΎΡΠΈΡΠ΅ ΠΏΠΎΠ»ΡΡΠΈΡΡ Π² ΠΏΠΎΠ΄Π°ΡΠΎΠΊ?\nΠΡΠ±Π΅ΡΠΈΡΠ΅ Π½ΠΈΠΆΠ΅:', reply_markup=markup)
    
        elif order.step == 4: 
            obj = Gift.objects.filter(name=message.text).first()
            order.user_gift = obj
            order.step += 1
            order.save()
            if lan == 'uz':
                bot.send_message(message.from_user.id, "Passportingiz yoki ID kartangizning oldi qism rasmini jo'nating:", reply_markup=secordary_markup_u)
            if lan == 'en':
                bot.send_message(message.from_user.id, "Send the frontside picture of your ID or passport:", reply_markup=secordary_markup_e)
            if lan == 'ru':
                bot.send_message(message.from_user.id, "ΠΡΠΏΡΠ°Π²ΡΡΠ΅ ΡΠΎΡΠΎΠ³ΡΠ°ΡΠΈΡ ΡΠ²ΠΎΠ΅Π³ΠΎ ΡΠ΄ΠΎΡΡΠΎΠ²Π΅ΡΠ΅Π½ΠΈΡ Π»ΠΈΡΠ½ΠΎΡΡΠΈ ΠΈΠ»ΠΈ ΠΏΠ°ΡΠΏΠΎΡΡΠ° Π½Π° Π»ΠΈΡΠ΅Π²ΠΎΠΉ ΡΡΠΎΡΠΎΠ½Π΅:", reply_markup=secordary_markup_r)
       
        elif order.step == 5:
            raw = message.photo[1].file_id
            path = raw + ".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            content = ContentFile(downloaded_file)
            order.id_picture.save(path, content, save=True)
            order.step += 1
            order.save()
            if lan == 'uz':
                bot.send_message(message.from_user.id, "Passportingiz yoki ID kartangizning orqa qism rasmini jo'nating:", reply_markup=secordary_markup_u)
            if lan == 'en':
                bot.send_message(message.from_user.id, "Send the backside picture of your ID or passport:", reply_markup=secordary_markup_e)
            if lan == 'ru':
                bot.send_message(message.from_user.id, "ΠΡΠΏΡΠ°Π²ΡΡΠ΅ ΡΠΎΡΠΎΠ³ΡΠ°ΡΠΈΡ ΠΎΠ±ΡΠ°ΡΠ½ΠΎΠΉ ΡΡΠΎΡΠΎΠ½Ρ Π²Π°ΡΠ΅Π³ΠΎ ΡΠ΄ΠΎΡΡΠΎΠ²Π΅ΡΠ΅Π½ΠΈΡ Π»ΠΈΡΠ½ΠΎΡΡΠΈ ΠΈΠ»ΠΈ ΠΏΠ°ΡΠΏΠΎΡΡΠ°:", reply_markup=secordary_markup_r)

        elif order.step == 6:
            raw = message.photo[1].file_id
            path = raw + ".jpg"
            file_info = bot.get_file(raw)
            downloaded_file = bot.download_file(file_info.file_path)
            content = ContentFile(downloaded_file)
            order.id_picture2.save(path, content, save=True)
            order.step += 1
            order.save()
            if lan == 'uz':
                bot.send_message(message.from_user.id, 'Manzilinginzi kiritingπ :', reply_markup=secordary_markup_u)
            if lan == 'en':
                bot.send_message(message.from_user.id, 'Enter your addressπ :', reply_markup=secordary_markup_e)
            if lan == 'ru':
                bot.send_message(message.from_user.id, 'ΠΠ²Π΅Π΄ΠΈΡΠ΅ ΡΠ²ΠΎΠΉ Π°Π΄ΡΠ΅Ρπ :', reply_markup=secordary_markup_r)
        elif order.step == 7:
            order.address = message.text
            order.step += 1
            order.active_sim = False
            order.save()
            if lan == 'uz':
                bot.send_message(message.from_user.id,
                             f"F I SH: {order.full_name}\nTelefon raqam: {order.tel_number}\nTanlangan sim karta turi:{order.sim_type}\nTanlangan sovg'a turi: {order.gift}\nYashash manzili: {order.address} " , reply_markup=secordary_markup_u)
                btn3_u = types.KeyboardButton('Tasdiqlashβ')
                secordary_markup_u.add(btn3_u)
                bot.send_message(message.from_user.id,
                             "Ma'lumotlar to'g'riligini tasdiqlang" , reply_markup=secordary_markup_u)
            if lan == 'en':
                bot.send_message(message.from_user.id,
                             f"Full name: {order.full_name}\nPhone number: {order.tel_number}\nChosen sim type:{order.sim_type}\nChosen gift: {order.gift}\nYour address: {order.address} ", reply_markup=secordary_markup_e)
                btn3_e = types.KeyboardButton('Confirmβ')
                secordary_markup_e.add(btn3_e)
                bot.send_message(message.from_user.id,
                             "Are your all credentials correct?" , reply_markup=secordary_markup_e)
            if lan == 'ru':
                bot.send_message(message.from_user.id,
                             f"ΠΠΎΠ»Π½ΠΎΠ΅ ΠΈΠΌΡ: {order.full_name}\nΠ’Π΅Π»Π΅ΡΠΎΠ½Π½ΡΠΉ Π½ΠΎΠΌΠ΅Ρ: {order.tel_number}\nΠΡΠ±ΡΠ°Π½Π½ΡΠΉ ΡΠΈΠΏ ΡΠΈΠΌ-ΠΊΠ°ΡΡΡ:{order.sim_type}\nΠΡΠ±ΡΠ°Π½Π½ΡΠΉ ΠΏΠΎΠ΄Π°ΡΠΎΠΊ: {order.gift}\nΠΠ°Ρ Π°Π΄ΡΠ΅Ρ: {order.address} " , reply_markup=secordary_markup_r) 
                btn3_r = types.KeyboardButton('ΠΠΎΠ΄ΡΠ²Π΅ΡΠ΄ΠΈΡΡβ')
                secordary_markup_r.add(btn3_r)
                bot.send_message(message.from_user.id,
                             "ΠΡΠ΅ Π»ΠΈ Π²Π°ΡΠΈ ΡΡΠ΅ΡΠ½ΡΠ΅ Π΄Π°Π½Π½ΡΠ΅ Π²Π΅ΡΠ½Ρ?" , reply_markup=secordary_markup_r)



@bot.callback_query_handler(func=lambda call: True)
def call_data(call):
    client = Client.objects.get(user_id=call.from_user.id)
    lan = client.language
    order = SimOrder.objects.get(id=call.data)
    order.delete()
    # send the orders again after deleting
    
    main_markup_uzbek = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1_u = types.KeyboardButton('Simkarta buyurtma berish')
    btn2_u = types.KeyboardButton('Mening buyurtmalarim')
    btn3_u = types.KeyboardButton('Linephone ')
    btn4_u = types.KeyboardButton('Ma\'lumot olishπ')
    main_markup_uzbek.add(btn1_u, btn2_u, btn3_u, btn4_u)

    main_markup_english = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1_e = types.KeyboardButton('Order simcard')
    btn2_e = types.KeyboardButton('My orders')
    btn3_e = types.KeyboardButton('Linephone ')
    btn4_e = types.KeyboardButton('Infoπ')
    main_markup_english.add(btn1_e, btn2_e, btn3_e, btn4_e)

    main_markup_russian = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1_r = types.KeyboardButton('ΠΠ°ΠΊΠ°Π·Π°ΡΡ ΡΠΈΠΌΠΊΠ°ΡΡΡ')
    btn2_r = types.KeyboardButton('ΠΠΎΠΈ Π·Π°ΠΊΠ°Π·Ρ')
    btn3_r = types.KeyboardButton('Linephone ')
    btn4_r = types.KeyboardButton('ΠΠ½ΡΠΎΡΠΌΠ°ΡΠΈΡπ')
    main_markup_russian.add(btn1_r, btn2_r, btn3_r, btn4_r)
    
    if lan == 'uz':
        bot.send_message(call.from_user.id,
                         f"O'chirildi!", reply_markup=main_markup_uzbek)
    elif lan == 'en':
        bot.send_message(call.from_user.id,
                         f"Deleted!", reply_markup=main_markup_english)
    elif lan == 'ru':
        bot.send_message(call.from_user.id,
                         f"Π£Π΄Π°Π»Π΅Π½ΠΎ!", reply_markup=main_markup_russian)

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()


def cancel_func(message):
    client = Client.objects.get(user_id=message.from_user.id)
    lan = client.language
    order = SimOrder.objects.filter(owner=client, active_sim=True).first()
    secordary_markup_u = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1_u = types.KeyboardButton('Orqaga β©οΈ')
    btn2_u = types.KeyboardButton('Bekor qilish π«')
    secordary_markup_u.add(btn1_u, btn2_u)

    secordary_markup_e = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1_e = types.KeyboardButton('Back β©οΈ')
    btn2_e = types.KeyboardButton('Cancel π«')
    secordary_markup_e.add(btn1_e, btn2_e)

    secordary_markup_r = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1_r = types.KeyboardButton('ΠΠ°Π·Π°Π΄ β©οΈ')
    btn2_r = types.KeyboardButton('ΠΡΠΌΠ΅Π½Π° π«')
    secordary_markup_r.add(btn1_r, btn2_r)
    
    if order.step == 1: 
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2) 
        if lan == 'uz':  
            btn2 = types.KeyboardButton('Bekor qilish π«')
            markup.add(btn2)
            bot.send_message(message.from_user.id, 'Ismingiz va familiyangizni kiriting:', reply_markup=markup)
        elif lan == 'en':   
            btn2 = types.KeyboardButton('Cancel π«')
            markup.add(btn2)
            bot.send_message(message.from_user.id, 'Enter your last and first name:', reply_markup=markup)
        elif lan == 'ru':   
            btn2 = types.KeyboardButton('ΠΡΠΌΠ΅Π½Π° π«')
            markup.add(btn2)
            bot.send_message(message.from_user.id, 'ΠΠ²Π΅Π΄ΠΈΡΠ΅ ΡΠ²ΠΎΡ ΡΠ°ΠΌΠΈΠ»ΠΈΡ ΠΈ ΠΈΠΌΡ:', reply_markup=markup)      
    
    elif order.step == 2:
        if lan == 'uz':
            bot.send_message(message.from_user.id, 'Telefon raqamingizni 9x xxx xx xx ko\'rinshda kiritingβοΈ:', reply_markup=secordary_markup_u)
        if lan == 'en':
            bot.send_message(message.from_user.id, 'Enter your phone number as shown: 9x xxx xx xxβοΈ:', reply_markup=secordary_markup_e)
        if lan == 'ru':
            bot.send_message(message.from_user.id, 'ΠΠ²Π΅Π΄ΠΈΡΠ΅ ΡΠ²ΠΎΠΉ Π½ΠΎΠΌΠ΅Ρ ΡΠ΅Π»Π΅ΡΠΎΠ½Π°, ΠΊΠ°ΠΊ ΠΏΠΎΠΊΠ°Π·Π°Π½ΠΎ: 9x xxx xx xxβοΈ:', reply_markup=secordary_markup_r)
    
    elif order.step == 3: 
        markup_t = types.ReplyKeyboardMarkup(resize_keyboard=True)
        sim_options = SimCardOption.objects.all()
        for s in sim_options:
            markup_t.add(types.KeyboardButton(s.sim_option))
        if lan == 'uz':
            markup_t.add(btn1_u, btn2_u)
            bot.send_message(message.from_user.id,
                                     'Sim karta turini tanlang:', reply_markup=markup_t)
        elif lan == 'en':
            markup_t.add(btn1_e, btn2_e)
            bot.send_message(message.from_user.id,
                                     'Choose the simcard type:', reply_markup=markup_t)
        elif lan == 'ru':
            markup_t.add(btn1_r, btn2_r)
            bot.send_message(message.from_user.id,
                                     'ΠΡΠ±Π΅ΡΠΈΡΠ΅ ΡΠΈΠΏ ΡΠΈΠΌ-ΠΊΠ°ΡΡΡ:', reply_markup=markup_t)      
      
    elif order.step == 4:
        markup_g = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        gifts = Gift.objects.all()
        for g in gifts:
            markup_g.add(types.KeyboardButton(g.name))
        if lan == 'uz':   
            markup_g.add(btn1_u, btn2_u)
            bot.send_message(
                    message.from_user.id, 'Sovga turini tanlang:', reply_markup=markup_g)
        elif lan == 'en':   
            markup_g.add(btn1_e, btn2_e)
            bot.send_message(
                    message.from_user.id, 'What do you want to get as a gift?\nChoose below:', reply_markup=markup_g)
        elif lan == 'ru':   
            markup_g.add(btn1_r, btn2_r)
            bot.send_message(
                    message.from_user.id, 'Π§ΡΠΎ Π²Ρ ΡΠΎΡΠΈΡΠ΅ ΠΏΠΎΠ»ΡΡΠΈΡΡ Π² ΠΏΠΎΠ΄Π°ΡΠΎΠΊ?\nΠΡΠ±Π΅ΡΠΈΡΠ΅ Π½ΠΈΠΆΠ΅:', reply_markup=markup_g)   
    elif order.step == 5:
        if lan == 'uz':
            bot.send_message(message.from_user.id, "Passportingiz yoki ID kartangiz oldi qism rasmini jo'nating:", reply_markup=secordary_markup_u)
        elif lan == 'en':
            bot.send_message(message.from_user.id, "Send the frontside picture of your ID or passport:", reply_markup=secordary_markup_e)
        elif lan == 'ru':
            bot.send_message(message.from_user.id, "ΠΡΠΏΡΠ°Π²ΡΡΠ΅ ΡΠΎΡΠΎΠ³ΡΠ°ΡΠΈΡ ΡΠ²ΠΎΠ΅Π³ΠΎ ΡΠ΄ΠΎΡΡΠΎΠ²Π΅ΡΠ΅Π½ΠΈΡ Π»ΠΈΡΠ½ΠΎΡΡΠΈ ΠΈΠ»ΠΈ ΠΏΠ°ΡΠΏΠΎΡΡΠ° Π½Π° Π»ΠΈΡΠ΅Π²ΠΎΠΉ ΡΡΠΎΡΠΎΠ½Π΅:", reply_markup=secordary_markup_r)

    elif order.step == 6:
        if lan == 'uz':
            bot.send_message(message.from_user.id, "Passportingiz yoki ID kartangiz orqa qism rasmini jo'nating:", reply_markup=secordary_markup_u)
        elif lan == 'en':
            bot.send_message(message.from_user.id, "Send the backside picture of your ID or passport:", reply_markup=secordary_markup_e)
        elif lan == 'ru':
            bot.send_message(message.from_user.id, "ΠΡΠΏΡΠ°Π²ΡΡΠ΅ ΡΠΎΡΠΎΠ³ΡΠ°ΡΠΈΡ ΠΎΠ±ΡΠ°ΡΠ½ΠΎΠΉ ΡΡΠΎΡΠΎΠ½Ρ Π²Π°ΡΠ΅Π³ΠΎ ΡΠ΄ΠΎΡΡΠΎΠ²Π΅ΡΠ΅Π½ΠΈΡ Π»ΠΈΡΠ½ΠΎΡΡΠΈ ΠΈΠ»ΠΈ ΠΏΠ°ΡΠΏΠΎΡΡΠ°:", reply_markup=secordary_markup_r)

    elif order.step == 7:
        if lan == 'uz': 
            bot.send_message(message.from_user.id, 'Manzilinginzi kiritingπ :', reply_markup=secordary_markup_u)
        elif lan == 'en': 
            bot.send_message(message.from_user.id, 'Enter your addressπ :', reply_markup=secordary_markup_e)
        elif lan == 'ru': 
            bot.send_message(message.from_user.id, 'ΠΠ²Π΅Π΄ΠΈΡΠ΅ ΡΠ²ΠΎΠΉ Π°Π΄ΡΠ΅Ρπ :', reply_markup=secordary_markup_r)

bot.polling()
