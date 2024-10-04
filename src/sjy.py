from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Refine string
refine_dict = { '&nbsp;': ' ', 
    '\\\'': '\'', '\\\"': '\"',
    '&gt;': ' ', '&it;': ' ', '&amp': ' ', '&lt;': '',
    '병신': '##', '존나': '##', '지랄': '##', '좆': '#', '좇': '#', '씹': '#'
}
def refine_string(string):
    for key, value in refine_dict.items():
        string = string.replace(key, f"{value}")
    return string

def login(driver, id='hckim', pw='hckim'):
    # Open chrome driver
    driver.get('http://jaeyongsong.com/bsr/login.php')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="sub_div"]/div/div/div/form/p'))
    )

    # Find input area
    login_id = driver.find_element(By.XPATH, '//*[@id="login_id"]')
    login_pw = driver.find_element(By.XPATH, '//*[@id="login_pw"]')
    login_btn = driver.find_element(By.XPATH, '//*[@id="sub_div"]/div/div/div/form/fieldset/input[3]')

    # Login
    login_id.send_keys(id)
    login_pw.send_keys(pw)
    login_btn.click()

    # Wait unril main page load
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="visual"]')) )

def logout(driver):
    # Open chrome driver
    driver.get('http://jaeyongsong.com/bsr/logout.php')

# lab_board_write
# Write lab board contents. Get title, content, date and write content as [title / content\n\ndate]
def lab_board_write(driver, title, content, date):
    # Open chrome driver
    driver.get('http://jaeyongsong.com/bsr/board.php?bo_table=lab')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="fboardlist"]/div[3]/div/ul/li/a')) )

    # Press write button
    write_btn = driver.find_element(By.XPATH, '//*[@id="fboardlist"]/div[3]/div/ul/li/a')
    write_btn.click()
    
    # Title
    title_inp = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="wr_subject"]')) )
    title_inp.send_keys(title)

    # Switch to iframe
    up_iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="fwrite"]/div[3]/div/iframe')) )
    driver.switch_to.frame(up_iframe)
    iframe = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="se2_iframe"]')) ) 
    driver.switch_to.frame(iframe)

    # Content
    content_area = driver.find_element(By.CSS_SELECTOR, "body > p")
    content_area.send_keys(content + '\n\n작성일:' + date)

    # Return to default content
    driver.switch_to.default_content()

    # Submit
    submit_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="btn_submit"]')) )
    submit_btn.click()

    # Wait until main page loaded
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="sub_div"]/div')))
    
    # Go to main page
    driver.get('http://jaeyongsong.com')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="visual"]')) )

# album_write
# Write album content. get title, list of image, list of comments, image folder
def album_write(driver, title="This is album title", image_lst = ['002.jpg', '005.jpg'], comment_lst=['Sample comment 1', '005 image'], date='2005-10-13', image_src='C:/Users/aaa86/OneDrive/바탕 화면/sjy/data/refine/image'):
    # Open chrome driver
    driver.get('http://jaeyongsong.com/bsr/board.php?bo_table=album')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="fboardlist"]/div[2]/div/ul/li/a')) )

    # Press write button
    write_btn = driver.find_element(By.XPATH, '//*[@id="fboardlist"]/div[2]/div/ul/li/a')
    write_btn.click()
    
    # Title
    title_inp = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="wr_subject"]')) )
    title_inp.send_keys(title)

    # Image
    def put_image(file):
        # Select iframe
        up_iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="fwrite"]/div[3]/div/iframe')) )
        driver.switch_to.frame(up_iframe)

        # Open popup window
        popup_tn = driver.find_element(By.XPATH, '//*[@id="se2_tool"]/div/ul[7]/li/button')
        popup_tn.click()
        WebDriverWait(driver, 20).until(EC.number_of_windows_to_be(2))

        # Save current window and switch window
        original_window = driver.current_window_handle
        for window_handle in driver.window_handles:
            if window_handle != original_window:
                driver.switch_to.window(window_handle)
                break

        # Upload file
        upload_inp = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="fileupload"]')))
        upload_inp.send_keys(file)

        # Wait until image loaded
        WebDriverWait(driver, 60).until(
            EC.invisibility_of_element_located((By.XPATH, "//img[@class='pre_thumb' and @src='./img/loading.gif']")))
        time.sleep(0.1)

        # Submit
        submit_btn = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="img_upload_submit"]')))
        submit_btn.click()

        # Return to original window
        driver.switch_to.window(original_window)

    # Content
    def put_content(content):
        # Switch to iframe
        up_iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="fwrite"]/div[3]/div/iframe')) )
        driver.switch_to.frame(up_iframe)
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="se2_iframe"]')) ) 
        driver.switch_to.frame(iframe)

        # Content
        content_area = driver.find_element(By.CSS_SELECTOR, "body > p")
        content_area.send_keys(content)

        # Return to default content
        driver.switch_to.default_content()

    for img, txt in zip(image_lst, comment_lst):
        put_image(f'{image_src}/{img}')
        put_content(f'\n{txt}\n')
    put_content(f'\n\n작성일: {date}')
    
    # Submit
    submit_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="btn_submit"]')) )
    submit_btn.click()

    # Wait until main page loaded
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="sub_div"]/div')))
    
    # Go to main page
    driver.get('http://jaeyongsong.com')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="visual"]')) )
    
# Column write
# Write column
def column_write(driver, title="This is title", content="This is content", url="www.naver.com", date="2005-10-13"):
    # Open chrome driver
    driver.get('http://jaeyongsong.com/bsr/board.php?bo_table=column')

    # Press write button
    write_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="fboardlist"]/div[3]/div/ul/li/a')) )
    write_btn.click()
    
    # Title
    title_inp = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="wr_subject"]')) )
    title_inp.send_keys(title)

    # Image
    def put_url(url):
        # Select iframe
        up_iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="fwrite"]/div[3]/div/iframe')) )
        driver.switch_to.frame(up_iframe)

        # Open popup window
        url_btn = driver.find_element(By.XPATH, '//*[@id="se2_tool"]/div/ul[6]/li[1]/button')
        url_btn.click()

        # Upload file
        url_inp = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="se2_tool"]/div/ul[6]/li[1]/div/div/div/input')))
        url_inp.send_keys(url)

        # Submit
        submit_btn = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="se2_tool"]/div/ul[6]/li[1]/div/div/div/button[1]')))
        submit_btn.click()

        # Return to default content
        driver.switch_to.default_content()

    # Content
    def put_content(content):
        # Switch to iframe
        up_iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="fwrite"]/div[3]/div/iframe')) )
        driver.switch_to.frame(up_iframe)
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="se2_iframe"]')) ) 
        driver.switch_to.frame(iframe)

        # Content
        content_area = driver.find_element(By.CSS_SELECTOR, "body > p")
        content_area.send_keys(content)

        # Return to default content
        driver.switch_to.default_content()

    put_content(f'{content}\n')
    if len(str(url)) > 3: put_url(url)
    put_content(f'\n\n작성일: {date}')
    
    # Submit
    submit_btn = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="btn_submit"]')) )
    submit_btn.click()

    # Wait until main page loaded
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="sub_div"]/div')))
    
    # Go to main page
    driver.get('http://jaeyongsong.com')
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="visual"]')) )
    
if __name__ == '__main__':
    driver = webdriver.Chrome()
    login(driver, id='jsong', pw='jsong')
    time.sleep(3)
    column_write(driver)
    time.sleep(3)
    logout(driver)
    time.sleep(3)