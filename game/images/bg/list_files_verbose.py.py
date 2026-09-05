import os
import sys
from pathlib import Path

def list_files(directory, output_file):
    # Преобразуем пути в абсолютные для ясности
    dir_path = Path(directory).resolve()
    out_path = Path(output_file).resolve() if output_file else Path('file_list.txt').resolve()

    # Проверяем существование исходной папки
    if not dir_path.is_dir():
        print(f"❌ Папка '{dir_path}' не существует.")
        return False

    # Проверяем, можно ли записать в целевую папку (где будет лежать output_file)
    try:
        # Попробуем создать родительские папки, если их нет
        out_path.parent.mkdir(parents=True, exist_ok=True)
        # Проверим запись, создав временный файл
        with open(out_path, 'w', encoding='utf-8') as test_f:
            test_f.write('test')
        os.remove(out_path)  # удалим тест
    except Exception as e:
        print(f"❌ Нет прав на запись в '{out_path.parent}': {e}")
        return False

    # Теперь основной обход
    try:
        with open(out_path, 'w', encoding='utf-8') as f:
            count = 0
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    full_path = Path(root) / file
                    rel_path = full_path.relative_to(dir_path)
                    f.write(str(rel_path) + '\n')
                    count += 1
        print(f"✅ Файл успешно создан: {out_path}")
        print(f"📄 Записано {count} файлов.")
        return True
    except Exception as e:
        print(f"❌ Ошибка при записи: {e}")
        return False

if __name__ == "__main__":
    # Аргументы командной строки: [папка] [выходной_файл]
    target_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    out_file   = sys.argv[2] if len(sys.argv) > 2 else "file_list.txt"

    print(f"🔍 Сканируем: {os.path.abspath(target_dir)}")
    print(f"📝 Сохраняем в: {os.path.abspath(out_file)}")

    if list_files(target_dir, out_file):
        print("✔ Готово.")
    else:
        print("✖ Не удалось создать список файлов.")