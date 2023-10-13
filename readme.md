## créer une variable d'environnement
``` bash
setx EPICEVENTS_PW password
```

``` bash
setx EPICEVENTS_USER epicevent_user
```

``` bash
setx EPICEVENTS_SK key
```

|                        | SALES | ACCOUNTING | SUPPORT |
|------------------------|:-----:|:--------:|:-------:|
| EMPLOYEES
| ``Employees``: create  |   ✖   |    ✔      |    ✖    |
| ``Employees``: read    |   ✔   |    ✔      |    ✔    |
| ``Employees``: filter  |       |           |         |
| ``Employees``: update  |   ✖   |    ✔      |    ✖    |
| ``Employees``: delete  |   ✖   |    ✔      |    ✖    |
| CLIENTS
| ``Clients``: create    |   ✔   |    ✖      |    ✖    |
| ``Clients``: read      |   ✔   |    ✔      |    ✔    |
| ``Clients``: filter    |       |           |         |
| ``Clients``: update    |   ✔   |    ✖      |    ✖    |
| ``Clients``: delete    |   ✔   |    ✖      |    ✖    |
| CONTRACTS
| ``Contracts``: create  |       |           |         |
| ``Contracts``: read    |       |           |         |
| ``Contracts``: filter  |       |           |         |
| ``Contracts``: update  |   ✔   |           |         |
| ``Contracts``: delete  |       |           |         |
| EVENTS
| ``Events``: create     |   ✔    |           |         |
| ``Events``: read       |       |           |         |
| ``Events``: filter     |       |           |         |
| ``Events``: update     |   ✖   |    ✔      |   ✔     |
| ``Events``: delete     |       |           |         |

