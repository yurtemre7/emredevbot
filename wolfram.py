from keys import WOLFRAM_ALPHA_API_KEY
from wolframalpha import Client

def wolframAPI(bot, cid, query):    
    client = Client(WOLFRAM_ALPHA_API_KEY)
    res = client.query(query)
    ans = next(res.results).text
    bot.sendMessage(cid, ans)

