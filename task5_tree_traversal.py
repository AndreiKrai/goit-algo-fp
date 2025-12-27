"""
Завдання 5. Візуалізація обходу бінарного дерева
Візуалізація обходів дерева: у глибину (DFS) та в ширину (BFS)
з використанням стеку та черги (БЕЗ рекурсії)
"""

import uuid
import heapq
import networkx as nx
import matplotlib.pyplot as plt
from collections import deque


class Node:
    def __init__(self, key, color="#000000"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color
        self.id = str(uuid.uuid4())


def generate_color_gradient(step, total_steps):
    """
    Генерує колір у градієнті від темного до світлого
    
    Args:
        step: Поточний крок обходу (0-based)
        total_steps: Загальна кількість кроків
    
    Returns:
        str: Колір у форматі #RRGGBB
    """
    # Інтенсивність від темного (0x10) до світлого (0xFF)
    intensity = int(0x10 + (0xFF - 0x10) * (step / max(total_steps - 1, 1)))
    
    # Створюємо відтінок синього (можна змінити на інші кольори)
    # Формат: темно-синій -> світло-синій
    r = intensity // 3  # Червона компонента
    g = intensity // 2  # Зелена компонента
    b = intensity       # Синя компонента (основна)
    
    return f"#{r:02x}{g:02x}{b:02x}"


def depth_first_search(root):
    """
    Обхід дерева у глибину (DFS) з використанням стеку
    
    Args:
        root: Корінь дерева
    
    Returns:
        list: Список вузлів у порядку обходу
    """
    if not root:
        return []
    
    visited = []
    stack = [root]  # Використовуємо список як стек
    
    while stack:
        # Витягуємо вузол зі стеку (LIFO - Last In First Out)
        node = stack.pop()
        visited.append(node)
        
        # Додаємо нащадків до стеку (правий першим, щоб лівий обробився першим)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    
    return visited


def breadth_first_search(root):
    """
    Обхід дерева в ширину (BFS) з використанням черги
    
    Args:
        root: Корінь дерева
    
    Returns:
        list: Список вузлів у порядку обходу
    """
    if not root:
        return []
    
    visited = []
    queue = deque([root])  # Використовуємо deque як чергу
    
    while queue:
        # Витягуємо вузол з черги (FIFO - First In First Out)
        node = queue.popleft()
        visited.append(node)
        
        # Додаємо нащадків до черги
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    
    return visited


def assign_colors_to_traversal(nodes):
    """
    Призначає кольори вузлам відповідно до порядку обходу
    
    Args:
        nodes: Список вузлів у порядку обходу
    """
    total_nodes = len(nodes)
    for i, node in enumerate(nodes):
        node.color = generate_color_gradient(i, total_nodes)


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    """Рекурсивно додає ребра та позиції вузлів до графа"""
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, title="Binary Tree Traversal"):
    """
    Візуалізує дерево з кольорами
    
    Args:
        tree_root: Корінь дерева
        title: Заголовок візуалізації
    """
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]['color'] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]['label'] for node in tree.nodes(data=True)}

    plt.figure(figsize=(12, 8))
    nx.draw(tree, pos=pos, labels=labels, arrows=False,
            node_size=2500, node_color=colors, font_size=10, 
            font_weight='bold', font_color='white')
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
    
    node = Node(heap_array[index])
    
    left_index = 2 * index + 1
    right_index = 2 * index + 2
    
    node.left = heap_to_tree(heap_array, left_index)
    node.right = heap_to_tree(heap_array, right_index)
    
    return node


def visualize_dfs(root):
    """
    Візуалізує обхід дерева у глибину (DFS)
    
    Args:
        root: Корінь дерева
    """
    # Виконуємо DFS обхід
    visited_nodes = depth_first_search(root)
    
    # Призначаємо кольори
    assign_colors_to_traversal(visited_nodes)
    
    # Виводимо порядок обходу
    print("\nПорядок обходу DFS (у глибину):")
    for i, node in enumerate(visited_nodes):
        print(f"  Крок {i + 1}: Вузол {node.val} -> Колір {node.color}")
    
    # Візуалізуємо дерево
    draw_tree(root, "Depth-First Search (DFS) - Обхід у глибину")


def visualize_bfs(root):
    """
    Візуалізує обхід дерева в ширину (BFS)
    
    Args:
        root: Корінь дерева
    """
    # Виконуємо BFS обхід
    visited_nodes = breadth_first_search(root)
    
    # Призначаємо кольори
    assign_colors_to_traversal(visited_nodes)
    
    # Виводимо порядок обходу
    print("\nПорядок обходу BFS (в ширину):")
    for i, node in enumerate(visited_nodes):
        print(f"  Крок {i + 1}: Вузол {node.val} -> Колір {node.color}")
    
    # Візуалізуємо дерево
    draw_tree(root, "Breadth-First Search (BFS) - Обхід в ширину")


def demonstrate_traversals():
    """Демонструє візуалізацію обходів дерева"""
    print("=" * 70)
    print("Візуалізація обходів бінарного дерева")
    print("=" * 70)
    
    # Створюємо бінарну купу для демонстрації
    elements = [10, 5, 15, 3, 7, 12, 18, 1, 4, 6, 8, 11, 13, 17, 20]
    heap = elements.copy()
    heapq.heapify(heap)
    
    print(f"\nВихідні дані (мін-купа): {heap}")
    print(f"Кількість вузлів: {len(heap)}")
    
    # Конвертуємо купу у дерево
    root = heap_to_tree(heap)
    
    # Візуалізація DFS
    print("\n" + "=" * 70)
    print("1. ОБХІД У ГЛИБИНУ (Depth-First Search - DFS)")
    print("   Використовується СТЕК")
    print("=" * 70)
    visualize_dfs(root)
    
    # Відновлюємо дерево (кольори змінились під час DFS)
    root = heap_to_tree(heap)
    
    # Візуалізація BFS
    print("\n" + "=" * 70)
    print("2. ОБХІД В ШИРИНУ (Breadth-First Search - BFS)")
    print("   Використовується ЧЕРГА")
    print("=" * 70)
    visualize_bfs(root)
    
    print("\n" + "=" * 70)
    print("Пояснення кольорів:")
    print("  • Темні відтінки - вузли, відвідані на початку")
    print("  • Світлі відтінки - вузли, відвідані наприкінці")
    print("  • Кожен вузол має унікальний колір залежно від порядку обходу")
    print("=" * 70)


if __name__ == "__main__":
    demonstrate_traversals()
