
import os
from urllib.parse import quote

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mvp.settings')
import django
django.setup()
import telebot
from telebot import types
from django.db.models import Q
from django.conf import settings
from article_panel.models import Article



BOT_TOKEN = '6626291416:AAHfGKX_7bP13QGVJ_IdTcRfaZ2_e3UAygU'

bot = telebot.TeleBot(BOT_TOKEN)

# Определяем обработчик inline-запросов
@bot.inline_handler(lambda query: len(query.query) > 0)
def inline_query(query):
    results = []

    # Здесь добавляем логику поиска статей по содержанию
    articles = Article.objects.filter(Q(title__icontains=query.query) | Q(tags__icontains=query.query) | Q(text__icontains=query.query))

    for article in articles:
        # URL миниатюры, в данном случае просто URL к изображению статьи
        thumbnail_url = article.thumbnail_image.url

        # Отправляем только заголовок статьи с миниатюрой
        result_article = types.InlineQueryResultArticle(
            id=str(article.id),
            title=article.title,
            input_message_content=types.InputTextMessageContent(message_text=f"*{article.title}*\n\nТеги: {article.tags}\n\n{article.text}", parse_mode='Markdown', disable_web_page_preview=True),
        )
        results.append(result_article)

    bot.answer_inline_query(query.id, results)

# Обработчик входящих сообщений
@bot.message_handler(content_types=['text'])
def handle_message(message):
    # Проверяем, если сообщение содержит ID статьи
    try:
        article_id = int(message.text)
        article = Article.objects.get(pk=article_id)
        photo_url = article.media.first().image.url
        bot.send_photo(message.chat.id, photo=open(photo_url[1:], 'rb'), caption=f"*{article.title}*\n\nТеги: {article.tags}\n\n{article.text}", parse_mode='Markdown')
    except (ValueError, Article.DoesNotExist):
        # Если сообщение не содержит ID статьи или статья не найдена, отправляем обычный ответ
        bot.send_message(message.chat.id, "Введите ID статьи для просмотра")


if __name__ == '__main__':
    bot.polling()

