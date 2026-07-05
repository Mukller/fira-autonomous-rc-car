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
- https://firaworldcup.org/leagues/fira-challenges/autonomous-cars-simulation-u19-pro/
- https://acc.firaworldcup.org/
- http://www.pmm.edu.my/pusatdata/zxc/2025/fira25/rule/simursof/Autonomous_Racing_Car_Challenge_2025.pdf (правила физического дивизиона, 2025)

Этот проект нацелен на **Physical Division** (1:10 RC-машина).

## Структура репозитория

```
models/     — 3D-модель шасси (STL/3MF) для печати
external/   — референсные проекты, подключены как git submodules (см. ниже)
docs/       — заметки по интеграции, план работ
```

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

## Roadmap

- [ ] Изучить полный регламент Physical Division 2025/2026 (PDF выше)
- [ ] Подобрать электронную начинку (Raspberry Pi/Arduino, серво, ESC, камера/лидар)
      под геометрию модели NITROUS
- [ ] Портировать/адаптировать ROS-ноды из `arduino-raspberry-ros-car` под своё железо
- [ ] Адаптировать алгоритмы детекции полос/знаков из `pandas-team-avis-engine`
      под реальную камеру (а не симулятор)
- [ ] Настроить сборку/прошивку Arduino для управления рулём и скоростью
- [ ] Собрать и протестировать физическое шасси по модели из `models/`
- [ ] Провести первый заезд на тестовой трассе
- [ ] Подготовить документацию/видео для подачи на соревнование

## Лицензия собственного кода

Код и документация, написанные в рамках этого репозитория (вне `external/` и `models/`),
распространяются по лицензии MIT (см. [LICENSE](LICENSE)), если не указано иное.
