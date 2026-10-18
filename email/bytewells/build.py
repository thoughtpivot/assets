import asyncio,re,html,os,sys,tempfile
HERE=os.path.dirname(os.path.abspath(__file__))
BW_LOGO="https://thoughtpivot.github.io/assets/email/bytewells-logo.png"
TP_LOGO="https://thoughtpivot.github.io/assets/email/tp-logo.png"
DISCORD_LOGO="https://thoughtpivot.github.io/assets/email/discord-logo.png"
WL="https://bytewells.com/developer-waitlist"
DISCORD="https://discord.gg/N7xyfmMRj"  # ThoughtPivot Discord invite; change it here only
ADDR="ThoughtPivot, Inc., 2937 East Grand Boulevard, Detroit, MI 48202"
GDPR="We're contacting you under legitimate interest because your email is public on your Apify developer profile. Unsubscribe anytime and we'll delete your data. Questions: bytewells@thoughtpivot.com."
WHY="You're receiving this because your email is listed on your public Apify profile."
RENT="{{#had_rentals}}You had rental Actors before Oct 1. This brings that model back.{{/had_rentals}}"
E1=dict(subject="Monthly rentals for your {{store_actor_count}} Apify Actors",pre="Apify retired rental pricing on Oct 1. Bytewells launches Nov 2.",paras=[
 "Hi {{first_name}},",
 "Apify retired rental pricing on Oct 1. We're launching Bytewells by ThoughtPivot on Nov 2: a second storefront for Apify Actors. Your Apify listing stays live.",
 "Renters pay monthly or buy 1-hour, 24-hour or 7-day passes. 10% commission, 0% on renters you bring.",
 "You have {{store_actor_count}} Actors on Apify (e.g. {{sample_actor_url}}).", RENT],cta="Join the developer waitlist")
E2=dict(subject="Re: Monthly rentals for your Apify Actors",pre="Quick follow-up: Bytewells launches Nov 2.",paras=[
 "Hi {{first_name}},",
 "Quick follow-up. Bytewells launches Nov 2. Your Apify listing stays live; you add monthly rentals and 1-hour, 24-hour or 7-day passes on top. 10% commission, 0% on renters you bring."],cta="Join the developer waitlist")
E3=dict(subject="Bytewells launches Nov 2",pre="Last note: waitlist developers get in first.",paras=[
 "Hi {{first_name}},",
 "Last note from me. Bytewells by ThoughtPivot opens Nov 2. Waitlist developers get in first.",
 "If it's not for you, no reply needed and I won't email again."],cta="Get early access")
R=dict(subject="Re: Developer waitlist: {{apify_username}}",pre="You're on the Bytewells developer waitlist.",paras=[
 "Hi there,",
 "Thanks for joining the Bytewells by ThoughtPivot developer waitlist with {{apify_username}}. <a href=\"%s\" style=\"color:#0284c7;\">You're on the waitlist</a>. We're onboarding developers in small batches during the private beta and will reach out when your spot opens."%WL,
 "If you'd like to share which Actors you'd list first, just reply here. You're also welcome to join us on Discord, where we share updates and you can talk with the team directly."],
 txt_paras=[
 "Hi there,",
 "Thanks for joining the Bytewells by ThoughtPivot developer waitlist with {{apify_username}}. You're on the waitlist (%s). We're onboarding developers in small batches during the private beta and will reach out when your spot opens."%WL,
 "If you'd like to share which Actors you'd list first, just reply here. You're also welcome to join us on Discord, where we share updates and you can talk with the team directly."],
 cta="Join us on Discord",url=DISCORD,icon=True,
 why="You're receiving this because you joined the Bytewells developer waitlist.",
 note="Questions? Reply to this email or write to bytewells@thoughtpivot.com.")
