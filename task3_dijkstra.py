"""
Завдання 3. Алгоритм Дейкстри для знаходження найкоротших шляхів у зваженому графі
Використовується бінарна купа (heapq) для оптимізації
"""

import heapq
from typing import Dict, List, Tuple, Optional


class Graph:
    """Клас для представлення зваженого графа"""
    
    def __init__(self):
        self.vertices: Dict[str, List[Tuple[str, int]]] = {}
    
    def add_vertex(self, vertex: str):
        """Додає вершину до графа"""
        if vertex not in self.vertices:
            self.vertices[vertex] = []
    
    def add_edge(self, from_vertex: str, to_vertex: str, weight: int):
        """
        Додає ребро між вершинами з вагою
        
        Args:
            from_vertex: Початкова вершина
            to_vertex: Кінцева вершина
            weight: Вага ребра
        """
        # Додаємо вершини, якщо їх ще немає
        self.add_vertex(from_vertex)
        self.add_vertex(to_vertex)
        
        # Додаємо ребро (для неорієнтованого графа додаємо в обидві сторони)
        self.vertices[from_vertex].append((to_vertex, weight))
        self.vertices[to_vertex].append((from_vertex, weight))
    
    def dijkstra(self, start_vertex: str) -> Dict[str, Tuple[int, Optional[str]]]:
        """
        Алгоритм Дейкстри для знаходження найкоротших шляхів
        
        Args:
            start_vertex: Початкова вершина
        
        Returns:
            Словник з найкоротшими відстанями та попередніми вершинами
            Формат: {вершина: (відстань, попередня_вершина)}
        """
        # Ініціалізація відстаней та попередніх вершин
        distances = {vertex: float('infinity') for vertex in self.vertices}
        distances[start_vertex] = 0
        previous = {vertex: None for vertex in self.vertices}
        
        # Бінарна купа для оптимізації вибору вершини з мінімальною відстанню
        # Формат: (відстань, вершина)
        priority_queue = [(0, start_vertex)]
        
        # Множина відвіданих вершин
        visited = set()
        
        while priority_queue:
            # Витягуємо вершину з мінімальною відстанню
            current_distance, current_vertex = heapq.heappop(priority_queue)
            
            # Якщо вершина вже відвідана, пропускаємо
            if current_vertex in visited:
                continue
            
            visited.add(current_vertex)
            
            # Якщо поточна відстань більша за збережену, пропускаємо
            if current_distance > distances[current_vertex]:
                continue
            
            # Перевіряємо всіх сусідів
            for neighbor, weight in self.vertices[current_vertex]:
                if neighbor in visited:
                    continue
                
                # Обчислюємо нову відстань
                new_distance = current_distance + weight
                
                # Якщо знайшли коротший шлях, оновлюємо
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (new_distance, neighbor))
        
        return {vertex: (distances[vertex], previous[vertex]) 
                for vertex in self.vertices}
    
    def get_shortest_path(self, start_vertex: str, end_vertex: str) -> Tuple[List[str], int]:
        """
        Знаходить найкоротший шлях між двома вершинами
        
        Args:
            start_vertex: Початкова вершина
            end_vertex: Кінцева вершина
        
        Returns:
            Кортеж (шлях, відстань)
        """
        result = self.dijkstra(start_vertex)
        
        # Відновлюємо шлях
        path = []
        current = end_vertex
        
        while current is not None:
            path.append(current)
            current = result[current][1]
        
        path.reverse()
        
        # Перевіряємо, чи існує шлях
        if path[0] != start_vertex:
            return [], float('infinity')
        
        distance = result[end_vertex][0]
        return path, distance
    
    def print_shortest_paths(self, start_vertex: str):
        """
        Виводить найкоротші шляхи від початкової вершини до всіх інших
        
        Args:
            start_vertex: Початкова вершина
        """
        result = self.dijkstra(start_vertex)
        
        print(f"\nНайкоротші шляхи від вершини '{start_vertex}':")
        print("=" * 60)
        
        for vertex in sorted(result.keys()):
            distance, _ = result[vertex]
            
            if distance == float('infinity'):
                print(f"До вершини {vertex}: недосяжна")
            elif vertex == start_vertex:
                print(f"До вершини {vertex}: 0 (початкова вершина)")
            else:
                path, _ = self.get_shortest_path(start_vertex, vertex)
                path_str = " → ".join(path)
                print(f"До вершини {vertex}: {distance} (шлях: {path_str})")


def create_example_graph() -> Graph:
    """Створює приклад графа для демонстрації"""
    graph = Graph()
    
    # Додаємо ребра з вагами
    edges = [
        ("A", "B", 4),
        ("A", "C", 2),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 8),
        ("C", "E", 10),
        ("D", "E", 2),
        ("D", "F", 6),
        ("E", "F", 3)
    ]
    
    for from_v, to_v, weight in edges:
        graph.add_edge(from_v, to_v, weight)
    
    return graph


def visualize_graph(graph: Graph):
    """Виводить структуру графа"""
    print("\nСтруктура графа:")
    print("=" * 60)
    for vertex in sorted(graph.vertices.keys()):
        neighbors = ", ".join([f"{n}(вага:{w})" for n, w in sorted(graph.vertices[vertex])])
        print(f"Вершина {vertex}: {neighbors}")


def main():
    """Головна функція для демонстрації алгоритму Дейкстри"""
    print("=" * 60)
    print("Алгоритм Дейкстри для знаходження найкоротших шляхів")
    print("=" * 60)
    
    # Створюємо граф
    graph = create_example_graph()
    
    # Виводимо структуру графа
    visualize_graph(graph)
    
    # Знаходимо найкоротші шляхи від вершини A
    start_vertex = "A"
    graph.print_shortest_paths(start_vertex)
    
    # Приклади знаходження конкретних шляхів
    print("\n" + "=" * 60)
    print("Приклади конкретних шляхів:")
    print("=" * 60)
    
    paths_to_find = [("A", "F"), ("A", "E"), ("B", "F")]
    
    for start, end in paths_to_find:
        path, distance = graph.get_shortest_path(start, end)
        if path:
            path_str = " → ".join(path)
            print(f"\nВід {start} до {end}:")
            print(f"  Шлях: {path_str}")
            print(f"  Відстань: {distance}")
        else:
            print(f"\nВід {start} до {end}: шлях не знайдено")
    
    # Демонстрація з іншою початковою вершиною
    print("\n" + "=" * 60)
    start_vertex = "D"
    graph.print_shortest_paths(start_vertex)


if __name__ == "__main__":
    main()
