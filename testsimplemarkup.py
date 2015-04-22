import unittest

import simplemarkup


class TestSimpleMarkup(unittest.TestCase):

    def test_type_check(self):
        sm = simplemarkup.SimpleMarkup()
        types = [None, True, 1, 0.1, 1j, "Hi", "", [], (), {}]

        ### test _verify_str_ ###

        # no strings
        with self.assertRaises(TypeError):
            for element in [x for x in types if not isinstance(x, str)]:
                sm._verify_str_(element)

        # only strings
        for element in [x for x in types if isinstance(x, str)]:
            self.assertIsNone(sm._verify_str_(element))

        ### test _verify_list_ ###

        # no lists
        with self.assertRaises(TypeError):
            for element in [x for x in types if not isinstance(x, list)]:
                sm._verify_list_(element)

        # empty list
        self.assertIsNone(sm._verify_list_([]))

        # 1 element lists
        with self.assertRaises(TypeError):
            for element in [[x] for x in types]:
                sm._verify_list_(element)

        # 2 element lists
        with self.assertRaises(TypeError):
            for element in [[x, y] for x in types for y in types]:
                sm._verify_list_(element)

        # 3 element lists
        with self.assertRaises(TypeError):
            for element in [[x, y, z] for x in types for y in types for z in types]:
                sm._verify_list_(element)

        # 1-tuple lists
        with self.assertRaises(TypeError):
            for element in [[(x,)] for x in types]:
                sm._verify_list_(element)

        # 2-tuple lists, no strings
        with self.assertRaises(TypeError):
            for element in [[(x, y)] for x in types if not isinstance(x, str) for y in types if not isinstance(y, str)]:
                sm._verify_list_(element)

        # 3-tuple lists
        with self.assertRaises(TypeError):
            for element in [[(x, y, z)] for x in types for y in types for z in types]:
                sm._verify_list_(element)

        # 2-tuple lists, only strings
        for element in [[(x, y)] for x in types if isinstance(x, str) for y in types if isinstance(y, str)]:
            self.assertIsNone(sm._verify_list_(element))

    def test_insert(self):
        sm = simplemarkup.SimpleMarkup()

        sm.insert("Hello")
        self.assertEqual(sm.output, ["Hello"])

        sm.insert("World")
        self.assertEqual(sm.output, ["Hello", "World"])

        sm.depth = 1
        sm.insert("One")
        one = sm.indent * sm.depth
        self.assertEqual(sm.output, ["Hello", "World", one + "One"])

        sm.depth = 2
        sm.insert("Two")
        two = sm.indent * sm.depth
        self.assertEqual(sm.output, ["Hello", "World", one + "One", two + "Two"])

        sm.depth = 3
        sm.insert("Three")
        three = sm.indent * sm.depth
        self.assertEqual(sm.output, ["Hello", "World", one + "One", two + "Two", three + "Three"])

        sm.depth = 0
        sm.insert("Bye").insert("Bye")
        self.assertEqual(sm.output, ["Hello", "World", one + "One", two + "Two", three + "Three", "Bye", "Bye"])

    def test_newline(self):
        sm = simplemarkup.SimpleMarkup()

        sm.newline()
        self.assertEqual(sm.output, ["\n"])

        sm.newline()
        self.assertEqual(sm.output, ["\n", "\n"])

        sm.depth = 1
        sm.newline()
        self.assertEqual(sm.output, ["\n", "\n", "\n"])

        sm.depth = 2
        sm.newline()
        self.assertEqual(sm.output, ["\n", "\n", "\n", "\n"])

        sm.depth = 3
        sm.newline()
        self.assertEqual(sm.output, ["\n", "\n", "\n", "\n", "\n"])

        sm.depth = 0
        sm.newline().newline()
        self.assertEqual(sm.output, ["\n", "\n", "\n", "\n", "\n", "\n", "\n"])


if __name__ == "__main__":
    unittest.main()