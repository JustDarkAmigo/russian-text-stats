
file_path = "example_Evgeniy_Onegin.txt"

all_letters = [
    'а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 
    'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 
    'э', 'ю', 'я'
]

vowels = ['а', 'е', 'ё', 'и', 'о', 'у', 'ы', 'э', 'ю', 'я']

consonants = [
    'б', 'в', 'г', 'д', 'ж', 'з', 'й', 'к', 'л', 'м', 'н', 'п', 'р', 'с', 'т', 
    'ф', 'х', 'ц', 'ч', 'ш', 'щ',"ъ", "ь"
]
vowels_count = [0]*10
consonants_count = [0]*23
VOWELS_SET     = set(vowels)
CONSONANTS_SET = set(consonants)


def number_of_vowels(letters):
  for i in letters:
    count = len(vowels)
    while count > 0:
      if (i.lower() == vowels[count - 1]):
        vowels_count[count - 1] +=1
      count -=1


def number_of_consonants(letters):
  for i in letters:
    count = len(consonants)
    while count > 0:
      if (i.lower() == consonants[count - 1]):
        consonants_count[count - 1] +=1
      count -=1


def keep_only_russian_letters(text: str) -> str:
    """
    Оставляет только буквы русского алфавита (а–я, А–Я, ё, Ё).
    Удаляет всё остальное: пробелы, переносы строк, знаки препинания, цифры, латиницу и т.д.
    """
    allowed = set("абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
                  "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ")
    return "".join(ch for ch in text if ch in allowed)


def letter_type(ch: str) -> str:
    """'V' — гласная, 'C' — согласная, None — что-то иное."""
    ch = ch.lower()
    if ch in VOWELS_SET:
        return 'V'
    if ch in CONSONANTS_SET:
        return 'C'
    return None

def count_pairs(text: str, first: str, second: str) -> int:
    """
    Считает, сколько раз в тексте подряд идут две буквы,
    первая из которых типа `first`, вторая — типа `second`.
    first/second: 'V' (гласная) или 'C' (согласная).
    """
    types = [letter_type(ch) for ch in text]
    count = 0
    for prev, cur in zip(types, types[1:]):
        if prev == first and cur == second:
            count += 1
    return count
      
def cons_cons(text): return count_pairs(text, 'C', 'C')
def cons_vow(text):  return count_pairs(text, 'C', 'V')
def vow_cons(text):  return count_pairs(text, 'V', 'C')
def vow_vow(text):   return count_pairs(text, 'V', 'V')




# Читаем исходный текст из файла по правильному пути
with open(file_path, "r", encoding="cp1251") as file:
  ext = file.read()
  ext = keep_only_russian_letters(ext)
  number_of_vowels(ext)
  number_of_consonants(ext)
  cc = cons_cons(ext)
  cv = cons_vow(ext)
  vc = vow_cons(ext)
  vv = vow_vow(ext)

sums = 0
print("Number of vowels:")
for i in range (len(vowels)):
  print(f"{vowels[i]}: {vowels_count[i]}")
  sums += vowels_count[i]
vow_sum = sums
print(vow_sum)
print("Number of consonants:")
for i in range (len(consonants)):
  print(f"{consonants[i]}: {consonants_count[i]}")
  sums += consonants_count[i]
consonants_sum = sums - vow_sum
print(consonants_sum)
print(f"Общий объем букв: {sums } \n")

print(f"Процент гласных {vow_sum/sums*100:.2f} %")
print(f"Процент согласных {consonants_sum/sums*100:.2f} %\n")

sums_pair = cc+cv+vc+vv

print(f"Количество пар: {sums_pair}")
cc_p = cc/sums_pair*100
cv_p = cv/sums_pair*100
vc_p =vc/sums_pair*100
vv_p = vv/sums_pair*100
print(f"Процент Согл-согл: {cc_p:.2f} %")
print(f"Процент Согл-гл: {cv_p:.2f} %")
print(f"Процент гл-согл: {vc_p:.2f} %")
print(f"Процент гл-гл: {vv_p:.2f} %")

print(f"Вероятность перехода из согласной в согласную: {cc_p/(consonants_sum/sums*100)*100:.2f} %")
print(f"Вероятность перехода из согласной в гласную: {cv_p/(consonants_sum/sums*100)*100:.2f} %")
print(f"Вероятность перехода из гласной в согласную: {vc_p/(vow_sum/sums*100)*100:.2f} %")
print(f"Вероятность перехода из гласной в гласную: {vv_p/(vow_sum/sums*100)*100:.2f} %")

