# import os
# from urllib.parse import quote

# # Установите переменную окружения DJANGO_SETTINGS_MODULE, указав путь к файлу settings.py
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mvp.settings')
# import django
# django.setup()
# import telebot
# from telebot import types
# from django.db.models import Q
# from django.conf import settings
# from article_panel.models import Article

# # Затем импортируйте модели из Django

# BOT_TOKEN = '6626291416:AAHfGKX_7bP13QGVJ_IdTcRfaZ2_e3UAygU'

# bot = telebot.TeleBot(BOT_TOKEN)

# # Определяем обработчик inline-запросов
# @bot.inline_handler(lambda query: len(query.query) > 0)
# def inline_query(query):
#     results = []

#     # Здесь добавляем логику поиска статей по содержанию
#     articles = Article.objects.filter(Q(title__icontains=query.query) | Q(tags__icontains=query.query) | Q(text__icontains=query.query))

#     for idx, article in enumerate(articles):
#         description = f"*{article.title}*\n\nТеги: {article.tags}\n\n{article.text}"

#         if article.media.count() > 1:
#             # Если в статье есть более одного медиа, отправляем их альбомом
#             media = [types.InputMediaPhoto(media=media.image.url, caption=description, parse_mode='Markdown') for media in article.media.all()]
    
#             result_album = types.InlineQueryR (
#                 id=str(article.id),
#                 title=article.title,
#                 input_message_content=types.InputTextMessageContent(message_text=description, parse_mode='Markdown', disable_web_page_preview=True),
#                 media=media
#             )
#             results.append(result_album)
#         elif article.media.count() == 1:
#             media_path = article.media.first().image.path

#             # Отправляем фотографию с помощью bot.send_photo()
#             with open(media_path, 'rb') as file:
#                 photo_msg = bot.send_photo(chat_id='@photoinline', photo=file, caption=description, parse_mode='Markdown')
#                 thumbphoto = photo_msg.photo[0].file_id
#                 originalphoto = photo_msg.photo[-1].file_id

#                 result_photo = types.InlineQueryResultCachedPhoto(
#                     id=str(article.id),
#                     title=article.title,
#                     photo_file_id=originalphoto,  # Используем originalphoto в качестве file_id
#                     caption=description,
#                     parse_mode='Markdown',
#                       # Используем thumbphoto в качестве thumb_file_id
#                 )
#                 results.append(result_photo)

#         else:
#             # Если в статье нет медиа, добавляем её как текстовый результат
#             result_text = types.InlineQueryResultArticle(
#                 id=str(article.id),
#                 title=article.title,
#                 input_message_content=types.InputTextMessageContent(message_text=description, parse_mode='Markdown', disable_web_page_preview=True),
#             )
#             results.append(result_text)

#     bot.answer_inline_query(query.id, results)

# # Ваша модель Article и Photo остаются без изменений
# # ...

# if __name__ == '__main__':
#     bot.polling()

import os
from urllib.parse import quote

# Установите переменную окружения DJANGO_SETTINGS_MODULE, указав путь к файлу settings.py
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mvp.settings')
import django
django.setup()
import telebot
from telebot import types
from django.db.models import Q
from django.conf import settings
from article_panel.models import Article

# Затем импортируйте модели из Django

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

# Ваша модель Article и Photo остаются без изменений
# ...

if __name__ == '__main__':
    bot.polling()

