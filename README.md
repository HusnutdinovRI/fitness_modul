# Модуль фитнес-трекера

## Модуль выполняет следующие функции:
- принимает от блока датчиков информацию о прошедшей тренировке,
- определят вид тренировки,
- рассчитыват результаты тренировки,
- выводит информационное сообщение о результатах тренировки.

## Установка:


Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/HusnutdinovRI/fitness_modul.git
```

```
cd fitness_modul
```

### *Установка на Windows:*

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/source/activate
```

Установить зависимости из файла requirements.txt:

```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### *Установка на Mac OS и Linux:*

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

## Технолгии

-   [Python](https://www.python.org/)  - язык программирования.

