import unittest

from libs.clamp import clamp

class TestClamp(unittest.TestCase):
    def test_default_clamping(self):
        in_lo = -0.99
        out_lo = -1.01
        in_hi = 0.99
        out_hi = 1.01
        mid = 0
        self.assertEqual(clamp(in_lo), in_lo)
        self.assertEqual(clamp(in_hi), in_hi)
        self.assertEqual(clamp(mid), mid)
        self.assertNotEqual(clamp(out_lo), out_lo)
        self.assertEqual(clamp(out_lo), -1)
        self.assertNotEqual(clamp(out_hi), out_hi)
        self.assertEqual(clamp(out_hi), 1)

    def test_clamping(self):
        lo = 0
        hi = 5
        in_lo = 0.01
        out_lo = -0.01
        in_hi = 4.99
        out_hi = 5.01
        on_lo = 0
        on_hi = 5
        self.assertEqual(clamp(in_lo, lo=lo, hi=hi), in_lo)
        self.assertEqual(clamp(in_hi, lo=lo, hi=hi), in_hi)
        self.assertEqual(clamp(on_lo, lo=lo, hi=hi), on_lo)
        self.assertEqual(clamp(on_hi, lo=lo, hi=hi), on_hi)
        self.assertNotEqual(clamp(out_lo, lo=lo, hi=hi), out_lo)
        self.assertEqual(clamp(out_lo, lo=lo, hi=hi), 0)
        self.assertNotEqual(clamp(out_hi, lo=lo, hi=hi), out_hi)
        self.assertEqual(clamp(out_hi, lo=lo, hi=hi), 5)


if __name__=="__main__":
    unittest.main()
