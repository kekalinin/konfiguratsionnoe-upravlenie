@echo off
echo === Тест: команды mv и cp ===
python src\main.py --vfs tests\nested.vfs.json --script tests\test_stage5.sh --log tests\stage5.log
