import pandas as pd
import random
import string

# Создаем список из 7 случайных названий
names = ['Camera', '1m Cabel', '1m Cabel(hard)', 'Windows', 'Security checker', 'Fire protect', 'Anti tief']

# Создаем список из 7 случайных названий
names2 = [''.join(random.choices(string.ascii_uppercase, k=5)) for i in range(7)]

# Создаем датафрейм с 1000000 строками
df = pd.DataFrame(index=range(1000000))

# Добавляем столбец id со случайными уникальными значениями в диапазоне от 1000000 до 3000000
df['id'] = random.sample(range(1000000, 3000000), 1000000)
print('[+] Добавлено: id')

# Добавляем столбец name со случайным выбранным названием из списка names
df['name'] = [random.choice(names) for i in range(1000000)]
print('[+] Добавлено: name')

# Создаем список из 20 случайных слов
words = [''.join(random.choices(string.ascii_lowercase, k=5)) for i in range(20)]
print('[+] Добавлено: words')

# Добавляем столбец description со случайным текстом из 20 слов
df['description'] = [' '.join(random.sample(words, 20)) for i in range(1000000)]
print('[+] Добавлено: description')

# Добавляем столбец price со случайными ценами от 1000 до 100000 с шагом 500
df['price'] = [random.randrange(1000, 100000, 500) for i in range(1000000)]
print('[+] Добавлено: price')

# Добавляем столбец срок выполнения со случайными числами от 30 до 90 с шагом 30
df['execution_days'] = [random.randrange(30, 90, 30) for i in range(1000000)]
print('[+] Добавлено: execution_days')

# Записываем датафрейм в excel файл
df.to_excel('data.xlsx', index=False)
print('[+] Файл записан: успешно')