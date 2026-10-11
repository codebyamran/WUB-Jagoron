#!/usr/bin/env python3
"""Builds the Jagoron Digital Guide: docs/index.html (GitHub Pages) and docs/downloads/*.pdf from ONE source.
Usage:  python build.py            -> draft build (shows a DRAFT banner if contacts are unverified/unfilled)
        python build.py --release  -> refuses to build until every contact is verified and filled in
"""
import json, sys, os, html, datetime
ROOT=os.path.dirname(os.path.abspath(__file__)); DOCS=os.path.join(ROOT,"docs")
CFG=json.load(open(os.path.join(ROOT,"config.json"),encoding="utf-8"))
RELEASE="--release" in sys.argv
e=lambda t: html.escape(t,quote=True)

# ---------- readiness checks ----------
unverified=[c for c in CFG["national_contacts"] if not c.get("verified")]
unfilled=[c for c in CFG["campus_contacts"] if not c["contact"].strip()]
draft=bool(unverified or unfilled)
if RELEASE and draft:
    print("RELEASE BLOCKED:")
    for c in unverified: print("  - not verified:",c["number"],c["label"])
    for c in unfilled: print("  - campus contact empty:",c["role"])
    print('Edit config.json (set "verified": true after checking each number, and fill the campus contacts).'); sys.exit(1)

# ---------- icons ----------
ICON={
"eye":'<path d="M-22 0 Q0 -20 22 0 Q0 20 -22 0 Z"/><circle r="6"/>',
"lock":'<rect x="-15" y="-3" width="30" height="23" rx="4"/><path d="M-8 -3 V-10 A8 8 0 0 1 8 -10 V-3"/>',
"window":'<rect x="-21" y="-17" width="42" height="34" rx="4"/><path d="M-21 -7 H21"/><path d="M-9 5 L-3 11 L9 -1"/>',
"warning":'<path d="M0 -22 L22 18 H-22 Z"/><path d="M0 -8 V5"/><circle cy="12" r="1.5"/>',
"hand":'<path d="M-10 18 V-4 M-4 18 V-14 M2 18 V-14 M8 18 V-8 M-10 -4 L-14 -8"/>',
"megaphone":'<path d="M-18 -6 H-6 L14 -18 V18 L-6 6 H-18 Z"/><path d="M-12 6 V18 H-4 V8"/>',
"quiz":'<circle r="19"/><path d="M-6 -6 A6 6 0 1 1 3 -1 C0 1 0 3 0 5"/><circle cy="12" r="1.2"/>',
"scale":'<path d="M0 -20 V18 M-14 18 H14 M-18 -8 H18"/><path d="M-18 -8 L-24 4 H-12 Z M18 -8 L12 4 H24 Z"/>',
"download":'<path d="M0 -18 V10 M-10 2 L0 12 L10 2 M-18 18 H18"/>',
"share":'<circle cx="-12" r="5"/><circle cx="12" cy="-12" r="5"/><circle cx="12" cy="12" r="5"/><path d="M-8 -2 L8 -10 M-8 2 L8 10"/>',
}
def ic(n,s=22): return f'<svg class="ic" width="{s}" height="{s}" viewBox="-26 -26 52 52" fill="none" stroke="currentColor" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[n]}</svg>'
LOGO='''<svg class="logo" viewBox="0 0 100 100" aria-hidden="true"><defs><clipPath id="sh"><path d="M50 4 L88 18 V50 C88 74 70 90 50 98 C30 90 12 74 12 50 V18 Z"/></clipPath></defs><g clip-path="url(#sh)"><rect x="12" width="19" height="100" fill="#E5484D"/><rect x="31" width="19" height="100" fill="#F5A524"/><rect x="50" width="19" height="100" fill="#2EAD6B"/><rect x="69" width="19" height="100" fill="#3B82F6"/></g><g transform="translate(50 52) scale(.78) translate(-50 -52)"><path d="M50 4 L88 18 V50 C88 74 70 90 50 98 C30 90 12 74 12 50 V18 Z" fill="#0B1B3A"/></g><path d="M27 50 Q50 31 73 50 Q50 69 27 50 Z" fill="none" stroke="#fff" stroke-width="3.5" stroke-linejoin="round"/><circle cx="50" cy="50" r="8" fill="#fff"/><circle cx="50" cy="50" r="3.5" fill="#0B1B3A"/></svg>'''

