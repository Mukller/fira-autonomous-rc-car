# Contributing Guide

Спасибо! Прочитайте [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md).

## Setup

```bash
git clone --recurse-submodules https://github.com/Mukller/fira-autonomous-rc-car
cd fira-autonomous-rc-car
```

Репозиторий использует git submodules (`external/`) — если уже склонировали
без `--recurse-submodules`, подтяните их отдельно:

```bash
git submodule update --init --recursive
```

## Development

1. Feature-ветка на конкретную задачу из [issues](https://github.com/Mukller/fira-autonomous-rc-car/issues)
   (они же — пункты roadmap в README.md)
2. Для ROS-нод (`ros_ws/`) — Python 3, ROS 2, синтаксис проверять
   `python3 -m py_compile <файл>` перед коммитом
3. Для прошивки (`firmware/`) — Arduino IDE, пройти bring-up чеклист из
   `firmware/drive_controller/README.md` перед тестом на реальной машине
4. Commit & PR

## Testing

- Синтаксическая проверка Python-кода перед коммитом
- Тест на реальном железе — обязателен перед тем, как считать
  ROS-ноду/прошивку готовой (см. пометки "не проверено на реальном железе"
  в соответствующих файлах)
- Не удалять пометки о непроверенном коде, пока не проверено на самом деле
