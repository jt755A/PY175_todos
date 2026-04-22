def error_for_list_title(title, lists):
    if any(lst['title'] == title for lst in lists):
        return "The title must be unique."
    elif not 1 <= len(title) <= 100:
        return "The title must be between 1 and 100 characters"
    else:
        return None

def error_for_todo_title(title):
    if not 1 <= len(title) <= 100:
        return "The title must be between 1 and 100 characters"
    else:
        return None

def find_list_by_id(list_id, lists):
    return next((lst for lst in lists if lst['id'] == list_id), None)

def find_todo_by_id(todo_id, todos):
    return next((todo for todo in todos if todo['id'] == todo_id), None)

def delete_list_by_id(list_id, lists):
    return [lst for lst in lists if lst['id'] != list_id]

def todos_remaining(lst):
    return sum(1 for todo in lst['todos'] if not todo['completed'])

def is_list_completed(lst):
    return len(lst['todos']) > 0 and todos_remaining(lst) == 0

def sort_lists(lists):
    sorted_lists = sorted(lists, key=lambda lst: lst['title'].lower())
    incomplete_lists = [lst for lst in sorted_lists
                        if not is_list_completed(lst)]
    completed_lists = [lst for lst in sorted_lists if is_list_completed(lst)]

    return incomplete_lists + completed_lists

def is_todo_completed(todo):
    return todo['completed']

def sort_items(items, select_completed):
    sorted_items = sorted(items, key=lambda item: item['title'].casefold())

    incomplete_items = [item for item in sorted_items
                        if not select_completed(item)]
    completed_items = [item for item in sorted_items
                       if select_completed(item)]

    return incomplete_items + completed_items