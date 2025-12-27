"""
Завдання 4. Візуалізація бінарної купи
Побудова та візуалізація бінарної купи (heap) у вигляді дерева
"""

import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # Додатковий аргумент для зберігання кольору вузла
        self.id = str(uuid.uuid4())  # Унікальний ідентифікатор для кожного вузла


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """Рекурсивно додає ребра та позиції вузлів до графа"""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            l = add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            r = add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, title="Binary Heap Visualization"):
    """Візуалізує дерево"""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(12, 8))
    nx.draw(tree, pos=pos, labels=labels, arrows=False, 
            node_size=2500, node_color=colors, font_size=10, font_weight='bold')
    plt.title(title, fontsize=16, fontweight='bold')
    plt.show()


def heap_to_tree(heap_array, index=0):
    """
    Конвертує масив купи у бінарне дерево
    
    Args:
        heap_array: Масив, що представляє купу
        index: Поточний індекс у масиві
    
    Returns:
        Node: Корінь дерева
    """
    if index >= len(heap_array):
        return None
    
    # Створюємо вузол для поточного елемента
    node = Node(heap_array[index])
    
    # Індекси лівого та правого нащадків у масиві купи
    left_index = 2 * index + 1
    right_index = 2 * index + 2
    
    # Рекурсивно створюємо ліве та праве піддерева
    node.left = heap_to_tree(heap_array, left_index)
    node.right = heap_to_tree(heap_array, right_index)
    
    return node


def visualize_heap(heap_array, title="Binary Heap"):
    """
    Візуалізує бінарну купу
    
    Args:
        heap_array: Масив, що представляє купу
        title: Заголовок візуалізації
    """
    if not heap_array:
        print("Купа порожня!")
        return
    
    # Конвертуємо купу у дерево
    root = heap_to_tree(heap_array)
    
    # Візуалізуємо дерево
    draw_tree(root, title)


def create_min_heap(elements):
    """
    Створює мін-купу з елементів
    
    Args:
        elements: Список елементів
    
    Returns:
        list: Масив мін-купи
    """
    heap = elements.copy()
    heapq.heapify(heap)
    return heap


def create_max_heap(elements):
    """
    Створює макс-купу з елементів
    (Python heapq підтримує лише мін-купу, тому інвертуємо значення)
    
    Args:
        elements: Список елементів
    
    Returns:
        list: Масив макс-купи
    """
    # Інвертуємо значення для створення макс-купи
    inverted = [-x for x in elements]
    heapq.heapify(inverted)
    # Повертаємо назад оригінальні значення
    return [-x for x in inverted]


def demonstrate_heap_operations():
    """Демонструє операції з купою та їх візуалізацію"""
    print("=" * 60)
    print("Демонстрація візуалізації бінарної купи")
    print("=" * 60)
    
    # Приклад 1: Мін-купа
    print("\n1. Створення мін-купи")
    elements = [4, 10, 3, 5, 1, 8, 9, 2, 6, 7]
    print(f"   Вхідні дані: {elements}")
    
    min_heap = create_min_heap(elements)
    print(f"   Мін-купа: {min_heap}")
    visualize_heap(min_heap, "Min Heap (Мін-купа)")
    
    # Приклад 2: Макс-купа
    print("\n2. Створення макс-купи")
    print(f"   Вхідні дані: {elements}")
    
    max_heap = create_max_heap(elements)
    print(f"   Макс-купа: {max_heap}")
    visualize_heap(max_heap, "Max Heap (Макс-купа)")
    
    # Приклад 3: Послідовне додавання елементів
    print("\n3. Побудова купи з послідовним додаванням")
    heap = []
    values = [15, 10, 20, 8, 21, 5, 30]
    
    for val in values:
        heapq.heappush(heap, val)
        print(f"   Додано {val}: {heap}")
    
    visualize_heap(heap, "Heap after sequential insertion")
    
    # Приклад 4: Видалення елементів
    print("\n4. Видалення мінімального елемента")
    heap_copy = heap.copy()
    min_element = heapq.heappop(heap_copy)
    print(f"   Видалено мінімум: {min_element}")
    print(f"   Купа після видалення: {heap_copy}")
    visualize_heap(heap_copy, "Heap after removing minimum")
    
    # Приклад 5: Купа з більшої кількості елементів
    print("\n5. Візуалізація більшої купи")
    large_elements = list(range(1, 16))  # 1-15
    import random
    random.shuffle(large_elements)
    print(f"   Вхідні дані: {large_elements}")
    
    large_heap = create_min_heap(large_elements)
    print(f"   Мін-купа: {large_heap}")
    visualize_heap(large_heap, "Large Min Heap (15 elements)")


def custom_heap_example():
    """Приклад створення користувацької купи"""
    print("\n" + "=" * 60)
    print("Користувацький приклад")
    print("=" * 60)
    
    # Створення купи з конкретних значень
    custom_values = [50, 30, 20, 15, 10, 8, 16]
    print(f"Значення: {custom_values}")
    
    visualize_heap(custom_values, "Custom Heap Structure")


def main():
    """Головна функція"""
    demonstrate_heap_operations()
    custom_heap_example()
    
    print("\n" + "=" * 60)
    print("Візуалізація завершена!")
    print("=" * 60)


if __name__ == "__main__":
    main()
