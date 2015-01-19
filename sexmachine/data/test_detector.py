# -*- coding: utf-8 -*-
import unittest
import sexmachine.detector as d


class TestDetector(unittest.TestCase):

    def setUp(self):
        self.case = d.Detector()
        self.incase = d.Detector(case_sensitive=False)

    def test_gender(self):
        self.assertEqual(self.case.get_gender(u"Bob"), "male")
        self.assertEqual(self.case.get_gender(u"Sally"), "female")
        self.assertEqual(self.case.get_gender(u"Pauley"), "andy")

    def test_unicode(self):
        self.assertEqual(self.case.get_gender(u"Álfrún"), "female")
        self.assertEqual(self.case.get_gender(u"Ayşe"), "female")
        self.assertEqual(self.case.get_gender(u"Gavriliţă"), "female")
        self.assertEqual(self.case.get_gender(u"İsmet"), "male")
        self.assertEqual(self.case.get_gender(u"Snæbjörn"), "male")

    def test_country(self):
        self.assertEqual(self.case.get_gender(u"Jamie"), "mostly_female")
        self.assertEqual(self.case.get_gender(u"Jamie", "great_britain"),
                         "mostly_male")

    def test_case(self):
        self.assertEqual(self.incase.get_gender(u"sally"), "female")
        self.assertEqual(self.incase.get_gender(u"Sally"), "female")
        self.assertEqual(self.incase.get_gender(u"aydın"), "male")
        self.assertEqual(self.incase.get_gender(u"Aydın"), "male")

if __name__ == '__main__':
    unittest.main()
