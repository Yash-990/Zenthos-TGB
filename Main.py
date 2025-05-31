import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    filters,
    ContextTypes,
)
from decouple import config

from diet_logic import calculate_bmi, get_sample_indian_diet

from decouple import config

TOKEN = config("TELEGRAM_BOT_TOKEN")

# States for ConversationHandler
ASK_WEIGHT, ASK_HEIGHT, ASK_GOAL = range(3)

# Logging setup
logging.basicConfig(level=logging.INFO)


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Zenthos! 🤖\nPlease enter your weight in kg:")
    return ASK_WEIGHT

import re
async def ask_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    height_text = update.message.text
    match = re.search(r'\d+\.?\d*', height_text)
    if not match:
        await update.message.reply_text("Please enter a valid height in centimeters (e.g. 170 or 175.5):")
        return ASK_HEIGHT

    context.user_data["height"] = float(match.group())
    reply_keyboard = [["weight_loss", "muscle_gain", "balanced", "PCOS", "Diabetics", "POST hERNIATED Surgery"]]
    await update.message.reply_text(
        "What is your goal?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return ASK_GOAL


# Handle weight input and ask for height
async def ask_height(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["weight"] = float(str(update.message.text))
    await update.message.reply_text("Now enter your height in cm:")
    return ASK_HEIGHT

# Handle height input and ask for goal
async def ask_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["height"] = float(str(update.message.text))
    reply_keyboard = [["weight_loss", "muscle_gain", "balanced", "PCOS", "Diabetics", "POST hERNIATED Surgery"]]
    await update.message.reply_text(
        "What is your goal?",
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
    )
    return ASK_GOAL

# Final handler to show diet plan and BMI
async def show_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    goal = update.message.text
    weight = context.user_data["weight"]
    height = context.user_data["height"]
    bmi = calculate_bmi(weight, height)
    diet_plan = get_sample_indian_diet(goal)

    response = (
        f"🧠 Your BMI is: {bmi}\n"
        f"🎯 Goal: {goal.replace('_', ' ').title()}\n\n"
        f"{diet_plan}"
    )
    await update.message.reply_text(response)
    return ConversationHandler.END

# Cancel handler
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Conversation cancelled.")
    return ConversationHandler.END

# Main function
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            ASK_WEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_height)],
            ASK_HEIGHT: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_goal)],
            ASK_GOAL: [MessageHandler(filters.TEXT & ~filters.COMMAND, show_plan)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Zenthos Bot is running...")
    app.run_polling()
