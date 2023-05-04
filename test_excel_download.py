import pandas as pd

# Загрузка файла
df = pd.read_excel('file.xlsx')

# Сумма всех займов для компаний, зарегистрированных не позднее 2021 года
total_amount = df.loc[df['registration_date'] <= '2021-12-31', 'amount'].sum()
print('Сумма всех займов для компаний, зарегистрированных не позднее 2021 года:', total_amount)

# Сумма займов для каждого из рейтингов
rating_amount = df.groupby('rating')['amount'].sum().reset_index()
print('Сумма займов для каждого из рейтингов:')
print(rating_amount)