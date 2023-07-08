# Lesta_task1
Есть список пользователей и хостов, далее "JSON"
"""
{
  "hosts": {
    "EU-CLUSTER": {
      "title": "Eu cluster discription",
      "host": "eu1-vm-host",
      "user": "euuser"
    },
    "NA-CLUSTER": {
      "title": "Na cluster description",
      "host": "na1-vm-host",
      "user": "nauser"
    }
  }
}
"""
1) Авторизация на ssh host может происходить либо по ssh ключу, либо по password, который равен user,
то есть для пользователя user1, пароль user1, если у пользователя нет ключа.
2) У каждого пользователя user в директории ~/bw/ может быть рабочая копия git или subversion.
Необходимо написать скрипт, который
3) Проходит по всем пользователям из JSON
4) Собирает информацию о рабочей копии, а именно
5.А) Для git узнаёт за какой веткой следит данная рабочая копия и на какой ревизии она находится.
5.Б) для subversion узнаёт какая ветка находится в рабочей копии и на какой ревизии
6) Добавляет в изначальный JSON собранную информацию из пунктов 5.А, 5.Б.
8) Полученный скрипт на python(3.9+) необходимо залить в любой публичный репозиторий по
желанию(gitlab/github/google code/etc)

Что хочется:
а) отсутствие башизмов
б) чистый и аккуратный код
в) хорошая обработка непредвиденных ситуаций
г) минимальное количество unit тестов
д) не думайте про это задание как про тест, в нём нет правильного или неправильного решения
