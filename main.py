from selenium import webdriver
import time
import requests
from discord import Webhook, RequestsWebhookAdapter
import smtplib
import ssl


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

ID = 123
hook_token = 'abcd'
webhook = Webhook.partial(
    ID, hook_token, adapter=RequestsWebhookAdapter())

driver = webdriver.Safari()
driver.maximize_window()

driver.get('https://accounts.google.com/signin/v2/identifier?service=classroom&passive=1209600&continue=https%3A%2F%2Fclassroom.google.com%2F%3Femr%3D0&followup=https%3A%2F%2Fclassroom.google.com%2F%3Femr%3D0&flowName=GlifWebSignIn&flowEntry=ServiceLogin')

driver_mail = 'X@YZ.com'
driver_pass = '123'
# Email input
time.sleep(2)
text_box = driver.find_elements_by_xpath('//*[@id="identifierId"]')
text_box[0].send_keys(driver_mail)
button = driver.find_elements_by_xpath('//*[@id="identifierNext"]/div/button')
button[0].click()

# Password input
time.sleep(2)
text_box = driver.find_elements_by_xpath(
    '//*[@id="password"]/div[1]/div/div[1]/input')
text_box[0].send_keys(driver_pass)
button = driver.find_elements_by_xpath('//*[@id="passwordNext"]/div/button')
button[0].click()

time.sleep(14)
home_url = driver.current_url
classroom_xpaths = [
    ['CLP',
     '//*[@id="yDmH0d"]/div[2]/div/div[2]/div/ol/li[4]/div[1]/div[3]/h2/a[1]'],
    # ['M1',
    # 'x_path goes here'],
    # ['TCE',
    # 'x_path goes here'],
    ['CP',
     '//*[@id="yDmH0d"]/div[2]/div/div[2]/div/ol/li[2]/div[1]/div[3]/h2/a[1]'],
    ['BE',
     '//*[@id="yDmH0d"]/div[2]/div/div[2]/div/ol/li[6]/div[1]/div[3]/h2/a[1]'],
    ['BE Lab',
     '//*[@id="yDmH0d"]/div[2]/div/div[2]/div/ol/li[5]/div[1]/div[3]/h2/a[1]'],
    ['CP Lab',
     '//*[@id="yDmH0d"]/div[2]/div/div[2]/div/ol/li[3]/div[1]/div[3]/h2/a[1]'],
    ['Physics Lab',
     '//*[@id="yDmH0d"]/div[2]/div/div[2]/div/ol/li[1]/div[1]/div[3]/h2/a[1]']
]
classrooms_post_count = [-1 for x in classroom_xpaths]

while True:
    for i in range(len(classroom_xpaths)):
        if driver.current_url != home_url:
            driver.get(home_url)
            time.sleep(14)
        cr = driver.find_element_by_xpath(classroom_xpaths[i][1])
        try:
            cr.click()
        except:
            pass
        time.sleep(7)
        posts = driver.find_elements_by_class_name('n8F6Jd')
        if classrooms_post_count[i] == -1 or len(posts) == 0:
            print(f'{classroom_xpaths[i][0]} has {len(posts)} posts.')
            if len(posts) == 0:
                continue
            classrooms_post_count[i] = posts[0].text
        if classrooms_post_count[i] != posts[0].text:
            print(f'{classroom_xpaths[i][0]} has new posts.')
            webhook.send(
                f'{classroom_xpaths[i][0]} has new post(s).', username='Classroom-Notifier')
            send_mail(f'{classroom_xpaths[i][0]} has new post(s).')
            classrooms_post_count[i] = posts[0].text
    time.sleep(10)
