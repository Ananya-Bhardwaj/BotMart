import telegram.bot as b 
from telegram.bot import *
from telegram import *
from telegram.ext import *
import keys
import requests


BOT_KEY = keys.token
STRIPE_TOKEN = keys.glocal
PRICE = 500



def get_Data(limit: str) -> dict:
    """Get data about x number of objects.
    Keyword arguments:
    limit:int - x
    Return:dict - JSON data
    """
    url = "https://fakestoreapi.com/products"
    response = requests.get(f"{url}/{limit}")
    return response.json()


# def handle_message(update, context):
#   message_type = update.message.chat.type
#   text = str(update.message.text).lower()

#   response = handle_response(text)

#   update.message.reply_text(response)
   
def fetch_data(text) -> str:
    data = get_Data(text)
    string = str(data)
    return string
   
    #b.Bot.send_message(message.chat.id, str)

def udata(update, context):
    update.message.reply_text("Enter id")
    text = str(update.message.text)
    r = fetch_data(text)
    update.message.reply_text(r, parse_mode="html")

def start(update: Update, context: CallbackContext):
    welcome_message = "Welcome to this bot!"
    update.message.reply_text(welcome_message, parse_mode="html")


def donate(update: Update, context: CallbackContext):
    out = context.bot.send_invoice(
        chat_id=update.message.chat_id,
        title="Test donation",
        description="Give money here.",
        payload="test",
        provider_token=STRIPE_TOKEN,
        currency="GBP",
        prices=[LabeledPrice("Give", 500)],
        need_name=False,
    )


def pre_checkout_handler(update: Update, context: CallbackContext):
    """https://core.telegram.org/bots/api#answerprecheckoutquery"""
    query = update.pre_checkout_query
    query.answer(ok=True)


def successful_payment_callback(update: Update, context):
    update.message.reply_text("Thank you for your purchase!")


def uid(update: Update, context: CallbackContext):
    uid = update.message.chat.username
    update.message.reply_text(f"Your uid is {uid}", parse_mode="html")


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(f"If you need support please contact example@email.com.")


def _add_handlers(updater):
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("give", donate))
    #updater.dispatcher.add_handler(sign_handler)
    updater.dispatcher.add_handler(CommandHandler("data", udata))
    updater.dispatcher.add_handler(PreCheckoutQueryHandler(pre_checkout_handler))
    #updater.dispatcher.add_handler(MessageHandler(Filters._SuccessfulPayment, successful_payment_callback))
    updater.dispatcher.add_handler(CommandHandler("uid", uid))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, udata))


if __name__ == "__main__":
    updater = Updater(BOT_KEY, use_context=True)
    _add_handlers(updater)
    print("starting to poll...")
    updater.start_polling()