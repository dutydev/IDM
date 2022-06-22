# Как предложить свои изменения в коде

1. [Регистрация на GitHub](./CONTRIBUTE.md#Регистрация-на-GitHub) ([Блиц-реквест](./CONTRIBUTE.md#Блиц-реквест))
2. Внесение изменений в свой репозиторий
   * [Первый вариант](./CONTRIBUTE.md#Вариант-1) (не требует установки никаких программ)
3. [Создание *pull request*](./CONTRIBUTE.md#Создание-pull-request)

---

# Регистрация на [GitHub](https://github.com/signup)

Переходишь по [ссылочке](https://github.com/signup), заполняешь все поля. Готово!

Теперь нужно форкнуть репозиторий, для этого зайти на [его страницу в GitHub](https://github.com/elchinchel/ICAD) и тыкнуть кнопочку **Fork**
![](https://sun9-67.userapi.com/impg/yhZ279ZOkNrJvM4XyUQ3I-9ao3zcg8Q1VSDJ-w/PR0Rq32yUlM.jpg?size=1280x677&quality=96&sign=69567704d0782d67d9cd364b08aea8b6&type=album)

## Блиц-реквест

>*ЭТОТ РЕКВЕСТ НУЖЕН МНЕ ЗДЕСЬ И СЕЙЧАС!!1!*

1. Открываешь нужный файлик в [репозитории ICAD](https://github.com/elchinchel/ICAD), тыкаешь на карандашик
![](https://sun9-51.userapi.com/impg/NMVJL4_zmSlVWkHEgLJaPmrUg7DFQaV2HrStZw/ezZI5sgZOhE.jpg?size=1280x677&quality=96&sign=4f75b1cbeab2946dafd095e7c18b1686&type=album)

2. Вносишь изменения, описываешь их с помощью двух полей в самом низу и тыкаешь *предложить изменения* (*Propose changes*)
![](https://sun9-83.userapi.com/impg/2W_b1EotOjqkH1UNx7VqsS2vLGeVLW8LhZ6f2g/KAnyM9VBfSw.jpg?size=1280x677&quality=96&sign=cb78e624d315a68cec0cc8b3ba1074b4&type=album)

3. ???????

4. Жди рассмотрения!

## Вариант 1

>*Вариант, который не потребует установки каких-либо программ, всё через браузер*

Заходишь к себе на [PythonAnywhere](https://eu.pythonanywhere.com) (или регистрируешь новый акк, если его нет)

Если не создал ранее, создаёшь веб приложение.

Открываешь *bash* консоль (которая у тебя уже была создана при установке вебхука) и клонируешь СВОЙ репозиторий (используешь ссылку из своего репозитория)
![](https://sun9-61.userapi.com/impg/lwa-EpeLjJik8r4Yb1JJRnFhwbz0lNEIHRu5DA/jNc0AcU-eA8.jpg?size=1280x677&quality=96&sign=5330f4818ce2374218627ffa66e6b36c&type=album)

> **Внимание!** Если у тебя уже установлен вебхук, команда **rm** его сотрёт. Поэтому можешь использовать вместо неё команду **mv**, которая переименует старую папку с вебхуком (например, "*mv ICAD ICAD_old*")

```bash
rm -rf ICAD
git clone ЗдесьСсылкаНаТвойРепозиторий ICAD
```

### Настройка **git**
1. Укажи своё имя/псевдоним и E-mail:
   ```bash
    git config --global user.name "Твоё Имя"
    git config --global user.email "твояпочта@чёутебятам.com"
    ```

2. Зайди на [страницу создания токенов в GitHub](https://github.com/settings/tokens)

3. Создай токен (не забудь отметить чекбокс **repo** в списке разрешений)
![](https://sun9-68.userapi.com/impg/2UnynhTTSHZYqpFzyTMKbcRzXhFhuWuMBVSfiw/3zm4OkS8q8s.jpg?size=722x138&quality=96&sign=4c0a9657730d3c080dd2360f1275d091&type=album)
4. Сохрани полученный GitHub токен куда-нибудь (но относись к нему как к паролю, он позволяет получить доступ к твоему аккаунту)

Начни делать, что хочешь, открывай вкладку Files, папку ICAD и редактируй код

> Не забывай перезапускать веб-приложение после изменений (кнопка *Reload* на вкладке *Web*)

Когда решишь, что всё готово и можно публиковать, открывай *bash* и пиши следующее:
```bash
git add *
git commit -m "Краткое описание изменений"
git push origin master-beta
```

Введи логин своего аккаунта GitHub и токен (да, он попросит пароль, введи вместо него [ранее полученный](./CONTRIBUTE.md#Настройка-git) токен)

Если всё сделал правильно, твои изменения появятся в твоём репозитории GitHub и ты сможешь перейти к [следующему шагу](./CONTRIBUTE.md#Создание-pull-request)

# Создание pull request

Закоммитил в свой репозиторий то, что хотел? Открывай GitHub, тыкай на Contribute и Open pull request
![](https://sun9-58.userapi.com/impg/G-5bYsn1lUpjFBzTXykOs5MNulSABhs8B4Tz-g/wh4v3p71bX8.jpg?size=1280x677&quality=96&sign=583039d5b55223e70f4a3a111b57518d&type=album)

Проверяй изменения и если всё окей, тыцкай **Create pull request**
![](https://sun9-55.userapi.com/impg/ydPS1nS01HyYHUtET6EiUTdMJfBaeDqjRhzo2A/sXxWKqqbTyQ.jpg?size=1280x677&quality=96&sign=45fea27179ee0bf3d3a8d96c89df50e3&type=album)

![](https://sun9-42.userapi.com/impg/-aTACZ3hhoNSvTaZJBX-OcoRlF0Yl3LPMUW2fA/mNt2awNoVbY.jpg?size=1280x677&quality=96&sign=3b404b098e0f58e0079b816e4e61d824&type=album)

## Готово!
## Можешь написать о своём крутом пулл реквесте в беседу и ждать, пока его рассмотрят

*ещё приколы допишу потом*