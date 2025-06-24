---
title: "Unusually patient suspected Russian hackers pose as State Department in ‘sophisticated’ attacks on researchers"
date: 2025-06-24
source: https://cyberscoop.com/russian-hackers-state-department-sophisticated-attacks-researchers-citizen-lab/
publisher: cyberscoop
tags: [cyber, geopolitics]
---

## TL;DR

 Russian military expert Keir Giles was targeted by State Department impersonators who compromised his account over the weekend . A report from the University of Toronto’s Citizen Lab details a “highly sophisticated attack” that bypasses multi-factor authentication . Google's Threat Intelligence Group is releasing a related blog post on who is behind the compromise of Giles’ accounts .

## Full Article

Voting is open for the 2025 CyberScoop 50 awards!

By
Tim Starks

June 18, 2025

The hackers targeting prominent researcher and Russian military expert Keir Giles were different this time.

The attackers, suspected to be working on behalf of the Russian government, had ginned up the May solicitation email for a consultation with a state.gov address, one that didn’t get a bounceback message when Giles replied. They spoke convincing English, and delivered their message during East Coast business hours. He said they created a realistic domain name to direct him to, rather than using a random string of text. They weren’t in a hurry, pressuring him to respond the way hackers usually do.

“Unlike any of the previous times when they’ve had a go at me, I haven’t actually seen anywhere they’ve put a foot wrong and done something which is implausible,” Giles, who is also a senior consulting fellow for the Russia and Eurasia program at the British think tank Chatham House, told CyberScoop. “It was totally straight up and very well-constructed from beginning to end.”

A report out Wednesday from the University of Toronto’s Citizen Lab that calls the targeting of Giles a “highly sophisticated attack” also details a “novel method” the hackers used to bypass one of the most well-regarded cyber defense tools, multi-factor authentication (MFA).

As Citizen Lab is publishing its forensic analysis of what happened with Giles, Google’s Threat Intelligence Group is also releasing a related blog post on who is behind the compromise of Giles’ accounts, and how he’s not the only one they’ve targeted with that specific technical attack method.

Giles warned over the weekend in a LinkedIn post about the State Department impersonators who had compromised his account, promising “more on the how, what and when later.”

The “how” involved the credible social engineering aspects that he and Citizen Lab have revealed. On the technical side, the final step was convincing Giles to create and share a screenshot of an app-specific password (ASP), a tool that can be used to give third parties access to users’ accounts that don’t support multi-factor authentication. ASPs are meant to be a convenience and security aid when using third parties without MFA, but in this case the hackers leveraged them to compromise Giles’ Google accounts.

Google picked up on what was happening, then sent Giles a security alert and locked his accounts.

“The days of just tricking someone to hand over a password are over,” John Scott-Railton, senior researcher at Citizen Lab, told CyberScoop. “Companies are getting smarter about detecting hacking, and have given users a lot of new security features, like muti-factor authentication. Users have also gotten wiser to what classic phishing looks like.

“So the more sophisticated hacking groups are constantly innovating and trying to spot new technical and psychological tricks to get access to accounts,” he continued. “This means that they are also probing other ways of gaining access, like tokens and app-specific passwords.”

The Google Threat Intelligence Group (GTIG) assessment is that the hackers in this case, which they’ve dubbed UNC6293, are potentially connected to a unit tied to Russia’s Foreign Intelligence Service, known by names such as APT29, Cozy Bear or ICECAP. The attacks on Giles aren’t the only slow-roll, ASP-based ones GTIG researchers have seen on academics and Russia critics from April through earlier this month, although they couldn’t give precise numbers.

It’s not, though, “widespread” by any means, said Wesley Shields, a security engineer with GTIG. Because the process is so time-consuming, it would be difficult to repeat on a larger scale, said Shields and Gabriella Roncone, Russia and Eastern European tech lead at GTIG.

“Normally we see APT29 or ICECAP targeting larger diplomatic organizations, NGOs — really going after corporate entities or large organizations,” Roncone said. “Whereas in this case, we’re seeing only individuals being targeted, and not only that, but individuals being targeted in a very specific and patient way.”

That patience was a standout feature to Scott-Railton as well.

“What impresses me about this attack is how patient the attackers were, slowly unfolding their deception over a period of weeks. It’s as if they knew everything we’d been taught to expect from Russian hackers, and then did the opposite,” Scott-Railton said.

The deception required a lot of effort and knowledge. For instance, the attackers were likely aware that the State Department’s email server is set up to accept all messages, and that it doesn’t send a bounceback message for non-existent addresses, according to the Citizen Lab report. The email’s authentic-sounding English might have been improved with the use of a large language model.

“There was not something about it, which, as so often happens, it gets your Spidey sense going, because something is off,” Giles said. “That was completely absent.”

Giles presumes a leak of any information the hackers obtained, with a mix of phony and altered data, is forthcoming. He quipped that if their goal was espionage, “they would have very quickly got very disappointed.” He was still hearing from the attackers even after he posted about it on social media, with the account he’d interacted with “complaining of technical difficulties and saying, ‘Bear with us a bit longer.’”

Giles said he was frustrated that he didn’t get an alert from Google about the risks of ASPs, and believed that since Google Workspace was a paid-for service, he would’ve gotten an explanation or more support from the company as opposed to shutting the account and saying it had been closed for security violations.

Google’s blog post said it does send such alerts about ASPs. It also encouraged users who could be at great risk of being hacked to sign up for its Advanced Protection Program, which forbids the use of ASPs.

Scott-Railton praised Giles, potentially the “patient zero” for this kind of attack, for speaking up about it.

Giles said he was “fairly relaxed” about being victimized.

“Nobody’s invulnerable, and they had been trying so very hard for so very long that it was bound to get through eventually,” he said.

During a round of cyberattacks last year, Giles said, “One of the really frustrating things was the people who had been infected and whose accounts were being leveraged to target me then, who were absolutely unwilling to talk about it because they were too embarrassed… they really limited what you could do with some of this stuff.

“So I’m not inclined to cover up the way in which they succeeded in outwitting me,” he said. “I guess if they’re spending this much effort on me, there are other more important targets that are getting less attention as a result. So that’s not such a bad thing.”