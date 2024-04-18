import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand


class TestHBNBCommand(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """setup for the test"""
        cls.console = HBNBCommand()

    def setUp(self):
        """Set up the test case"""
        self.mock_stdout = StringIO()
        self.patcher = patch('sys.stdout', new=self.mock_stdout)
        self.patcher.start()

    def tearDown(self):
        """Tear down the test case"""
        self.patcher.stop()
        self.mock_stdout.close()

    def clear_stdout(self):
        """Clear the content of the mocked stdout"""
        self.mock_stdout.truncate(0)
        self.mock_stdout.seek(0)

    def test_create(self):
        self.console.onecmd("create")
        self.assertEqual("** class name missing **\n",
                         self.mock_stdout.getvalue())
        self.clear_stdout()

        self.console.onecmd("create BaseModel")
        self.assertEqual("** class doesn't exist **\n",
                         self.mock_stdout.getvalue())
        self.clear_stdout()

        self.console.onecmd("create State")
        self.clear_stdout()
        self.console.onecmd("all State")
        self.assertIn("[State]", self.mock_stdout.getvalue())

    def test_do_quit(self):
        with patch('sys.stdout', new=StringIO()) as output:
            with self.assertRaises(SystemExit):
                self.console.onecmd("quit")
        self.assertEqual('', output.getvalue())


if __name__ == "__main__":
    unittest.main()