P='font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;font-size:16px;line-height:24px;color:#0c0d0f;margin:0 0 16px 0;'
def tpl(e):
  rply="why" in e
  url=e.get("url",WL)
  if e.get("icon"):
    label=f'<img src="{DISCORD_LOGO}" width="24" height="24" alt="" style="display:inline-block;vertical-align:middle;border:0;width:24px;height:24px;margin:0 10px 0 0;"><span style="vertical-align:middle;">{e["cta"]}</span>'
    bg,pad="#5865F2","12px 26px 12px 22px"
  else:
    label=e["cta"]; bg,pad="#0284c7","13px 26px"
  if rply:
    foot=f'<strong style="color:#0c0d0f;">Bytewells by ThoughtPivot</strong><br>{ADDR}<br>{e["why"]}<br><span style="font-size:11px;line-height:16px;color:#8a8f98;">{e["note"].replace("bytewells@thoughtpivot.com","<a href=\"mailto:bytewells@thoughtpivot.com\" style=\"color:#8a8f98;\">bytewells@thoughtpivot.com</a>")}</span>'
  else:
    foot=f'''<strong style="color:#0c0d0f;">Bytewells by ThoughtPivot</strong><br>{ADDR}<br>{WHY}<br><span style="font-size:11px;line-height:16px;color:#8a8f98;">{GDPR.replace("bytewells@thoughtpivot.com","<a href=\"mailto:bytewells@thoughtpivot.com\" style=\"color:#8a8f98;\">bytewells@thoughtpivot.com</a>")}</span><br><a href="{{{{unsubscribe_url}}}}" style="color:#646973;text-decoration:underline;">Unsubscribe</a>'''
  def para(p):
    m=re.fullmatch(r"\{\{#had_rentals\}\}(.*)\{\{/had_rentals\}\}",p)
    return f'{{{{#had_rentals}}}}<p style="{P}">{m.group(1)}</p>{{{{/had_rentals}}}}' if m else f'<p style="{P}">{p}</p>'
  ps="\n".join(para(p.replace("{{sample_actor_url}}",chr(60)+"a href=\"{{sample_actor_url}}\" style=\"color:#0284c7;\""+chr(62)+"{{sample_actor_url}}</a>")) for p in e["paras"])
  return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="x-apple-disable-message-reformatting">
<title>{e["subject"]}</title>
<style>@media only screen and (max-width:620px){{.c{{width:100%!important}}.p{{padding-left:20px!important;padding-right:20px!important}}.btn a{{display:block!important}}}}</style></head>
<body style="margin:0;padding:0;background:#f5f6f7;">
<div style="display:none;max-height:0;overflow:hidden;opacity:0;">{e["pre"]}</div>
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#f5f6f7;"><tr><td align="center" style="padding:24px 0;">
<table role="presentation" class="c" width="600" cellpadding="0" cellspacing="0" border="0" style="width:600px;max-width:600px;background:#ffffff;border:1px solid #ebedf1;border-radius:8px;">
<tr><td class="p" style="padding:28px 40px 20px 40px;border-bottom:3px solid #0284c7;">
 <table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr>
 <td valign="middle"><img src="{BW_LOGO}" width="160" height="30" alt="Bytewells" style="display:block;border:0;width:160px;height:auto;"></td>
 <td valign="middle" style="padding-left:12px;font-family:Helvetica,Arial,sans-serif;font-size:13px;color:#646973;white-space:nowrap;">by&nbsp;</td>
 <td valign="middle"><img src="{TP_LOGO}" width="105" height="17" alt="ThoughtPivot" style="display:block;border:0;width:105px;height:auto;"></td>
 </tr></table></td></tr>
