import unittest
import naming as n


class SolveCase(unittest.TestCase):
    def test_explicit(self):
        name = "foo_L_anim"
        solved = n.solve(description="foo", side="left", type="animation")
        self.assertEqual(solved, name)

        name = "foo_M_anim"
        solved = n.solve(description="foo", side="center", type="animation")
        self.assertEqual(solved, name)

if __name__ == "__main__":
    unittest.main()
