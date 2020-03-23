### Проект Форум

Запустить в контейнере
```
chmod +x entrypoint.sh
docker-compose up -d --build
```

Закрыть контейнер
```
docker-compose down
```

Просто остановить контейнер
```
docker stop CONTAINER ID 
```


Запустить ранее остановленный контейнер
```
docker start CONTAINER ID
```


Перегрузка контейнера
```
docker restart CONTAINER ID
```
