"""
Домашнее задание для лекции "Задачки на собеседованиях для продвинутых,
с тонкостями языка"

Описание
    Перестроить заданный связанный список (LinkedList) в обратном порядке.
    Для этого использовать метод `LinkedList.reverse()`, представленный
    в данном файле

Примечание
    Проверить работоспособность решения можно при помощи тестов,
    которые можно запустить следующей командой:

    python3 -m unittest linked_list_reverse.py
"""

import unittest

from typing import Iterable


class LinkedListNode:

    def __init__(self, data):
        self.data = data
        self.next = None  # type: LinkedListNode

    def link(self, node: 'LinkedListNode') -> None:
        self.next = node


class LinkedList:

    def __init__(self, values: Iterable):
        previous = None
        self.head = None
        for value in values:
            current = LinkedListNode(value)
            if previous:
                previous.link(current)
            self.head = self.head or current
            previous = current

    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next
            print(current)

    def reverse(self) -> None:
        cntr = 0
        if self.head is None:
            return True
        element = self.head
        prev_elem = self.head
        new_head = None
        new_prev_element = None
        while element:
            if element.next is None:
                if new_head:
                    new_prev_element.link(element)
                    prev_elem.link(None)
                    new_prev_element = element
                    if cntr > 10:
                        element= None
                        continue
                    if prev_elem == self.head:
                        new_prev_element.link(prev_elem)
                        element = None
                    else:
                        element = self.head
                    continue
                else:
                    new_head = element
                    new_prev_element = new_head
                    prev_elem.link(None)
                    element = self.head
                    if prev_elem == self.head:
                        new_prev_element.link(prev_elem)
                        element = None
                    else:
                        element = self.head
                    if new_head.next == new_head:
                        new_head.link(None)
                    continue

            prev_elem = element
            element = element.next
            if cntr > 10:
                element = None
            cntr += 1
        self.head = new_head
        return True

        # for value in values:
        #     current = LinkedListNode(value)
        #     if previous:
        #         previous.link(current)
        #     self.head = self.head or current
        #     previous = current


class LinkedListTestCase(unittest.TestCase):

    def test_reverse(self):
        cases = dict(
            empty=dict(
                items=[],
                expected_items=[],
            ),
            single=dict(
                items=[1],
                expected_items=[1],
            ),
            double=dict(
                items=[1, 2],
                expected_items=[2, 1],
            ),
            triple=dict(
                items=[1, 2, 3],
                expected_items=[3, 2, 1],
            ),
        )
        for case, data in cases.items():
            with self.subTest(case=case):
                linked_list = LinkedList(data['items'])
                linked_list.reverse()
                self.assertListEqual(
                    data['expected_items'],
                    list(linked_list),
                )

asf = LinkedList([1])

asf.reverse()
# m.iter()
for num in asf:
    print(num)