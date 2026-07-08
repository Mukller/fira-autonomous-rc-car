<div align="center">

[English](README_EN.md) • **Русский**

</div>

# FIRA Autonomous RC Car

Проект автономного RC-автомобиля масштаба 1:10 для физического дивизиона
**FIRA Autonomous Cars League (FACL)** / RoboCup Autonomous Cars.
Собирает воедино 3D-модель шасси, референсный код автономного вождения
из симуляционных проектов FIRA и open-source ROS-стек для Raspberry Pi + Arduino.

Статус: в разработке. Это не готовый продукт — репозиторий последовательно
собирает и интегрирует компоненты, начиная с июля 2026.

## Регламент соревнования

FIRA Autonomous Cars League состоит из двух дивизионов:

- **Physical Division** — команды проектируют, строят и программируют
  автономный RC-автомобиль масштаба 1:10 с рулевым управлением Ackermann,
  который должен проехать трассу без вмешательства человека.
- **Simulation Division** — разработка ПО/AI для автономного вождения
  в симуляторе **AVIS Engine** (на основе ROS + Gazebo).

Официальные источники регламента (сверяться перед соревнованием — правила
обновляются по годам):

- https://firaworldcup.org/leagues/fira-challenges/autonomous-cars/
- Правила Pro (Google Docs, актуальная версия): https://docs.google.com/document/d/1PgeKrsCEL-KnZFci-iQUgFKoVnY7qiXql9oOvQACfEY/
- Правила Youth: https://docs.google.com/document/d/1pyhgvSQw7eaGDG0dzchA0VkbOYnGsd1_AVNhvs1iz8c/

Своими словами пересказанная сводка ключевых требований (масштаб 1:10,
лимит 600×450мм, Ackermann steering, множитель за onboard/offboard обработку)
— в [`docs/regulation-summary.md`](docs/regulation-summary.md).

Этот проект нацелен на **Physical Division** (1:10 RC-машина).

## Структура репозитория

```
models/     — 3D-модель шасси (STL/3MF) для печати
external/   — референсные проекты, подключены как git submodules (см. ниже)
docs/       — регламент, электронная схема, план адаптации алгоритмов
ros_ws/     — ROS 2 пакет fira_car_control: ноды детекции полосы, руля,
              скорости и serial-моста к микроконтроллеру
firmware/   — прошивка микроконтроллера привода (серво + DC-мотор)
tools/      — STL bbox, калибровка камеры, калибровка HSV
```

## Документация

- [`docs/regulation-summary.md`](docs/regulation-summary.md) — сводка регламента
- [`docs/electronics-bom.md`](docs/electronics-bom.md) — электронная схема, BOM,
  реальные размеры деталей (посчитаны из STL скриптом `tools/stl_bbox.py`)
- [`docs/lane-detection-adaptation.md`](docs/lane-detection-adaptation.md) —
  план адаптации алгоритма детекции полосы из симулятора под реальную камеру

## Используемые внешние материалы (атрибуция)

### 3D-модель шасси

**NITROUS — 3D Printed RC Car** by **TommyB**
- Источник: https://www.printables.com/model/415497-3d-printed-rc-car
- Лицензия: Creative Commons CC0 1.0 (Public Domain) — автор пометил модель
  как оригинальную работу, атрибуция не обязательна юридически, но указана
  здесь из уважения к автору.
- Файлы лежат в [`models/`](models/), без изменений относительно оригинала.

### Референсный код (git submodules)

Код из внешних репозиториев **не скопирован**, а подключён как git submodule —
это сохраняет полную историю, авторство и лицензию оригинала.

