# IrCA Duty - дежурный Iris Chat Manager

## Содержание
1. [Как установить](https://github.com/Elchinchel/IDM-SC-mod#Как-установить)
2. [Как обновить](https://github.com/Elchinchel/IDM-SC-mod#Как-обновить)
3. [Сигналы](https://github.com/Elchinchel/IDM-SC-mod#Сигналы)
4. [Благодарности](https://github.com/Elchinchel/IDM-SC-mod#Благодарности)

## Как установить
Для установки мы будем использовать сайт [pythonanywhere.com](https://www.eu.pythonanywhere.com/)

Переходим по [ссылке](https://www.eu.pythonanywhere.com/registration/register/beginner/), заполняем форму и нажимаем *Register*

*(Под словами "вкладка X" далее по тексту, имеются в виду ссылки на этой панели)*
[![](https://sun9-35.userapi.com/GvwS8jmduczHApabBhlJyeJcAzhMLkFEE8Bqmw/_UZT_5jUQtk.jpg)](https://sun9-35.userapi.com/GvwS8jmduczHApabBhlJyeJcAzhMLkFEE8Bqmw/_UZT_5jUQtk.jpg)


Далее открываем вкладку *Web*
Кликаем на *Add a new web app*
В появившемся окошке *next*  -> *Flask* -> *Python3.8*\
В путь вводим /home/`имя аккаунта`/ICAD/start.py

[![](https://sun1-88.userapi.com/7GyijrmWOq2WKYg-RqZMsZjn_5J9FAN0yTv8hA/EzO72_mIHwc.jpg)](https://sun1-88.userapi.com/7GyijrmWOq2WKYg-RqZMsZjn_5J9FAN0yTv8hA/EzO72_mIHwc.jpg)

Тыкаем на вкладку *Consoles*. Ищем блок *Start a new console*, в нем выбираем *Bash*

После загрузки набираем в консоли
(это две команды, после каждой нужно нажимать Enter)
```bash
rm -rf ICAD
git clone https://github.com/elchinchel/ICAD
```
Убедитесь, что после выполнения второй команды в консоли присутствует текст, выделенный на картинке
[![](https://sun1-25.userapi.com/jHRFDx7NyayBffN6AKCK4_Daxu7tBDoCCFulyw/nTtDNh3aeD0.jpg)](https://sun1-25.userapi.com/jHRFDx7NyayBffN6AKCK4_Daxu7tBDoCCFulyw/nTtDNh3aeD0.jpg)


Далее переходим во вкладку *Web* и нажимаем на кнопку *Reload* `имя аккаунта`.eu.pythonanywhere.com

Переходим по ссылке `имя аккаунта`.eu.pythonanywhere.com (ссылка над кнопкой перезагрузки)

[![](https://sun9-58.userapi.com/BQNI2zd65Erkq0AU9DlMfohvqJ8id8rFZ0yx3A/UVdo0UBPYSo.jpg)](https://sun9-58.userapi.com/BQNI2zd65Erkq0AU9DlMfohvqJ8id8rFZ0yx3A/UVdo0UBPYSo.jpg)

*(По дальнейшим действиям есть **[более подробная статья](https://vk.com/@idmmod-install)**)*

Вводим данные, нажимаем *Установить в CallBack режиме*.

Если все прошло успешно, откроется страница с виджетом ВКонтакте. Авторизуемся.

После этого нажимаем на синюю кнопку *Отправить конфигурационную фразу Ирису*

Проверяем ЛС Ириса. Если наблюдается похожая картина, все прошло успешно.

[![](https://sun9-30.userapi.com/sVe1HXsLTeJJAooKetexpUA2SgzebW5x04XRPQ/IiwM_MRWBdc.jpg)](https://sun9-30.userapi.com/sVe1HXsLTeJJAooKetexpUA2SgzebW5x04XRPQ/IiwM_MRWBdc.jpg)

Поздравляю, у тебя теперь есть дежурный. Подключиться к нужному чату можно, написав в нем команду `+api`

### Внимание! Через три месяца на бесплатном тарифе сайт отключается!
Чтобы этого не произошло, нужно как минимум раз в три месяца заходить в аккаунт и нажимать на эту кнопку\
[![](https://sun9-45.userapi.com/jCRPUmhR1BziUy5dWC-9RFd6ymSU9zbNC3DgCg/AlaKKXFA_Ko.jpg)](https://sun9-45.userapi.com/jCRPUmhR1BziUy5dWC-9RFd6ymSU9zbNC3DgCg/AlaKKXFA_Ko.jpg)

### Как создать приложение ВК
Переходим по ссылке [https://vk.com/editapp?act=create](https://vk.com/editapp?act=create "https://vk.com/editapp?act=create"), в поле платформа выбираем *сайт*

Адрес сайта и базовый домен `http://{имя вашего аккаунта}.eu.pythonanywhere.com`

[![](https://sun1-83.userapi.com/g4A8pmmIpssJtHlXUqb1K6OcPOVsmePa2Wb6WA/oaGRBEOYixc.jpg)](https://sun1-83.userapi.com/g4A8pmmIpssJtHlXUqb1K6OcPOVsmePa2Wb6WA/oaGRBEOYixc.jpg)`

Кликаем на *подключить сайт*.

## Как обновить
Вводим в консоль команды, 
**перезагружаем сайт на вкладке *Web***\
**Команды только для версий от 1.1.1 beta rev.1 (проверить можно командой .с инфо)**
``` bash
cd ICAD
git fetch --all
git reset --hard origin/master-beta
```
**Команды для старых версий**
``` bash
cp -rf ICAD/database database
rm -rf ICAD
git clone https://github.com/elchinchel/ICAD
cp -rf database ICAD
rm -rf database
```

(команды, если устанавливали IDM-SC-mod)
``` bash
cp -rf IDM/database database
rm -rf IDM
git clone https://github.com/elchinchel/IDM
cp -rf database IDM
rm -rf database
```

## Сигналы
(здесь не все, потом дополню)\
Команды могут начинаться как с "!с", так и с ".с"

### Доступные в любом чате с Iris

|Команда|Описание|
|---|---|
|!с пинг / пиу / кинг / тик |Отправляется сообщение с временем задержки|
|!с инфо / инфа / -i / info |Отправляется сообщение с информацией о дежурном|
|!с -смс [количество] |Удаляет свои сообщения|
|!с +др / +друг [+ответ на сообщение/упоминание] |Отправляется запрос на добавление в друзья|
|!с -др / -друг [+ответ на сообщение/упоминание] |Отправляется запрос на удаление из друзей|
|!с +чс [+ответ на сообщение/упоминание] |Добавление в черный список|
|!с -чс [+ответ на сообщение/упоминание] |Удаление из черного списка|
|!с +шаб [имя шаблона]&#124;[название категории] | Добавляет новый шаблон (в сообщении должна содержаться какая-то информация помимо команды, например ответ на сообщение или какой-либо текст)|
|!с -шаб имя шаблона | Удаляет шаблон |
|!с шабы [название категории/"все"] | Выводит список шаблонов |
|!с шаб имя шаблона | Отправляет сохраненный шаблон |
|!с +дов [+ответ на сообщение/упоминание] | Добавляет пользователя в список доверенных |
|!с -дов [+ответ на сообщение/упоминание] | Исключает пользователя из списка доверенных |
|!с довы | Выводит список доверенных пользователей |


### Доступные когда вы дежурный в чате
|Команда|Описание|
|---|---|
|!д пинг / пиу / кинг / тик | Отправляется сообщение с временем задержки|
|!д инфо / инфа / -i / info |Отправляется сообщение с информацией о дежурном|
|!д повтори/скажи/напиши[новая строка]Текст| Дежурный повторит текст (только для доверенных пользователей) |

Так же обрабатываются все стандартные сигналы, кроме `ignoreMessages`. О стандартных сигналах Вы можете узнать в [статье](https://vk.com/@iris_cm-api2).


## Благодарности

Спасибо за исходный код:

>[Юрий Юшманов](https://vk.com/llordrall)


Спасибо за идеи и помощь в тестировании:

>[Аня Фельченко](https://vk.com/id324036713)
>
>[Степа Та](https://vk.com/st_ta)


Спасибо за помощь в тестировании (от Юрия):

>[Ридэль Яумбаев](https://vk.com/ss_20)
>
>[Влад Богданов](https://vk.com/gamtz)
>
>[Владислав Джениа](https://vk.com/klubnishhhka)
>
>[Дмитрий Ким](https://vk.com/iris_wolf)
