"""
Задача вибору їжі з найбільшою калорійністю в межах бюджету.
Реалізовано два підходи: жадібний алгоритм та динамічне програмування.
"""

def greedy_algorithm(items, budget):
    """
    Жадібний алгоритм для вибору страв з максимальною калорійністю.
    
    Алгоритм сортує страви за співвідношенням калорій до вартості
    і вибирає їх у порядку спадання цього співвідношення.
    
    Args:
        items: словник з стравами {назва: {"cost": вартість, "calories": калорії}}
        budget: доступний бюджет
    
    Returns:
        tuple: (список обраних страв, загальна вартість, загальні калорії)
    """
    # Обчислюємо співвідношення калорій до вартості для кожної страви
    items_ratio = []
    for name, data in items.items():
        ratio = data["calories"] / data["cost"]
        items_ratio.append((name, data["cost"], data["calories"], ratio))
    
    # Сортуємо страви за співвідношенням у спадному порядку
    items_ratio.sort(key=lambda x: x[3], reverse=True)
    
    selected_items = []
    total_cost = 0
    total_calories = 0
    
    # Жадібно вибираємо страви
    for name, cost, calories, ratio in items_ratio:
        if total_cost + cost <= budget:
            selected_items.append(name)
            total_cost += cost
            total_calories += calories
    
    return selected_items, total_cost, total_calories


def dynamic_programming(items, budget):
    """
    Алгоритм динамічного програмування для вибору оптимального набору страв.
    
    Використовує підхід задачі про рюкзак (knapsack problem) для знаходження
    оптимального розв'язку, який максимізує калорійність при заданому бюджеті.
    
    Args:
        items: словник з стравами {назва: {"cost": вартість, "calories": калорії}}
        budget: доступний бюджет
    
    Returns:
        tuple: (список обраних страв, загальна вартість, загальні калорії)
    """
    # Перетворюємо словник у список для зручності індексації
    items_list = list(items.items())
    n = len(items_list)
    
    # Створюємо таблицю DP: dp[i][w] - максимальні калорії для перших i страв з бюджетом w
    dp = [[0 for _ in range(budget + 1)] for _ in range(n + 1)]
    
    # Заповнюємо таблицю DP
    for i in range(1, n + 1):
        name, data = items_list[i - 1]
        cost = data["cost"]
        calories = data["calories"]
        
        for w in range(budget + 1):
            # Не беремо поточну страву
            dp[i][w] = dp[i - 1][w]
            
            # Беремо поточну страву, якщо вона поміщається в бюджет
            if cost <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - cost] + calories)
    
    # Відновлюємо набір обраних страв
    selected_items = []
    w = budget
    total_calories = dp[n][budget]
    
    for i in range(n, 0, -1):
        # Якщо значення змінилось, значить ми взяли цю страву
        if dp[i][w] != dp[i - 1][w]:
            name, data = items_list[i - 1]
            selected_items.append(name)
            w -= data["cost"]
    
    selected_items.reverse()
    
    # Обчислюємо загальну вартість
    total_cost = sum(items[name]["cost"] for name in selected_items)
    
    return selected_items, total_cost, total_calories


def main():
    """Головна функція для демонстрації роботи алгоритмів."""
    
    # Дані про страви
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350}
    }
    
    budget = 100
    
    print("=" * 70)
    print(f"Задача вибору їжі з максимальною калорійністю при бюджеті {budget}")
    print("=" * 70)
    print("\nДоступні страви:")
    print(f"{'Страва':<15} {'Вартість':>10} {'Калорії':>10} {'Співвідношення':>15}")
    print("-" * 70)
    
    for name, data in items.items():
        ratio = data["calories"] / data["cost"]
        print(f"{name:<15} {data['cost']:>10} {data['calories']:>10} {ratio:>15.2f}")
    
    # Жадібний алгоритм
    print("\n" + "=" * 70)
    print("ЖАДІБНИЙ АЛГОРИТМ")
    print("=" * 70)
    
    greedy_items, greedy_cost, greedy_calories = greedy_algorithm(items, budget)
    
    print(f"\nОбрані страви: {', '.join(greedy_items)}")
    print(f"Загальна вартість: {greedy_cost}")
    print(f"Загальна калорійність: {greedy_calories}")
    
    # Динамічне програмування
    print("\n" + "=" * 70)
    print("ДИНАМІЧНЕ ПРОГРАМУВАННЯ")
    print("=" * 70)
    
    dp_items, dp_cost, dp_calories = dynamic_programming(items, budget)
    
    print(f"\nОбрані страви: {', '.join(dp_items)}")
    print(f"Загальна вартість: {dp_cost}")
    print(f"Загальна калорійність: {dp_calories}")
    
    # Порівняння результатів
    print("\n" + "=" * 70)
    print("ПОРІВНЯННЯ РЕЗУЛЬТАТІВ")
    print("=" * 70)
    
    print(f"\nЖадібний алгоритм:")
    print(f"  Калорії: {greedy_calories}, Вартість: {greedy_cost}")
    print(f"  Ефективність: {greedy_calories / greedy_cost:.2f} калорій на одиницю вартості")
    
    print(f"\nДинамічне програмування:")
    print(f"  Калорії: {dp_calories}, Вартість: {dp_cost}")
    print(f"  Ефективність: {dp_calories / dp_cost:.2f} калорій на одиницю вартості")
    
    difference = dp_calories - greedy_calories
    if difference > 0:
        print(f"\nДинамічне програмування дало на {difference} калорій більше!")
    elif difference < 0:
        print(f"\nЖадібний алгоритм дав на {abs(difference)} калорій більше!")
    else:
        print(f"\nОбидва алгоритми дали однаковий результат!")
    
    print("\n" + "=" * 70)
    
    # Додатковий приклад з іншим бюджетом
    print("\n\nДодатковий приклад з бюджетом 50:")
    print("=" * 70)
    
    budget2 = 50
    greedy_items2, greedy_cost2, greedy_calories2 = greedy_algorithm(items, budget2)
    dp_items2, dp_cost2, dp_calories2 = dynamic_programming(items, budget2)
    
    print(f"\nЖадібний алгоритм (бюджет {budget2}):")
    print(f"  Страви: {', '.join(greedy_items2)}")
    print(f"  Калорії: {greedy_calories2}, Вартість: {greedy_cost2}")
    
    print(f"\nДинамічне програмування (бюджет {budget2}):")
    print(f"  Страви: {', '.join(dp_items2)}")
    print(f"  Калорії: {dp_calories2}, Вартість: {dp_cost2}")


if __name__ == "__main__":
    main()
