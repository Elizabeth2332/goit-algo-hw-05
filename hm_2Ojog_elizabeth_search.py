list_of_floats = [1.1, 2.2, 3.3, 4.4, 5.5, 6.6, 7.7, 8.8, 9.9]


def binary_search(list_of_floats, target):
    bottom, top = 0, len(list_of_floats) - 1
    # mid = bottom + top // 2
    iterations, new_top_bound = 0, None
    while bottom <= top:
        iterations += 1
        mid = (bottom + top) // 2   
        
        if list_of_floats[mid] < target:
            bottom = mid + 1
        elif list_of_floats[mid] > target:
            top = mid - 1
            new_top_bound = list_of_floats[mid]
            #print(f"Верхня межа: {new_top_bound}")
        else:
            new_top_bound = list_of_floats[mid]
            return iterations, new_top_bound

    # Якщо елемент не знайдено, визначаємо верхню межу
    if new_top_bound is None and bottom < len(list_of_floats):
        new_top_bound = list_of_floats[bottom]        
    return iterations, new_top_bound


print(binary_search(sorted(list_of_floats), 5.6))