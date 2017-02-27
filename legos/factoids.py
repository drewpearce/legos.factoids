import logging
import random
from Legobot.Lego import Lego

logger = logging.getLogger(__name__)


class Factoids(Lego):
    def __init__(self, baseplate, lock, triggers, responses, *args, **kwargs):
        super().__init__(baseplate, lock)

        self.t = triggers
        self.r = responses
        return

    def listening_for(self, message):
        triggers_list = self.get_all_file_items(self.t)
        for trigger in triggers_list:
            if trigger in message['text']:
                logger.info('Lego %s activated' % self.get_name())
                return True

    def handle(self, message):
        opts = None
        logger.info(message)
        try:
            target = message['metadata']['source_channel']
            opts = {'target': target}
        except IndexError:
            logger.error('Could not identify message source in message: %s'
                         % str(message))
        txt = self.get_single_response(self.get_all_file_items(self.r))
        self.reply(message, txt, opts)

    def get_name(self):
        return 'factoid'

    def get_help(self):
        help_text = "Returns random response from supplied list in response "\
                    "to triggers from supplied list of trigger."
        return help_text

    def get_single_response(self, responses):
        response = random.choice(responses)  # nosec
        response = response.strip()
        logger.info(response)
        return response

    def get_all_file_items(self, infile):
        with open(infile, 'r') as f:
            content = f.read().splitlines()
        logger.info(content)
        return content