# ---------- QR ----------
qr_svg=""
if CFG["site_url"].strip():
    import qrcode, qrcode.image.svg
    img=qrcode.make(CFG["site_url"].strip(),image_factory=qrcode.image.svg.SvgPathImage,box_size=10,border=2)
    os.makedirs(DOCS,exist_ok=True); img.save(os.path.join(DOCS,"qr.svg"))
    qr_svg=open(os.path.join(DOCS,"qr.svg"),encoding="utf-8").read().split("?>",1)[-1]
    qr_svg=qr_svg.replace("<svg ",'<svg class="qr" role="img" aria-label="QR code for this guide" ',1)
QRBOX=qr_svg or '<div class="qr qrph">QR code appears here after you set "site_url" in config.json and rebuild</div>'

# ---------- content ----------
PRIV=["My Facebook or Instagram profile is not public to strangers","Only people I choose can see my phone number","Only people I choose can see my email","Strangers cannot send me messages","My friend list is not public","Not everyone can tag me","Location sharing is off unless an app really needs it","I know which apps can use my location","I know which apps can use my camera and microphone","I only share what I'd put on a university notice board"]
DEV=["PIN or password is on","Fingerprint or face unlock is on","Auto-lock is set to 30 seconds or 1 minute","Phone software is updated","Apps are updated","Find My Device (Android) or Find My (iPhone) is on","WhatsApp two-step verification is on","2FA is on for email, Facebook and my university account","Lock-screen notifications hide private content"]
DAMAGE=[("Message your contacts","\"Brother, I'm in an emergency. Please send BDT 5,000 to this number.\""),("Open your email","and reset your other accounts"),("See your private photos","a serious privacy violation"),("Open payment apps","and try unauthorised transactions"),("Change your settings","and lock you out"),("Post as you","and damage your reputation")]
ALT=[("Documents","LibreOffice","FOSS","libreoffice.org","https://www.libreoffice.org"),("Photo editing","GIMP","FOSS","gimp.org","https://www.gimp.org"),("Vector graphics","Inkscape","FOSS","inkscape.org","https://inkscape.org"),("3D and animation","Blender","FOSS","blender.org","https://www.blender.org"),("Video editing","Kdenlive","FOSS","kdenlive.org","https://kdenlive.org"),("Video editing","DaVinci Resolve (free version)","Free","blackmagicdesign.com","https://www.blackmagicdesign.com/products/davinciresolve")]
CARDS=[
("Privacy","A stranger sends you a friend request. You share 3 mutual friends.",["Accept: you have mutual friends","Accept, then look at their profile","Check their profile and ask a mutual friend first","Accept and send them your number"],2,"Fake accounts add real friends to look genuine. Check how old the profile is and what it posts, and ask first.","B feels safe, but by then they can already see your posts."),
("Privacy","A photo-editing app asks for your camera, contacts and location.",["Allow everything so it works","Allow only what editing needs","Allow all now, check later","Use it without reading anything"],1,"An app should get only what it needs to do its job. A photo editor does not need your contacts or location.","C: \"later\" rarely comes."),
("Privacy","A friend posts a photo of you that you don't like.",["Post an embarrassing photo of them","Ask them to remove it; untag or report if they refuse","Say nothing and hope it goes away","Comment angrily under the post"],1,"Start with a calm request. You can untag yourself and report the post if it is not removed.","D: anger in public makes it spread."),
("Device","Your phone has said \"Update available\" for 3 weeks.",["Ignore it; the phone works fine","Update it: updates fix known security holes","Wait for the next version","Turn off update notifications"],1,"Attackers use known holes in old versions. Updating closes them.","A: \"works fine\" means you can't see the problem."),
("Device","You lose your phone and it has no screen lock.",["Hope an honest person finds it","Lock it with Find My Device, change passwords from another device","Wait a few days before doing anything","Only block the SIM"],1,"Lock or erase it remotely, then change your email and social passwords. Add a screen lock to your next phone.","D: blocking the SIM does not protect your apps and accounts."),
("Device","A friend's WhatsApp says: \"Urgent! I need BDT 3,000. Send it now.\"",["Send it immediately","Reply on WhatsApp and ask why","Call your friend another way to confirm","Forward it to see if others know"],2,"Their account may be hacked, and a reply goes to the attacker. A call confirms who it really is.","B: replying keeps you talking to the attacker."),
("Software","A friend gives you a \"pre-activated\" version of expensive software.",["Install it immediately","Turn off antivirus first","Look for a legitimate or free alternative","Ask someone to send another crack"],2,"You can't know what was changed inside it. A free or student version is safer.","B: switching off protection is often the first step of an attack."),
("Software","A download site tells you to disable your antivirus before installing.",["Disable it and continue","Stop. That is a red flag","Disable it for five minutes only","Ask a friend to install it for you"],1,"Legitimate software never needs your protection switched off.","C: five minutes is enough for malware to settle in."),
("Upstander","An edited photo of a classmate is going around a group chat.",["Share it; it's funny","Don't share; save evidence, support them and report","Ignore it; it's not your problem","Comment \"haha\" so you don't look soft"],1,"Sharing makes you part of it. Saving evidence and supporting them helps, and reporting can stop it.","D: a laugh still spreads it and hurts them."),
("Upstander","A fake account is using your friend's name and photo.",["Ignore it","Follow it to see what happens","Tell your friend, report the account and use the report routes","Message the fake account to threaten them"],2,"Your friend needs to know. Reports from several people can speed up removal.","D: threatening back can make things worse and put you at risk."),
]
CATCOL={"Privacy":"blue","Device":"green","Software":"amber","Upstander":"violet"}
L="ABCD"

