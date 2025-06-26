---
title: "Stealth China-linked ORB network gaining footholds in US, East Asia"
date: 2025-06-26
source: https://cyberscoop.com/orb-network-china-lapdogs/
publisher: cyberscoop
tags: [cyber, geopolitics]
---

## TL;DR

A network controlled by a China-linked threat group already exceeds 1,000 devices. The ORB network is primarily composed of routers designed for small or home offices. More than one-third of the infections are located in the United States.

## Full Article

Voting is open for the 2025 CyberScoop 50 awards!

By
Matt Kapko

June 25, 2025

A recently discovered operational relay box (ORB) network controlled by a China-linked threat group already exceeds 1,000 devices and is growing across the United States and East Asia, SecurityScorecard said in a threat report released Monday.

The ORB network, which SecurityScorecard dubbed “LapDogs,” is primarily composed of routers designed for small or home offices but also includes infected IoT devices, virtual servers and IP cameras.

Earliest nodes detected by researchers date back to September 2023 and the network has gradually grown since, infecting no more than 60 devices at a time, indicating a highly targeted operation focused on specific locations. Researchers have identified 162 distinct intrusion sets, and more devices are added to the ORB with each intrusion campaign.

“The expansion rate of LapDogs is going up,” Gilad Maizles, security researcher at SecurityScorecard, said in an email. “Campaigns become more frequent, and with greater yield in numbers, which ultimately leads to more devices added than removed from the network.”

More than one-third of the infections are located in the United States, followed by Japan, South Korea, Taiwan and Hong Kong. Active infections span devices and services from Ruckus Wireless, Asus, Buffalo Technology, Cisco-Linksys, D-Link, Microsoft, Panasonic and Synology. More than half of the compromised devices are Ruckus Wireless access points, according to SecurityScorecard.

“Post-infection activity from this network is still unclear,” Maizles said. “Some ORBs used by China-Nexus actors are shared infrastructure and can host and facilitate more than one intrusion set at once. This makes questions regarding APT motivations, TTPs and post-infection activities much harder to answer. This also ultimately demonstrates how harmful and dangerous ORBs are as an emerging threat within the China-Nexus APT landscape.”

ORB networks are more complicated than botnets, allowing threat groups who control them more stealth capabilities typically used for espionage.

Botnets are similar in that they also ride on a large set of internet-facing devices or virtual services, but “ORB networks are more like Swiss Army knives, and can contribute to any stage of the intrusion lifecycle,” SecurityScorecard researchers said in the report. This includes reconnaissance, anonymized browsing, network traffic data collection for port and vulnerability scanning, node reconfiguration and relaying stolen data upstream.

Mandiant Intelligence previously chronicled China state-sponsored threat groups’ growing use of ORB networks as a low-effort exercise designed to “create a constantly evolving mesh network that can be used to conceal espionage operations.”

ORB networks chip away at the notion of attacker-controlled architecture and because they cycle through network infrastructure on a monthly basis. Mandiant researchers warn that the elimination of indicators of compromise is accelerating, because these operational characteristics of ORB networks make it harder for threat researchers to spot and attribute unusual activity on infected nodes.

The number of devices infected by LapDogs is smaller than other ORBs, but that is likely due to a deliberate decision by the threat group operating the ORB, Maizles said.

“We speculate that it is an attempt to keep the ORB under the radar and successfully so for the past two years,” he said. “LapDogs could be utilized for long-term, covert and localized operations, which can carry much greater impact on any given organization, rather than widespread infections.”