import matplotlib.pyplot as plt
from collections import defaultdict
from datetime import datetime
import matplotlib.dates as mdates


def plot_dates_by_month_no_pandas(dates, title="Распределение дат по месяцам"):
    """
    Версия без использования pandas
    """
    if not dates:
        print("Массив дат пуст")
        return

    dates.sort()

    # Группируем даты по году и месяцу
    monthly_counts = defaultdict(int)
    for date in dates:
        # Создаем ключ в формате (год, месяц)
        key = (date.year, date.month)
        monthly_counts[key] += 1

    # Преобразуем в списки для построения графика
    months = []
    counts = []

    # Сортируем по дате
    sorted_months = sorted(monthly_counts.keys())

    for year, month in sorted_months:
        # Создаем дату для первого числа месяца
        month_date = datetime(year, month, 1)
        months.append(month_date)
        counts.append(monthly_counts[(year, month)])

    # Строим график
    plt.figure(figsize=(16, 6))
    bars = plt.bar(months, counts, width=30, alpha=0.7, color='lightgreen', edgecolor='darkgreen')

    # Добавляем значения на столбцы
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                 str(count), ha='center', va='bottom', fontsize=7)

    # Настраиваем ось X
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))

    russian_months = {
        1: 'Янв', 2: 'Фев', 3: 'Мар', 4: 'Апр',
        5: 'Май', 6: 'Июн', 7: 'Июл', 8: 'Авг',
        9: 'Сен', 10: 'Окт', 11: 'Ноя', 12: 'Дек'
    }
    # Создаем смещенные позиции для тиков (15-е число каждого месяца)
    tick_positions = [datetime(year, month, 15) for year, month in sorted_months]
    tick_labels = [f"{russian_months[month]} {year}" for year, month in sorted_months]
    # Устанавливаем тики и подписи
    plt.xticks(tick_positions, tick_labels, rotation=90, ha='right')

    plt.title(title, fontsize=14, fontweight='bold')
    plt.xlabel('Месяц')
    plt.ylabel('Количество записей')
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Выводим статистику
    print(f"Всего записей: {len(dates)}")
    print(f"Период: с {dates[0].strftime('%d.%m.%Y')} по {dates[-1].strftime('%d.%m.%Y')}")
    print(f"Всего месяцев: {len(monthly_counts)}")

    return monthly_counts

# Использование с вашим массивом дат
# your_dates = [...]  # ваш массив объектов datetime
# plot_dates_by_month(your_dates, "Ваш заголовок")