<tr><td class="p" style="padding:32px 40px 8px 40px;">
{ps}
<table role="presentation" class="btn" cellpadding="0" cellspacing="0" border="0" style="margin:8px 0 24px 0;"><tr><td align="center" bgcolor="{bg}" style="border-radius:6px;">
<a href="{url}" style="display:inline-block;padding:{pad};font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:bold;line-height:24px;color:#ffffff;text-decoration:none;border-radius:6px;">{label}</a></td></tr></table>
</td></tr>
<tr><td class="p" style="padding:20px 40px 28px 40px;background:#f5f6f7;border-top:1px solid #ebedf1;border-radius:0 0 8px 8px;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:18px;color:#646973;">
{foot}
</td></tr></table></td></tr></table></body></html>'''
def txt(e):
  if "why" in e:
    return "\n\n".join(e["txt_paras"])+f"\n\n{e['cta']}: {e['url']}\n\n--\nBytewells by ThoughtPivot\n{ADDR}\n{e['why']} {e['note']}\n"
  body=""
  for p in e["paras"]:
    m=re.fullmatch(r"\{\{#had_rentals\}\}(.*)\{\{/had_rentals\}\}",p)
    body+=("{{#had_rentals}}\n\n"+m.group(1)+"{{/had_rentals}}") if m else (("\n\n" if body else "")+p)
  return body+f"\n\n{e['cta']}: {WL}\n\n--\nBytewells by ThoughtPivot\n{ADDR}\n{WHY}\n{GDPR}\nUnsubscribe: {{{{unsubscribe_url}}}}\n"
S={"apify_username":"example-actors","first_name":"Shahid","store_actor_count":"14","sample_actor_url":"https://apify.com/example/google-maps-scraper","unsubscribe_url":"https://bytewells.com/unsubscribe?t=sample"}
def fill(h):
  for k,v in S.items(): h=h.replace("{{"+k+"}}",v)
  h=re.sub(r"\{\{#had_rentals\}\}(.*?)\{\{/had_rentals\}\}",r"\1",h)
  return h
async def main():
  # usage: python3 build.py [--logos] [--previews]
  # default: regenerate the .html/.txt files only. --logos re-renders the PNG logos into ../ (repo email/);
  # --previews writes preview screenshots to a temp dir (not committed).
  for n,e,f in [("email1",E1,"email1"),("email2",E2,"email2"),("email3",E3,"email3")]:
    h=tpl(e); open(os.path.join(HERE,f+".html"),"w").write(h); open(os.path.join(HERE,f+".txt"),"w").write(txt(e))
  open(os.path.join(HERE,"reply_waitlist.html"),"w").write(tpl(R)); open(os.path.join(HERE,"reply_waitlist.txt"),"w").write(txt(R))
  if not ("--logos" in sys.argv or "--previews" in sys.argv): return
  from playwright.async_api import async_playwright  # only needed for --logos / --previews
  out=tempfile.mkdtemp(prefix="bw-email-")
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(device_scale_factor=2)
    if "--logos" in sys.argv:
      for n,f,h in [("bytewells-logo","bytewells-logo.svg",60),("tp-logo","tp-logo.svg",34),("discord-logo","discord-logo.svg",48)]:
        open(os.path.join(out,"l.html"),"w").write(f'<html><body style="margin:0;background:transparent"><img id=i src="file://{HERE}/assets/{f}" style="height:{h}px;display:block"></body></html>'); await pg.goto("file://"+os.path.join(out,"l.html"))
        await pg.wait_for_timeout(300); await pg.locator("#i").screenshot(path=os.path.join(HERE,"..",n+".png"),omit_background=True)
    if "--previews" in sys.argv:
      for n,e in [("email1",E1),("email2",E2),("email3",E3),("reply_waitlist",R)]:
        pv=os.path.join(out,n+".html"); open(pv,"w").write(fill(tpl(e)))
        for w,sfx in [(700,""),(380,"_mobile")]:
          await pg.set_viewport_size({"width":w,"height":800}); await pg.goto("file://"+pv)
          await pg.screenshot(path=os.path.join(out,n+sfx+".png"),full_page=True)
      print("previews in",out)
    await b.close()
asyncio.run(main())
