# NewsPaper_D7.5
# for SkillFactory Модуль D7.5
Приложение, создающее сайт "Портал новостей"
# Для запуска приложения понадобится три окна Терминала
# В двух из них должно быть одно и то же виртуальное окружение
# cd NewsPaper
python3 manage.py runserver
celery -A NewsPaper worker -l INFO
redis-server

