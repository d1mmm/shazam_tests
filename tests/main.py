from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import unittest
import time

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class ShazamTests(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
        })
        self.driver = webdriver.Chrome(options=options)
        self.driver.get("https://www.shazam.com/")
        self.driver.maximize_window()

    def test_search_music_by_name(self):
        driver = self.driver
        driver.find_element(By.CLASS_NAME, "Search_icon__Poc_G").click()
        search_box = driver.find_element(By.CLASS_NAME, "Search_input__HkJTl")
        search_box.send_keys("Shape of You")
        time.sleep(2)
        search_box.send_keys(Keys.RETURN)
        time.sleep(2)

        try:
            title = driver.title
            artist = ' '.join(title.split()[4:6])
            song_text = driver.find_element(By.CLASS_NAME, "Lyrics_lyrics__f3QkJ").text

            print("Information about track:")
            print(f"Title: {title}")
            print(f"Artist: {artist}")
            print(f"Song text: {' '.join(song_text.split()[1:])}")

            self.assertTrue(title and artist, "Main information about track was not find")
        except Exception as e:
            self.fail(f"Could not find full track information: {e}")

    def test_check_chrome_extension(self):
        driver = self.driver
        try:
            driver.find_element(By.CSS_SELECTOR, 'a[data-test-id="home_userevent_headerElement_appsMenu"]').click()
            time.sleep(2)
            chrome_ext = driver.find_element(By.CLASS_NAME,'AppsPage_browserLink__YK5zW')
            driver.execute_script("arguments[0].scrollIntoView(); window.scrollBy(0, -100)", chrome_ext)
            chrome_ext.click()
            driver.find_element(By.CLASS_NAME, "UywwFc-vQzf8d").click()
            self.assertIn("chromewebstore.google.com", driver.current_url, "Chrome extension page did not load")
        except Exception as e:
            self.fail("The Chrome Extension option is not available or the site structure has changed")

    def test_find_concert_for_artist(self):
        driver = self.driver
        try:
            driver.find_element(By.CSS_SELECTOR, 'a[data-test-id="home_userevent_headerElement_concertsMenu"]').click()
            time.sleep(2)
            input = driver.find_element(By.CSS_SELECTOR, "input[placeholder='Artists or bands']")
            input.click()
            input.send_keys("Boombox")
            time.sleep(2)
            input.send_keys(Keys.RETURN)
            time.sleep(2)

            results = driver.find_elements(By.CLASS_NAME, "page_resultList__f_5d8")
            self.assertGreater(len(results), 0, "No results found for 'Boombox'")

            print(f"Result found:\n{results[0].text}")
        except Exception as e:
            self.fail(f"The section with concerts for the artist was not found or the site structure has changed: {e}")

    def test_search_music(self):
        driver = self.driver
        shazam_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "FloatingShazamButton_shazamButton__WD_TY"))
        )
        shazam_button.click()
        try:
            time.sleep(10)

            self.assertTrue(driver.title, "Main information about track was not find")
            print(f"Information about track: {driver.title}")
        except Exception as e:
            print(f"Unable to retrieve track information: {e}")

    def test_get_top_song(self):
        driver = self.driver
        try:
            driver.find_element(By.CSS_SELECTOR, 'a[data-test-id="home_userevent_headerElement_chartsMenu"]').click()
            time.sleep(2)
            first_track = driver.find_element(By.CLASS_NAME, "SongItem-module_mainItemsContainer__9MRor").text
            title = ' '.join(first_track.split()[0:2])
            artist = ''.join(first_track.split()[2])

            self.assertTrue(title and artist, "Main information about track was not find")

            print("First track on the page:")
            print(f"Title: {title}")
            print(f"Artist: {artist}")

        except Exception as e:
            self.fail(f"Failed to get top song info {e}")

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
