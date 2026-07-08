# Список закупки электроники (AliExpress)

Готовый список для самостоятельной покупки — по каждой позиции: что искать,
зачем, на что смотреть при выборе, и прямая ссылка на поиск на AliExpress
(не на конкретный товар — площадка регулярно меняет карточки/продавцов,
поэтому ссылка ведёт на поисковую выдачу, а не на угаданный товар).

**Важно:** я не могу оформить и оплатить заказ за вас (это финансовая
операция) — ниже только подготовка к покупке. Цены — ориентировочные
диапазоны для планирования бюджета, не текущие цены с площадки; сверяйте
на месте перед покупкой.

## 1. Бортовой компьютер

**Raspberry Pi 4 Model B, 4GB RAM**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=Raspberry+Pi+4+Model+B+4GB
- Ориентир: $45–65 (оригинал от авторизованных продавцов дороже клонов —
  для этой задачи нужен оригинал, не клон, ради стабильности USB/CSI)
- На что смотреть: продавец с рейтингом, явно "Raspberry Pi 4B 4GB" (не 2GB,
  не Zero, не клон "Orange Pi" под видом Pi)
- Зачем: единственный компонент, который тянет OpenCV-пайплайн детекции
  полосы в реальном времени onboard (обязательное требование регламента,
  см. `regulation-summary.md`)

**MicroSD карта 32–64GB, class A1/A2**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=microsd+64gb+a2+sandisk
- Ориентир: $8–15
- Зачем: под Raspberry Pi OS — не входила в исходный BOM автора модели
  (у него был ESP32 без ОС), но обязательна для Pi

**Блок питания USB-C 5V/3A**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=raspberry+pi+4+power+supply+5v+3a+usb-c
- Ориентир: $6–10
- Зачем: Pi 4B требователен к стабильности питания — обычная USB-зарядка
  от телефона часто не тянет ток

## 2. Камера

**Raspberry Pi Camera Module 3 (или совместимая с CSI)**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=Raspberry+Pi+Camera+Module+3
- Ориентир: $25–35
- Альтернатива подешевле: любая USB-камера с UVC (USB Video Class),
  поиск: https://www.aliexpress.com/wholesale?SearchText=usb+camera+module+uvc+raspberry+pi
  ($8–15, но выше задержка и хуже качество при плохом освещении)
- Зачем: обязательна по регламенту — ИК line-following датчики прямо
  запрещены (см. `regulation-summary.md`), только камера + CV

## 3. Микроконтроллер привода

**Arduino Nano (оригинал или клон на CH340)**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=Arduino+Nano+CH340
- Ориентир: $3–6 (клоны на CH340 стандартны и надёжны для этой задачи)
- Зачем: принимает команды от Pi по serial, крутит серво+мотор
  (`firmware/drive_controller/`)

## 4. Привод (частично уже в стоковом BOM модели NITROUS)

Эти позиции уже перечислены автором модели в `docs/electronics-bom.md` —
дублирую здесь для единого списка закупки:

**Сервопривод MG90S**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=MG90S+servo+metal+gear
- Ориентир: $2–5 за штуку (берите металлическую шестерню, не пластик —
  надёжнее при постоянной работе руля)

**DC-мотор 280 (щёточный)**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=280+DC+motor+brushed+RC
- Ориентир: $3–7

**Вал 3мм×100мм (1шт), 3мм×30мм (2шт)**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=3mm+steel+shaft+rc+car
- Ориентир: $2–5 за набор

**Подшипники 3×7×3мм (12шт)**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=3x7x3+bearing+10pcs
- Ориентир: $3–6 за упаковку 10-20шт

**Пластиковая шестерня 12T 122A**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=12T+plastic+gear+RC+car
- Ориентир: $2–4 (может не найтись точный модуль — сверить с посадкой
  на вал мотора 280 при заказе, зубья должны совпадать по модулю)

**Стопорные кольца на вал 3мм (3шт)**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=shaft+collar+3mm
- Ориентир: $2–4 за набор

**Крепёж: винты M2.5/M3, гайки M3 нейлоновые, шайбы M3**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=M3+screw+nut+washer+kit+RC
- Ориентир: $5–10 за универсальный набор (дешевле и практичнее купить
  один большой набор, чем штучно)

**Колёсные ступицы под вал 3мм (4шт)**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=3mm+wheel+hub+rc+car
- Ориентир: $3–6

## 5. Управление мотором и питание

**H-мост L298N (модуль)**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=L298N+motor+driver+module
- Ориентир: $2–4
- Альтернатива компактнее: TB6612FNG-модуль (упомянут в референсном
  репозитории COONEO, `EXTERNAL_SOURCES.md`) —
  поиск: https://www.aliexpress.com/wholesale?SearchText=TB6612FNG+module
  ($2–3, компактнее и эффективнее L298N, но чуть сложнее в распайке)

**Аккумулятор Li-ion 18650 (2-3шт) + держатель, или LiPo 2S 7.4V**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=18650+battery+holder+RC+car
  или https://www.aliexpress.com/wholesale?SearchText=lipo+2s+7.4v+rc+car
- Ориентир: $8–20 в зависимости от типа
- Зачем: питание Pi (через отдельный USB-power bank/step-down до 5В — Pi
  нельзя питать напрямую от LiPo без регулятора) + питание мотора/сервы
- ⚠️ Обязательно подбирать по реальному току мотора 280 и энергопотреблению
  Pi 4B под нагрузкой — уточнить при получении датащитов на конкретные
  купленные компоненты

**Step-down/DC-DC модуль 7.4V → 5V (для питания Pi от общей батареи)**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=DC-DC+step+down+5v+3a+usb
- Ориентир: $3–6

## 6. Провода и разное

**Джамперы (папа-папа, папа-мама), макетная плата или перфоплата**
- Поиск: https://www.aliexpress.com/wholesale?SearchText=jumper+wire+breadboard+kit
- Ориентир: $5–10

## Итоговая ориентировочная сумма

Грубый диапазон по всему списку: **$120–200** — сильно зависит от того,
берёте ли оригинальный Raspberry Pi (дороже) или клоны/аналоги, и от того,
сколько из мелкого крепежа (валы/подшипники/шестерня) реально нужно
докупать — часть могла бы идти вместе с готовым "kit" для этой модели,
если такой найдётся на AliExpress по названию "NITROUS RC car kit" или
"DKS-Pro DukeDoks" (стоит проверить перед тем, как заказывать компоненты
по отдельности — возможно дешевле выйдет готовый набор).

## После получения — что делать дальше

1. Проверить компоненты на bring-up чеклист из
   `firmware/drive_controller/README.md`
2. Обновить `docs/electronics-bom.md`, если реально купленные компоненты
   отличаются от предложенных здесь (другая модель серво/мотора и т.д.)
3. Закрыть issue [#1](https://github.com/Mukller/fira-autonomous-rc-car/issues/1)
   на GitHub
4. Перейти к issue #4 (сборка шасси) и #11 (критический замер колеи/колёсной
   базы)
