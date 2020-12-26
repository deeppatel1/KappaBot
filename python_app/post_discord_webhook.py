from discord import Webhook, RequestsWebhookAdapter, Embed

WEBHOOKS_TO_POST = ["https://discordapp.com/api/webhooks/529864369824071691/7Wa0N516n6nMPdaJB78ex85PWi2loPq18IWij3LCUugVhOwMR8h8I_ROokrPIQShyxgs"]
# WEBHOOKS_TO_POST = ["https://discordapp.com/api/webhooks/792195748065574912/foWeFreUrk6CW82zJU3UxcBzz6qxKAWNNr4ZvvID45Ld-SDBgZxkm_1dg02HfY1cFeBF"]

def sendWebhookMessage(username: str, avatar_url: str, content=None):
    for webhook in WEBHOOKS_TO_POST:
        print("Sending to Webhook " +  str(webhook) + " content: " + str(content))
        send_the_message(username, avatar_url, webhook, content=content)


def sendWebhookListEmbeds(username: str, avatar_url: str, embeds, content=None):
    for webhook in WEBHOOKS_TO_POST:
        print("Sending an embed to " + str(webhook))
        send_the_message(username, avatar_url, webhook, content=None, embeds=embeds)


def send_the_message(username, avatar_url, webhook, content=None, embeds=None):
    print("sending to webhook " + webhook)
    webhook = Webhook.from_url(url = webhook, adapter = RequestsWebhookAdapter())
    print("Sending to Webhook " +  str(webhook) + " content: " + str(content))
    webhook.send(content, username=username, avatar_url=avatar_url)