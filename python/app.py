from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import platform
from kivymd.app import MDApp
from kivy.clock import mainthread

if platform == "android":
    from jnius import autoclass

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDToolbar:
        title: 'LakshyOrbit'
        left_action_items: [["arrow-left", lambda x: app.navigate_back()]]
        right_action_items: [["home", lambda x: app.navigate_home()], ["refresh", lambda x: app.reload_page()]]
        elevation: 10
        md_bg_color: app.theme_cls.primary_color

    TextInput:
        id: url_input
        multiline: False
        size_hint_y: None
        height: "48dp"
        hint_text: "Enter URL and press Enter"
        on_text_validate: app.navigate_to_url(self.text)

    BoxLayout:
        id: webview_container
'''
class WebViewApp(MDApp):
    def build(self):
        self.webview = None
        self.home_url = "https://snehaghosh-technical-isopod-portfolio.vercel.app/"
        self.default_url = "http://google.com"
        self.current_url = self.default_url
        self.load_webview()
        return Builder.load_string(KV)

    def on_start(self):
        self.load_url(self.default_url)

    @mainthread
    def load_webview(self):
        """Sets up Android WebView."""
        if platform == "android":
            WebView = autoclass("android.webkit.WebView")
            WebSettings = autoclass("android.webkit.WebSettings")
            activity = autoclass("org.kivy.android.PythonActivity").mActivity

            self.webview = WebView(activity)
            self.webview.getSettings().setJavaScriptEnabled(True)
            self.webview.getSettings().setCacheMode(WebSettings.LOAD_CACHE_ELSE_NETWORK)

            layout = autoclass("android.widget.LinearLayout")(activity)
            activity.setContentView(layout)
            layout.addView(self.webview)

    def load_url(self, url):
        """Loads a URL into WebView after validating it."""
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url
        self.current_url = url
        if self.webview:
            self.webview.loadUrl(url)

    def reload_page(self):
        """Reloads the current page."""
        if self.webview:
            self.webview.reload()

    def navigate_back(self):
        """Navigates back in WebView if possible."""
        if self.webview and self.webview.canGoBack():
            self.webview.goBack()

    def navigate_home(self):
        """Navigates to the home URL."""
        self.load_url(self.home_url)

    def navigate_to_url(self, url):
        """Loads a new URL entered in the text field."""
        self.load_url(url)
