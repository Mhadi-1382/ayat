
import requests
from .bale import TOKEN

def set_bale_webhook():
    """
    Run once after deployment.

    Example:
        python manage.py shell

        >>> from panel.bale_set_webhook import set_bale_webhook
        >>> set_bale_webhook()
    """

    url = (f"https://tapi.bale.ai/" f"bot{TOKEN}/setWebhook")
    response = requests.get(url, params={"url": ("https://ayat.chbkn.run/" "api/private/v1/bale/webhook/" )}, timeout=10)
    return response.json()
