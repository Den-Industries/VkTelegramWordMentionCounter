import json

import os
import re
from datetime import datetime

all_words = False
target_words = ["love"]
telegram_username = "Jack"

def parse_dates_from_vk_messages(base_path):
    dates_array = []
    counter = 0
    # Проходим по всем папкам в директории messages
    for root, dirs, files in os.walk(os.path.join(base_path, 'messages')):
        print(counter, 625)
        counter += 1
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)

                with open(file_path, 'r') as f:
                    lines = f.readlines()

                    for i, line in enumerate(lines):
                        # Ищем строку с заголовком сообщения от "Вы"
                        if 'class="message__header">Вы,' in line:
                            # Извлекаем дату из заголовка
                            date_match = re.search(r'Вы, (.+? \d{4} в \d{2}:\d{2}:\d{2})', line)
                            if date_match:
                                date_str = date_match.group(1)

                                # Пропускаем строки до нахождения блока kludges
                                for j in range(i + 1, len(lines)):
                                    if '<div class="kludges">' in lines[j]:
                                        # Ищем текст между <div> и следующим <div
                                        text_content = extract_text_between_divs(lines[j:])

                                        use_it = all_words
                                        for target_word in target_words:
                                            if target_word in text_content.lower().replace(",", " ").replace(".", " ").split():
                                                use_it = True
                                        if use_it:
                                            # Конвертируем дату в единый формат
                                            try:
                                                parsed_date = parse_russian_date(date_str)
                                                dates_array.append(parsed_date)
                                            except ValueError as e:
                                                print(f"Ошибка парсинга даты: {date_str} - {e}")
                                        break
    return dates_array


def extract_text_between_divs(lines):
    for line in lines:
        # Ищем начало контента после <div>
        if '<div>' in line:
            start_idx = line.find('<div>') + 5
            end_idx = line.find('<div', start_idx)

            if end_idx != -1:
                return line[start_idx:end_idx]

    return ''

def parse_russian_date(date_str):
    months = {
        'янв': 1, 'фев': 2, 'мар': 3, 'апр': 4,
        'мая': 5, 'июн': 6, 'июл': 7, 'авг': 8,
        'сен': 9, 'окт': 10, 'ноя': 11, 'дек': 12
    }

    # Регулярное выражение для извлечения компонентов даты
    match = re.search(r'(\d{1,2}) (\w{3}) (\d{4}) в (\d{2}):(\d{2}):(\d{2})', date_str)
    if match:
        day = int(match.group(1))
        month_str = match.group(2)
        year = int(match.group(3))
        hour = int(match.group(4))
        minute = int(match.group(5))
        second = int(match.group(6))

        month = months.get(month_str.lower())
        if not month:
            raise ValueError(f"Неизвестный месяц: {month_str}")

        return datetime(year, month, day, hour, minute, second)
    else:
        raise ValueError(f"Неправильный формат даты: {date_str}")


base_path = 'vk'  # Путь к основной папке vk
main_target_counter = parse_dates_from_vk_messages(base_path)

def parse_iso_date(date_str):
    """Парсит дату в формате 2025-09-03T09:54:16"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S')
    except ValueError as e:
        raise ValueError(f"Неверный формат даты: {date_str}. Ожидается: YYYY-MM-DDTHH:MM:SS") from e


with open('tg/result.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
    counter = 0
    for i in range(len(data["chats"]["list"])):
        for u in range(len(data["chats"]["list"][i]["messages"])):
            if "from" in data["chats"]["list"][i]["messages"][u]:
                if data["chats"]["list"][i]["messages"][u]['from'] == telegram_username:
                    if isinstance(data["chats"]["list"][i]["messages"][u]['text'], str):
                        use_it = all_words
                        for target_word in target_words:
                            if target_word in data["chats"]["list"][i]["messages"][u]['text'].lower().replace(",", " ").replace(".", " ").split():
                                use_it = True
                        if use_it:
                            main_target_counter.append(parse_iso_date(data["chats"]["list"][i]["messages"][u]['date']))
        counter += 1
        print(counter, len(data["chats"]["list"]))

print(len(main_target_counter))

from plot import plot_dates_by_month_no_pandas

plot_dates_by_month_no_pandas(main_target_counter)