import copy


class SelfReferencingEntity:
    def __init__(self):
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent


class SomeComponent:
    """
    Python предоставляет свой собственный интерфейс Прототипа через функции `copy.copy` и
    `copy.deepcopy`. И любому классу, который хочет реализовать собственные
    варианты, необходимо переопределить члены функций `__copy__` и `__deepcopy__`.
    """

    def __init__(self, some_int, some_list_of_objects, some_circular_ref):
        self.some_int = some_int
        self.some_list_of_objects = some_list_of_objects
        self.some_circular_ref = some_circular_ref

    def __copy__(self):
        """
        Создание поверхностной копии. Этот метод будет вызываться, когда кто-то вызывает
        `copy.copy` с этим объектом, и возвращенное значение используется как новая
        поверхностная копия.
        """

        # Сначала создадим копии вложенных объектов.
        some_list_of_objects = copy.copy(self.some_list_of_objects)
        some_circular_ref = copy.copy(self.some_circular_ref)

        # Затем склонируем сам объект, используя подготовленные копии вложенных объектов.
        new = self.__class__(
            self.some_int, some_list_of_objects, some_circular_ref
        )
        new.__dict__.update(self.__dict__)

        return new

    def __deepcopy__(self, memo=None):
        """
        Создание глубокой копии. Этот метод будет вызываться, когда кто-то вызывает
        `copy.deepcopy` с этим объектом, и возвращенное значение используется как новая
        глубокая копия.

        Зачем нужен аргумент `memo`? Memo - это словарь, используемый библиотекой `deepcopy`,
        чтобы предотвратить бесконечные рекурсивные копии в случаях циклических ссылок.
        Передавайте его ко всем вызовам `deepcopy` в реализации `__deepcopy__`,
        чтобы предотвратить бесконечные рекурсии.
        """
        if memo is None:
            memo = {}

        # Сначала создадим копии вложенных объектов.
        some_list_of_objects = copy.deepcopy(self.some_list_of_objects, memo)
        some_circular_ref = copy.deepcopy(self.some_circular_ref, memo)

        # Затем склонируем сам объект, используя подготовленные копии вложенных объектов.
        new = self.__class__(
            self.some_int, some_list_of_objects, some_circular_ref
        )
        new.__dict__ = copy.deepcopy(self.__dict__, memo)

        return new


if __name__ == "__main__":

    list_of_objects = [1, {1, 2, 3}, [1, 2, 3]]
    circular_ref = SelfReferencingEntity()
    component = SomeComponent(23, list_of_objects, circular_ref)
    circular_ref.set_parent(component)

    shallow_copied_component = copy.copy(component)

    # Изменим список в shallow_copied_component и посмотрим, изменится ли он в component.
    shallow_copied_component.some_list_of_objects.append("еще один объект")
    if component.some_list_of_objects[-1] == "еще один объект":
        print(
            "Добавление элементов в some_list_of_objects `shallow_copied_component` добавляет их в some_list_of_objects `component`."
        )
    else:
        print(
            "Добавление элементов в some_list_of_objects `shallow_copied_component` не добавляет их в some_list_of_objects `component`."
        )

    # Изменим множество в списке объектов.
    component.some_list_of_objects[1].add(4)
    if 4 in shallow_copied_component.some_list_of_objects[1]:
        print(
            "Изменение объектов в some_list_of_objects `component` изменяет этот объект в some_list_of_objects `shallow_copied_component`."
        )
    else:
        print(
            "Изменение объектов в some_list_of_objects `component` не изменяет этот объект в some_list_of_objects `shallow_copied_component`."
        )

    deep_copied_component = copy.deepcopy(component)

    # Изменим список в deep_copied_component и посмотрим, изменится ли он в component.
    deep_copied_component.some_list_of_objects.append("еще один объект")
    if component.some_list_of_objects[-1] == "еще один объект":
        print(
            "Добавление элементов в some_list_of_objects `deep_copied_component` добавляет их в some_list_of_objects `component`."
        )
    else:
        print(
            "Добавление элементов в some_list_of_objects `deep_copied_component` не добавляет их в some_list_of_objects `component`."
        )

    # Изменим множество в списке объектов.
    component.some_list_of_objects[1].add(10)
    if 10 in deep_copied_component.some_list_of_objects[1]:
        print(
            "Изменение объектов в some_list_of_objects `component` изменяет этот объект в some_list_of_objects `deep_copied_component`."
        )
    else:
        print(
            "Изменение объектов в some_list_of_objects `component` не изменяет этот объект в some_list_of_objects `deep_copied_component`."
        )

    print(
        f"id(deep_copied_component.some_circular_ref.parent): "
        f"{id(deep_copied_component.some_circular_ref.parent)}"
    )
    print(
        f"id(deep_copied_component.some_circular_ref.parent.some_circular_ref.parent): "
        f"{id(deep_copied_component.some_circular_ref.parent.some_circular_ref.parent)}"
    )
    print(
        "^^ Это показывает, что скопированные глубоким образом объекты содержат ту же самую ссылку, и они не клонируются повторно."
    )
