# type: ignore

from parser import extract_news, extract_next_page_url, get_news

import requests
from bs4 import BeautifulSoup


@pytest.fixture
def html_doc():
    return """
    <html lang="en" op="news"><head><meta name="referrer" content="origin"><meta name="viewport" content="width=device-width, initial-scale=1.0"><link rel="stylesheet" type="text/css" href="news.css?DqVgzIak3Krx8fVwunvN">
        <link rel="shortcut icon" href="favicon.ico">
          <link rel="alternate" type="application/rss+xml" title="RSS" href="rss">
        <title>Hacker News</title></head><body><center><table id="hnmain" border="0" cellpadding="0" cellspacing="0" width="85%" bgcolor="#f6f6ef">
        <tr><td bgcolor="#ff6600"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="padding:2px"><tr><td style="width:18px;padding-right:4px"><a href="https://news.ycombinator.com"><img src="y18.gif" width="18" height="18" style="border:1px white solid;"></a></td>
                  <td style="line-height:12pt; height:10px;"><span class="pagetop"><b class="hnname"><a href="news">Hacker News</a></b>
              <a href="newest">new</a> | <a href="front">past</a> | <a href="newcomments">comments</a> | <a href="ask">ask</a> | <a href="show">show</a> | <a href="jobs">jobs</a> | <a href="submit">submit</a>            </span></td><td style="text-align:right;padding-right:4px;"><span class="pagetop">
                              <a href="login?goto=news">login</a>
                          </span></td>
              </tr></table></td></tr>
<tr id="pagespace" title="" style="height:10px"></tr><tr><td><table border="0" cellpadding="0" cellspacing="0" class="itemlist">
              <tr class='athing' id='27617256'>
      <td align="right" valign="top" class="title"><span class="rank">1.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27617256' href='vote?id=27617256&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://www.npr.org/2021/06/23/1009567351/hubble-trouble-nasa-cant-figure-out-whats-causing-computer-issues-on-the-telesco" class="storylink">NASA Can't Figure Out What's Causing Computer Issues on the Hubble Telescope</a><span class="sitebit comhead"> (<a href="from?site=npr.org"><span class="sitestr">npr.org</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27617256">140 points</span> by <a href="user?id=fortran77" class="hnuser">fortran77</a> <span class="age"><a href="item?id=27617256">2 hours ago</a></span> <span id="unv_27617256"></span> | <a href="hide?id=27617256&amp;goto=news">hide</a> | <a href="item?id=27617256">133&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27619672'>
      <td align="right" valign="top" class="title"><span class="rank">2.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27619672' href='vote?id=27619672&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://www.backblaze.com/blog/next-backblaze-storage-pod/" class="storylink">The Next Backblaze Storage Pod</a><span class="sitebit comhead"> (<a href="from?site=backblaze.com"><span class="sitestr">backblaze.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27619672">17 points</span> by <a href="user?id=TangerineDream" class="hnuser">TangerineDream</a> <span class="age"><a href="item?id=27619672">14 minutes ago</a></span> <span id="unv_27619672"></span> | <a href="hide?id=27619672&amp;goto=news">hide</a> | <a href="item?id=27619672">2&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27618206'>
      <td align="right" valign="top" class="title"><span class="rank">3.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27618206' href='vote?id=27618206&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://themarkup.org/citizen-browser/2021/06/24/after-repeatedly-promising-not-to-facebook-keeps-recommending-political-groups-to-its-users" class="storylink">After Repeatedly Promising Not To, Facebook Keeps Recommending Political Groups</a><span class="sitebit comhead"> (<a href="from?site=themarkup.org"><span class="sitestr">themarkup.org</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27618206">202 points</span> by <a href="user?id=jbegley" class="hnuser">jbegley</a> <span class="age"><a href="item?id=27618206">1 hour ago</a></span> <span id="unv_27618206"></span> | <a href="hide?id=27618206&amp;goto=news">hide</a> | <a href="item?id=27618206">80&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27619015'>
      <td align="right" valign="top" class="title"><span class="rank">4.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27619015' href='vote?id=27619015&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://blog.m3o.com/2021/06/24/micro-apis-for-everyday-use.html" class="storylink">Micro APIs for Everyday Use</a><span class="sitebit comhead"> (<a href="from?site=m3o.com"><span class="sitestr">m3o.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27619015">24 points</span> by <a href="user?id=friendly_chap" class="hnuser">friendly_chap</a> <span class="age"><a href="item?id=27619015">56 minutes ago</a></span> <span id="unv_27619015"></span> | <a href="hide?id=27619015&amp;goto=news">hide</a> | <a href="item?id=27619015">discuss</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27619030'>
      <td align="right" valign="top" class="title"><span class="rank">5.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27619030' href='vote?id=27619030&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://www.forbrukerradet.no/side/new-report-details-threats-to-consumers-from-surveillance-based-advertising/" class="storylink">International coalition calls for action against surveillance-based advertising</a><span class="sitebit comhead"> (<a href="from?site=forbrukerradet.no"><span class="sitestr">forbrukerradet.no</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27619030">13 points</span> by <a href="user?id=dredmorbius" class="hnuser">dredmorbius</a> <span class="age"><a href="item?id=27619030">55 minutes ago</a></span> <span id="unv_27619030"></span> | <a href="hide?id=27619030&amp;goto=news">hide</a> | <a href="item?id=27619030">discuss</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27615516'>
      <td align="right" valign="top" class="title"><span class="rank">6.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27615516' href='vote?id=27615516&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="http://bashrcgenerator.com/" class="storylink">Bash PS1 Generator</a><span class="sitebit comhead"> (<a href="from?site=bashrcgenerator.com"><span class="sitestr">bashrcgenerator.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27615516">193 points</span> by <a href="user?id=nailer" class="hnuser">nailer</a> <span class="age"><a href="item?id=27615516">6 hours ago</a></span> <span id="unv_27615516"></span> | <a href="hide?id=27615516&amp;goto=news">hide</a> | <a href="item?id=27615516">99&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27619191'>
      <td align="right" valign="top" class="title"><span class="rank">7.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27619191' href='vote?id=27619191&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://www.theverge.com/2021/6/24/22548428/microsoft-windows-11-android-apps-support-amazon-store" class="storylink">Microsoft is bringing Android apps to Windows 11</a><span class="sitebit comhead"> (<a href="from?site=theverge.com"><span class="sitestr">theverge.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27619191">64 points</span> by <a href="user?id=ArchUser2255" class="hnuser">ArchUser2255</a> <span class="age"><a href="item?id=27619191">44 minutes ago</a></span> <span id="unv_27619191"></span> | <a href="hide?id=27619191&amp;goto=news">hide</a> | <a href="item?id=27619191">32&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27617670'>
      <td align="right" valign="top" class="title"><span class="rank">8.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27617670' href='vote?id=27617670&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://www.blender.org/press/canonical-offering-blender-support/" class="storylink">Canonical Offering Blender Support</a><span class="sitebit comhead"> (<a href="from?site=blender.org"><span class="sitestr">blender.org</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27617670">90 points</span> by <a href="user?id=asicsp" class="hnuser">asicsp</a> <span class="age"><a href="item?id=27617670">2 hours ago</a></span> <span id="unv_27617670"></span> | <a href="hide?id=27617670&amp;goto=news">hide</a> | <a href="item?id=27617670">10&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27616018'>
      <td align="right" valign="top" class="title"><span class="rank">9.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27616018' href='vote?id=27616018&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://developer.apple.com/documentation/xcode/writing-arm64-code-for-apple-platforms" class="storylink">Writing ARM64 Code for Apple Platforms</a><span class="sitebit comhead"> (<a href="from?site=developer.apple.com"><span class="sitestr">developer.apple.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27616018">108 points</span> by <a href="user?id=ingve" class="hnuser">ingve</a> <span class="age"><a href="item?id=27616018">5 hours ago</a></span> <span id="unv_27616018"></span> | <a href="hide?id=27616018&amp;goto=news">hide</a> | <a href="item?id=27616018">54&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27617466'>
      <td align="right" valign="top" class="title"><span class="rank">10.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27617466' href='vote?id=27617466&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://cloud.google.com/bigquery/docs/row-level-security-intro" class="storylink">BigQuery row-level security</a><span class="sitebit comhead"> (<a href="from?site=cloud.google.com"><span class="sitestr">cloud.google.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27617466">42 points</span> by <a href="user?id=santhoshkumar3" class="hnuser">santhoshkumar3</a> <span class="age"><a href="item?id=27617466">2 hours ago</a></span> <span id="unv_27617466"></span> | <a href="hide?id=27617466&amp;goto=news">hide</a> | <a href="item?id=27617466">5&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27614912'>
      <td align="right" valign="top" class="title"><span class="rank">11.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27614912' href='vote?id=27614912&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="http://strlen.com/treesheets/" class="storylink">Treesheets: cross-platform, free-form data organizer app</a><span class="sitebit comhead"> (<a href="from?site=strlen.com"><span class="sitestr">strlen.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27614912">253 points</span> by <a href="user?id=open-source-ux" class="hnuser">open-source-ux</a> <span class="age"><a href="item?id=27614912">8 hours ago</a></span> <span id="unv_27614912"></span> | <a href="hide?id=27614912&amp;goto=news">hide</a> | <a href="item?id=27614912">49&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27589040'>
      <td align="right" valign="top" class="title"><span class="rank">12.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27589040' href='vote?id=27589040&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://www.androidauthority.com/oneplus-oxygen-os-rise-fall-1234103/" class="storylink">The rise and fall of Oxygen OS</a><span class="sitebit comhead"> (<a href="from?site=androidauthority.com"><span class="sitestr">androidauthority.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27589040">35 points</span> by <a href="user?id=jiri" class="hnuser">jiri</a> <span class="age"><a href="item?id=27589040">3 hours ago</a></span> <span id="unv_27589040"></span> | <a href="hide?id=27589040&amp;goto=news">hide</a> | <a href="item?id=27589040">4&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27617196'>
      <td align="right" valign="top" class="title"><span class="rank">13.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27617196' href='vote?id=27617196&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://www.juststeveking.uk/introducing-laravel-transporter/" class="storylink">Laravel Transporter</a><span class="sitebit comhead"> (<a href="from?site=juststeveking.uk"><span class="sitestr">juststeveking.uk</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27617196">28 points</span> by <a href="user?id=mooreds" class="hnuser">mooreds</a> <span class="age"><a href="item?id=27617196">2 hours ago</a></span> <span id="unv_27617196"></span> | <a href="hide?id=27617196&amp;goto=news">hide</a> | <a href="item?id=27617196">19&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27616656'>
      <td align="right" valign="top" class="title"><span class="rank">14.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27616656' href='vote?id=27616656&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://mrale.ph/blog/2018/02/03/maybe-you-dont-need-rust-to-speed-up-your-js.html" class="storylink">Maybe you don't need Rust and WASM to speed up your JS (2018)</a><span class="sitebit comhead"> (<a href="from?site=mrale.ph"><span class="sitestr">mrale.ph</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27616656">42 points</span> by <a href="user?id=zbentley" class="hnuser">zbentley</a> <span class="age"><a href="item?id=27616656">3 hours ago</a></span> <span id="unv_27616656"></span> | <a href="hide?id=27616656&amp;goto=news">hide</a> | <a href="item?id=27616656">23&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27616325'>
      <td align="right" valign="top" class="title"><span class="rank">15.</span></td>      <td></td><td class="title"><a href="https://www.workatastartup.com/jobs/43782" class="storylink" rel="nofollow">Literably (IK12 W13) Is Hiring a Senior Software Engineer (Remote)</a><span class="sitebit comhead"> (<a href="from?site=workatastartup.com"><span class="sitestr">workatastartup.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="age"><a href="item?id=27616325">4 hours ago</a></span> | <a href="hide?id=27616325&amp;goto=news">hide</a>      </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27615507'>
      <td align="right" valign="top" class="title"><span class="rank">16.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27615507' href='vote?id=27615507&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://www.rijksmuseum.nl/en/stories/operation-night-watch/story/night-watch-the-missing-pieces" class="storylink">Recreating the Missing Pieces of the Night Watch with the Help of AI</a><span class="sitebit comhead"> (<a href="from?site=rijksmuseum.nl"><span class="sitestr">rijksmuseum.nl</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27615507">99 points</span> by <a href="user?id=BjoernKW" class="hnuser">BjoernKW</a> <span class="age"><a href="item?id=27615507">6 hours ago</a></span> <span id="unv_27615507"></span> | <a href="hide?id=27615507&amp;goto=news">hide</a> | <a href="item?id=27615507">15&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27617620'>
      <td align="right" valign="top" class="title"><span class="rank">17.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27617620' href='vote?id=27617620&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://digiday.com/marketing/cheat-sheet-google-extends-cookie-execution-deadline-until-late-2023-will-pause-floc-testing-in-july/" class="storylink">Google extends third party cookie deadline until late 2023</a><span class="sitebit comhead"> (<a href="from?site=digiday.com"><span class="sitestr">digiday.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27617620">59 points</span> by <a href="user?id=lhpz" class="hnuser">lhpz</a> <span class="age"><a href="item?id=27617620">2 hours ago</a></span> <span id="unv_27617620"></span> | <a href="hide?id=27617620&amp;goto=news">hide</a> | <a href="item?id=27617620">33&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27596453'>
      <td align="right" valign="top" class="title"><span class="rank">18.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27596453' href='vote?id=27596453&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://glenngillen.com/getting-the-pm-interview/" class="storylink">Getting to the Product Manager interview stage</a><span class="sitebit comhead"> (<a href="from?site=glenngillen.com"><span class="sitestr">glenngillen.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27596453">28 points</span> by <a href="user?id=glenngillen" class="hnuser">glenngillen</a> <span class="age"><a href="item?id=27596453">3 hours ago</a></span> <span id="unv_27596453"></span> | <a href="hide?id=27596453&amp;goto=news">hide</a> | <a href="item?id=27596453">12&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27617127'>
      <td align="right" valign="top" class="title"><span class="rank">19.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27617127' href='vote?id=27617127&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://dpreview.com/news/4668719994/faa-releases-trust-free-online-training-required-for-recreational-pilots-to-fly-legally" class="storylink">FAA releases TRUST: Free online training required to fly drones recreationally</a><span class="sitebit comhead"> (<a href="from?site=dpreview.com"><span class="sitestr">dpreview.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27617127">110 points</span> by <a href="user?id=asix66" class="hnuser">asix66</a> <span class="age"><a href="item?id=27617127">2 hours ago</a></span> <span id="unv_27617127"></span> | <a href="hide?id=27617127&amp;goto=news">hide</a> | <a href="item?id=27617127">127&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27614855'>
      <td align="right" valign="top" class="title"><span class="rank">20.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27614855' href='vote?id=27614855&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://android-developers.googleblog.com/2021/06/continuing-to-boost-developer-success.html" class="storylink">Google will consider lowering Play Store cut to 15% for certain apps</a><span class="sitebit comhead"> (<a href="from?site=googleblog.com"><span class="sitestr">googleblog.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27614855">116 points</span> by <a href="user?id=Pandabob" class="hnuser">Pandabob</a> <span class="age"><a href="item?id=27614855">8 hours ago</a></span> <span id="unv_27614855"></span> | <a href="hide?id=27614855&amp;goto=news">hide</a> | <a href="item?id=27614855">80&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27616212'>
      <td align="right" valign="top" class="title"><span class="rank">21.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27616212' href='vote?id=27616212&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://www.nytimes.com/2021/06/23/upshot/remote-work-innovation-office.html" class="storylink">No evidence that chance meetings in office boosts innovation</a><span class="sitebit comhead"> (<a href="from?site=nytimes.com"><span class="sitestr">nytimes.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27616212">211 points</span> by <a href="user?id=remt" class="hnuser">remt</a> <span class="age"><a href="item?id=27616212">4 hours ago</a></span> <span id="unv_27616212"></span> | <a href="hide?id=27616212&amp;goto=news">hide</a> | <a href="item?id=27616212">132&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27614874'>
      <td align="right" valign="top" class="title"><span class="rank">22.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27614874' href='vote?id=27614874&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://3dasd.com/" class="storylink">Show HN: 3dasd – open-source DIY room-scale 3D scanner</a><span class="sitebit comhead"> (<a href="from?site=3dasd.com"><span class="sitestr">3dasd.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27614874">134 points</span> by <a href="user?id=dvoros" class="hnuser">dvoros</a> <span class="age"><a href="item?id=27614874">8 hours ago</a></span> <span id="unv_27614874"></span> | <a href="hide?id=27614874&amp;goto=news">hide</a> | <a href="item?id=27614874">36&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27616822'>
      <td align="right" valign="top" class="title"><span class="rank">23.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27616822' href='vote?id=27616822&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://spectrum.ieee.org/computing/software/the-dawn-of-haiku-os" class="storylink">The Dawn of Haiku OS (2012)</a><span class="sitebit comhead"> (<a href="from?site=ieee.org"><span class="sitestr">ieee.org</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27616822">25 points</span> by <a href="user?id=bitigchi" class="hnuser">bitigchi</a> <span class="age"><a href="item?id=27616822">3 hours ago</a></span> <span id="unv_27616822"></span> | <a href="hide?id=27616822&amp;goto=news">hide</a> | <a href="item?id=27616822">6&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27614381'>
      <td align="right" valign="top" class="title"><span class="rank">24.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27614381' href='vote?id=27614381&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="http://tylerneylon.com/a/lsh1/" class="storylink">Introduction to Locality-Sensitive Hashing</a><span class="sitebit comhead"> (<a href="from?site=tylerneylon.com"><span class="sitestr">tylerneylon.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27614381">192 points</span> by <a href="user?id=polm23" class="hnuser">polm23</a> <span class="age"><a href="item?id=27614381">10 hours ago</a></span> <span id="unv_27614381"></span> | <a href="hide?id=27614381&amp;goto=news">hide</a> | <a href="item?id=27614381">42&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27618423'>
      <td align="right" valign="top" class="title"><span class="rank">25.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27618423' href='vote?id=27618423&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://en.wikipedia.org/wiki/Angus_Barbieri%27s_fast" class="storylink">Angus Barbieri's fast</a><span class="sitebit comhead"> (<a href="from?site=wikipedia.org"><span class="sitestr">wikipedia.org</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27618423">48 points</span> by <a href="user?id=nixass" class="hnuser">nixass</a> <span class="age"><a href="item?id=27618423">1 hour ago</a></span> <span id="unv_27618423"></span> | <a href="hide?id=27618423&amp;goto=news">hide</a> | <a href="item?id=27618423">20&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27617051'>
      <td align="right" valign="top" class="title"><span class="rank">26.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27617051' href='vote?id=27617051&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://www.theguardian.com/education/2021/jun/24/half-of-uk-university-students-think-degree-is-poor-value-for-money" class="storylink">Half of UK university students think degree is poor value for money</a><span class="sitebit comhead"> (<a href="from?site=theguardian.com"><span class="sitestr">theguardian.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27617051">79 points</span> by <a href="user?id=mocko" class="hnuser">mocko</a> <span class="age"><a href="item?id=27617051">2 hours ago</a></span> <span id="unv_27617051"></span> | <a href="hide?id=27617051&amp;goto=news">hide</a> | <a href="item?id=27617051">87&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27615849'>
      <td align="right" valign="top" class="title"><span class="rank">27.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27615849' href='vote?id=27615849&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://www.technologyreview.com/2021/06/24/1027048/youtube-xinjiang-censorship-human-rights-atajurt/" class="storylink">How YouTube’s rules are used to silence human rights activists</a><span class="sitebit comhead"> (<a href="from?site=technologyreview.com"><span class="sitestr">technologyreview.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27615849">250 points</span> by <a href="user?id=headalgorithm" class="hnuser">headalgorithm</a> <span class="age"><a href="item?id=27615849">5 hours ago</a></span> <span id="unv_27615849"></span> | <a href="hide?id=27615849&amp;goto=news">hide</a> | <a href="item?id=27615849">134&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27614580'>
      <td align="right" valign="top" class="title"><span class="rank">28.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27614580' href='vote?id=27614580&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://www.cam.ac.uk/research/news/vegan-spider-silk-provides-sustainable-alternative-to-single-use-plastics" class="storylink">‘Vegan spider silk’ provides sustainable alternative to single-use plastics</a><span class="sitebit comhead"> (<a href="from?site=cam.ac.uk"><span class="sitestr">cam.ac.uk</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27614580">113 points</span> by <a href="user?id=montalbano" class="hnuser">montalbano</a> <span class="age"><a href="item?id=27614580">9 hours ago</a></span> <span id="unv_27614580"></span> | <a href="hide?id=27614580&amp;goto=news">hide</a> | <a href="item?id=27614580">82&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27593490'>
      <td align="right" valign="top" class="title"><span class="rank">29.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27593490' href='vote?id=27593490&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://sanfrancisco.cbslocal.com/2021/06/07/catalytic-converter-theft-precious-metals-manufacturers-middlemen-making-money/" class="storylink">Catalytic Converter Theft</a><span class="sitebit comhead"> (<a href="from?site=cbslocal.com"><span class="sitestr">cbslocal.com</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27593490">57 points</span> by <a href="user?id=secondary" class="hnuser">secondary</a> <span class="age"><a href="item?id=27593490">7 hours ago</a></span> <span id="unv_27593490"></span> | <a href="hide?id=27593490&amp;goto=news">hide</a> | <a href="item?id=27593490">82&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
                <tr class='athing' id='27594733'>
      <td align="right" valign="top" class="title"><span class="rank">30.</span></td>      <td valign="top" class="votelinks"><center><a id='up_27594733' href='vote?id=27594733&amp;how=up&amp;goto=news'><div class='votearrow' title='upvote'></div></a></center></td><td class="title"><a href="https://hynek.me/articles/python-subclassing-redux/" class="storylink">Subclassing in Python Redux</a><span class="sitebit comhead"> (<a href="from?site=hynek.me"><span class="sitestr">hynek.me</span></a>)</span></td></tr><tr><td colspan="2"></td><td class="subtext">
        <span class="score" id="score_27594733">75 points</span> by <a href="user?id=hprotagonist" class="hnuser">hprotagonist</a> <span class="age"><a href="item?id=27594733">6 hours ago</a></span> <span id="unv_27594733"></span> | <a href="hide?id=27594733&amp;goto=news">hide</a> | <a href="item?id=27594733">2&nbsp;comments</a>              </td></tr>
      <tr class="spacer" style="height:5px"></tr>
            <tr class="morespace" style="height:10px"></tr><tr><td colspan="2"></td><td class="title"><a href="news?p=2" class="morelink" rel="next">More</a></td></tr>
  </table>
</td></tr>
<tr><td><img src="s.gif" height="10" width="0"><table width="100%" cellspacing="0" cellpadding="1"><tr><td bgcolor="#ff6600"></td></tr></table><br><center><span class="yclinks"><a href="newsguidelines.html">Guidelines</a>
        | <a href="newsfaq.html">FAQ</a>
        | <a href="lists">Lists</a>
        | <a href="https://github.com/HackerNews/API">API</a>
        | <a href="security.html">Security</a>
        | <a href="http://www.ycombinator.com/legal/">Legal</a>
        | <a href="http://www.ycombinator.com/apply/">Apply to YC</a>
        | <a href="mailto:hn@ycombinator.com">Contact</a></span><br><br><form method="get" action="//hn.algolia.com/">Search:
          <input type="text" name="q" value="" size="17" autocorrect="off" spellcheck="false" autocapitalize="off" autocomplete="false"></form>
            </center></td></tr>
      </table></center></body><script type='text/javascript' src='hn.js?DqVgzIak3Krx8fVwunvN'></script></html>
    """


