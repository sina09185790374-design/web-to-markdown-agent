import os
import unittest

from reader.convert import html_to_markdown

HERE = os.path.dirname(os.path.abspath(__file__))
SAMPLE = os.path.join(HERE, "..", "sample.html")


class TestSampleFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.md = html_to_markdown(open(SAMPLE, encoding="utf-8").read())

    def test_h1_heading(self):
        self.assertIn("# کارت گرافیک RTX 4060", self.md)

    def test_h2_headings(self):
        self.assertIn("## مشخصات فنی", self.md)
        self.assertIn("## مراحل خرید", self.md)

    def test_link_as_markdown(self):
        self.assertIn("[صفحه محصول](https://example.com/rtx-4060)", self.md)

    def test_unordered_list(self):
        self.assertIn("- حافظه ۸ گیگابایت GDDR6", self.md)

    def test_ordered_list(self):
        self.assertIn("1. افزودن به سبد خرید", self.md)

    def test_emphasis_kept(self):
        self.assertIn("**کارت گرافیک RTX 4060**", self.md)

    def test_script_removed(self):
        self.assertNotIn("DO_NOT_INCLUDE_THIS_SCRIPT", self.md)
        self.assertNotIn("analytics.js", self.md)

    def test_style_removed(self):
        self.assertNotIn("font-weight", self.md)

    def test_nav_footer_aside_removed(self):
        self.assertNotIn("NAV_JUNK", self.md)
        self.assertNotIn("FOOTER_JUNK", self.md)
        self.assertNotIn("ASIDE_JUNK", self.md)

    def test_price_text_kept(self):
        self.assertIn("۲۸٬۵۰۰٬۰۰۰ تومان", self.md)


class TestInlineHtml(unittest.TestCase):
    def test_simple(self):
        md = html_to_markdown("<h1>Hi</h1><p>See <a href='https://x.co'>this</a>.</p>")
        self.assertIn("# Hi", md)
        self.assertIn("[this](https://x.co)", md)

    def test_empty(self):
        self.assertEqual(html_to_markdown(""), "\n")


if __name__ == "__main__":
    unittest.main()