# ---------- html pieces ----------
def chips(items): return '<ul class="four">'+"".join(f'<li class="c-{c}"><b>{w}</b><span>{d}</span></li>' for w,c,d in items)+'</ul>'
FOUR=[("STOP","red","Don't react immediately."),("CHECK","amber","Is this message, link, software, account or request trustworthy?"),("SECURE","green","Fix your device, account and privacy settings."),("SWITCH","blue","Choose safer behaviour and legitimate or open-source alternatives.")]
def sec(id_,col,icon,kicker,title,body): return f'<section id="{id_}" class="sec s-{col}"><header class="sh"><span class="badge">{ic(icon,26)}</span><div><p class="kick">{kicker}</p><h2>{title}</h2></div></header>{body}</section>'

draft_banner='<div class="draft" role="note"><b>DRAFT.</b> Contact details have not been verified or filled in yet. Do not share this version.</div>' if draft else ""

priv_rows="".join(f'<li class="row"><span class="t">{e(t)}</span><span class="tog"><label class="ok"><input type="radio" name="p{i}" value="ok"><span>Good</span></label><label class="fix"><input type="radio" name="p{i}" value="fix"><span>Fix</span></label></span></li>' for i,t in enumerate(PRIV))
privacy=sec("privacy","blue","eye","Booth 1","Check your digital privacy",
f'''<p class="lead">What does the internet know about you? Open your own settings and mark each line. Nothing you tick leaves your phone.</p>
<ul class="rows" id="privrows">{priv_rows}</ul>
<div class="score" id="privscore" aria-live="polite"><b>Your score:</b> <span id="privtxt">mark each line to see it</span></div>
<p class="scale"><i class="g">0 to 2 Fix: Good</i><i class="a">3 to 5: Needs attention</i><i class="r">6 or more: High risk</i></p>
<h3>Quick fixes</h3>
<dl class="fixes">
<dt>Facebook</dt><dd>Settings and privacy, then Privacy Checkup. Set profile details, posts and friend list to Friends or Only me.</dd>
<dt>Instagram</dt><dd>Settings and activity, then Account privacy, then turn on Private account.</dd>
<dt>WhatsApp</dt><dd>Settings, then Privacy. Set Last seen, Profile photo and About to My contacts.</dd>
<dt>Android</dt><dd>Settings, then Privacy, then Permission manager. Review Location, Camera and Microphone.</dd>
<dt>iPhone</dt><dd>Settings, then Privacy and Security. Review Location Services, Camera and Microphone.</dd>
<dt>Location rule</dt><dd>Choose "While using the app" for apps that need it, and "Don't allow" for the rest.</dd>
</dl>
<p class="note">Menu names change with app updates and phone brands. Use the search bar in Settings.</p>
<blockquote class="pull">If you wouldn't put it on a university notice board, think twice before putting it online.</blockquote>''')

