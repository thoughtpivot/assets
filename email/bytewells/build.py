import asyncio,re,html
from playwright.async_api import async_playwright
BW_LOGO="https://thoughtpivot.github.io/assets/email/bytewells-logo.png"
TP_LOGO="https://thoughtpivot.github.io/assets/email/tp-logo.png"
WL="https://bytewells.com/developer-waitlist"
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
P='font-family:-apple-system,Segoe UI,Helvetica,Arial,sans-serif;font-size:16px;line-height:24px;color:#0c0d0f;margin:0 0 16px 0;'
def tpl(e):
  ps="\n".join(f'<p style="{P}">{p.replace("{{sample_actor_url}}",chr(60)+"a href=\"{{sample_actor_url}}\" style=\"color:#0284c7;\""+chr(62)+"{{sample_actor_url}}</a>")}</p>' for p in e["paras"])
  return f'''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="x-apple-disable-message-reformatting">
<!-- Subject: {e["subject"]} | From: Dan at Bytewells <bytewells@thoughtpivot.com> | Reply-To: bytewells@thoughtpivot.com | List-Unsubscribe: <{{{{unsubscribe_url}}}}> -->
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
<table role="presentation" class="btn" cellpadding="0" cellspacing="0" border="0" style="margin:8px 0 20px 0;"><tr><td align="center" bgcolor="#0284c7" style="border-radius:6px;">
<a href="{WL}" style="display:inline-block;padding:13px 26px;font-family:Helvetica,Arial,sans-serif;font-size:16px;font-weight:bold;color:#ffffff;text-decoration:none;border-radius:6px;">{e["cta"]}</a></td></tr></table>
<p style="{P}font-size:14px;color:#646973;">Or open: <a href="{WL}" style="color:#0284c7;">{WL}</a></p>
<p style="{P}">_dan</p>
</td></tr>
<tr><td class="p" style="padding:20px 40px 28px 40px;background:#f5f6f7;border-top:1px solid #ebedf1;border-radius:0 0 8px 8px;font-family:Helvetica,Arial,sans-serif;font-size:12px;line-height:18px;color:#646973;">
<strong style="color:#0c0d0f;">Bytewells by ThoughtPivot</strong><br>{ADDR}<br>{WHY}<br><span style="font-size:11px;line-height:16px;color:#8a8f98;">{GDPR.replace("bytewells@thoughtpivot.com","<a href=\"mailto:bytewells@thoughtpivot.com\" style=\"color:#8a8f98;\">bytewells@thoughtpivot.com</a>")}</span><br><a href="{{{{unsubscribe_url}}}}" style="color:#646973;text-decoration:underline;">Unsubscribe</a>
</td></tr></table></td></tr></table></body></html>'''
def txt(e):
  return "\n\n".join(e["paras"])+f"\n\n{e['cta']}: {WL}\n\n_dan\n\n--\nBytewells by ThoughtPivot\n{ADDR}\n{WHY}\n{GDPR}\nUnsubscribe: {{{{unsubscribe_url}}}}\n"
S={"first_name":"Shahid","store_actor_count":"14","sample_actor_url":"https://apify.com/example/google-maps-scraper","unsubscribe_url":"https://bytewells.com/unsubscribe?t=sample"}
def fill(h):
  for k,v in S.items(): h=h.replace("{{"+k+"}}",v)
  h=re.sub(r"\{\{#had_rentals\}\}(.*?)\{\{/had_rentals\}\}",r"\1",h)
  return h
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(); pg=await b.new_page(device_scale_factor=2)
    for n,f in [("bytewells-logo","assets/bytewells-logo.svg"),("tp-logo","assets/tp-logo.svg")]:
      open('/tmp/l.html','w').write(f'<html><body style="margin:0;background:transparent"><img id=i src="file:///workspace/email_templates/{f}" style="height:{60 if n[0]=="b" else 34}px;display:block"></body></html>'); await pg.goto('file:///tmp/l.html')
      await pg.wait_for_timeout(300); await pg.locator("#i").screenshot(path=f"assets/{n}.png",omit_background=True)
    for i,e in enumerate([E1,E2,E3],1):
      h=tpl(e); open(f"email{i}.html","w").write(h); open(f"email{i}.txt","w").write(f"Subject: {e['subject']}\n\n"+txt(e))
      open(f"preview{i}.html","w").write(fill(h))
      for w,sfx in [(700,""),(380,"_mobile")]:
        await pg.set_viewport_size({"width":w,"height":800}); await pg.goto(f"file:///workspace/email_templates/preview{i}.html")
        await pg.screenshot(path=f"email{i}{sfx}.png",full_page=True)
    await b.close()
asyncio.run(main())
