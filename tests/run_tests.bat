@echo off
echo === Тест 1: запуск без параметров ===
python src\main.py

echo === Тест 2: запуск с логом ===
python src\main.py --log tests\test.log

echo === Тест 3: запуск со скриптом ===
python src\main.py --script tests\test_script.sh

echo === Тест 4: все параметры ===
python src\main.py --vfs tests\test.vfs.json ^
 --log tests\test.log ^
 --script tests\test_script.sh
