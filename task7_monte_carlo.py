"""
Завдання 7. Використання методу Монте-Карло
Симуляція кидання двох кубиків та обчислення ймовірностей сум
"""

import random
from collections import Counter


def analytical_probabilities():
    """
    Повертає аналітичні ймовірності для сум двох кубиків.
    Всього можливих комбінацій: 6 * 6 = 36
    """
    probabilities = {
        2: 1/36,   # (1,1)
        3: 2/36,   # (1,2), (2,1)
        4: 3/36,   # (1,3), (2,2), (3,1)
        5: 4/36,   # (1,4), (2,3), (3,2), (4,1)
        6: 5/36,   # (1,5), (2,4), (3,3), (4,2), (5,1)
        7: 6/36,   # (1,6), (2,5), (3,4), (4,3), (5,2), (6,1)
        8: 5/36,   # (2,6), (3,5), (4,4), (5,3), (6,2)
        9: 4/36,   # (3,6), (4,5), (5,4), (6,3)
        10: 3/36,  # (4,6), (5,5), (6,4)
        11: 2/36,  # (5,6), (6,5)
        12: 1/36   # (6,6)
    }
    return probabilities


def simulate_dice_rolls(num_simulations):
    """
    Симулює кидання двох кубиків num_simulations разів.
    
    Args:
        num_simulations: кількість кидків
        
    Returns:
        dict: словник з ймовірностями для кожної суми
    """
    sums = []
    
    # Виконуємо симуляцію
    for _ in range(num_simulations):
        dice1 = random.randint(1, 6)
        dice2 = random.randint(1, 6)
        sums.append(dice1 + dice2)
    
    # Підраховуємо частоту кожної суми
    sum_counts = Counter(sums)
    
    # Обчислюємо ймовірності
    probabilities = {}
    for sum_value in range(2, 13):
        probabilities[sum_value] = sum_counts.get(sum_value, 0) / num_simulations
    
    return probabilities, sum_counts


def print_comparison_table(monte_carlo_prob, analytical_prob, num_simulations):
    """
    Виводить таблицю порівняння результатів Монте-Карло та аналітичних розрахунків.
    """
    print(f"\n{'='*80}")
    print(f"Результати симуляції методом Монте-Карло ({num_simulations:,} кидків)")
    print(f"{'='*80}")
    print(f"{'Сума':<6} {'Монте-Карло':<15} {'Аналітична':<15} {'Різниця':<15}")
    print(f"{'-'*80}")
    
    for sum_value in range(2, 13):
        mc_prob = monte_carlo_prob[sum_value]
        an_prob = analytical_prob[sum_value]
        difference = abs(mc_prob - an_prob)
        
        print(f"{sum_value:<6} {mc_prob*100:>6.4f}% ({mc_prob:.6f})  "
              f"{an_prob*100:>6.4f}% ({an_prob:.6f})  "
              f"{difference*100:>6.4f}%")
    
    print(f"{'='*80}\n")


def save_results_to_markdown(monte_carlo_prob, analytical_prob, num_simulations, filename='task7_results.md'):
    """
    Зберігає результати у markdown файл.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("# Симуляція кидання двох кубиків методом Монте-Карло\n\n")
        f.write(f"Кількість симуляцій: **{num_simulations:,}**\n\n")
        
        f.write("## Таблиця порівняння ймовірностей\n\n")
        f.write("| Сума | Монте-Карло | Аналітична | Різниця |\n")
        f.write("|------|-------------|------------|----------|\n")
        
        for sum_value in range(2, 13):
            mc_prob = monte_carlo_prob[sum_value]
            an_prob = analytical_prob[sum_value]
            difference = abs(mc_prob - an_prob)
            
            f.write(f"| {sum_value} | {mc_prob:.5f} ({mc_prob*100:.2f}%) | "
                   f"{an_prob:.5f} ({an_prob*100:.2f}%) | "
                   f"{difference:.5f} ({difference*100:.2f}%) |\n")
        
        f.write("\n## Висновки\n\n")
        max_diff = max(abs(monte_carlo_prob[s] - analytical_prob[s]) for s in range(2, 13))
        f.write(f"- Максимальна різниця: **{max_diff*100:.4f}%**\n")
        f.write(f"- Сума 7 має найвищу ймовірність (~16.67%)\n")
        f.write(f"- Суми 2 та 12 мають найнижчу ймовірність (~2.78%)\n")
        f.write(f"- Результати Монте-Карло дуже близькі до аналітичних розрахунків\n")
    
    print(f"Результати збережено у файл: {filename}")


def main():
    """
    Головна функція програми.
    """
    # Кількість симуляцій
    num_simulations = 1_000_000
    
    print("\n" + "="*80)
    print("Симуляція кидання двох кубиків методом Монте-Карло")
    print("="*80)
    
    # Отримуємо аналітичні ймовірності
    analytical_prob = analytical_probabilities()
    
    # Виконуємо симуляцію
    print(f"\nВиконується симуляція {num_simulations:,} кидків кубиків...")
    monte_carlo_prob, sum_counts = simulate_dice_rolls(num_simulations)
    
    # Виводимо частоту появи кожної суми
    print(f"\nЧастота появи кожної суми:")
    print(f"{'-'*40}")
    for sum_value in range(2, 13):
        count = sum_counts.get(sum_value, 0)
        print(f"Сума {sum_value:2d}: {count:7,} разів")
    
    # Виводимо таблицю порівняння
    print_comparison_table(monte_carlo_prob, analytical_prob, num_simulations)

    # Зберігаємо результати у markdown файл
    save_results_to_markdown(monte_carlo_prob, analytical_prob, num_simulations)


if __name__ == "__main__":
    main()
