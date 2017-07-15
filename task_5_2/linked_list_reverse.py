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
        reversed_llist = []
        element = self.head
        prev_elem = self.head
        new_head = None
        new_prev_element = None
        while element:
            if element.next is None:
                print('Next element is  None! Addr {}, Value: {}'.format(element, element.data))
                if new_head:
                    new_prev_element.link(element)
                    prev_elem.link(None)
                    new_prev_element = element
                    print('BL Prev elem:{}, {}. Value: {}'.format(prev_elem, prev_elem.next, prev_elem.data))
                    print('BL Work elem:{}, {}. Value: {}'.format(element, element.next, element.data))
                    print('BL New List {}, {} Value: {}'.format(new_prev_element, new_prev_element.next, new_prev_element.data))
                    if prev_elem == self.head:
                        new_prev_element.link(prev_elem)
                        element = None
                    else:
                        element = self.head
                    continue
                else:
                    new_head = element
                    prev_elem.link(None)
                    new_prev_element = new_head
                    element = self.head
                    print('Prev elem:{}, {}. Value: {}'.format(prev_elem, prev_elem.next, prev_elem.data))
                    print('Work elem:{}, {}. Value: {}'.format(element, element.next, element.data))
                    print('New List {}, {}. Value: {}'.format(new_head, new_head.next, new_head.data))

                    continue
            prev_elem = element
            element = element.next
            print('Main cycle:{}, {}. Value:{}'.format(prev_elem, prev_elem.next, prev_elem.data))
        self.head = new_head
        print('Done')
        return reversed_llist

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

asf = LinkedList([1, 2, 3, 4, 5])

asf.reverse()
# m.iter()
for num in asf:
    print(num)