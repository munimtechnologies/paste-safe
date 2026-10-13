"""Runs the JavaScript test suite (test/core.test.mjs) with Node.

Paste-Safe is a browser app; this wrapper only lets Python test runners
gate a commit on the same `node --test` run that CI does.
"""
import os
import shutil
import subprocess
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))


def find_node():
    found = shutil.which("node")
    if found:
        return found
    for path in (r"C:\Program Files\nodejs\node.exe", "/usr/local/bin/node", "/usr/bin/node"):
        if os.path.exists(path):
            return path
    return None


class NodeSuite(unittest.TestCase):
    def test_core(self):
        node = find_node()
        if not node:
            self.skipTest("node is not installed")
        if not os.path.exists(os.path.join(HERE, "test", "core.test.mjs")):
            self.skipTest("test/core.test.mjs is not next to this file")
        result = subprocess.run(
            [node, "--test", os.path.join("test", "core.test.mjs")],
            cwd=HERE, capture_output=True, text=True, timeout=180,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
