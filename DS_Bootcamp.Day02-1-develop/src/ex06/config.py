LOG_FILE = "analytics.log"
LOG_FORMAT = "%(asctime)s %(message)s"

TELEGRAM_CHAT_ID = "455782463"
TELEGRAM_API_URL = "https://api.telegram.org/bot7239112908:AAFPUFUbSueT2GFHgO6grzNJzejkqLLwKIM/sendMessage"

num_of_steps = 3

report_template = """
Report
We have made {observations} observations from tossing a coin: {tails} of them were tails and {heads} of them were heads. The probabilities are {tail_prob:.2f}% and {head_prob:.2f}%, respectively. Our forecast is that in the next {num_of_steps} observations we will have: {predicted_tails} tail(s) and {predicted_heads} head(s).
"""