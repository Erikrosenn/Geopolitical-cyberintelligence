---
title: "North Korea-linked Supply Chain Attack Targets Developers with 35 Malicious npm Packages"
date: 2025-06-25
source: https://thehackernews.com/2025/06/north-korea-linked-supply-chain-attack.html
publisher: thehackernews
tags: [cyber, geopolitics]
---

## TL;DR

 35 malicious packages that were uploaded from 24 npm accounts have been collectively downloaded over 4,000 times . Each of the identified packages contains a hex-encoded loader dubbed HexEval, which is designed to collect host information post installation . BeaverTail is configured to download and execute a Python backdoor called InvisibleFerret, enabling the threat actors to collect sensitive data and establish remote control .

## Full Article

Cybersecurity researchers have uncovered a fresh batch of malicious npm packages linked to the ongoing Contagious Interview operation originating from North Korea.

According to Socket, the ongoing supply chain attack involves 35 malicious packages that were uploaded from 24 npm accounts. These packages have been collectively downloaded over 4,000 times. The complete list of the JavaScript libraries is below -

Of these, six continue to remain available for download from npm: react-plaid-sdk, sumsub-node-websdk, vite-plugin-next-refresh, vite-loader-svg, node-orm-mongoose, and router-parse.

Each of the identified npm packages contains a hex-encoded loader dubbed HexEval, which is designed to collect host information post installation and selectively deliver a follow-on payload that's responsible for delivering a known JavaScript stealer called BeaverTail.

BeaverTail, in turn, is configured to download and execute a Python backdoor called InvisibleFerret, enabling the threat actors to collect sensitive data and establish remote control of infected hosts.

"This nesting-doll structure helps the campaign evade basic static scanners and manual reviews," Socket researcher Kirill Boychenko said. "One npm alias also shipped a cross-platform keylogger package that captures every keystroke, showing the threat actors' readiness to tailor payloads for deeper surveillance when the target warrants it."

Contagious Interview, first publicly documented by Palo Alto Networks Unit 42 in late 2023, is an ongoing campaign undertaken by North Korean state-sponsored threat actors to obtain unauthorized access to developer systems with the goal of conducting cryptocurrency and data theft.

The cluster is also broadly tracked under the monikers CL-STA-0240, DeceptiveDevelopment, DEV#POPPER, Famous Chollima, Gwisin Gang, Tenacious Pungsan, UNC5342, and Void Dokkaebi.

Recent iterations of the campaign have also been observed taking advantage of the ClickFix social engineering tactic to deliver malware such as GolangGhost and PylangGhost. This sub-cluster of activity has been designated the name ClickFake Interview.

The latest findings from Socket point to a multi-pronged approach where Pyongyang threat actors are embracing various methods to trick prospective targets into installing malware under the pretext of an interview or a Zoom meeting.

The npm offshoot of Contagious Interview typically involves the attackers posing as recruiters on LinkedIn, sending job seekers and developers coding assignments by sharing a link to a malicious project hosted on GitHub or Bitbucket that embeds the npm packages within them.

"They target software engineers who are actively job-hunting, exploiting the trust that job-seekers typically place in recruiters," Boychenko said. "Fake personas initiate contact, often with scripted outreach messages and convincing job descriptions."

The victims are then coaxed into cloning and running these projects outside containerized environments during the purported interview process.

"This malicious campaign highlights an evolving tradecraft in North Korean supply chain attacks, one that blends malware staging, OSINT-driven targeting, and social engineering to compromise developers through trusted ecosystems," Socket said.

"By embedding malware loaders like HexEval in open source packages and delivering them through fake job assignments, threat actors sidestep perimeter defenses and gain execution on the systems of targeted developers. The campaign's multi-stage structure, minimal on-registry footprint, and attempt to evade containerized environments point to a well-resourced adversary refining its intrusion methods in real-time."