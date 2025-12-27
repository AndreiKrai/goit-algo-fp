import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import turtle
import math


def draw_pythagoras_tree(t, branch_length, level, angle=45):
    """
    Рекурсивна функція для малювання дерева Піфагора.
    
    Параметри:
    t - об'єкт turtle
    branch_length - довжина поточної гілки
    level - рівень рекурсії (глибина)
    angle - кут нахилу гілок (за замовчуванням 45 градусів)
    """
    if level == 0:
        return
    
    # Малюємо основну гілку (квадрат)
    t.forward(branch_length)
    
    # Зберігаємо поточну позицію та напрямок
    pos = t.position()
    heading = t.heading()
    
    # Малюємо ліву гілку
    t.left(angle)
    new_length = branch_length * math.cos(math.radians(angle))
    draw_pythagoras_tree(t, new_length, level - 1, angle)
    
    # Повертаємося до збереженої позиції
    t.penup()
    t.goto(pos)
    t.setheading(heading)
    t.pendown()
    
    # Малюємо праву гілку
    t.right(angle)
    draw_pythagoras_tree(t, new_length, level - 1, angle)
    
    # Повертаємося до початкової позиції та напрямку
    t.penup()
    t.goto(pos)
    t.setheading(heading)
    t.pendown()
    
    # Повертаємося назад
    t.backward(branch_length)


def main():
    """
    Основна функція для налаштування та запуску візуалізації дерева Піфагора.
    """
    # Отримуємо рівень рекурсії від користувача
    try:
        level = int(input("Введіть рівень рекурсії (рекомендовано 5-12): "))
        if level < 0:
            print("Рівень рекурсії повинен бути невід'ємним числом!")
            return
    except ValueError:
        print("Будь ласка, введіть ціле число!")
        return
    
    # Налаштування вікна
    screen = turtle.Screen()
    screen.setup(width=1000, height=800)
    screen.bgcolor("white")
    screen.title(f"Дерево Піфагора - Рівень рекурсії: {level}")
    
    # Налаштування turtle
    t = turtle.Turtle()
    t.speed(0)  # Найшвидша швидкість
    t.color("green")
    t.pensize(2)
    
    # Переміщуємо turtle в початкову позицію
    t.penup()
    t.goto(0, -300)
    t.setheading(90)  # Напрямок вгору
    t.pendown()
    
    # Малюємо дерево Піфагора
    initial_length = 100
    draw_pythagoras_tree(t, initial_length, level)
    
    # Ховаємо курсор
    t.hideturtle()
    
    # Виводимо інформацію
    t.penup()
    t.goto(0, 350)
    t.color("black")
    t.write(f"Дерево Піфагора (рівень: {level})", 
            align="center", font=("Arial", 16, "bold"))
    
    print(f"\nДерево Піфагора з рівнем рекурсії {level} намальовано!")
    print("Закрийте вікно, щоб завершити програму.")
    
    # Тримаємо вікно відкритим
    screen.mainloop()


if __name__ == "__main__":
    main()
