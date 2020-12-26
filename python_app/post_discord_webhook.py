from discord import Webhook, RequestsWebhookAdapter, Embed

WEBHOOKS_TO_POST = ["https://discordapp.com/api/webhooks/529864369824071691/7Wa0N516n6nMPdaJB78ex85PWi2loPq18IWij3LCUugVhOwMR8h8I_ROokrPIQShyxgs"]
# WEBHOOKS_TO_POST = ["https://discordapp.com/api/webhooks/792195748065574912/foWeFreUrk6CW82zJU3UxcBzz6qxKAWNNr4ZvvID45Ld-SDBgZxkm_1dg02HfY1cFeBF"]

def sendWebhookMessage(username: str, avatar_url: str, content=None):
    for webhook in WEBHOOKS_TO_POST:
        webhook = Webhook.from_url(url = webhook, adapter = RequestsWebhookAdapter())
        print("Sending to Webhook " +  webhook + " content: " + content)
        webhook.send(content, username=username, avatar_url=avatar_url)


def sendWebhookListEmbeds(username: str, avatar_url: str, embeds, content=None):
    for webhook in WEBHOOKS_TO_POST:
        webhook = Webhook.from_url(url = webhook, adapter = RequestsWebhookAdapter())

        print("Sending an embed to " + webhook)
        webhook.send(content, username=username, avatar_url=avatar_url, embeds=embeds)
