import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ConversationHandler, MessageHandler, ContextTypes, filters
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

NAME, CATEGORY, PURPOSE, FEATURES, CONTACT, BUDGET = range(6)

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌐 Services", callback_data="services"),
         InlineKeyboardButton("👀 Portfolio", callback_data="portfolio")],
        [InlineKeyboardButton("💰 Pricing", callback_data="pricing"),
         InlineKeyboardButton("🆓 Free Demo", callback_data="demo")],
        [InlineKeyboardButton("📋 Request a Quote", callback_data="quote"),
         InlineKeyboardButton("💬 Contact", callback_data="contact")],
        [InlineKeyboardButton("❓ FAQ", callback_data="faq")]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌐 Welcome to VELQORA\n\n"
        "Professional websites for local businesses.\n\n"
        "📱 Mobile & Desktop Responsive\n"
        "🎨 Custom Professional Design\n"
        "⚡ Modern & User-Friendly\n"
        "🆓 Free Demo Available\n\n"
        "Choose an option below:",
        reply_markup=main_menu()
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == "services":
        text = ("🌐 VELQORA SERVICES\n\n"
                "• Business Websites\n• Responsive Design\n• Custom Professional UI\n"
                "• WhatsApp & Contact Integration\n• Services, Pricing & Gallery\n"
                "• Location & Booking Integration\n• Enquiry Forms\n\n"
                "🆓 Free Demo Available")
    elif data == "portfolio":
        text = ("👀 VELQORA PORTFOLIO\n\n"
                "Explore our website work for local businesses.\n\n"
                "🌐 Modern Business Websites\n📱 Mobile & Desktop Responsive\n"
                "🎨 Custom Professional Design\n⚡ Fast & User-Friendly\n\n"
                "Live demos are available on request.")
    elif data == "pricing":
        text = ("💰 VELQORA PRICING\n\n"
                "🌐 Basic Website — ₹999+\n"
                "🚀 Professional Website — ₹1,499+\n"
                "✨ Custom Website — ₹2,499+\n\n"
                "Final pricing depends on your requirements.\n\n"
                "🆓 Free Demo Available")
    elif data == "demo":
        text = ("🆓 FREE WEBSITE DEMO\n\n"
                "Get a professional website demo created for your business before making a decision.\n\n"
                "✨ Demo includes:\n• Modern design\n• Responsive layout\n"
                "• Business services\n• Contact / WhatsApp section\n• Location & basic sections")
    elif data == "contact":
        text = ("💬 CONTACT VELQORA\n\n"
                "Need a website or have a question?\n\n"
                "Use 📋 Request a Quote to share your requirements.")
    else:
        text = ("❓ VELQORA FAQ\n\n"
                "Q: How long does a website take?\n"
                "A: Usually 2–5 days, depending on requirements.\n\n"
                "Q: Is a free demo available?\nA: Yes.\n\n"
                "Q: Will it work on mobile?\nA: Yes, websites are responsive.\n\n"
                "Q: Can I request changes?\nA: Yes, revisions depend on the package and agreed requirements.\n\n"
                "Q: How does payment work?\nA: Payment terms are discussed after requirements and the final quote are confirmed.")

    if data == "quote":
        await q.message.reply_text("📋 WEBSITE QUOTE\n\nPlease enter your business name:")
        return
    await q.message.reply_text(text, reply_markup=main_menu())

async def quote_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text("📋 WEBSITE QUOTE\n\nPlease enter your business name:")
    return NAME

async def name(update, context):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("What type of business is it?\n\nExample: Salon, Gym, Restaurant, Clothing")
    return CATEGORY

async def category(update, context):
    context.user_data["category"] = update.message.text
    await update.message.reply_text("What do you need the website for?")
    return PURPOSE

async def purpose(update, context):
    context.user_data["purpose"] = update.message.text
    await update.message.reply_text("Which pages or features do you need?")
    return FEATURES

async def features(update, context):
    context.user_data["features"] = update.message.text
    await update.message.reply_text("Please share your Instagram, WhatsApp, or preferred contact.")
    return CONTACT

async def contact(update, context):
    context.user_data["contact"] = update.message.text
    await update.message.reply_text("What is your approximate budget?\n\nExample: ₹999 / ₹1,499 / ₹2,499+ / Not sure")
    return BUDGET

async def budget(update, context):
    context.user_data["budget"] = update.message.text
    d = context.user_data
    lead = (
        "📩 NEW VELQORA LEAD\n\n"
        f"Business: {d['name']}\n"
        f"Category: {d['category']}\n"
        f"Purpose: {d['purpose']}\n"
        f"Pages/Features: {d['features']}\n"
        f"Contact: {d['contact']}\n"
        f"Budget: {d['budget']}\n"
        f"Telegram ID: {update.effective_user.id}"
    )
    if ADMIN_CHAT_ID:
        try:
            await context.bot.send_message(chat_id=int(ADMIN_CHAT_ID), text=lead)
        except Exception:
            pass
    await update.message.reply_text(
        "✅ Thank you! Your requirements have been received.\n\n"
        "Our team will review them and contact you with the next steps."
    )
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update, context):
    context.user_data.clear()
    await update.message.reply_text("❌ Your request has been cancelled.\n\nYou can start again anytime using /quote.")
    return ConversationHandler.END

def build_app():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is missing.")
    app = Application.builder().token(BOT_TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("quote", quote_start)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name)],
            CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, category)],
            PURPOSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, purpose)],
            FEATURES: [MessageHandler(filters.TEXT & ~filters.COMMAND, features)],
            CONTACT: [MessageHandler(filters.TEXT & ~filters.COMMAND, contact)],
            BUDGET: [MessageHandler(filters.TEXT & ~filters.COMMAND, budget)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(conv)
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(CommandHandler("cancel", cancel))
    return app

if __name__ == "__main__":
    build_app().run_polling()
