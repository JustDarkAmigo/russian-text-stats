import re
import random
from collections import defaultdict

def tokenize_text(text: str) -> list:
    """
    Разбивает текст на токены: слова (в нижнем регистре) и заданные знаки препинания.
    """
    # Регулярное выражение ищет слова (русские, английские) или знаки , . ? ! 
    tokens = re.findall(r'[а-яА-ЯёЁa-zA-Z]+|[.,?!]', text.lower())
    return tokens

class MarkovLanguageModel:
    def __init__(self):
        # Одномерная таблица всех слов (m токенов)
        self.unigram_counts = defaultdict(int)
        # Таблица mxm, содержащая внутри m элементов: dict[w1][w2][w3] = count
        self.transition_table = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        self.total_tokens = 0
        self.vocabulary = set()

    def train(self, text: str):
        """Проводит анализ текста и заполняет таблицы частотностей."""
        tokens = tokenize_text(text)
        self.total_tokens += len(tokens)
        
        for i in range(len(tokens)):
            current_token = tokens[i]
            
            # Заполняем глобальную вероятность (появление среди всех остальных слов)
            self.unigram_counts[current_token] += 1
            self.vocabulary.add(current_token)
            
            # Заполняем таблицу переходов для 2 предыдущих слов
            if i >= 2:
                w1 = tokens[i-2]
                w2 = tokens[i-1]
                self.transition_table[w1][w2][current_token] += 1

    def generate_text(self, start_phrase: str, length: int = 50, global_weight: float = 0.2) -> str:
        """
        Генерирует текст на основе стартовой фразы.
        global_weight - коэффициент значимости глобальной вероятности токена (от 0 до 1).
        """
        tokens = tokenize_text(start_phrase)
        if len(tokens) < 2:
            raise ValueError("Стартовая фраза должна содержать минимум 2 слова/знака.")
        
        result = tokens[:]
        vocab_list = list(self.vocabulary)
        
        # Предварительный расчет глобальных вероятностей (составляющая 1)
        global_probs = {w: self.unigram_counts[w] / self.total_tokens for w in vocab_list}
        
        for _ in range(length):
            w1, w2 = result[-2], result[-1]
            
            # Получаем локальный контекст m элементов для конкретной ячейки [w1][w2]
            local_context = self.transition_table[w1][w2]
            total_local_transitions = sum(local_context.values())
            
            next_word_probs = []
            
            for w in vocab_list:
                # 1. Вероятность появления среди всех остальных слов
                p_global = global_probs[w]
                
                # 2. Количество появлений после 2 предыдущих слов (переведенное в вероятность)
                if total_local_transitions > 0:
                    p_local = local_context.get(w, 0) / total_local_transitions
                else:
                    p_local = 0.0
                
                # Итоговая вероятность: объединение двух составляющих
                p_final = (1 - global_weight) * p_local + global_weight * p_global
                next_word_probs.append(p_final)
            
            # Выбор следующего слова на основе вектора вероятностей для всех m слов
            next_token = random.choices(vocab_list, weights=next_word_probs, k=1)[0]
            result.append(next_token)

        last_token = result[-1]
        if last_token in ['.', '?', '!']:
            pass  # оставляем как есть
        elif last_token == ',':
            result[-1] = '.'  # запятая заменяется на точку
        else:
            result.append('.')  # после слова ставим точку
        
        # Форматирование итогового текста (убираем пробелы перед знаками препинания)
        output_text = result[0].capitalize()
        for token in result[1:]:
            if token in ['.', ',', '?', '!']:
                output_text += token
            else:
                output_text += " " + token
        return output_text

# Пример использования (аналогично чтению файла в Simple_analysis.py)
if __name__ == "__main__":
    file_path = "corpus_clean.norm.txt"
    model = MarkovLanguageModel()
    
    print("Идет обучение модели...")

    # Лимит строк для обучения (200 000 строк — это примерно 15-20 МБ текста)
    LINES_LIMIT = 3000000 
    
    # Читаем файл построчно, не загружая его целиком
    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
        for i, line in enumerate(file):
            if i > LINES_LIMIT:
                break
            model.train(line)
            if i % 10000 == 0 and i > 0:
               print(f"Обработано строк: {i}...")

    print(f"Обучение завершено. Размер словаря: {len(model.vocabulary)} токенов.")
    
    # Слово "Мой" и "дядя" должны быть в прочитанном куске текста
    start_phrase = "Делу время"
    
    print("\nГенерация текста...\n")
    print(model.generate_text(start_phrase, length=50, global_weight=0.01))