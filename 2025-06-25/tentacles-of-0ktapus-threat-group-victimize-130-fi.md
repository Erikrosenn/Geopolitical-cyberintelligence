---
title: "Tentacles of ‘0ktapus’ Threat Group Victimize 130 Firms"
date: 2025-06-25
source: https://threatpost.com/0ktapus-victimize-130-firms/180487/
publisher: threatpost
tags: [cyber, geopolitics]
---

## TL;DR

Share this article:

Over 130 companies tangled in sprawling phishing campaign that spoofed a multi-factor authentication system Targeted attacks on Twilio and Cloudflare employees are tied to a massive phishing campaign that resulted in 9,931 accounts at over 130 organizations being compromised “These users received text messages containing links to phishing sites that mimicked the Okta authentication page of their organization

## Full Article

Share this article:

Over 130 companies tangled in sprawling phishing campaign that spoofed a multi-factor authentication system.

Targeted attacks on Twilio and Cloudflare employees are tied to a massive phishing campaign that resulted in 9,931 accounts at over 130 organizations being compromised. The campaigns are tied to focused abuse of identity and access management firm Okta, which gained the threat actors the 0ktapus moniker, by researchers.

“The primary goal of the threat actors was to obtain Okta identity credentials and multi-factor authentication (MFA) codes from users of the targeted organizations,” wrote Group-IB researchers in a recent report. “These users received text messages containing links to phishing sites that mimicked the Okta authentication page of their organization.”

Impacted were 114 US-based firms, with additional victims of sprinkled across 68 additional countries.

Roberto Martinez, senior threat intelligence analyst at Group-IB, said the scope of the attacks is still an unknown. “The 0ktapus campaign has been incredibly successful, and the full scale of it may not be known for some time,” he said.

The 0ktapus attackers are believed to have begun their campaign by targeting telecommunications companies in hopes of winning access to potential targets’ phone numbers.

While unsure exactly how threat actors obtained a list of phone numbers used in MFA-related attacks, one theory researchers posit is that 0ktapus attackers began their campaign targeting telecommunications companies.

“[A]ccording to the compromised data analyzed by Group-IB, the threat actors started their attacks by targeting mobile operators and telecommunications companies and could have collected the numbers from those initial attacks,” researchers wrote.

Next, attackers sent phishing links to targets via text messages. Those links led to webpages mimicking the Okta authentication page used by the target’s employer. Victims were then asked to submit Okta identity credentials in addition to a multi-factor authentication (MFA) codes employees used to secure their logins.

In an accompanying technical blog, researchers at Group-IB explain that the initial compromises of mostly software-as-a-service firms were a phase-one in a multi-pronged attack. 0ktapus’ ultimate goal was to access company mailing lists or customer-facing systems in hopes of facilitating supply-chain attacks.

In a possible related incident, within hours of Group-IB publishing its report late last week, the firm DoorDash revealed it was targeted in an attack with all the hallmarks of an 0ktapus-style attack.

In a blog post DoorDash revealed; “unauthorized party used the stolen credentials of vendor employees to gain access to some of our internal tools.” The attackers, according to the post, went on to steal personal information – including names, phone numbers, email and delivery addresses – from customers and delivery people.

In the course of its campaign, the attacker compromised 5,441 MFA codes, Group-IB reported.

“Security measures such as MFA can appear secure… but it is clear that attackers can overcome them with relatively simple tools,” researchers wrote.

“This is yet another phishing attack showing how easy it is for adversaries to bypass supposedly secure multifactor authentication,” Roger Grimes, data-driven defense evangelist at KnowBe4, wrote in a statement via email. “It simply does no good to move users from easily phish-able passwords to easily phish-able MFA. It’s a lot of hard work, resources, time, and money, not to get any benefit.”

To mitigate 0ktapus-style campaigns, the researchers recommended good hygiene around URLs and passwords, and using FIDO2-compliant security keys for MFA.

“Whatever MFA someone uses,” Grimes advised, “the user should be taught about the common types of attacks that are committed against their form of MFA, how to recognize those attacks, and how to respond. We do the same when we tell users to pick passwords but don’t when we tell them to use supposedly more secure MFA.”

Share this article: