import json
import os
import random
import time

from PyWebScraper import Scraper

from MeetupAPI.log import Log


class MeetupMessage():
    def __init__(self,
                 receiver_members,
                 message,
                 json_placeholders=[],
                 save_log=True,
                 log_path='sent_messages_log.json',
                 spam_prevention=True,
                 spam_prevention_wait_time_minutes=1440,
                 test=False,
                 auto_close_selenium=True,
                 scraper=None,
                 ):
        self.logs = ['self.__init__']
        self.started = round(time.time())
        self.scraper = scraper

        self.log('MeetupMessage()')

        if self.reached_limit_for_today == True:
            self.log('ERROR: You reached the maximum limit of sent messages per day. This limit is in your own interest, to prevent you from getting blocked by Meetup.')
            if self.scraper.selenium:
                self.scraper.selenium.close()
            self.value = False, None

        else:
            self.receiver_members = receiver_members if type(
                receiver_members) == list else [receiver_members]
            self.message = self.message_without_placeholders(
                message, json_placeholders)
            self.messages_log = []

            self.boolean_save_log = save_log
            self.str_log_path = log_path
            self.boolean_spam_prevention = spam_prevention
            self.int_spam_prevention_wait_time_minutes = spam_prevention_wait_time_minutes

            if not self.scraper:
                # login on meetup
                self.log('A web browser will pop up in a second. Enter your login data there, solve the "I am not a robot" test (if it shows up) and click on "Login".')
                self.scraper = Scraper(url='https://secure.meetup.com/login/',
                                       scraper_type='selenium', headless=False, auto_close_selenium=False)

                # check if user loggedin, then continue
                while self.scraper.selenium.current_url != 'https://www.meetup.com/':
                    time.sleep(0.5)

            # open message window and send message/s, if spam test passed
            for receiver in self.receiver_members:
                if self.spam_check_passed(receiver['id'], self.message) == False:
                    self.log(
                        'ERROR: Failed to send message. Seems you already messaged {} recently. Since spam prevention is active, {} didnt got messaged again.'.format(receiver['name'], receiver['name']))

                elif self.on_ignore_list(receiver['name']) == True:
                    self.log('ERROR: User {} is on ignore_receivers.json list. Therefore there was no message sent to user.'.format(
                        receiver['name']))

                else:
                    self.log(
                        '-> Send message to {}'.format(receiver['name']))
                    self.scraper.selenium.get(
                        'https://secure.meetup.com/messages/?new_convo=true&member_id={}'.format(receiver['id']))
                    time.sleep(random.randint(2, 9))
                    textfield = self.scraper.selenium.find_element_by_id(
                        'messaging-new-convo')
                    self.scraper.selenium.execute_script(
                        "arguments[0].scrollIntoView();", textfield)
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
                    if auto_close_selenium and (receiver == self.receiver_members[-1]):
                        self.scraper.selenium.close()

                    # save that message was sent, to prevent spam
                    if not test and self.boolean_save_log:
                        self.messages_log.insert(0, {
                            'int_time_sent_unix': round(time.time()),
                            'str_receiver_member_id': receiver['id'],
                            'str_receiver_member_name': receiver['name'],
                            'str_message_sent': self.message
                        })
                        with open(self.str_log_path, 'w') as outfile:
                            json.dump(self.messages_log,
                                      outfile, indent=4)

                        self.log('Sent message to {}'.format(
                            receiver['name']))

            self.value = True, self.scraper

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

    def on_ignore_list(self, receiver_name):
        if os.path.exists('ignore_receivers.json'):
            with open('ignore_receivers.json') as json_file:
                ignored_receivers = json.load(json_file)

                for keyword in ignored_receivers:
                    if keyword in receiver_name:
                        return True

        return False

    def reached_limit_for_today(self):
        if os.path.exists(self.str_log_path):
            with open(self.str_log_path) as json_file:
                self.messages_log = json.load(json_file)

                sent_messages_in_last_24_hours = 0

                # count existing messages from last 24 hours and see if limit is reached
                for log_message in self.messages_log:
                    if log_message['int_time_sent_unix'] >= (time.time()-24*60*60):
                        sent_messages_in_last_24_hours += 1

                        if sent_messages_in_last_24_hours == 20:
                            return True

        return False

    def log(self, text):
        import os
        self.logs.append(text)
        Log().print('{}'.format(text), os.path.basename(__file__), self.started)
