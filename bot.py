import telebot
from openai import OpenAI
import os
TOKEN = os.getenv("8386303215:AAE9Uo1g6YlD4NNrL9vnxfENvXSxqpHl-ts")
OPENAI_KEY = os.getenv("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")

client = OpenAI(api_key=OPENAI_KEY)
bot = telebot.TeleBot(8386303215:AAE9Uo1g6YlD4NNrL9vnxfENvXSxqpHl-ts)

def calculate_calories(weight, height, age, activity=1.4):
    bmr = 10*weight + 6.25*height - 5*age + 5
    return int(bmr * activity)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! 💪 Напиши данные: Вес Рост Возраст")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()

    try:
        weight, height, age = map(int, text.split())
        calories = calculate_calories(weight, height, age)

        protein = int(weight * 2)
        fat = int(weight * 1)
        carbs = int((calories - (protein*4 + fat*9)) / 4)

        reply = f"""🔥 Твоя норма:

Калории: {calories}
Белки: {protein}г
Жиры: {fat}г
Углеводы: {carbs}г

Задай вопрос по питанию или тренировкам 👇"""
        bot.reply_to(message, reply)

    except:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты фитнес тренер и диетолог. Отвечай кратко и по делу."},
                {"role": "user", "content": message.text}
            ]
        )
        bot.reply_to(message, response.choices[0].message.content)

bot.polling(none_stop=True)
