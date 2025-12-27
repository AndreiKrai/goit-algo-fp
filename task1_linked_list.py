"""
Завдання 1. Структури даних. Сортування. Робота з однозв'язним списком

Реалізація однозв'язного списку з функціями:
1. Реверсування списку
2. Сортування злиттям
3. Об'єднання двох відсортованих списків
"""


class Node:
    """Вузол однозв'язного списку"""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """Однозв'язний список"""
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        """Вставка елемента на початок списку"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        """Вставка елемента в кінець списку"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def print_list(self):
        """Виведення списку"""
        if self.head is None:
            print("Список порожній")
            return
        
        current = self.head
        elements = []
        while current:
            elements.append(str(current.data))
            current = current.next
        print(" -> ".join(elements))

    def to_list(self):
        """Перетворення зв'язного списку в звичайний список Python"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result


def reverse_linked_list(linked_list):
    """
    Реверсування однозв'язного списку шляхом зміни посилань між вузлами.
    
    Алгоритм:
    - Використовуємо три покажчики: prev, current, next
    - Перебираємо список і змінюємо напрямок кожного посилання
    - Складність: O(n) за часом, O(1) за пам'яттю
    """
    prev = None
    current = linked_list.head
    
    while current:
        # Зберігаємо посилання на наступний вузол
        next_node = current.next
        # Змінюємо напрямок посилання
        current.next = prev
        # Переміщуємо покажчики на один крок вперед
        prev = current
        current = next_node
    
    # Оновлюємо голову списку
    linked_list.head = prev
    return linked_list


def merge_sort_linked_list(linked_list):
    """
    Сортування однозв'язного списку алгоритмом злиття (merge sort).
    
    Алгоритм:
    - Рекурсивно ділимо список навпіл
    - Сортуємо кожну половину
    - Зливаємо відсортовані половини
    - Складність: O(n log n) за часом, O(log n) за пам'яттю (стек рекурсії)
    """
    if linked_list.head is None:
        return linked_list
    
    linked_list.head = _merge_sort_recursive(linked_list.head)
    return linked_list


def _merge_sort_recursive(head):
    """Рекурсивна функція сортування злиттям"""
    # Базовий випадок: список з 0 або 1 елемента вже відсортований
    if head is None or head.next is None:
        return head
    
    # Знаходимо середину списку
    middle = _get_middle(head)
    next_to_middle = middle.next
    
    # Розділяємо список на дві частини
    middle.next = None
    
    # Рекурсивно сортуємо обидві половини
    left = _merge_sort_recursive(head)
    right = _merge_sort_recursive(next_to_middle)
    
    # Зливаємо відсортовані половини
    return _merge_sorted_lists(left, right)


def _get_middle(head):
    """Знаходження середнього вузла списку (техніка двох покажчиків)"""
    if head is None:
        return head
    
    slow = head
    fast = head
    
    # fast рухається вдвічі швидше, коли він дійде до кінця,
    # slow буде посередині
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next
    
    return slow


def _merge_sorted_lists(left, right):
    """
    Допоміжна функція для злиття двох відсортованих списків.
    Використовується в merge sort.
    """
    if left is None:
        return right
    if right is None:
        return left
    
    # Вибираємо менший елемент як початок результуючого списку
    if left.data <= right.data:
        result = left
        result.next = _merge_sorted_lists(left.next, right)
    else:
        result = right
        result.next = _merge_sorted_lists(left, right.next)
    
    return result


def merge_two_sorted_lists(list1, list2):
    """
    Об'єднання двох відсортованих однозв'язних списків в один відсортований список.
    
    Алгоритм:
    - Створюємо новий список
    - Використовуємо два покажчики для обходу обох списків
    - На кожному кроці вибираємо менший елемент
    - Складність: O(n + m) за часом, O(1) за пам'яттю (окрім результату)
    """
    # Створюємо новий список для результату
    merged_list = LinkedList()
    
    # Якщо один зі списків порожній, повертаємо інший
    if list1.head is None:
        merged_list.head = list2.head
        return merged_list
    if list2.head is None:
        merged_list.head = list1.head
        return merged_list
    
    # Використовуємо допоміжну функцію для злиття
    merged_list.head = _merge_sorted_lists(list1.head, list2.head)
    
    return merged_list


def main():
    """Демонстрація роботи функцій"""
    print("=" * 60)
    print("Завдання 1: Однозв'язний список")
    print("=" * 60)
    
    # Тест 1: Реверсування списку
    print("\n1. Реверсування списку")
    print("-" * 60)
    llist = LinkedList()
    for value in [5, 3, 8, 1, 9]:
        llist.insert_at_end(value)
    
    print("Оригінальний список:")
    llist.print_list()
    
    reverse_linked_list(llist)
    print("Після реверсування:")
    llist.print_list()
    
    # Тест 2: Сортування списку
    print("\n2. Сортування списку (merge sort)")
    print("-" * 60)
    llist2 = LinkedList()
    for value in [64, 34, 25, 12, 22, 11, 90]:
        llist2.insert_at_end(value)
    
    print("Несортований список:")
    llist2.print_list()
    
    merge_sort_linked_list(llist2)
    print("Відсортований список:")
    llist2.print_list()
    
    # Тест 3: Об'єднання двох відсортованих списків
    print("\n3. Об'єднання двох відсортованих списків")
    print("-" * 60)
    
    # Створюємо перший відсортований список
    list1 = LinkedList()
    for value in [1, 3, 5, 7, 9]:
        list1.insert_at_end(value)
    print("Перший відсортований список:")
    list1.print_list()
    
    # Створюємо другий відсортований список
    list2 = LinkedList()
    for value in [2, 4, 6, 8, 10]:
        list2.insert_at_end(value)
    print("Другий відсортований список:")
    list2.print_list()
    
    # Об'єднуємо списки
    merged = merge_two_sorted_lists(list1, list2)
    print("Об'єднаний відсортований список:")
    merged.print_list()
    
    # Додатковий тест: об'єднання списків різної довжини
    print("\n4. Об'єднання списків різної довжини")
    print("-" * 60)
    
    list3 = LinkedList()
    for value in [1, 5, 10]:
        list3.insert_at_end(value)
    print("Список 1:")
    list3.print_list()
    
    list4 = LinkedList()
    for value in [2, 3, 4, 6, 7, 8, 9]:
        list4.insert_at_end(value)
    print("Список 2:")
    list4.print_list()
    
    merged2 = merge_two_sorted_lists(list3, list4)
    print("Об'єднаний список:")
    merged2.print_list()
    
    print("\n" + "=" * 60)
    print("Всі тести виконано успішно!")
    print("=" * 60)


if __name__ == "__main__":
    main()
