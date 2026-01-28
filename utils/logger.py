# panini_engine/utils/logger.py

import logging
import os


def setup_logger(name="PaniniEngine"):
    """
    इंजन के लिए एक मानक लॉगर सेटअप करता है।
    यह 'Debug' मोड में काम करेगा ताकि हर सूत्र का प्रभाव ट्रैक हो सके।
    """
    logger = logging.getLogger(name)

    # यदि लॉगर पहले से सेटअप है, तो दोबारा न करें
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)

    # १. कंसोल हैंडलर (Output for Terminal)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.INFO)

    # २. फाइल हैंडलर (For Surgical History/Audit)
    log_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'panini_engine.log')
    f_handler = logging.FileHandler(log_path, encoding='utf-8')
    f_handler.setLevel(logging.DEBUG)

    # ३. फॉर्मेटिंग (दिखने में कैसा होगा)
    # [समय] - [लेवल] - [मेसेज]
    format_str = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(format_str)
    f_handler.setFormatter(format_str)

    # ४. हैंडलर्स को जोड़ना
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger


# इंजन में उपयोग के लिए एक डिफ़ॉल्ट इंस्टेंस
engine_logger = setup_logger()