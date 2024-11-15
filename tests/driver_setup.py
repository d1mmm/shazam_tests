from selenium import webdriver

def get_driver():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "profile.default_content_setting_values.media_stream_mic": 1,
    })
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver
