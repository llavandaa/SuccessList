import json
import os


class Task:
    # Конструктор для создания новой задачи
    def __init__(self, task_id, description, priority, deadline):
        self.task_id = task_id
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.completed = False

    def mark_as_completed(self):
        self.completed = True
        print(f'Задача "{self.description}" завершена.')

    def get_status(self):
        if self.completed:
            return 'Завершена'
        else:
            return 'В работе'

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks() # Загружаем из файла задачи, если они есть

    def load_tasks(self):
        if os.path.exists('tasks.json'):
            with open('tasks.json', 'r', encoding='utf-8') as file:
                tasks_data = json.load(file)
                for task_data in tasks_data:
                    task = Task(task_data['task_id'], task_data['description'], task_data['priority'], task_data['deadline'])
                    if task_data['completed']:
                        task.completed = True
                    self.tasks.append(task)
    
    # Сохраняет список задач в файле
    def save_tasks(self):
        tasks_data = [{
            'task_id': task.task_id,
            'description': task.description,
            'priority': task.priority,
            'deadline': task.deadline,
            'completed': task.completed
        } for task in self.tasks]
        
        with open('tasks.json', 'w', encoding='utf-8') as file:
            json.dump(tasks_data, file, ensure_ascii=False, indent=4)

    # Получает задачу по её уникальному идентификаторy
    # Возвращает None если такой задачи нет 
    def get_tasks(self, task_id):
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    

    # Добавляет новую задачу в список
    def add_task(self, task):
        self.tasks.append(task)



    # Удаляет задачу из списка
    def remove_task(self, task_id):
        task = self.get_tasks(task_id)
        if task:
            self.tasks.remove(task)
            print(f'Задача "{task.description}" была удалена.')
        else:
            print('Задача не найдена.')
    
    # Отображает список всех задач
    def show_tasks(self):
        if not self.tasks:
            print('Список задач пуст.')
            return
        
        print('Ваши задачи:')
        for task in self.tasks:
            description = task.description if task.description else "Отсутствует"
            priority = task.priority if task.priority else "Отсутствует"
            deadline = task.deadline if task.deadline else "Отсутствует"
            
            status = task.get_status() # Получаем статус задачи
            print(f'ID: {task.task_id}, Задача: {description}, Приоритет: {priority}, Дедлайн: {deadline}, Статус: {status}')

    # Изменяет задачу по ее уникальному ID
    def update_task(self, task_id, description=None, priority=None, deadline=None):
        task = self.get_tasks(task_id)
        if task:
            if description is not None:  # Обновляем только если значение не None
                task.description = description
            if priority is not None:  # Обновляем только если значение не None
                task.priority = priority
            if deadline is not None:  # Обновляем только если значение не None
                task.deadline = deadline
            
            print(f'Задача с ID {task.task_id} была изменена.')
        else:
            print('Задача не найдена.')

    # Помечает задачу как выполненную
    def mark_as_completed(self, task_id):
        task = self.get_tasks(task_id)
        if task:
            task.mark_as_completed()
        else:
            print('Задача не найдена.')
    

def main():
    manager = TaskManager()
    task_id_counter = 1 # Счетчик для уникальных идентификаторов задач
    
    while True:
        print('\n')
        print(f'################################')
        print('1. Добавить новую задачу')
        print('2. Удалить задачу')
        print('3. Отобразить список всех задач')
        print('4. Изменить задачу')
        print('5. Пометить задачу как выполненную')
        print('0. Выход')
        print(f'################################')
        print('\n')
        choice = input('Выберите действие: ')
        
        if choice == '1':
            print()
            description = input('Введите описание задачи: ')
            priority = input('Введите приоритет (1 - Высокий, 3 - Средний, 5 - Низкий): ')
            deadline = input('Введите дедлайн (формат: dd.mm.yyyy): ')
            
            task = Task(task_id_counter, description, priority, deadline)
            manager.add_task(task)
            task_id_counter += 1
            
        elif choice == '2':
            print()
            try:
                task_id = int(input('Введите ID удаляемой задачи: '))
                manager.remove_task(task_id)
            except ValueError:
                print('Задача с таким ID не найдена.')
        
        elif choice == '3':
            print()
            manager.show_tasks()

        elif choice == '4':
            print()
            if not manager.tasks:
                print('Список задач пуст.')
                continue
            try:
                task_id = int(input('Введите ID изменяемой задачи: '))
                description = input('Введите новое описание задачи (или нажмите Enter для пропуска): ')
                priority = input('Введите новый приоритет (1 - Высокий, 3 - Средний, 5 - Низкий или нажмите Enter для пропуска): ')
                deadline = input('Введите новый дедлайн (формат: dd.mm.yyyy или нажмите Enter для пропуска): ')

                # Теперь передаем все необходимые параметры в метод update_task
                manager.update_task(task_id,
                                    description if description else None,
                                    priority if priority else None,
                                    deadline if deadline else None)
            except ValueError:
                print('Пожалуйста, введите корректный ID задачи.')


        elif choice == '5':
            print()
            try:
                task_id = int(input('Введите ID завершенной задачи: '))
                manager.mark_as_completed(task_id)
            except ValueError:
                print('Задача с таким ID не найдена.')

        elif choice == '0':
            manager.save_tasks()  # Сохраняем список задач в файле перед выходом
            print()
            print('Выход из программы.')
            break
        
        

        else:
            print('Пожалуйста, введите корректное число.')


if __name__ == '__main__':
    main()