dev_rows="".join(f'<li class="row"><label><input type="checkbox" class="devck"><span class="t">{e(t)}</span></label></li>' for t in DEV)
dmg="".join(f'<li><b>{e(a)}</b><span>{e(b)}</span></li>' for a,b in DAMAGE)
device=sec("device","green","lock","Booth 2","Secure your device",
f'''<p class="lead">If you lost your phone right now, could someone open it? Ten minutes is enough to:</p>
<ul class="dmg">{dmg}</ul>
<blockquote class="pull">The attacker doesn't need hacking tools. Sometimes the weakness is simply an unlocked phone.</blockquote>
<h3>Fix it now</h3><p class="lead">Do the first three now. Finish the rest at home.</p>
<ul class="rows" id="devrows">{dev_rows}</ul>
<div class="bar" aria-live="polite"><div class="barfill" id="devfill"></div><span id="devtxt">0 of {len(DEV)} done</span></div>''')

chain=["Cracked software","Unknown modification","Possible malware or unwanted software","Credential and session theft","Data loss and privacy loss","Account compromise"]
chain_h='<ol class="chain">'+"".join(f'<li>{e(c)}</li>' for c in chain)+'</ol>'
alt_rows="".join(f'<tr><td>{e(a)}</td><td><b>{e(b)}</b></td><td><span class="tag {"foss" if k=="FOSS" else "free"}">{k}</span></td><td><a href="{u}" rel="noopener">{e(d)}</a></td></tr>' for a,b,k,d,u in ALT)
software=sec("software","amber","window","Booth 3","Crack, risk, switch",
f'''<p class="lead">Why do people use cracked software? It's free, it's easy, everyone does it. Here is what you can't see.</p>
{chain_h}
<blockquote class="pull">You don't know what was modified, what you're installing, or what it is doing.</blockquote>
<h3>Switch to software you can trust</h3>
<div class="tw"><table><thead><tr><th>You need</th><th>Try</th><th>Type</th><th>Official site</th></tr></thead><tbody>{alt_rows}</tbody></table></div>
<ul class="plain"><li>Download only from the official site.</li><li>FOSS means free and open source. Free is not always open source.</li><li>Ask your university about student licences before you reach for a crack.</li></ul>
<p class="ask"><b>Don't only ask: Is it free?</b> Ask: <b>Can I trust what I'm installing?</b></p>''')

click_rows=[("STOP","red","Don't react. Scammers want you in a hurry."),("CHECK","amber","Sender, link, urgency, and any request for money or a password."),("VERIFY","green","Call or meet the person another way. Never use the link in the message."),("ACT","blue","Report it, block it, then delete it.")]
click=sec("click","red","warning","Think first","Before you click",
f'''<p class="lead">Four steps for any message, link or request that feels urgent.</p>
<ol class="steps">{"".join(f'<li class="c-{c}"><b>{w}</b><span>{d}</span></li>' for w,c,d in click_rows)}</ol>
<h3>Messages like these are scams</h3>
<ul class="bubbles"><li>"Urgent! I need BDT 3,000. Send it now."</li><li>"Your university account will be disabled today. Click here immediately."</li><li>"You won a prize! Share your details to claim it."</li></ul>
<p class="ask"><b>Call, don't reply.</b> If a friend asks for money, confirm by phone call first.</p>''')

bully_items=["Someone keeps sending me insulting or threatening messages","A group is leaving me out or making fun of me online","My photo or video is shared or edited without my permission","A fake account is using my name or photo","Someone is threatening to leak private things unless I pay or obey","My private chat or photos were shared publicly","I'm being tagged or posted about to humiliate me","Someone follows me across apps and won't stop","I feel afraid, ashamed or anxious to open my phone"]
bully=sec("bullying","violet","hand","Be an upstander","Cyberbullying: check, save, report",
f'''<p class="lead">Is this cyberbullying? If any of these is true, it is worth acting on.</p>
<ul class="rows plainrows">{"".join(f'<li class="row"><label><input type="checkbox"><span class="t">{e(t)}</span></label></li>' for t in bully_items)}</ul>
<p class="care"><b>It is not your fault.</b> The person bullying is responsible, and you do not have to handle it alone.</p>
<h3>If it happens to you</h3>
<ol class="steps">
<li class="c-red"><b>STOP</b><span>Don't reply, don't pay, don't meet. Don't delete anything yet.</span></li>
<li class="c-amber"><b>SAVE</b><span>Screenshot with the date, username and link. Save the chat and profile URL. Note the times.</span></li>
<li class="c-green"><b>SECURE</b><span>Block the account, change passwords, turn on 2FA, make your profile private, log out of other devices.</span></li>
<li class="c-blue"><b>REPORT</b><span>Platform, then campus, then police or a helpline (next section). Tell someone you trust.</span></li></ol>
<h3>If you see it happen to someone else</h3>
<ul class="plain"><li>Don't share it, don't comment, don't laugh.</li><li>Save evidence and support them privately.</li><li>Report the post or account, and help them use the routes below.</li></ul>''')

