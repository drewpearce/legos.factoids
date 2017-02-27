import logging
import random
from Legobot.Lego import Lego

logger = logging.getLogger(__name__)


class Factoids(Lego):
    def __init__(self, baseplate, lock, responses, *args, **kwargs):
        super().__init__(baseplate, lock)

        self.r = responses
        return

    def listening_for(self, message):
        if 'encourage me' in message['text']:
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
        txt = self.get_single_response(self.get_all_responses(self.r))
        self.reply(message, txt, opts)

    def get_name(self):
        return 'factoid'

    def get_help(self):
        help_text = "Helpful motivational quotes "\
                    "from influential figures such as Shia LeBouf, "\
                    "Courage Wolf, and your drill sergeant."
        return help_text

    def get_single_response(self, responses):
        response = random.choice(responses)  # nosec
        response = response.strip()
        logger.info(response)
        return response

    def get_all_responses(self, infile):
        with open(infile, 'r') as f:
            content = f.readlines()
        logger.info(content)
        return content
