import unittest
import naming as n


class SolveCase(unittest.TestCase):
    def setUp(self):
        n.flush_tokens()
        n.add_token("description")
        n.add_token("side", left="L", right="R", middle="M", default="M")
        n.add_token("type", animation="anim", control="ctrl", joint="jnt", default="ctrl")

        n.flush_rules()
        n.add_rule("test1", "description", "side", "type")
        n.add_rule("test2", "side", "description")
        n.set_active_rule("test1")

    def test_explicit(self):
        name = "foo_L_anim"
        solved = n.solve(description="foo", side="left", type="animation")
        self.assertEqual(solved, name)

        name = "foo_M_anim"
        solved = n.solve(description="foo", side="middle", type="animation")
        self.assertEqual(solved, name)

        n.set_active_rule("test2")

        name = "L_foo"
        solved = n.solve(description="foo", side="left", type="animation")
        self.assertEqual(solved, name)

        name = "M_foo"
        solved = n.solve(description="foo", side="middle", type="animation")
        self.assertEqual(solved, name)

    def test_defaults(self):
        name = "foo_M_anim"
        solved = n.solve(description="foo", type="animation")
        self.assertEqual(solved, name)

        name = "foo_M_ctrl"
        solved = n.solve(description="foo")
        self.assertEqual(solved, name)

        n.set_active_rule("test2")

        name = "M_foo"
        solved = n.solve(description="foo", type="animation")
        self.assertEqual(solved, name)

        solved = n.solve(description="foo")
        self.assertEqual(solved, name)

    def test_implicit(self):
        name = "foo_M_anim"
        solved = n.solve("foo", type="animation")
        self.assertEqual(solved, name)

        name = "foo_M_ctrl"
        solved = n.solve("foo")
        self.assertEqual(solved, name)

        n.set_active_rule("test2")

        name = "M_foo"
        solved = n.solve("foo", type="animation")
        self.assertEqual(solved, name)

        name = "M_foo"
        solved = n.solve("foo")
        self.assertEqual(solved, name)


class ParseCase(unittest.TestCase):
    def setUp(self):
        n.flush_tokens()
        n.add_token("description")
        n.add_token("side", left="L", right="R", middle="M", default="M")
        n.add_token("type", animation="anim", control="ctrl", joint="jnt", default="ctrl")

        n.flush_rules()
        n.add_rule("test1", "description", "side", "type")
        n.add_rule("test2", "side", "description")
        n.set_active_rule("test1")

    def test_parsing(self):
        name = "foo_M_ctrl"
        parsed = n.parse(name)
        self.assertEqual(parsed["description"], "foo")
        self.assertEqual(parsed["side"], "middle")
        self.assertEqual(parsed["type"], "control")
        self.assertEqual(len(parsed), 3)

        n.set_active_rule("test2")

        name = "M_foo"
        parsed = n.parse(name)
        self.assertEqual(parsed["description"], "foo")
        self.assertEqual(parsed["side"], "middle")
        self.assertEqual(len(parsed), 2)


class TokenCase(unittest.TestCase):
    def setUp(self):
        n.flush_tokens()

    def test_add(self):
        result = n.add_token("description")
        self.assertTrue(result)

        result = n.add_token("side", left="L", right="R", middle="M", default="M")
        self.assertTrue(result)

    def test_flush(self):
        result = n.flush_tokens()
        self.assertTrue(result)

    def test_remove(self):
        n.add_token("test")
        result = n.remove_token("test")
        self.assertTrue(result)

        result = n.remove_token("test2")
        self.assertFalse(result)

    def test_has(self):
        name = "foo"
        n.add_token(name)
        r = n.has_token(name)
        self.assertTrue(r)

        n.remove_token(name)
        r = n.has_token(name)
        self.assertFalse(r)

class RuleCase(unittest.TestCase):
    def setUp(self):
        n.flush_rules()

    def test_add(self):
        result = n.add_rule("test", "description", "side", "type")
        self.assertTrue(result)

    def test_flush(self):
        result = n.flush_rules()
        self.assertTrue(result)

    def test_remove(self):
        n.add_rule("test", "description", "side", "type")
        result = n.remove_rule("test")
        self.assertTrue(result)

        result = n.remove_rule("test2")
        self.assertFalse(result)

    def test_has(self):
        name = "foo"
        n.add_rule(name, "description", "side", "type")
        r = n.has_rule(name)
        self.assertTrue(r)

        n.remove_rule(name)
        r = n.has_rule(name)
        self.assertFalse(r)

    def test_active(self):
        name = "foo"
        n.add_rule(name, "description", "side", "type")
        r = n.active_rule()
        self.assertIsNotNone(r)


if __name__ == "__main__":
    unittest.main()