nat="".join(f'<tr><td class="num">{e(c["number"])}</td><td><b>{e(c["label"])}</b><br><span class="sm">{e(c["detail"])}</span></td></tr>' for c in CFG["national_contacts"])
camp="".join(f'<tr><td><b>{e(c["role"])}</b></td><td class="{"" if c["contact"].strip() else "fill"}">{e(c["contact"]) if c["contact"].strip() else "[to be added]"}</td></tr>' for c in CFG["campus_contacts"])
report=sec("report","red","megaphone","Get help","Where to report",
f'''<h3>On campus</h3><div class="tw"><table class="ct"><tbody>{camp}</tbody></table></div>
<h3>Outside campus (Bangladesh)</h3><div class="tw"><table class="ct"><tbody>{nat}
<tr><td class="num">GD</td><td><b>Any serious threat</b><br><span class="sm">Go to your local police station and file a General Diary (GD) with your evidence.</span></td></tr>
<tr><td class="num">App</td><td><b>Fake profile or abusive content</b><br><span class="sm">Use the in-app Report on Facebook, Instagram, WhatsApp, TikTok or YouTube.</span></td></tr>
<tr><td class="num">Photos</td><td><b>Intimate photos shared or threatened</b><br><span class="sm">Adults: <a href="https://stopncii.org" rel="noopener">stopncii.org</a>. Under 18: <a href="https://takeitdown.ncmec.org" rel="noopener">takeitdown.ncmec.org</a>.</span></td></tr>
</tbody></table></div>
<p class="note">Online harassment, blackmail and sharing intimate images without consent can be crimes in Bangladesh under its cyber-security law. This guide is not legal advice. Civil society groups such as Bangladesh Mahila Parishad, ActionAid Bangladesh, Digitally Right and PrivaC also support people facing online abuse.</p>''')

def qcard(i,c):
    cat,sc,opts,best,why,trap=c
    ob="".join(f'<li><button type="button"><span class="l">{L[k]}</span><span>{e(o)}</span></button></li>' for k,o in enumerate(opts))
    return f'''<article class="qc q-{CATCOL[cat]}" data-best="{best}"><header><span>{cat}</span><b>Card {i}</b></header><h3>{e(sc)}</h3><ol class="opts">{ob}</ol>
<div class="ans"><p class="best">Best answer: <b>{L[best]}</b>. {e(opts[best])}</p><p><b>Why.</b> {e(why)}</p><p class="watch"><b>Watch out.</b> {e(trap)}</p></div></article>'''
quiz=sec("quiz","violet","quiz","Practise","What would you do?",
f'''<p class="lead">Ten real situations. Tap an answer to see the best choice. Nothing is recorded.</p>
<p class="qscore" id="qscore" aria-live="polite">Answered: 0 of {len(CARDS)}</p>
{"".join(qcard(i,c) for i,c in enumerate(CARDS,1))}''')

about=sec("about","blue","scale","Why it matters","About Jagoron and SDG 16",
f'''<p class="lead">Jagoron means awakening. A safe campus online is a peaceful and just campus: students know their rights, protect their privacy, and know where to report.</p>
<div class="sdg"><span class="sdgb"><i>SDG</i><b>16</b></span><p><b>Peace, Justice and Strong Institutions.</b> Jagoron supports targets on reducing violence and harassment (16.1), protecting children from abuse and exploitation (16.2), access to justice (16.3), accountable institutions (16.6), inclusive and participatory decisions (16.7), and access to information and protection of fundamental freedoms (16.10).</p></div>
<p>{e(CFG["organisation"])}. {("Contact: "+e(CFG["contact_email"])) if CFG["contact_email"] else ""}</p>''')

