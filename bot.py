import requests
from telegram import *
from telegram.ext import *
import keys
import json
import telegram.bot

BOT_KEY = keys.token
TOKEN = keys.unlimit
STRIPE_TOKEN = keys.glocal

def start(update: Update, context: CallbackContext):
    welcome_message = "Welcome to this bot!"
    update.message.reply_text(welcome_message, parse_mode="html")
    buttons=[[KeyboardButton("Categories")] , [KeyboardButton("Support")]]
    context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardMarkup(buttons), text = "Hello!")
   
def message_handler(update: Update, context: CallbackContext):
    category="Categories"
    help="Support"
    if "Categories" in update.message.text:
        buttons = [[InlineKeyboardButton("Electronics", callback_data='e')], [InlineKeyboardButton("Jewelery", callback_data='j')], [InlineKeyboardButton("Men's Clothing", callback_data='men')], [InlineKeyboardButton("Women's clothing", callback_data='women')]]
        context.bot.send_message(chat_id = update.effective_chat.id, reply_markup=InlineKeyboardMarkup(buttons), text = "The available categories are:")
    if "Support" in update.message.text:
        context.bot.send_message(chat_id = update.effective_chat.id, text="What do you want?")

def donate(update: Update, context: CallbackContext):
    out = context.bot.send_invoice(
        chat_id=update.message.chat_id,
        title="Test pay",
        description="Give money here.",
        payload="test",
        provider_token=TOKEN,
        currency="INR",
        prices=[LabeledPrice("Give", 50000)],
        #2 zero less hoke print hota hai this amounts to 500
        need_name=False,
    )

# def sendphotos(message, image):
#     # baseurl = f"https://api.telgram.org/bot{BOT_KEY}/sendPhoto"
#     # parameters = {

#     #     "photo": image
#     # }
#     #h = context.bot.sendPhoto 
#     Bot.sendPhoto(message.chat.id, image)
# def donate(update: Update, context: CallbackContext):
#     out = context.bot.send_invoice(
#         chat_id=update.message.chat_id,
#         title="Test donation",
#         description="Give money here.",
#         payload="test",
#         provider_token=TOKEN,
#         currency="INR",
#         prices=[LabeledPrice("Give", 500000)],
#         need_name=False,
#     )
    # r = update.pre_checkout_query.answer(ok=True)


# def pre_checkout_handler(update: Update, context: CallbackContext):
#     """https://core.telegram.org/bots/api#answerprecheckoutquery"""
#     query = update.pre_checkout_query
#     query.answer(ok=True)

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
    if 'j' in query:
        url = f"{url}jewelery"
    if 'men' in query:
        url = f"https://fakestoreapi.com/products/category/men's{string}clothing"
    if 'women' in query:
        url = f"https://fakestoreapi.com/products/category/women's{string}clothing"
    
    response = requests.get(url)
    #x = json.loads(response.json())
    l = response.json()
    fentry = l[0]
    title = fentry.get('title')
    price = fentry.get('price')
    desc = fentry.get('description')
    image = fentry.get('image')
    context.bot.send_message(chat_id = update.effective_chat.id, text = title)
    context.bot.sendMediaGroup(chat_id = update.effective_chat.id, media = [InputMediaPhoto(image, caption="")])
    context.bot.send_message(chat_id = update.effective_chat.id, text = desc )
    out = context.bot.send_invoice(
        chat_id=update.message.chat_id,
        title="Test pay",
        description="Give money here.",
        payload="test",
        provider_token=TOKEN,
        currency="INR",
        prices=[LabeledPrice("Give", price*100)],
        #2 zero less hoke print hota hai this amounts to 500
        need_name=False,
    )
    # otext = f'''{title}
    #         {desc}'''
    #update.message.reply_text(text, parse_mode="html")
    
    # #sendphotos(message, image)
    # out = context.bot.send_invoice(
    #     chat_id=update.message.chat_id,
    #     title="Test pay",
    #     description="Give money here.",
    #     payload="test",
    #     provider_token=TOKEN,
    #     currency="INR",
    #     prices=[LabeledPrice("Give", price)],
    #     #2 zero less hoke print hota hai this amounts to 500
    #     need_name=False,
    # )
    # r = update.pre_checkout_query.answer(ok=True)


# def category():
#      message_handler(update, context)


if __name__ == "__main__":
    updater = Updater(BOT_KEY, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("give", donate))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
    #updater.dispatcher.add_handler(PreCheckoutQueryHandler(pre_checkout_handler))
    updater.dispatcher.add_handler(CallbackQueryHandler(query_handler))
    
    print("starting to poll...")
    updater.start_polling()


# url = 'https://fakestoreapi.com/products/categories'

# response = requests.get(url)

# print(response.json())
