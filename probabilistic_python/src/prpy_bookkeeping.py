## borrowed from source: "https://docs.python.org/2/howto/logging.html#logging-basic-tutorial"
import logging

logging.basicConfig(filename='probpy.log', level=logging.INFO)

def log_prefixer(script):
    def loginfo(text):
        logging.info(script + ": " + text)
    return(loginfo)

