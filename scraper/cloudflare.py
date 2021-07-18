import undetected_chromedriver.v2 as uc
from selenium.webdriver.common.proxy import Proxy, ProxyType
from pathlib import Path
import time

from xvfbwrapper import Xvfb


class BypassCloudflare(object):
    """
    Read site web 'under attack mode'
    and bypass tests

    @return html 
    """
    
    def __init__(self, url, proxy=""):
        """
        url: the webpage to load
        proxy: http proxy to use if needed
        user_data_dir: folder to save cookies and preferences
        """

        self.url = url 
        self.proxy = proxy 
        self.user_data_dir = self.check_user_data_dir()

    
    def check_user_data_dir(self) -> str:
        """
        Check folder where cookies and site preferences persist across sessions.
        Create if not exists.

        @return string
        """

        user_data_dir = Path("{}/cloudflare-bypass/scraper".format(Path.home()))
        Path(user_data_dir).mkdir(parents=True, exist_ok=True)
        print(user_data_dir)
        return "{}/cloudflare-bypass/scraper".format(Path.home())

    def read_webpage(self) -> str:
        """
        Bypass DDos protection:
        this function read the webpage with selenium driver
        and return the html code of the scraped page.

        @return: string
        """

        vdisplay = Xvfb(width=800, height=1280)
        vdisplay.start()

        options = uc.ChromeOptions()
        # setting profile
        options.user_data_dir = self.user_data_dir

        # another way to set profile is the below (which takes precedence if both variants are used
        options.add_argument('--user-data-dir={}'.format(self.user_data_dir))

        options.headless = False

        # just some options passing in to skip annoying popups
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

        # Proxy 
        print("Use proxy: {proxy}".format(proxy=self.proxy))
        if self.proxy:
            options.add_argument('--proxy-server={proxy}'.format(proxy=self.proxy))

        driver = uc.Chrome(options=options)

        # now all these events will be printed in my console

        with driver:
            driver.get_cookies()
            try:
                driver.get(self.url) # known url using cloudflare's "under attack mode"
            except Exception as e:
                print('Error | ', e)
                return
            print('Loaded...')
            
        html = driver.page_source
        #time.sleep(20)
        #print(html)
        driver.close()
        vdisplay.stop()
        return html