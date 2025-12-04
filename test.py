import bltype

print("Модуль bltype загружен:", bltype)
print("Содержимое модуля:", dir(bltype))

# Попробуй получить доступ к классу
if hasattr(bltype, 'blType'):
    print("blType найден:", bltype.blType)
    print("Доступ к Achromatopsia:", bltype.blType.Achromatopsia)
else:
    print("blType НЕ найден в модуле!")