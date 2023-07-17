""" import packages """
# import asyncio
import constant
import pandas as pd
import buttons as but
import answers
import database as DB
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext
global messages, buttons1, my_DB

# =======================================================================
async def hello(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')


# =======================================================================
async def start(update: Update, context: CallbackContext) -> None:
    # global messages, buttons1
    ans = messages.loc[messages["title"] == "start_command"]["message"].iloc[0]
    temp0 = update.effective_user.id
    temp = my_DB.execute(f"SELECT 1 FROM ids_states WHERE tel_id = {temp0}")
    temp = temp.fetchall()
    if not temp:
        my_DB.execute(f"INSERT INTO ids_states(tel_id, last_state, connected_to_account) VALUES ({temp0}, 0, 0)")
    else:
        my_DB.execute(f"UPDATE ids_states SET last_state = 0 and connected_to_account = 0 WHERE tel_id = {temp0};")
    await update.message.reply_text(ans, reply_markup=buttons1.get_starter_keys())


# =======================================================================
async def help_dev(update: Update, context: CallbackContext):
    print(update.effective_user)
    print("\n=======================\n")
    print(update.message)
    print("\n=======================\n")
    print(context.user_data)
    # context.user_data["test"] = "55"
    print("\n=======================\n")


# =======================================================================
async def handle_message(update: Update, context: CallbackContext):
    # global messages
    text = str(update.message.text)
    temp_ans = answers.manager(text, 0, messages, pd)
    if temp_ans[0] == 0:
        await update.message.reply_text(temp_ans[1])
    elif temp_ans[0] == 1:
        await update.message.reply_photo(temp_ans[1], caption=temp_ans[2])
    elif temp_ans[0] == 2:
        await update.message.reply_video(temp_ans[1], caption=temp_ans[2])

    # print(text)


# =======================================================================
async def write_log(message: str):
    with open("user_errors.log", "a+", encoding="utf-8") as f:
        f.write(message)

# =======================================================================
async def error_message(update: Update, context: CallbackContext):
    await update.message.reply_text("There is on error while doing last request.\n Please try again Or Notify the technical support.")
    text = f"Update {update} caused error {context.error}"
    text = "\n +--------------------------------+ \n" + text
    await write_log(text)
    print(text)

# =======================================================================

if __name__=="__main__":
    # init base proj
    app = ApplicationBuilder().token(constant.BOT_KEY).build()
    messages = pd.read_csv("default_messages.csv")
    messages["message"] = messages["message"].str.replace(r'nwl', '\n')
    buttons1 = but.before_login()
    data_base = 'tel_bot_data.db'
    my_DB = DB.DataBase(data_base)
    
    # -------------------------------------------------------------------
    # command handelers :
    app.add_handler(CommandHandler("hello", hello))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("dev_help", help_dev))
    # message handler
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    # error handler
    app.add_error_handler(error_message)
    # -------------------------------------------------------------------
    try:
        print("\tstarted polling ... \n\n")
        app.run_polling()
    except Exception as e:
        print(f"\n\nerror message:\n{e}\n\n")
    finally:
        my_DB.commit()
        my_DB.close()
        print("\n\n\tfinish ...")
