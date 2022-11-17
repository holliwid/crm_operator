# CRM для оператора грузовых перевозок
Одна из ранних версий, которую можно показать, так как разрабатывалась специально под клиента.




Реализована сложная бизнес логика машин и водителей, свободных и находящихся в рейсе.  

Можно добавлять новых водителей и новые машины. Менять параметры уже существующих машин. Добавление нового рейса учитывает категорию водителя, свободен ли водитель, свободна ли машина, водите ли эту машину этот водитель, подходящия ли категория у водителя.
Также можно распечатать прототип накладной.


## Стек технологий:
```
python3.8
postgeresql
PyQt5
```


## Интрерфейс
![contracts](./img_for_readme/contracts.png)
![drivers](./img_for_readme/drivers.png)
![free_drivers](./img_for_readme/free_drivers.png)
![cars](./img_for_readme/cars.png)
![free_cars](./img_for_readme/free_cars.png)
![garage](./img_for_readme/garage.png)
![clients](./img_for_readme/clients.png)

Накладная выдаётся в виде html страницы, которую в дальгнейшем легко конвертировать в pdf.
![report](./img_for_readme/report.png)
## Схема базы данных
![db](./img_for_readme/db.png)
