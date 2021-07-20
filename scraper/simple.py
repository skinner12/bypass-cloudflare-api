from xvfbwrapper import Xvfb
vdisplay = Xvfb(width=800, height=1280)
vdisplay.start()

import undetected_chromedriver.v2 as uc

options = uc.ChromeOptions()
options.add_argument(f'--no-first-run --no-service-autorun --password-store=basic')
options.user_data_dir = f'./tmp/test_undetected_chromedriver'
options.add_argument(f'--disable-gpu')
options.add_argument(f'--no-sandbox')
options.add_argument(f'--disable-dev-shm-usage')

driver = uc.Chrome(
    options=options,
    headless=False)
with driver:
    driver.get('https://nowsecure.nl')
    print(driver.page_source)

vdisplay.stop()