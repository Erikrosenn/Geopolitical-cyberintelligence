---
title: "Over 1,000 SOHO Devices Hacked in China-linked LapDogs Cyber Espionage Campaign"
date: 2025-06-28
source: https://thehackernews.com/2025/06/over-1000-soho-devices-hacked-in-china.html
publisher: thehackernews
tags: [cyber, geopolitics]
---

## TL;DR

A network of more than 1,000 compromised small office and home office (SOHO) devices has been discovered. The Operational Relay Box (ORB) network has been codenamed LapDogs by SecurityScorecard's STRIKE team. The network has a high concentration of victims across the United States and Southeast Asia.

## Full Article

Threat hunters have discovered a network of more than 1,000 compromised small office and home office (SOHO) devices that have been used to facilitate a prolonged cyber espionage infrastructure campaign for China-nexus hacking groups.

The Operational Relay Box (ORB) network has been codenamed LapDogs by SecurityScorecard's STRIKE team.

"The LapDogs network has a high concentration of victims across the United States and Southeast Asia, and is slowly but steadily growing in size," the cybersecurity company said in a technical report published this week.

Other regions where the infections are prevalent include Japan, South Korea, Hong Kong, and Taiwan, with victims spanning IT, networking, real estate, and media sectors. Active infections span devices and services from Ruckus Wireless, ASUS, Buffalo Technology, Cisco-Linksys, Cross DVR, D-Link, Microsoft, Panasonic, and Synology.

LapDogs' beating heart is a custom backdoor called ShortLeash that's engineered to enlist infected devices in the network. Once installed, it sets up a fake Nginx web server and generates a unique, self-signed TLS certificate with the issuer name "LAPD" in an attempt to impersonate the Los Angeles Police Department. It's this reference that has given the ORB network its name.

ShortLeash is assessed to be delivered by means of a shell script to primarily penetrate Linux-based SOHO devices, although artifacts serving a Windows version of the backdoor have also been found. The attacks themselves weaponize N-day security vulnerabilities (e.g., CVE-2015-1548 and CVE-2017-17663) to obtain initial access.

First signs of activity related to LapDogs have been detected as far back as September 6, 2023, in Taiwan, with the second attack recorded four months later, on January 19, 2024. There is evidence to suggest that the campaigns are launched in batches, each of which infects no more than 60 devices. A total of 162 distinct intrusion sets have been identified to date.

The ORB has been found to share some similarities with another cluster referred to as PolarEdge, which was documented by Sekoia earlier this February as exploiting known security flaws in routers and other IoT devices to corral them into a network since late 2023 for an as-yet-undetermined purpose.

The overlaps aside, LapDogs and PolarEdge are assessed as two separate entities, given the differences in the infection process, the persistence methods used, and the former's ability to also target virtual private servers (VPSs) and Windows systems.

"While PolarEdge backdoor replaces the CGI script of the devices with the operator's designated webshell, ShortLeash merely inserts itself into the system directory as a .service file, ensuring the persistence of the service upon reboot, with root-level privileges," SecurityScorecard noted.

What's more, it has been gauged with medium confidence that the China-linked hacking crew tracked as UAT-5918 used LapDogs in at least one of its operations aimed at Taiwan. It's currently not known if UAT-5918 is behind the network or is just a client.

Chinese threat actors' use of ORB networks as a means of obfuscation has been previously documented by Google Mandiant, Sygnia and SentinelOne, indicating that they are being increasingly adopted into their playbooks for highly targeted operations.

"While both ORBs and botnets commonly consist of a large set of compromised, legitimate internet-facing devices or virtual services, ORB networks are more like Swiss Army knives, and can contribute to any stage of the intrusion lifecycle, from reconnaissance, anonymized actor browsing, and netflow collection to port and vulnerability scanning, initiating intrusion cycles by reconfiguring nodes into staging or even C2 servers, and relaying exfiltrated data up the stream," SecurityScorecard said.