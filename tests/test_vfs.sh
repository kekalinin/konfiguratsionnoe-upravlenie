# Тестирование работы с VFS
# Проверяет ls, cd, обработку ошибок

ls
cd home
ls
cd user
ls
cd documents
ls
# Попытка перейти в несуществующую папку
cd nonexistent
# Возврат на уровень вверх
cd ..
ls
# Переход в корень
cd /
ls
# Проверка conf-dump
conf-dump
# Неизвестная команда
unknown_cmd
exit
