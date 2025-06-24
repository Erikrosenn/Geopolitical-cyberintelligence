---
title: "Hackers Target Over 70 Microsoft Exchange Servers to Steal Credentials via Keyloggers"
date: 2025-06-25
source: https://thehackernews.com/2025/06/hackers-target-65-microsoft-exchange.html
publisher: thehackernews
tags: [cyber, geopolitics]
---

## TL;DR

 Unidentified threat actors have been observed targeting publicly exposed Microsoft Exchange servers to inject malicious code into login pages that harvest their credentials . Positive Technologies identified two different kinds of keylogger code written in JavaScript on Outlook login page . The Russian cybersecurity vendor said the attacks have targeted 65 victims in 26 countries .

## Full Article

Unidentified threat actors have been observed targeting publicly exposed Microsoft Exchange servers to inject malicious code into the login pages that harvest their credentials.

Positive Technologies, in a new analysis published last week, said it identified two different kinds of keylogger code written in JavaScript on the Outlook login page -

The Russian cybersecurity vendor said the attacks have targeted 65 victims in 26 countries worldwide, and marks a continuation of a campaign that was first documented in May 2024 as targeting entities in Africa and the Middle East.

At that time, the company said it had detected no less than 30 victims spanning government agencies, banks, IT companies, and educational institutions, with evidence of the first compromise dating back to 2021.

The attack chains involve exploiting known flaws in Microsoft Exchange Server (e.g., ProxyShell) to insert keylogger code into the login page. It's presently not known who is behind these attacks.

Some of the vulnerabilities weaponized are listed below -

"Malicious JavaScript code reads and processes the data from the authentication form, then sends it via an XHR request to a specific page on the compromised Exchange Server," security researchers Klimentiy Galkin and Maxim Suslov said.

"The target page's source code contains a handler function that reads the incoming request and writes the data to a file on the server."

The file containing the stolen data is accessible from an external network. Select variants with the local keylogging capability have been found to also collect user cookies, User-Agent strings, and the timestamp.

One advantage of this approach is that the chances of detection are next to nothing as there is no outbound traffic to transmit the information.

The second variant detected by Positive Technologies, on the other hand, uses a Telegram bot as an exfiltration point via XHR GET requests with the encoded login and password stored in the APIKey and AuthToken headers, respectively.

A second method involves using a Domain Name System (DNS) tunnel in conjunction with an HTTPS POST request to send the user credentials and sneak past an organization's defenses.

Twenty-two of the compromised servers have been found in government organizations, followed by infections in the IT, industrial, and logistics companies. Vietnam, Russia, Taiwan, China, Pakistan, Lebanon, Australia, Zambia, the Netherlands, and Turkey are among the top 10 targets.

"A large number of Microsoft Exchange servers accessible from the Internet remain vulnerable to older vulnerabilities," the researchers said. "By embedding malicious code into legitimate authentication pages, attackers are able to stay undetected for long periods while capturing user credentials in plaintext."