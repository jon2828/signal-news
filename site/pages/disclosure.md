# How this site works

Every post on Unspent Thoughts is produced by software. A script pulls feeds from about a dozen sources twice a day, a language model scores each story for importance, another writes the post, and a third checks it against those sources before anything goes up. No human edits a post before it publishes. The writer and the fact-checker are different model families with different instructions, so a mistake has to fool two independent systems to reach you.

The whole thing runs on free tiers first. When those run dry, it falls back to paid APIs that cost a few dollars in a busy month — about the price of a latte. The hosting and scheduling are free, so the site never needs to chase traffic to pay for itself.

The rules the software follows: nothing over 1,000 words, every factual claim links to its source, and stories are linked and summarized, never republished. On a day without important news, nothing gets posted. That is deliberate. A quota is the enemy of relevance, so the site is allowed to be quiet.

The score on each post is the triage rating, 1 to 10, that the story earned when it was picked. Anything that scored too low was dropped, and the rejections are logged with the reason. All of it lives in the site's open source repository, along with every draft the system ever declined to publish. If a post turns out to be wrong, the correction shows up in the repo history the same way the mistake does.

The infrastructure is nearly free on purpose: GitHub Actions for scheduling, free language-model tiers tried first, and Cloudflare for hosting. The paid API fallbacks only kick in on busy days. The site never needs to chase traffic to pay for itself.