| Путь | Источник | Лицензия | Назначение |
|---|---|---|---|
| `external/pandas-team-avis-engine` | [Pandas-Team/Autonomous-Car-Simulation-Based-on-AVIS-Engine-FIRA-2021](https://github.com/Pandas-Team/Autonomous-Car-Simulation-Based-on-AVIS-Engine-FIRA-2021) | GPL-3.0 | Детекция полос/знаков, PID-управление — референс для simulation-алгоритмов |
| `external/fira-autonomous-cars-simulator` | [Fira-Autonomous-Cars/FIRA-Autonomous-Cars-Simulator](https://github.com/Fira-Autonomous-Cars/FIRA-Autonomous-Cars-Simulator) | CC0-1.0 | Официальный симулятор FIRA |
| `external/arduino-raspberry-ros-car` | [COONEO/Arduino_Raspberry_ROS_Car](https://github.com/COONEO/Arduino_Raspberry_ROS_Car) | не указана (все права у автора) | Референс ROS-стека Raspberry Pi + Arduino для физической машины |

Код из репозитория `COONEO/Arduino_Raspberry_ROS_Car` не имеет открытой лицензии —
используется только как справочный материал/submodule для чтения, без копирования
кода в собственные файлы этого репозитория.

### Дополнительные материалы для изучения

- Обсуждение управления RC-машиной через ROS + Raspberry Pi:
  https://www.reddit.com/r/robotics/comments/alpfrj/i_controlled_a_rc_car_using_ros_and_a_raspberry/

Полная выжимка по каждому источнику (авторы, лицензии, архитектура, что
именно можно переиспользовать) — в [`EXTERNAL_SOURCES.md`](EXTERNAL_SOURCES.md).

## Roadmap

- [x] Изучить регламент Physical Division (сводка в `docs/regulation-summary.md`,
      габариты модели проверены против лимитов — с запасом)
- [x] Разобрать электронную схему и BOM под геометрию NITROUS
      (`docs/electronics-bom.md`, размеры посчитаны из STL)
- [x] Написать план адаптации детекции полосы под реальную камеру
      (`docs/lane-detection-adaptation.md`)
- [x] Создать каркас ROS 2 нод управления рулём/скоростью (`ros_ws/`) —
      требует реальной камеры и калибровки для доводки
- [x] Написать `serial_bridge_node.py` — мост ROS-топиков к микроконтроллеру
      по UART (протокол `S<angle>`/`T<throttle>`)
- [x] Написать прошивку микроконтроллера привода
      (`firmware/drive_controller/`) — серво+мотор, safety timeout;
      не проверена на реальном железе (нет платы/H-моста в наличии)
- [x] Написать `tools/calibrate_camera.py` и `tools/calibrate_hsv.py` —
      готовы к запуску, как только появится реальная камера
- [x] Вынести чистую логику (детекция полосы, регуляторы руля/скорости) в
      `algorithms.py` и покрыть pytest-тестами (12 тестов, реально
      запускаются и проходят — единственная часть стека, которая уже
      проверена, а не просто написана)
- [ ] Закупить электронику по BOM — список позиций с поисковыми ссылками
      и ориентировочными ценами готов в [`docs/purchase-list.md`](docs/purchase-list.md),
      сама покупка/оплата — вручную
- [x] Спроектировать черновик крепления камеры —
      [`mounts/camera_mount.scad`](mounts/camera_mount.scad), размеры платы
      Camera Module 3 взяты из официального чертежа Raspberry Pi, пазы
      вместо точных отверстий на случай погрешности. **Не скомпилировано**
      (OpenSCAD не удалось установить в этом окружении) — открыть и
      проверить перед печатью
- [ ] Напечатать и подогнать крепление камеры под реальную плату
- [ ] Собрать физическое шасси по модели из `models/`
- [ ] Прогнать bring-up чеклист прошивки на реальном железе
      (`firmware/drive_controller/README.md`)
- [ ] Довести `lane_detection_node.py` на реальных кадрах с трассы
- [ ] Провести первый заезд на тестовой трассе
- [x] Проверить открытые вопросы регламента — большинство закрыто
      (см. чеклист в `docs/regulation-summary.md`): нет лимита по массе,
      ИК line-following датчики запрещены (камера обязательна), готовые
      платформы разрешены в Pro. **Открыт критический пункт**: колея
      (150–350мм) и колёсная база (200–550мм) модели NITROUS не измерены —
      есть риск, что компактная модель в них не укладывается
- [ ] Измерить колею и колёсную базу при сборке шасси, подтвердить
      соответствие регламенту (см. предупреждение в `docs/regulation-summary.md`)
- [ ] Уточнить даты этапов 2026 года ближе к сезону
- [ ] Подготовить документацию/видео для подачи на соревнование

## Лицензия собственного кода

Код и документация, написанные в рамках этого репозитория (вне `external/` и `models/`),
распространяются по лицензии MIT (см. [LICENSE.md](LICENSE.md)), если не указано иное.

## Дополнительные файлы

- [CHANGELOG.md](CHANGELOG.md) — история изменений
- [CONTRIBUTING.md](CONTRIBUTING.md) — как участвовать в разработке
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) — правила поведения в проекте
- [RELEASE_INFO.md](RELEASE_INFO.md) — статус релиза
- [EXTERNAL_SOURCES.md](EXTERNAL_SOURCES.md) — атрибуция и выжимка по всем внешним источникам
