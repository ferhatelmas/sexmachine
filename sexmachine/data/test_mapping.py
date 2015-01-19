# -*- coding: utf-8 -*-
import unittest
import sexmachine.mapping as m


class TestMapping(unittest.TestCase):

    def test_map_name(self):
        self.assertEqual(m.map_name(u"Ay<s,>e"), u"Ayşe")
        self.assertEqual(m.map_name(u"<ß>ahri"), u"ẞahri")
        self.assertEqual(m.map_name(u"<Ö>mer"), u"Őmer")
        self.assertEqual(m.map_name(u"<SCH>vet"), u"Švet")

if __name__ == '__main__':
    unittest.main()