# @pytest.fixture
# def html_link():
#     return """<a href="?page=2">next</a>"""


def test_extract_news():
    # url = "https://news.ycombinator.com/"

    assert extract_news(html_doc(), 1) == [
        {
            "author": "fortran77",
            "author_url": "user?id=fortran77",
            "comments": "133",
            "points": 140,
            "title": "NASA Can't Figure Out What's Causing Computer Issues on the Hubble Telescope",
            "url": "https://www.npr.org/2021/06/23/1009567351/hubble-trouble-nasa-cant-figure-out-whats-causing-computer-issues-on-the-telesco",
            "resource_text": "npr.org",
            "resource_url": "from?site=npr.org",
        }
    ]

    assert extract_news(html_doc(), 2) == [
        {
            "author": "fortran77",
            "author_url": "user?id=fortran77",
            "comments": "133",
            "points": 140,
            "title": "NASA Can't Figure Out What's Causing Computer Issues on the Hubble Telescope",
            "url": "https://www.npr.org/2021/06/23/1009567351/hubble-trouble-nasa-cant-figure-out-whats-causing-computer-issues-on-the-telesco",
            "resource_text": "npr.org",
            "resource_url": "from?site=npr.org",
        },
        {
            "author": "TangerineDream",
            "author_url": "user?id=TangerineDream",
            "comments": "2",
            "points": 17,
            "title": "The Next Backblaze Storage Pod",
            "url": "https://www.backblaze.com/blog/next-backblaze-storage-pod/",
            "resource_text": "backblaze.com",
            "resource_url": "from?site=backblaze.com",
        },
    ]


def extract_next_page_url():
    assert extract_next_page(html_doc()) == "?p=2"


@responses.activate
def test_get_news():
    news = []
    url = "https://news.ycombinator.com/"
    n_pages = 3

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    current_news = extract_news(soup)
    next_url = extract_next_page_url(soup)
    url = "https://news.ycombinator.com/" + next_url
    news.extend(current_news)

    assert get_news("https://news.ycombinator.com/") == news
