<div align="center">

[English below](#english) • **Русский**

</div>

# Внешние источники: атрибуция и выжимка

Этот файл — детальная выжимка по каждому внешнему источнику, который
использован (или изучен) в этом проекте: кто автор, что внутри, какая
лицензия и что из этого реально можно переиспользовать в будущем.
Дополняет таблицу в [README.md](README.md), но глубже по содержанию.

Общее правило по всем пунктам ниже: код чужих репозиториев **не скопирован**
построчно в этот репозиторий (кроме случаев, где это явно указано и
разрешено лицензией) — там, где это возможно, подключено как git submodule
(`external/`), сохраняя историю и авторство оригинала. Там, где копировать
нельзя (нет лицензии) или невозможно (не GitHub-репозиторий, например
Reddit-обсуждение), материал описан своими словами со ссылкой на оригинал.

---

## 1. Pandas-Team — Autonomous Car Simulation Based on AVIS Engine (FIRA 2021)

- **Репозиторий:** https://github.com/Pandas-Team/Autonomous-Car-Simulation-Based-on-AVIS-Engine-FIRA-2021
- **Путь в этом репо:** `external/pandas-team-avis-engine` (git submodule)
- **Лицензия:** GPL-3.0 — при переиспользовании кода итоговая работа должна
  оставаться под GPL-3.0 (copyleft)
- **Авторы (команда Pandas-Team):**
  - Omid Omidi — [LinkedIn](https://www.linkedin.com/in/omidomidi77/) · [GitHub](https://github.com/omidomidi77)
  - Milad Soltany — [LinkedIn](https://www.linkedin.com/in/milad-soltany/) · [GitHub](https://github.com/miladsoltany)
  - Amirhossein Kazerooni — [LinkedIn](https://www.linkedin.com/in/amirhossein477/) · [GitHub](https://github.com/amirhossein-kz)
  - Amirhossein Heydarian — [LinkedIn](https://www.linkedin.com/in/amirhosseinh77/) · [GitHub](https://github.com/amirhosseinh77)
  - Aida Mohammadshahi — [LinkedIn](https://www.linkedin.com/in/aida-mohammadshahi-9845861b3/) · [GitHub](https://github.com/aidamohammadshahi)
- **Отдельная атрибуция внутри репозитория:** файлы `FiraAuto.py`/`AVISEngine.py`
  (клиентская библиотека для связи с симулятором) подписаны
  `@ 2020, Copyright Amirmohammad Zarif` — это автор Python API для AVIS Engine
  (оригинальный проект: https://github.com/AvisEngine/AVIS-Engine-Python-API),
  а не команда Pandas-Team. Разграничивайте: алгоритмы вождения — Pandas-Team,
  транспортный протокол до симулятора — Amirmohammad Zarif/AvisEngine.
- **Результат на соревновании FIRA 2021:** 1-е место (технический отчёт),
  2-е место (гонка/suburban), 3-е место (urban), 3-е место в общем зачёте.
  https://iran.firaworldcup.org/?leagues=autonomous-cars

### Что внутри (по факту, не с чужих слов)

- `RACE/` — код для загородной/скоростной трассы:
  - `functions.py` — детекция полосы через Canny + Hough Transform,
    HSV-маска для жёлтой линии, линейная регрессия по точкам линии
  - `FIRA_car_V2.py`…`V5.py` — итерации основного цикла управления
  - PID-регулятор скорости/руля, использование цифрового энкодера,
    ультразвуковые датчики для объезда препятствий
  - В README авторы упоминают также эксперименты с behavioral cloning
- `URBAN/` — код для городской трассы:
  - Всё из RACE плюс распознавание дорожных знаков через YOLOv5
    (обученная модель `best_model.h5`, `car_mask.npy`)
  - Принудительная остановка (forced stop) как система безопасности —
    из-за требований к точности в городском сценарии авторы явно снизили
    скорость в пользу надёжности
- `extra/` — вспомогательные скрипты (сохранение изображений, HSV-подбор,
  примеры)
- **Архитектура связи с симулятором** (`FiraAuto.py`): TCP-сокет,
  класс `car` с методами `connect()`, `setSteering()`, `setSpeed()`,
  `move()`; изображение с камеры передаётся как base64-строка

### Что уже использовано в этом репозитории

- `docs/lane-detection-adaptation.md` — построчный разбор `functions.py` и
  план адаптации под реальную камеру (без копирования кода)

### Что можно взять в будущем (с соблюдением GPL-3.0)

- Идею PID-регулятора скорости с цифровым энкодером — для контроля
  скорости на реальном приводе DC-мотора 280 (см. `docs/electronics-bom.md`)
- Общую архитектуру forced-stop (принудительная остановка при
  неуверенности алгоритма) — применимо и на физической машине как мера
  безопасности
- Если понадобится реальный YOLO-инференс для знаков на Urban Track —
  это единственный из источников, где есть готовый пайплайн детекции
  знаков (`best_model.h5`), но переиспользование самого кода требует
  сохранения GPL-3.0 для того модуля, который его использует

---

## 2. FIRA-Autonomous-Cars — FIRA Autonomous Cars Simulator

- **Репозиторий:** https://github.com/Fira-Autonomous-Cars/FIRA-Autonomous-Cars-Simulator
- **Путь в этом репо:** `external/fira-autonomous-cars-simulator` (git submodule)
- **Лицензия:** CC0-1.0 (Public Domain) — свободное использование без
  ограничений
- **Автор:** официальный аккаунт организации FIRA Autonomous Cars
  (не привязан к конкретному физлицу); отдельная благодарность в
  changelog — Sina Moghimi ([GitHub](https://github.com/sinamoghimi73))
  за обновление под ROS Noetic

### Что внутри

- Полноценный ROS 1 (Noetic) + Gazebo симулятор, catkin workspace
- Две трассы: Race Track и Urban Track (со знаками и AprilTags)
- Пакеты `autonomous_vehicle_simple/project/teb/nosecurity`,
  `avisengine_environment`, `avisengine_resources`
- **`example_pkg/`** — минимальный пример работы с топиками:
  - `drive.py` — публикует `geometry_msgs/Twist` в топик
    `/catvehicle/cmd_vel_safe` (стандартный ROS-паттерн управления
    скоростью/поворотом, тот же message type, что используется в
    большинстве ROS-роботов)
  - `imageReceive.py` — подписка на `sensor_msgs/Image` в топике
    `/catvehicle/camera_front/image_raw_front` через `cv_bridge`
- В комплекте — сторонние ROS-пакеты для CAN-шины и реального автомобиля
  Lincoln MKZ (`dataspeed_can`, `dbw_mkz_ros`, `lusb`) — унаследованы от
  более крупного автопром-стека, не имеют отношения к нашей RC-машине

### Что уже использовано в этом репозитории

- Формат топиков (`Twist` для управления, `Image` для камеры) — концептуальный
  ориентир для наших ROS 2 нод, хотя мы используем `Float32` для
  steering/throttle, а не `Twist` (сервопривод с Ackermann-геометрией не
  является differential-drive роботом, для которого предназначен `Twist`)

### Что можно взять в будущем

- При необходимости протестировать наш алгоритм в симуляторе перед
  реальным заездом — этот симулятор прямо для этого предназначен, лицензия
  CC0 позволяет свободно это делать

---

## 3. COONEO — Arduino_Raspberry_ROS_Car

- **Репозиторий:** https://github.com/COONEO/Arduino_Raspberry_ROS_Car
- **Путь в этом репо:** `external/arduino-raspberry-ros-car` (git submodule,
  подключён только для чтения — код не копируется)
- **Лицензия:** не указана — по умолчанию все права сохраняются за автором,
  переиспользование кода без отдельного разрешения автора не допускается
- **Автор/бренд:** COONEO — китайский maker/образовательный бренд,
  публикуется также как WeChat 公众号 "COONEO", Zhihu-аккаунт "Neor",
  Bilibili-канал "COONEO"

### Что внутри

- Прошивки для Arduino Mega 2560 под два варианта драйвера мотора:
  TB6612FNG и A4950T, с PID-регулированием скорости по энкодеру
  (`RobotPIDDriver_tb6612/`, `RobotPIDDriver_A4950T/`)
- ROS-нода на Raspberry Pi 4B (Ubuntu), мост Arduino↔ROS через пакет
  `ros_arduino_bridge` (публикация/подписка на топик `cmd_vel`)
- Демонстрация SLAM/gmapping и автономной навигации (differential-drive
  робот на 4 колёсах — НЕ Ackermann steering, архитектурно другой класс
  машины, чем наша)
- Видео-демонстрации детекции огня по цвету, навигации

### Важное отличие от нашей задачи

Это дифференциальный привод (два независимых мотора с энкодерами), а не
Ackermann-руление сервоприводом, как в NITROUS/FIRA. Прямое заимствование
кода управления не подходит один-в-один — полезен как референс архитектуры
"Arduino ↔ serial ↔ ROS на Raspberry Pi", а не как источник алгоритмов
руления.

### Что можно взять в будущем

- Общий паттерн `ros_arduino_bridge` (serial-мост Arduino↔ROS) — идейно
  похож на наш `serial_bridge_node.py`, но переиспользовать сам код нельзя
  без лицензии — нужно писать самостоятельно (что и сделано)
- Если в будущем понадобится добавить энкодеры на колёса для точной
  одометрии — можно списаться с автором по указанным каналам за
  разрешением на использование PID-кода

---

## 4. tommybee456 — ESP32-Car-Project (автор 3D-модели NITROUS)

- **Репозиторий:** https://github.com/tommybee456/ESP32-Car-Project
- **В этом репо:** НЕ подключён как submodule (нет лицензии) — только
  описан здесь и в `docs/electronics-bom.md`
- **Лицензия:** не указана
- **Автор:** TommyB (тот же автор, что спроектировал 3D-модель шасси
  NITROUS, см. ниже) — https://www.printables.com/@TommyB_646474

### Что внутри

- `esp32Sender/` — прошивка ручного RC-пульта на ESP32
- `esp32Receiver/` — прошивка приёмника в машине, управление серво+мотором
  по протоколу ESP-NOW (не автономное вождение — обычный ручной RC)
- Ссылки на PCB-разводку в EasyEDA:
  https://oshwlab.com/tommybdog/esp32withmotorcontrol,
  https://oshwlab.com/tommybdog/espcontroller
- Параметры ШИМ из `esp32Receiver.ino` (использованы как справочные числа
  в `docs/electronics-bom.md` и `firmware/drive_controller/`, код не
  скопирован):
  - сервопривод: 50 Гц, 10-битное разрешение, пин GPIO9
  - DC-мотор: H-мост, 1 кГц, пины GPIO5/GPIO7, sleep-пин GPIO4

### Что можно взять в будущем

- Готовые PCB-схемы (EasyEDA) — если решите делать кастомную плату вместо
  готового H-моста/сервопривода на проводах, это отправная точка (но
  нужно запросить разрешение у автора — лицензии нет)

---

## 5. NITROUS — 3D Printed RC Car (3D-модель шасси)

- **Источник:** https://www.printables.com/model/415497-3d-printed-rc-car
- **В этом репо:** `models/` — файлы STL/3MF без изменений
- **Лицензия:** Creative Commons CC0 1.0 (Public Domain) — автор явно
  пометил модель как оригинальную работу, свободную для любого
  использования, включая коммерческое, без обязательной атрибуции
- **Автор:** TommyB — https://www.printables.com/@TommyB_646474 (тот же
  автор, что и пункт 4 выше)

### BOM автора (из описания модели)

- 1× вал 3мм×100мм, 2× вал 3мм×30мм, 12× подшипники 3×7×3мм
- 1× пластиковая шестерня 12T 122A
- 1× сервопривод MG90s, 1× DC-мотор 280
- Крепёж: стопорные кольца, винты M2.5/M3, гайки, шайбы
- 4× колёсные ступицы под вал 3мм

Полный разбор геометрии (реальные размеры из STL) — в
[`docs/electronics-bom.md`](docs/electronics-bom.md).

---

## 6. Обсуждение на Reddit: управление RC-машиной через ROS + Raspberry Pi

- **Источник:** https://www.reddit.com/r/robotics/comments/alpfrj/i_controlled_a_rc_car_using_ros_and_a_raspberry/
- **Автор:** пользователь Reddit `tizianofiorenzani` (Tiziano Fiorenzani) —
  ведёт образовательную серию видео по ROS на YouTube:
  https://www.youtube.com/playlist?list=PLuteWQUGtU9BU0sQIVqRQa24p-pSBCYNv
- Это не репозиторий с кодом, а обсуждение/анонс видео-серии — ничего не
  подключено как submodule, только описано здесь

### Ключевая находка

Автор в комментариях подтвердил: показанная в видео машина — это сборка
на базе **DonkeyCar** (http://www.donkeycar.com), известной open-source
платформы "hardware+software" для автономных RC-машин на Raspberry Pi.

### Рекомендация на будущее (не сделано в этом репозитории, требует решения)

DonkeyCar — активно поддерживаемый проект (MIT License,
https://github.com/autorope/donkeycar, тысячи звёзд на GitHub) и решает
ровно ту же задачу, что и этот проект: автономное вождение RC-машины по
камере на Raspberry Pi. **Обновление (проверено по регламенту, см.
`docs/regulation-summary.md`): Pro-версия правил FIRA явно разрешает
использовать готовые платформы целиком** (запрет действует только в
Youth-категории) — значит юридических препятствий к использованию
DonkeyCar нет, если проект остаётся в Pro. Прежде чем продолжать писать
`lane_detection_node.py` с нуля, имеет смысл оценить, не закрывает ли
DonkeyCar большую часть задачи "из коробки" (у него есть готовый
веб-интерфейс для сбора данных, обучение behavioral-cloning моделей
вождения, поддержка серво+ESC через PCA9685).
Если решите его использовать — это добавление нового источника, о котором
стоит отдельно договориться с точки зрения архитектуры (ROS 2 стек уже
написан в этом репозитории, DonkeyCar не является ROS-пакетом, а
самостоятельным фреймворком — интеграция потребует выбора одного из двух
подходов, а не смешивания).

---

<a id="english"></a>
## English

<div align="center">

**English** • [Русский](#внешние-источники-атрибуция-и-выжимка)

</div>

This file is a detailed extract of every external source used or studied in
this project: who the author is, what's inside, what license applies, and
what's actually reusable going forward. It supplements the table in
[README_EN.md](README_EN.md) with deeper content.

General rule for everything below: third-party repository code is **not
copied** line-for-line into this repository (except where explicitly noted
and license-permitted) — wherever possible it's attached as a git submodule
(`external/`), preserving the original's history and authorship. Where that
isn't possible (no license) or doesn't apply (not a GitHub repo, e.g. the
Reddit thread), the material is described in our own words with a link to
the original.

### Summary table

| # | Source | Author(s) | License | Attached as |
|---|---|---|---|---|
| 1 | [Pandas-Team AVIS engine code](https://github.com/Pandas-Team/Autonomous-Car-Simulation-Based-on-AVIS-Engine-FIRA-2021) | Omid Omidi, Milad Soltany, Amirhossein Kazerooni, Amirhossein Heydarian, Aida Mohammadshahi (transport layer: Amirmohammad Zarif) | GPL-3.0 | git submodule |
| 2 | [FIRA official simulator](https://github.com/Fira-Autonomous-Cars/FIRA-Autonomous-Cars-Simulator) | FIRA Autonomous Cars org (ROS Noetic update by Sina Moghimi) | CC0-1.0 | git submodule |
| 3 | [COONEO ROS car](https://github.com/COONEO/Arduino_Raspberry_ROS_Car) | COONEO (WeChat/Zhihu "Neor"/Bilibili) | unspecified | git submodule, read-only reference |
| 4 | [tommybee456/ESP32-Car-Project](https://github.com/tommybee456/ESP32-Car-Project) | TommyB | unspecified | described only, not attached |
| 5 | [NITROUS RC car model](https://www.printables.com/model/415497-3d-printed-rc-car) | TommyB | CC0-1.0 | files in `models/` |
| 6 | [Reddit thread](https://www.reddit.com/r/robotics/comments/alpfrj/i_controlled_a_rc_car_using_ros_and_a_raspberry/) | u/tizianofiorenzani (Tiziano Fiorenzani) | n/a (discussion) | described only |

See the Russian sections above for the full per-source breakdown (what's
inside each repo, what's already used, what's reusable going forward) — the
technical content is identical, this file was written once and the English
section intentionally points back up rather than duplicating ~250 lines of
identical technical detail twice.
