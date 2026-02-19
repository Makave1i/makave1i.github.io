import json
import os

def get_unit_class(armor, range):
    """Визначає клас юніта на основі броні"""
    if armor >= 45:
        return "tank"
    elif armor >= 25:
        return "med"
    else:
        if range >= 3:
            return "ranged"
        return "dps"

def compile_simulation_data(units_dir, output_file):
    compiled_units = []

    if not os.path.exists(units_dir):
        print(f"Помилка: Папка '{units_dir}' не знайдена.")
        return

    for filename in sorted(os.listdir(units_dir)):
        if filename.endswith(".json"):
            file_path = os.path.join(units_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 1. Витягуємо статки для зручності
                    stats = data.get('stats', {})
                    armor_val = stats.get('armor', 0)
                    
                    # 2. Формуємо новий об'єкт
                    unit_id = data.get('id', filename.replace('.json', ''))
                    
                    # Беремо перший скіл як основний
                    skills = data.get('skills', [])
                    primary_skill = skills[0] if skills else None
                    isRanged = primary_skill.get('range', 0) >= 3 if primary_skill else False
                    new_unit = {
                        "id": unit_id,
                        "label": data.get('unitName') or data.get('name') or unit_id.capitalize(),
                        "class": get_unit_class(armor_val, primary_skill.get('range', 0) if primary_skill else 0),
                        "stats": {
                            "hp": stats.get('hp'),
                            "stamina": stats.get('stamina'),
                            "speed": stats.get('speed'),
                            "armor": armor_val,
                            "evasion": stats.get('evasion'),
                            "meleeSkill": stats.get('meleeSkill') if not isRanged else stats.get('rangedSkill'),
                            "initiative": stats.get('initiative'),
                            "critChance": stats.get('critChance'),
                            "critMult": stats.get('critMult'),
                            "damageMin": stats.get('damageMin'),
                            "damageMax": stats.get('damageMax')
                        },
                        "primarySkill": primary_skill
                    }
                    
                    compiled_units.append(new_unit)
                    print(f"Оброблено: {new_unit['label']} ({new_unit['class']})")

            except Exception as e:
                print(f"Помилка у файлі {filename}: {e}")

    # Зберігаємо результат
    with open(output_file, 'w', encoding='utf-8') as f:
        # Використовуємо indent=2 для читабельності, 
        # або indent=None якщо треба максимально компактно
        json.dump(compiled_units, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ База для симуляції згенерована: {output_file}")

if __name__ == "__main__":
    compile_simulation_data(
        units_dir='units', 
        output_file='sim_database.json'
    )


# import json
# import os

# def compile_simulation_data(units_dir, output_file):
#     compiled_units = []

#     if not os.path.exists(units_dir):
#         print(f"Помилка: Папка '{units_dir}' не знайдена.")
#         return

#     # Список полів, які ми хочемо ігнорувати для симуляції
#     FIELDS_TO_REMOVE = ['hitArea', 'anchor']

#     for filename in os.listdir(units_dir):
#         if filename.endswith(".json"):
#             file_path = os.path.join(units_dir, filename)
            
#             try:
#                 with open(file_path, 'r', encoding='utf-8') as f:
#                     unit_data = json.load(f)
                    
#                     # Видаляємо візуальні параметри
#                     for field in FIELDS_TO_REMOVE:
#                         if field in unit_data:
#                             del unit_data[field]
                    
#                     compiled_units.append(unit_data)
#                     print(f"Додано до симуляції: {unit_data.get('name', filename)}")
#             except Exception as e:
#                 print(f"Помилка у файлі {filename}: {e}")

#     # Зберігаємо чисті дані
#     result = {
#         "units": compiled_units
#     }

#     with open(output_file, 'w', encoding='utf-8') as f:
#         json.dump(result, f, ensure_ascii=False, indent=2)
    
#     print(f"\n✅ Файл для симуляції готовий! Зібрано юнітів: {len(compiled_units)}")

# if __name__ == "__main__":
#     compile_simulation_data(
#         units_dir='units', 
#         output_file='sim_database.json'
#     )
