import unittest
import naming as n


class SolveCase(unittest.TestCase):
    def setUp(self):
        n.add_token("description")
        n.add_token("side", left="L", right="R", middle="M", default="M")
        n.add_token("type", animation="anim", control="ctrl", joint="jnt", default="ctrl")

    def tearDown(self):
        n.flush_tokens()

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
    def setUp(self):
        n.add_token("description")
        n.add_token("side", left="L", right="R", middle="M", default="M")
        n.add_token("type", animation="anim", control="ctrl", joint="jnt", default="ctrl")

    def tearDown(self):
        n.flush_tokens()

    def test_parsing(self):
        name = "foo_M_ctrl"
        parsed = n.parse(name)
        self.assertEqual(parsed["description"], "foo")
        self.assertEqual(parsed["side"], "middle")
        self.assertEqual(parsed["type"], "control")


class TokenCase(unittest.TestCase):
    def test_add(self):
        result = n.add_token("description")
        self.assertTrue(result)

        result = n.add_token("side", left="L", right="R", middle="M", default="M")
        self.assertTrue(result)

    def test_flush(self):
        result = n.flush_tokens()
        self.assertTrue(result)

    def remove_token(self):
        n.add_token("test")
        result = n.remove_token("test")
        self.assertTrue(result)

        result = n.remove_token("test2")
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
