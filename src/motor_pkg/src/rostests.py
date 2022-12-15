#!/usr/bin/env python
import unittest
import rostest

class TestCase(unittest.TestCase):
    def test_whatever(self):
        pass

if __name__ == "__main__":
    rostest.rosrun("motor_pkg","rostests",TestCase)