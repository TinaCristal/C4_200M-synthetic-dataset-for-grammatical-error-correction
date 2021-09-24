"""Looks up C4 sentences by their hashes and stores them in a TSV file."""

import hashlib
import heapq
import json
from absl import app
import tensorflow_datasets as tfds

LOGGING_STEPS = 100000


def main(argv):
  if len(argv) != 3:
    raise app.UsageError(
        "python3 c4200m_get_target_sentences.py <edits-tsv> <output-tsv>")
  edits_tsv_path = argv[1]
  output_tsv_path = argv[2]

  print("Loading C4_200M target sentence hashes from %r..." % edits_tsv_path)
  remaining_hashes = set()
  with open(edits_tsv_path,encoding='utf-8') as edits_tsv_reader:
    for tsv_line in edits_tsv_reader:
      remaining_hashes.add(tsv_line.split("\t", 1)[0])
  print("Searching for %d target sentences in the C4 dataset..." %len(remaining_hashes))
  target_sentences = []
#   a=[{"text":"Beginners BBQ Class Taking Place in Missoula!\nDo you want to get better at making delicious BBQ? You will have the opportunity, put this on your calendar now. Thursday, September 22nd join World Class BBQ Champion, Tony Balay from Lonestar Smoke Rangers. He will be teaching a beginner level class for everyone who wants to get better with their culinary skills.\nHe will teach you everything you need to know to compete in a KCBS BBQ competition, including techniques, recipes, timelines, meat selection and trimming, plus smoker and fire information.\nThe cost to be in the class is $35 per person, and for spectators it is free. Included in the cost will be either a t-shirt or apron and you will be tasting samples of each meat that is prepared.","timestamp":"2019-04-25T12:57:54Z","url":"https://klyq.com/beginners-bbq-class-taking-place-in-missoula/"},
# {"text":"Discussion in 'Mac OS X Lion (10.7)' started by axboi87, Jan 20, 2012.\nI've got a 500gb internal drive and a 240gb SSD.\nWhen trying to restore using disk utility i'm given the error \"Not enough space on disk ____ to restore\"\nBut I shouldn't have to do that!!!\nAny ideas or workarounds before resorting to the above?\nUse Carbon Copy Cloner to copy one drive to the other. I've done this several times going from larger HDD to smaller SSD and I wound up with a bootable SSD drive. One step you have to remember not to skip is to use Disk Utility to partition the SSD as GUID partition scheme HFS+ before doing the clone. If it came Apple Partition Scheme, even if you let CCC do the clone, the resulting drive won't be bootable. CCC usually works in \"file mode\" and it can easily copy a larger drive (that's mostly empty) onto a smaller drive. If you tell CCC to clone a drive you did NOT boot from, it can work in block copy mode where the destination drive must be the same size or larger than the drive you are cloning from (if I recall).\nI've actually done this somehow on Disk Utility several times (booting from a different drive (or even the dvd) so not running disk utility from the drive your cloning) and had it work just fine from larger to smaller bootable clone. Definitely format the drive cloning to first, as bootable Apple etc..\nThanks for pointing this out. My only experience using DU to go larger to smaller was when I was trying to make a Lion install stick and I was unable to restore InstallESD.dmg to a 4 GB USB stick but of course the reason that wouldn't fit is there was slightly more than 4 GB of data.","timestamp":"2019-04-21T10:07:13Z","url":"https://forums.macrumors.com/threads/restore-from-larger-disk-to-smaller-disk.1311329/"},
# {"text":"Foil plaid lycra and spandex shortall with metallic slinky insets. Attached metallic elastic belt with O-ring. Headband included. Great hip hop or jazz dance costume. Made in the USA.","timestamp":"2019-04-25T10:40:23Z","url":"https://awishcometrue.com/Catalogs/Clearance/Tweens/V1960-Find-A-Way"},
# {"text":"How many backlinks per day for new site?\nDiscussion in 'Black Hat SEO' started by Omoplata, Dec 3, 2010.\n1) for a newly created site, what's the max # backlinks per day I should do to be safe?\n2) how long do I have to let my site age before I can start making more blinks?\nI did about 6000 forum profiles every 24 hours for 10 days for one of my sites which had a brand new domain.\nThere is three backlinks for every of these forum profile so thats 18 000 backlinks every 24 hours and nothing happened in terms of being penalized or sandboxed. This is now maybe 3 months ago and the site is ranking on first page for a lot of my targeted keywords.\nbuild more you can in starting but do manual submission and not spammy type means manual + relevant to the post.. then after 1 month you can make a big blast..\nWow, dude, you built 18k backlinks a day on a brand new site? How quickly did you rank up? What kind of competition/searches did those keywords have?","timestamp":"2019-04-21T12:46:19Z","url":"https://www.blackhatworld.com/seo/how-many-backlinks-per-day-for-new-site.258615/"},
# {"text":"The Denver Board of Education opened the 2017-18 school year with an update on projects that include new construction, upgrades, heat mitigation and quality learning environments.\nWe are excited that Denver students will be the beneficiaries of a four year, $572 million General Obligation Bond. Since the passage of the bond, our construction team has worked to schedule the projects over the four-year term of the bond.\nDenver voters on Tuesday approved bond and mill funding measures for students in Denver Public Schools, agreeing to invest $572 million in bond funding to build and improve schools and $56.6 million in operating dollars to support proven initiatives, such as early literacy.\nDenver voters say yes to bond and mill levy funding support for DPS students and schools. Click to learn more about the details of the voter-approved bond measure.\nDenver voters on Nov. 8 approved bond and mill funding measures for DPS students and schools. Learn more about what’s included in the mill levy measure.","timestamp":"2019-04-20T14:33:21Z","url":"http://bond.dpsk12.org/category/news/"},
# {"text":"BANGALORE CY JUNCTION SBC to GONDIA JUNCTION G train timings, routes, stops, and complete info.\nAs of now, 1 trains run between from BANGALORE CY JUNCTION (YPR) to GONDIA JUNCTION (G).\nThe fastest train from BANGALORE CY JUNCTION (YPR) to GONDIA JUNCTION (G) is YPR KRBA WAINGANGA EXP (12251) that departs at 23:40 and arrives to at 21:15. It takes approximately 21:35 hours.","timestamp":"2019-04-20T04:25:39Z","url":"https://tatkalforsure.com/trains-between-stations/bangalore-cy-junction-sbc-to-gondia-junction-g/"},
# {"text":"I thought I was going to finish the 3rd season of the Wire tonight.\nBut there was a commentary on episode 11, so I had to re-watch Middle Ground with the commentary. Hopefully I can finish the season next weekend.","timestamp":"2019-04-18T14:16:05Z","url":"https://karaokegal.livejournal.com/1773485.html"},
# {"text":"The rich get richer and the poor get poorer eh?\nOr is it the rich think different and play by a different set of rules?\nDo the rich take responsibility and action?\nPoor people believe 'Life happens to me.' Rich people are committed to be rich.\nPoor people WANT to be rich. Rich people think big.\nPoor people think small. Rich people focus on opportunities.\nPoor people focus on obstacles. Rich people are willing to promote themselves and their value.\nPoor people think negatively about selling and promotion.\nPoor people are closed to new ideas..\nDo You think rich or poor?","timestamp":"2019-04-23T00:39:43Z","url":"http://www.iammeek.com/2018/06/the-rich-get-richer-and-poor-get-poorer.html"},
# {"text":"Biomedics 1 Day Extra are daily replacement disposable contact lenses by CooperVision Hydron. Buy one box of 90 lenses.\nBiomedics 1 Day Extra contacts give you all the convenience of a daily disposable lens with no need for solutions, cases or cleaning and are perfect for the occasional wear. These lenses have greater comfort handling with superior ease of insertion and removal.\nBiomedic 1 Day Extra are also marketed under various other brand names including Clear Choice 1-day, Ascend 1-day, easyvision CLARISION SPHERE, Clearsight 1 Day and ProView Daily Disposable.","timestamp":"2019-04-26T09:38:13Z","url":"https://www.webcontacts.com.au/Biomedics-contact-lenses/Biomedics-1-Day-Extra-90-pack"},
# {"text":"Sysco Corp. has terminated its planned $3.5 billion takeover of US Foods, it announced Monday, after a federal judge blocked the combination. The company is opting instead to add $3 billion to its stock-buyback program.\nWith the deal breaking up, Sysco will pay a $300 million termination fee to US Foods and a $12.5 million fee to Performance Food Group, which had agreed to buy some US Foods facilities. Sysco, based in Houston, plans to make the share repurchases over the next two years.\nRosemont, Illinois-based US Foods operates a major distribution center in Fishers. Sysco has a large warehouse at 4000 W. 62nd St., in Indianapolis.\nSysco had fought for more than a year to gain government approval for the transaction, which antitrust regulators said would hurt competition and lead to higher prices. Sysco and US Foods dominate a market known as broadline foodservice, which supplies school cafeterias, restaurants and hotels. Sysco had argued that the acquisition would bring $1 billion in savings, letting it offer lower prices to customers.\nInvestors have responded with relief to the deal’s demise, reflecting concerns about the company undertaking an ambitious merger. Sysco shares rose 3.1 percent the day the transaction was halted by U.S. District Judge Amit Mehta, and the stock climbed again Monday morning after the merger was withdrawn.\nMehta blocked the merger on June 23 when he granted a Federal Trade Commission request to delay the transaction. The FTC had sued the companies in February, saying the deal would give Sysco an oversized share of an industry where it’s already the biggest player.\nIn arguments before Mehta in May, the two sides clashed over the scope of the market in which the companies compete. Sysco and US Foods argued that the commission was relying on a “tortured” analysis, ignoring the variety of distribution channels available to customers.\nSysco said on Monday that it weighed embarking on an appeal but decided against it.\nShares of Sysco rose as much as 1.6 percent to $39 in early trading. The stock had slid 3.3 percent this year through the end of last week.","timestamp":"2019-04-23T08:52:53Z","url":"https://www.ibj.com/articles/53814-sysco-terminates-planned-35b-takeover-of-us-foods"},
# {"text":"Pencarian FILM Untuk \"Peace Breaker 2017\"\nyuk mampir ke channel say..\nEdges East provides the l..\nA corrupt cop makes one w..\nPeace Breaker 2017 ~ 破�..\nNáo Loạn - Peace Break..\nPlease subscribe and hit ..\nuploaded in HD at http://..\nI cannot believe I manage..","timestamp":"2019-04-24T22:04:22Z","url":"http://layarbioskop21.info/search/peace-breaker-2017"},
# {"text":"Below you'll find some great videos that will encourage you, train you and build you up in hearing from GOD and being able to let HIM fulfill HIS plan in your life.\nSOMETHING NEW THAT WILL HELP YOU HEAR GODS VOICE!\nHow to Understand and Rightly Divide It & How It Applies to Life!\nIn this important teaching Terry reveals the clear distinction between the Spirit & Soul and how critical it is that we learn how to operate in the Spirit and not be deceived. It's a serious matter that must be reviewed no matter what your level of faith and maturity.\nMarriage & How it Applies to the Spirit & The Soul!\nIn this enlightening class Terry reveals a key insight that helps us to better discern the Spirit vs the Soul as it's reflected in the Marriage relationship from the intuitive nature, the emotional component of the woman and the power aspect of a male in submission to the LORD.\nIn this eye-opening teaching Terry shares how the Tabernacle as it represents the body soul and spirit of man and how it applies to our spiritual walk.\nThis complete deliverance packet helps to walk you through what you can do to free yourself from the hidden forced buried deep in your soul that is hindering you from walking in the fullness that GOD paid for you to walk in.\nIn today's video, Terry defines salvation better and the things that get in the way of our soul's salvation and ways we can increase our spiritual maturity.","timestamp":"2019-04-26T06:11:48Z","url":"http://trivisionglobal.com/members-dashboard/the-kings-table-members/the-kings-table-video-vault/other-videos/"}]

  a=[]
  with open("8ef8d75b0e045dec4aa5123a671b4564466b0707086a7ed1ba8721626dfffbc9","r",encoding="utf-8") as f:
      for line in f:
          a.append(json.loads(line))
  for num_done_examples, example in enumerate(a):
      for line in example["text"].split("\n"):
        line_md5 = hashlib.md5(line.encode("utf-8")).hexdigest()
        if line_md5 in remaining_hashes:
          heapq.heappush(target_sentences, (line_md5, line))
          remaining_hashes.remove(line_md5)
      if not remaining_hashes:
        break
      if num_done_examples % LOGGING_STEPS == 0:
        print("-- %d C4 examples done, %d sentences still to be found" %(num_done_examples, len(remaining_hashes)))
  print("Found %d target sentences (%d not found)." %(len(target_sentences), len(remaining_hashes)))
  print("Writing C4_200M sentence pairs to %r..." % output_tsv_path)
      with open(output_tsv_path, "w",encoding="utf-8") as output_tsv_writer:
        with open(edits_tsv_path,encoding="utf-8") as edits_tsv_reader:
          while target_sentences:
            output_tsv_writer.write("%s\t%s\n" % heapq.heappop(target_sentences))

if __name__ == "__main__":
  argv=['c4200m_get_target_sentences.py','edits.tsv-00001-of-00010','target_sentence.tsv-00001-of-00010']
  main(argv)