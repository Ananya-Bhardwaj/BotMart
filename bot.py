import requests
from telegram import *
from telegram.ext import *
import keys
import json
import telegram.bot
import random
import main
import pymongo

BOT_KEY = keys.token
#TOKEN = keys.unlimit
TOKEN = keys.glocal

#this defines the start command and sets three keyboard buttons for the bot
def start(update: Update, context: CallbackContext):
    welcome_message = '''Hello
Welcome to this bot!'''
    update.message.reply_text(welcome_message, parse_mode="html")
    buttons=[[KeyboardButton("Categories")] , [KeyboardButton("Support")], [KeyboardButton("Orders")]]
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardMarkup(buttons), text = "This bot would allow you to order products! Click on Categories to know more")
    
#this is handling payements
def pre_checkout_handler(update: Update, context: CallbackContext):
    """https://core.telegram.org/bots/api#answerprecheckoutquery"""
    query = update.pre_checkout_query
    query.answer(ok=True)

#this sends a recipt telling about successful payment
def successful_payment_callback(update: Update, context):
    col = get_collection()
    receipt = update.message.successful_payment
    col.insert_one({"telegram_uid": update.message.chat.username, 
                   "donated_amount": receipt.total_amount,
                   "currency": receipt.currency,
                   "datetime": str(datetime.datetime.now())})
    print_col(col)
    update.message.reply_text("Thank you for your purchase!")
    
    
#this handles the messages that are received with buttons    
def message_handler(update: Update, context: CallbackContext):
    category="Categories"
    help="Support"
    if "Categories" in update.message.text:
        buttons = [[InlineKeyboardButton("Electronics", callback_data='e')], [InlineKeyboardButton("Jewelery", callback_data='j')], [InlineKeyboardButton("Men's Clothing", callback_data='boy')], [InlineKeyboardButton("Women's clothing", callback_data='girl')]]
        context.bot.send_message(chat_id = update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text = "The available categories are:")
    if "Support" in update.message.text:
        text = '''What do you want to order? 
Click on the categories button to check out the various categories available'''
        context.bot.send_message(chat_id = update.effective_chat.id, text= text)
    if "Orders" in update.message.text:
        #status and shipped in time 
        context.bot.send_message(chat_id = update.effective_chat.id, text="Your order has been confirmed and will be shipped at the earliest") 

#this fetches product data for a given category from fake store api
def sendProduct(url: str)->dict:
    response = requests.get(url)
    #x = json.loads(response.json())
    l = response.json()
    random_num = random.choice(l)
    return random_num

