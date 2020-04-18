import json
import os
import random
import time

from PyWebScraper import Scraper

from MeetupAPI.log import Log


class MeetupMessage():
    def __init__(self,
                 email,
                 password,
                 receiver_member_ids,
                 message,
                 json_placeholders=[],
                 save_log=True,
                 log_path='sent_messages_log.json',
                 spam_prevention=True,
                 spam_prevention_wait_time_minutes=1440,
                 test=False):
        self.logs = ['self.__init__']
        self.started = round(time.time())

        self.log('MeetupMessage()')

        # check if email and password entered
        if not (email and password):
            self.log('ERROR: Email and password required to send messages from your account, since Meetup doesnt have this feature yet in their API.')
            self.value = False

        else:
            self.receiver_member_ids = receiver_member_ids if type(
                receiver_member_ids) == list else [receiver_member_ids]
            self.message = self.message_without_placeholders(
                message, json_placeholders)
            self.messages_log = []

            self.boolean_save_log = save_log
            self.str_log_path = log_path
            self.boolean_spam_prevention = spam_prevention
            self.int_spam_prevention_wait_time_minutes = spam_prevention_wait_time_minutes

            # login on meetup
            self.log('-> Login into Meetup...')
            self.scraper = Scraper(url='https://secure.meetup.com/login/',
                                   scraper_type='selenium', auto_close_selenium=False)

            # click cookie consent
            time.sleep(random.randint(1, 6))
            self.scraper.selenium.find_element_by_css_selector(
                'a.margin-none:nth-child(1)').click()
            time.sleep(random.randint(1, 6))
            self.scraper.selenium.find_element_by_id('email').send_keys(email)
            time.sleep(random.randint(1, 6))
            self.scraper.selenium.find_element_by_id(
                'password').send_keys(password)
            self.scraper.selenium.find_element_by_id('loginFormSubmit').click()

            # check if scraper was redirected to landingpage or is still on login page (means something went wrong, robot check most likely)
            if self.scraper.selenium.current_url != 'https://www.meetup.com/':
                self.log(
                    'ERROR: Couldnt login into Meetup. Probably a "prove you are not a robot" test. To fix this: open a new "Private Window" in your web browser, login and solve the "I am not a robot" test. Then run Meetup().message() again.')
                self.scraper.selenium.save_screenshot(
                    'error_landingpage_not_loaded.png')
                self.scraper.selenium.close()
                self.value = False

            # open message window and send message/s, if spam test passed
            else:
                for receiver_id in self.receiver_member_ids:
                    if self.spam_check_passed(receiver_id, self.message) == False:
                        self.log(
                            'ERROR: Failed to send message. Seems you already messaged that member recently. Since spam prevention is active, the member didnt got messaged again.')

                    else:
                        self.log('-> Send message to {}'.format(receiver_id))
                        self.scraper.selenium.get(
                            'https://secure.meetup.com/messages/?new_convo=true&member_id={}'.format(receiver_id))
                        time.sleep(random.randint(2, 9))
                        textfield = self.scraper.selenium.find_element_by_id(
                            'messaging-new-convo')
                        textfield.click()
                        textfield.send_keys(self.message)
                        time.sleep(random.randint(1, 6))

                        if test:
                            self.scraper.selenium.save_screenshot(
                                'message_test.png')
                        else:
                            self.scraper.selenium.find_element_by_id(
                                'messaging-new-send').click()

                        # if last receiver id, close browser
                        if receiver_id == self.receiver_member_ids[-1]:
                            self.scraper.selenium.close()

                        # save that message was sent, to prevent spam
                        if not test and self.boolean_save_log:
                            self.messages_log.insert(0, {
                                'int_time_sent_unix': round(time.time()),
                                'str_receiver_member_id': receiver_id,
                                'str_message_sent': self.message
                            })
                            with open(self.str_log_path, 'w') as outfile:
                                json.dump(self.messages_log, outfile, indent=4)

                self.value = True

    def spam_check_passed(self, receiver_id, message):
        # see if person was already messaged the same message or already messaged within xx minutes, to prevent spam
        if self.boolean_save_log:
            if os.path.exists(self.str_log_path):
                with open(self.str_log_path) as json_file:
                    self.messages_log = json.load(json_file)

                    if self.boolean_spam_prevention:
                        for log_message in self.messages_log:
                            if log_message['str_receiver_member_id'] == receiver_id:
                                # check if member_id was messaged in the last xx minutes
                                if log_message['int_time_sent_unix'] >= (time.time()-(self.int_spam_prevention_wait_time_minutes*60)):
                                    return False

                                # check if member was already messaged with exactly the same message
                                if log_message['str_message_sent'] == message:
                                    return False

        return True

    def message_without_placeholders(self, message, json_placeholders):
        if not json_placeholders:
            return message

        for placeholder in json_placeholders:
            message = message.replace(
                '{{ '+placeholder['keyword']+' }}', placeholder['replace_with']).replace(
                '{{'+placeholder['keyword']+'}}', placeholder['replace_with'])

        return message

    def log(self, text):
        import os
        self.logs.append(text)
        Log().print('{}'.format(text), os.path.basename(__file__), self.started)
