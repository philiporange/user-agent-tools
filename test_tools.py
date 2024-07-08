import unittest
from tools import UA


class TestUA(unittest.TestCase):
    def setUp(self):
        self.ua = UA()

    def test_top_user_agent(self):
        self.assertEqual(
            self.ua.top_user_agent(), self.ua.user_agents[0]["ua"]
        )

    def test_top_n_user_agents(self):
        self.assertEqual(
            self.ua.top_n_user_agents(3),
            [ua["ua"] for ua in self.ua.user_agents[:3]],
        )

    def test_random_no_filter(self):
        ua = self.ua.random()
        self.assertIn(ua, [item["ua"] for item in self.ua.user_agents])

    def test_random_with_browser_filter(self):
        ua = self.ua.random(browser="Chrome")
        self.assertIn("Chrome", ua)

    def test_random_with_system_filter(self):
        ua = self.ua.random(system="Linux")
        self.assertIn("Linux", ua)

    def test_random_with_both_filters(self):
        ua = self.ua.random(browser="Safari", system="macOS")
        self.assertIn("Safari", ua)
        self.assertIn("Macintosh", ua)

    def test_random_with_invalid_filter(self):
        with self.assertRaises(ValueError):
            self.ua.random(browser="InvalidBrowser")

    def test_interpret_windows_chrome(self):
        ua_string = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        result = self.ua.interpret(ua_string)
        self.assertEqual(result["os"], "Windows 10")
        self.assertEqual(result["browser"], "Chrome")
        self.assertEqual(result["browser_version"], "91.0.4472.124")
        self.assertEqual(result["platform"], "windows")

    def test_interpret_macos_safari(self):
        ua_string = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 "
            "Safari/605.1.15"
        )
        result = self.ua.interpret(ua_string)
        self.assertEqual(result["os"], "macOS")
        self.assertEqual(result["browser"], "Safari")
        self.assertEqual(result["browser_version"], "605.1.15")
        self.assertEqual(result["platform"], "macos")

    def test_interpret_linux_firefox(self):
        ua_string = (
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) "
            "Gecko/20100101 Firefox/89.0"
        )
        result = self.ua.interpret(ua_string)
        self.assertEqual(result["os"], "Linux")
        self.assertEqual(result["browser"], "Firefox")
        self.assertEqual(result["browser_version"], "89.0")
        self.assertEqual(result["platform"], "linux")

    def test_interpret_android(self):
        ua_string = (
            "Mozilla/5.0 (Linux; Android 10; SM-A505F) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
        )
        result = self.ua.interpret(ua_string)
        self.assertEqual(result["os"], "Android")
        self.assertEqual(result["browser"], "Chrome")
        self.assertEqual(result["platform"], "android")

    def test_interpret_ios(self):
        ua_string = (
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) "
            "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 "
            "Mobile/15E148 Safari/604.1"
        )
        result = self.ua.interpret(ua_string)
        self.assertEqual(result["os"], "iOS")
        self.assertEqual(result["browser"], "Safari")
        self.assertEqual(result["platform"], "ios")

    def test_interpret_kindle(self):
        ua_string = (
            "Mozilla/5.0 (X11; U; Linux armv7l like Android; en-us) "
            "AppleWebKit/531.2+ (KHTML, like Gecko) Version/5.0 "
            "Safari/533.2+ Kindle/3.0+"
        )
        result = self.ua.interpret(ua_string)
        self.assertEqual(result["platform"], "kindle")


if __name__ == "__main__":
    unittest.main()
