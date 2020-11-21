# IrCA Duty - дежурный Iris Chat Manager

## Содержание
1. [Как установить](https://github.com/Elchinchel/IDM-SC-mod#Как-установить)
2. [Как обновить](https://github.com/Elchinchel/IDM-SC-mod#Как-обновить)
3. [Сигналы](https://github.com/Elchinchel/IDM-SC-mod#Сигналы)
4. [Благодарности](https://github.com/Elchinchel/IDM-SC-mod#Благодарности)

## Как установить

### [Здесь](https://vk.com/video332619272_456239231) есть видео. Если что, [этот прекрасный человек](https://vk.com/id365530525) может помочь.

Для установки мы будем использовать сайт [pythonanywhere.com](https://www.eu.pythonanywhere.com/)

Переходим по [ссылке](https://www.eu.pythonanywhere.com/registration/register/beginner/), заполняем форму и нажимаем *Register*

*(Под словами "вкладка X" далее по тексту, имеются в виду ссылки на этой панели)*
[![](https://sun9-35.userapi.com/GvwS8jmduczHApabBhlJyeJcAzhMLkFEE8Bqmw/_UZT_5jUQtk.jpg)](https://sun9-35.userapi.com/GvwS8jmduczHApabBhlJyeJcAzhMLkFEE8Bqmw/_UZT_5jUQtk.jpg)


Открываем вкладку *Web*\
Кликаем на *Add a new web app*\
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
Убедитесь, что после выполнения второй команды в консоли присутствует текст, выделенный на картинке\
[![](https://sun1-25.userapi.com/jHRFDx7NyayBffN6AKCK4_Daxu7tBDoCCFulyw/nTtDNh3aeD0.jpg)](https://sun1-25.userapi.com/jHRFDx7NyayBffN6AKCK4_Daxu7tBDoCCFulyw/nTtDNh3aeD0.jpg)


Далее переходим во вкладку *Web* и нажимаем на кнопку *Reload* `имя аккаунта`.eu.pythonanywhere.com

Переходим по ссылке `имя аккаунта`.eu.pythonanywhere.com (ссылка над кнопкой перезагрузки)

[![](https://sun9-58.userapi.com/BQNI2zd65Erkq0AU9DlMfohvqJ8id8rFZ0yx3A/UVdo0UBPYSo.jpg)](https://sun9-58.userapi.com/BQNI2zd65Erkq0AU9DlMfohvqJ8id8rFZ0yx3A/UVdo0UBPYSo.jpg)

Вводим данные, нажимаем *Установить*.

Проверяем ЛС Ириса. Если наблюдается похожая картина, все прошло успешно.

[![](https://sun9-30.userapi.com/sVe1HXsLTeJJAooKetexpUA2SgzebW5x04XRPQ/IiwM_MRWBdc.jpg)](https://sun9-30.userapi.com/sVe1HXsLTeJJAooKetexpUA2SgzebW5x04XRPQ/IiwM_MRWBdc.jpg)

Поздравляю, у тебя теперь есть дежурный. Подключиться к нужному чату можно, написав в нем команду `+api`

### **Внимание!** Через три месяца на бесплатном тарифе сайт отключается!
Чтобы этого не произошло, нужно как минимум раз в три месяца заходить в аккаунт и нажимать на эту кнопку (на вкладке Web под кнопкой перезагрузки)\
[![](https://sun9-45.userapi.com/jCRPUmhR1BziUy5dWC-9RFd6ymSU9zbNC3DgCg/AlaKKXFA_Ko.jpg)](https://sun9-45.userapi.com/jCRPUmhR1BziUy5dWC-9RFd6ymSU9zbNC3DgCg/AlaKKXFA_Ko.jpg)

## Как обновить
*".c обновить"*

Если такого сигнала нет, то вводим следующие команды и 
**перезагружаем сайт на вкладке *Web***
``` bash
cp -rf ICAD/database database
rm -rf ICAD
git clone https://github.com/elchinchel/ICAD
cp -rf database ICAD
rm -rf database
```


## Команды
Команды можно найти [тут](http://vk.com/@ircaduty-commands) (потом переделаю в нормальный вид, пока так)

## Благодарности

Спасибо за исходный код:

> Юрий Юшманов [VK](https://vk.com/id460908267) | [GitHub](https://github.com/lordralinc)


Спасибо за идеи и помощь в тестировании:

> [Аня Фельченко](https://vk.com/id324036713)
>
> [Степа Та](https://vk.com/id365530525)
