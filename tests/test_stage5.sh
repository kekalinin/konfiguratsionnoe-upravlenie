# Тестирование команд для Этапа 5
# Проверяет mv, cp и обработку ошибок

# 1. Переход в папку с файлами
cd home/user/documents
ls

# 2. Копирование файла
cp report.txt report_copy.txt
ls

# 3. Переименование файла
mv report_copy.txt report_backup.txt
ls

# 4. Перемещение файла в другую папку
mv report_backup.txt ../report_backup.txt
ls
cd ..
ls

# 5. Копирование папки (если поддерживается)
# cp documents documents_backup

# 6. Обработка ошибок: файл не найден
mv nonexistent.txt backup.txt

# 7. Обработка ошибок: неверное количество аргументов
mv report.txt

# 8. Возврат в корень и завершение
cd /
conf-dump
exit
