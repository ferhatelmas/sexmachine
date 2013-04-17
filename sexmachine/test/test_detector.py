# -*- coding: utf-8 -*-
import unittest
import sexmachine.detector as d


class TestDetector(unittest.TestCase):

    def setUp(self):
        self.case = d.Detector()
        self.incase = d.Detector(case_sensitive=False)

    def test_gender(self):
        self.assertEqual(self.case.get_gender(u"Bob"), u"male")
        self.assertEqual(self.case.get_gender(u"Sally"), u"female")
        self.assertEqual(self.case.get_gender(u"Pauley"), u"andy")

    def test_unicode(self):
        self.assertEqual(self.case.get_gender(u"Álfrún"), u"female")

    def test_country(self):
        self.assertEqual(self.case.get_gender(u"Jamie"), u"mostly_female")
        self.assertEqual(self.case.get_gender(u"Jamie", u"great_britain"),
                         u"mostly_male")

    def test_case(self):
        self.assertEqual(self.incase.get_gender(u"sally"), u"female")
        self.assertEqual(self.incase.get_gender(u"Sally"), u"female")

if __name__ == '__main__':
    unittest.main()