NAV=[("privacy","Privacy","blue"),("device","Device","green"),("software","Software","amber"),("click","Click","red"),("bullying","Bullying","violet"),("report","Report","red"),("quiz","Quiz","violet"),("about","About","blue")]
nav="".join(f'<a class="n-{c}" href="#{i}">{t}</a>' for i,t,c in NAV)
TITLES={"privacy":"Check your digital privacy","device":"Secure your device","software":"Crack, risk, switch","click":"Before you click","bullying":"Cyberbullying: check, save, report","report":"Where to report","quiz":"What would you do?","about":"About Jagoron and SDG 16"}
toc="".join(f'<li><a href="#{i}"><span>{TITLES[i]}</span><span class="pg"></span></a></li>' for i,t,c in NAV)
url=CFG["site_url"].strip()
PDF_NAME="Jagoron-Digital-Guide.pdf"
share=f'''<section id="share" class="sec s-blue"><header class="sh"><span class="badge">{ic("share",26)}</span><div><p class="kick">Take it with you</p><h2>Download and share</h2></div></header>
<div class="shr"><div><a class="btn" href="downloads/{PDF_NAME}" download>{ic("download",20)} Download the PDF</a>
<button class="btn ghost" type="button" id="copy">Copy link</button><button class="btn ghost" type="button" id="shareb" hidden>Share</button>
<p class="note">The PDF has the same content as this page, for offline reading and printing. {("Link: "+e(url)) if url else ""}</p></div>{QRBOX}</div></section>'''

CSS=open(os.path.join(ROOT,"style.css"),encoding="utf-8").read()
JS=open(os.path.join(ROOT,"app.js"),encoding="utf-8").read()
cover=f'''<div class="cover">{LOGO}<h1>JAGORON</h1><p class="cv-sub">Digital guide: cyber safety and digital responsibility</p>
{chips(FOUR)}<p class="cv-meta">{e(CFG["organisation"])}<br>Updated {e(CFG["updated"])}{("<br>Latest version: "+e(url)) if url else ""}</p>{"<p class='cv-draft'>DRAFT: contacts not yet verified</p>" if draft else ""}</div>'''
page=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(CFG["site_title"])}</title><meta name="description" content="Stop, check, secure, switch. A short guide to staying safe online for students.">
<meta name="theme-color" content="#0B1B3A"><link rel="icon" href="favicon.svg" type="image/svg+xml">
<meta property="og:title" content="{e(CFG["site_title"])}"><meta property="og:description" content="Stop, check, secure, switch. Cyber safety for students.">
<style>{CSS}</style><noscript><style>.ans{{display:block!important}}</style></noscript></head><body>
{cover}
<nav class="toc"><h2>Contents</h2><ol>{toc}<li><a href="#share"><span>Download and share</span><span class="pg"></span></a></li></ol></nav>
{draft_banner}
<header class="top"><a class="brand" href="#top">{LOGO}<span>Jagoron</span></a><a class="btn sm" href="downloads/{PDF_NAME}" download>{ic("download",16)} PDF</a></header>
<nav class="chipnav" aria-label="Sections">{nav}</nav>
<main id="top"><section class="hero"><p class="kick">Cyber safety and digital responsibility</p><h1>Four habits.<br>Five minutes.<br>Do one thing on your own phone today.</h1>
{chips(FOUR)}<p><a class="btn" href="#privacy">Start the 5-minute check</a> <a class="btn ghost" href="#quiz">Try the quiz</a></p></section>
{privacy}{device}{software}{click}{bully}{report}{quiz}{about}{share}</main>
<footer><p>{e(CFG["organisation"])}. Updated {e(CFG["updated"])}. Nothing you tick or tap on this page is stored or sent anywhere.</p></footer>
<script>{JS}</script></body></html>'''

os.makedirs(os.path.join(DOCS,"downloads"),exist_ok=True)
open(os.path.join(DOCS,"index.html"),"w",encoding="utf-8").write(page)
open(os.path.join(DOCS,"404.html"),"w",encoding="utf-8").write('<!doctype html><meta charset="utf-8"><meta http-equiv="refresh" content="0; url=./"><title>Jagoron</title><p>Page not found. <a href="./">Go to the Jagoron guide</a>.</p>')
open(os.path.join(DOCS,".nojekyll"),"w").write("")
open(os.path.join(DOCS,"favicon.svg"),"w").write(LOGO.replace('<svg class="logo"','<svg xmlns="http://www.w3.org/2000/svg"',1))

from weasyprint import HTML
pdfhtml=page
HTML(string=pdfhtml,base_url=DOCS).write_pdf(os.path.join(DOCS,"downloads",PDF_NAME))
print("Built docs/index.html and docs/downloads/"+PDF_NAME, "(DRAFT)" if draft else "(RELEASE)")
if draft: print("Draft reasons:",len(unverified),"unverified numbers,",len(unfilled),"empty campus contacts")
