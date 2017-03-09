import unittest
import naming as n


class SolveCase(unittest.TestCase):
    def test_explicit(self):
        name = "foo_L_anim"
        solved = n.solve(description="foo", side="left", type="animation")
        self.assertEqual(solved, name)

        name = "foo_M_anim"
        solved = n.solve(description="foo", side="middle", type="animation")
        self.assertEqual(solved, name)

    def test_defaults(self):
        name = "foo_M_anim"
        solved = n.solve(description="foo", type="animation")
        self.assertEqual(solved, name)

        name = "foo_M_ctrl"
        solved = n.solve(description="foo")
        self.assertEqual(solved, name)

    def test_implicit(self):
        name = "foo_M_anim"
        solved = n.solve("foo", type="animation")
        self.assertEqual(solved, name)

        name = "foo_M_ctrl"
        solved = n.solve("foo")
        self.assertEqual(solved, name)


class ParseCase(unittest.TestCase):
    def test_parsing(self):
        name = "foo_M_ctrl"
        parsed = n.parse(name)
        self.assertEqual(parsed["description"], "foo")
        self.assertEqual(parsed["side"], "middle")
        self.assertEqual(parsed["type"], "control")


if __name__ == "__main__":
    unittest.main()
