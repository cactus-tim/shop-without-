from django.db import models


class Good(models.Model):
    title = models.CharField('Название', max_length=100)
    price = models.IntegerField('Стоимость')
    quantity = models.IntegerField('Количество')

    def __str__(self):
        return self.title


class Users(models.Model):
    ID = models.IntegerField('ID', primary_key=True)
    Name = models.CharField('Имя', max_length=100)
    Surname = models.CharField('Фамилия', max_length=100)
    Email = models.EmailField('Почта')
    Pass1 = models.CharField('Пароль', max_length=20)
    Pass2 = models.CharField('Проверка пароля', max_length=20)
    Age = models.IntegerField('Возраст')
    Face = models.CharField('Фотография', max_length=400)
    Balance = models.IntegerField('Баланс')

    def __str__(self):
        return self.Email
