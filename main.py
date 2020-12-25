from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from discord import Webhook, RequestsWebhookAdapter
import smtplib
import ssl
import os


def send_mail(msg):
    port = 465
    context = ssl._create_unverified_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        sender_email = "XYZ@gmail.com"
        sender_pass = "123"
        # notifier-subs
        receiver_emails = ["ABC@gmail.com", "DEF@gmail.com"]
        server.login(sender_email, sender_pass)
        try:
            server.sendmail(sender_email, receiver_emails, msg)
            print("Successfully sent email")
        except:
            print("Error: unable to send email")


def hold(driver, timeout, element_id, choice):
    opt = [By.XPATH, By.CLASS_NAME]
    try:
        print(
            f'Holding for {"..." if len(element_id) > 20 else ""}{element_id[(len(element_id)-20):]} on {driver.current_url[8:30]}...')
        element_present = EC.element_to_be_clickable((opt[choice], element_id))
        WebDriverWait(driver, timeout).until(element_present)
        print(f'{element_id} found.\n')
    except TimeoutException:
        print("Timed out waiting for page to load")


ID = 123
hook_token = 'abcd'
webhook = Webhook.partial(
    ID, hook_token, adapter=RequestsWebhookAdapter())
ID_debug = 456
hook_token_debug = 'efgh'
webhook_debug = Webhook.partial(
    ID_debug, hook_token_debug, adapter=RequestsWebhookAdapter())

op = webdriver.ChromeOptions()
op.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
op.add_argument("--headless")
op.add_argument(
    '--user-agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')
op.add_argument("--no-sandbox")
op.add_argument("--disable-dev-sh-usage")

driver = webdriver.Chrome(executable_path=os.environ.get(
    'CHROMEDRIVER_PATH'), options=op)
# driver = webdriver.Chrome(executable_path="./chromedriver87", options=op)
driver.maximize_window()

driver.get('https://accounts.google.com/signin/v2/identifier?service=classroom&passive=1209600&continue=https%3A%2F%2Fclassroom.google.com%2F%3Femr%3D0&followup=https%3A%2F%2Fclassroom.google.com%2F%3Femr%3D0&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

driver_mail = 'X@YZ.com'
driver_pass = '123'
# Email input
hold(driver, 100, '//*[@id="identifierId"]', 0)
text_box = driver.find_elements_by_xpath('//*[@id="identifierId"]')
text_box[0].send_keys(driver_mail)
button = driver.find_elements_by_xpath('//*[@id="identifierNext"]/div/button')
button[0].click()

# Password input
hold(driver, 100, '//*[@id="password"]/div[1]/div/div[1]/input', 0)
text_box = driver.find_elements_by_xpath(
    '//*[@id="password"]/div[1]/div/div[1]/input')
text_box[0].send_keys(driver_pass)
button = driver.find_elements_by_xpath('//*[@id="passwordNext"]/div/button')
button[0].click()

home_url = driver.current_url
classroom_xpaths = [
    ['CLP',
     '//*[@id="yDmH0d"]/div[2]/div[1]/div[2]/div/ol/li[5]/div[1]/div[3]/h2/a[1]'],
    ['M1',
     '//*[@id="yDmH0d"]/div[2]/div[1]/div[2]/div/ol/li[1]/div[1]/div[3]/h2/a[1]'],
    # ['TCE',
    # 'x_path goes here'],
    ['CP',
     '//*[@id="yDmH0d"]/div[2]/div[1]/div[2]/div/ol/li[3]/div[1]/div[3]/h2/a[1]'],
    ['BE',
     '//*[@id="yDmH0d"]/div[2]/div[1]/div[2]/div/ol/li[7]/div[1]/div[3]/h2/a[1]'],
    ['BE Lab',
     '//*[@id="yDmH0d"]/div[2]/div[1]/div[2]/div/ol/li[6]/div[1]/div[3]/h2/a[1]'],
    ['CP Lab',
     '//*[@id="yDmH0d"]/div[2]/div[1]/div[2]/div/ol/li[4]/div[1]/div[3]/h2/a[1]'],
    ['Physics Lab',
     '//*[@id="yDmH0d"]/div[2]/div[1]/div[2]/div/ol/li[2]/div[1]/div[3]/h2/a[1]']
]
classrooms_post_count = [-1 for x in classroom_xpaths]

while True:
    for i in range(len(classroom_xpaths)):
        if driver.current_url != home_url:
            driver.get(home_url)
        hold(driver, 100, classroom_xpaths[i][1], 0)
        cr = driver.find_element_by_xpath(classroom_xpaths[i][1])
        try:
            cr.click()
        except:
            pass
        hold(driver, 10, 'n8F6Jd', 1)
        temp_posts = driver.find_elements_by_class_name('n8F6Jd')
        posts = [temp_posts[i].find_element_by_xpath(
            './div[1]') for i in range(len(temp_posts))]
        if classrooms_post_count[i] == -1 or len(posts) == 0:
            print(f'{classroom_xpaths[i][0]} has {len(posts)} posts.\n')
            if len(posts) == 0:
                continue
            try:
                webhook_debug.send(
                    f'<@USER-ID> {classroom_xpaths[i][0]} initialisation:\n```{posts[0].text}```', username='Debug-Andy')
            except:
                webhook_debug.send(
                    f'<@USER-ID> {classroom_xpaths[i][0]} initialisation:\n```Exceeds discord character limit```', username='Debug-Andy')
            classrooms_post_count[i] = posts[0].text
        if classrooms_post_count[i] != posts[0].text:
            print(f'old\n{classrooms_post_count[i]}\nnew\n{posts[0].text}\n')
            try:
                webhook_debug.send(
                    f'<@USER-ID> {classroom_xpaths[i][0]} changelog:\nOld:\n```{classrooms_post_count[i]}```\nNew:\n```{posts[0].text}```', username='Debug-Andy')
            except:
                webhook_debug.send(
                    f'<@USER-ID> {classroom_xpaths[i][0]} changelog:\n```Exceeds discord character limit```', username='Debug-Andy')
            print(f'{classroom_xpaths[i][0]} has new posts.\n')
            webhook.send(
                f'{classroom_xpaths[i][0]} has new post(s)/edit(s).', username='Classroom-Notifier')
            send_mail(f'{classroom_xpaths[i][0]} has new post(s)/edit(s).')
            classrooms_post_count[i] = posts[0].text
    time.sleep(10)
