# IrCA Duty - дежурный Iris Chat Manager

## Содержание
1. [Как установить](./README.md#Как-установить)
2. [Как обновить](./README.md#Как-обновить)
3. [Сигналы](./README.md#Сигналы)
4. [Благодарности](./README.md#Благодарности)
5. [**Статья про ЛП**](http://vk.com/@ircaduty-lp-module)

### [Здесь](https://vk.com/video332619272_456239231) есть видео.
<!-- Если что, [в нашей беседке](https://vk.me/join/cDa3Oe01mwpXuBL2QPOIPLfmJlaLKYBHWEo=) тебе могут помочь. -->
<!-- **(уважай чужое время и проверь сначала заметки беседы, скорее всего, там есть ответ на твой вопрос)** -->

## Как установить

Для установки мы будем использовать сайт [pythonanywhere.com](https://www.eu.pythonanywhere.com/)

Переходим по [ссылке](https://www.eu.pythonanywhere.com/registration/register/beginner/), заполняем форму и нажимаем *Register*

*(Под словами "вкладка X" далее по тексту, имеются в виду ссылки на этой панели)*
[![](https://sun9-35.userapi.com/GvwS8jmduczHApabBhlJyeJcAzhMLkFEE8Bqmw/_UZT_5jUQtk.jpg)](https://sun9-35.userapi.com/GvwS8jmduczHApabBhlJyeJcAzhMLkFEE8Bqmw/_UZT_5jUQtk.jpg)


Открываем вкладку *Web*\
Кликаем на *Add a new web app*\
В появившемся окошке *next*  -> *Flask* -> *Python3.8*\
В путь вводим /home/`имя аккаунта`/ICAD/start.py

[![](https://sun1-88.userapi.com/7GyijrmWOq2WKYg-RqZMsZjn_5J9FAN0yTv8hA/EzO72_mIHwc.jpg)](https://sun1-88.userapi.com/7GyijrmWOq2WKYg-RqZMsZjn_5J9FAN0yTv8hA/EzO72_mIHwc.jpg)

Тыкаем на вкладку *Files*. Смотрим на картинку:\
[![](https://sun9-79.userapi.com/impf/UxI4dBLSwiYBT_JojwqN1O6xq_I0tZSVqKvBoQ/zVjLKL9NpKc.jpg?size=777x137&quality=96&sign=fd988e120467f5046da6a4ce944947d8&type=album)](https://sun9-79.userapi.com/impf/UxI4dBLSwiYBT_JojwqN1O6xq_I0tZSVqKvBoQ/zVjLKL9NpKc.jpg?size=777x137&quality=96&sign=fd988e120467f5046da6a4ce944947d8&type=album)

Вставляем в открывшийся редактор следующий текст и тыкаем на кнопку **Run**
```python
import os
os.system('rm -rf ICAD')
os.system('git clone https://github.com/elchinchel/ICAD')
```


Далее переходим во вкладку *Web* и нажимаем на кнопку *Reload* `имя аккаунта`.eu.pythonanywhere.com

Переходим по ссылке `имяаккаунта`.eu.pythonanywhere.com (ссылка над кнопкой перезагрузки)

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

Если дежурный не работает, обновиться можно, открыв bash консоль и введя следующие команды:
```bash
git fetch --all
git reset --hard origin/master-beta
```

## Команды
Команды можно найти [тут](http://vk.com/@ircaduty-commands)

## Благодарности

Спасибо за поддержку в сложные времена, public relations и просто всё хорошее:

> [Мария Громова](https://vk.com/id549315693)

Спасибо за исходный код:

> Юрий Юшманов [VK](https://vk.com/id460908267) | [GitHub](https://github.com/lordralinc)

Спасибо за идеи и помощь в тестировании:

> [Степа Та](https://vk.com/id365530525)
>
> [Аня Фельченко](https://vk.com/id324036713)

Спасибо за вклад в кодовую базу:

> [Алексей Кузнецов](https://vk.com/id194861150)
>
> [Альнур Ахмадуллин](https://vk.com/id197786896)
>
> [Серёжа Сафронов](https://vk.com/id266287518)