#this handles the queries that is for categories
def query_handler(update: Update, context: CallbackContext):
    query = update.callback_query.data
    update.callback_query.answer()
    # qparams = {
    #     "limit": 1
    # }
    url = "https://fakestoreapi.com/products/category/"
    string = "%20"
    if 'e' in query:
        url = f"{url}electronics"
        fentry = sendProduct(url)
        title = fentry.get('title')
        price = int(fentry.get('price'))
        desc = fentry.get('description')
        image = fentry.get('image')
        context.bot.send_message(chat_id = update.effective_chat.id, text = title)
        context.bot.sendMediaGroup(chat_id = update.effective_chat.id, media = [InputMediaPhoto(image, caption="")])
        context.bot.send_message(chat_id = update.effective_chat.id, text = desc )
        context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title=title,
        description="Give money here.",
        payload="test",
        provider_token=TOKEN,
        currency="INR",
        prices=[LabeledPrice("Give", price*100)],
        #2 zero less hoke print hota hai this amounts to 500
        need_name=False,
        )
        r = update.pre_checkout_query.answer(ok=True)
        context.bot.send_message(chat_id = update.effective_chat.id, text = "Order confirmed")
        # buttons = [[InlineKeyboardButton("YES", callback_data='yes')], [InlineKeyboardButton("NO", callback_data='n')]]
        # context.bot.send_message(chat_id = update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
        # text = "Do you like the item and wish to pay?")
    elif 'j' in query:
        url = f"{url}jewelery"
        fentry = sendProduct(url)
        title = fentry.get('title')
        price = int(fentry.get('price'))
        desc = fentry.get('description')
        image = fentry.get('image')
        context.bot.send_message(chat_id = update.effective_chat.id, text = title)
        context.bot.sendMediaGroup(chat_id = update.effective_chat.id, media = [InputMediaPhoto(image, caption="")])
        context.bot.send_message(chat_id = update.effective_chat.id, text = desc )
        context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title=title,
        description="Give money here.",
        payload="test",
        provider_token=TOKEN,
        currency="INR",
        prices=[LabeledPrice("Give", price*100)],
        #2 zero less hoke print hota hai this amounts to 500
        need_name=False,
        )
        r = update.pre_checkout_query.answer(ok=True)
        context.bot.send_message(chat_id = update.effective_chat.id, text = "Order confirmed")
        # buttons = [[InlineKeyboardButton("YES", callback_data='yes')], [InlineKeyboardButton("NO", callback_data='n')]]
        # context.bot.send_message(chat_id = update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
        # text = "Do you like the item and wish to pay?")
    elif 'boy' in query:
        url = f"https://fakestoreapi.com/products/category/men's{string}clothing"
        fentry = sendProduct(url)
        title = fentry.get('title')
        price = int(fentry.get('price'))
        desc = fentry.get('description')
        image = fentry.get('image')
        context.bot.send_message(chat_id = update.effective_chat.id, text = title)
        context.bot.sendMediaGroup(chat_id = update.effective_chat.id, media = [InputMediaPhoto(image, caption="")])
        context.bot.send_message(chat_id = update.effective_chat.id, text = desc )
        # buttons = [[InlineKeyboardButton("YES", callback_data='yes')], [InlineKeyboardButton("NO", callback_data='n')]]
        # context.bot.send_message(chat_id = update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
        # text = "Do you like the item and wish to pay?")
        context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title=title,
        description="Give money here.",
        payload="test",
        provider_token=TOKEN,
        currency="INR",
        prices=[LabeledPrice("Give", price*100)],
        #2 zero less hoke print hota hai this amounts to 500
        need_name=False,
        )
        r = update.pre_checkout_query.answer(ok=True)
        context.bot.send_message(chat_id = update.effective_chat.id, text = "Order confirmed")

    elif 'girl' in query:
        url = f"https://fakestoreapi.com/products/category/women's{string}clothing"
        fentry = sendProduct(url)
        title = fentry.get('title')
        price = int(fentry.get('price'))
        desc = fentry.get('description')
        image = fentry.get('image')
        context.bot.send_message(chat_id = update.effective_chat.id, text = title)
        context.bot.sendMediaGroup(chat_id = update.effective_chat.id, media = [InputMediaPhoto(image, caption="")])
        context.bot.send_message(chat_id = update.effective_chat.id, text = desc )
        # buttons = [[InlineKeyboardButton("YES", callback_data='yes')], [InlineKeyboardButton("NO", callback_data='n')]]
        # context.bot.send_message(chat_id = update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons),
        # text = "Do you like the item and wish to pay?")
        context.bot.send_invoice(
        chat_id=update.effective_chat.id,
        title=title,
        description="Give money here.",
        payload="test",
        provider_token=TOKEN,
        currency="INR",
        prices=[LabeledPrice("Give", price*100)],
        #2 zero less hoke print hota hai this amounts to 500
        need_name=False,
        )
        r = update.pre_checkout_query.answer(ok=True)
        context.bot.send_message(chat_id = update.effective_chat.id, text = "Order confirmed")


if __name__ == "__main__":
    #add handlers
    updater = Updater(BOT_KEY, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("payment", donate))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    updater.dispatcher.add_handler(PreCheckoutQueryHandler(pre_checkout_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters._SuccessfulPayment, successful_payment_callback))
    updater.dispatcher.add_handler(CallbackQueryHandler(query_handler))
    print("starting to poll...")
    updater.start_polling()
