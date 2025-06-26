---
title: "Citrix Releases Emergency Patches for Actively Exploited CVE-2025-6543 in NetScaler ADC"
date: 2025-06-26
source: https://thehackernews.com/2025/06/citrix-releases-emergency-patches-for.html
publisher: thehackernews
tags: [cyber, geopolitics]
---

## TL;DR

Citrix has released security updates to address a critical flaw affecting NetScaler ADC. The vulnerability, tracked as CVE-2025-6543, carries a CVSS score of 9.2. The company did not reveal how the flaw is being exploited in real-world attacks.

## Full Article

Citrix has released security updates to address a critical flaw affecting NetScaler ADC that it said has been exploited in the wild.

The vulnerability, tracked as CVE-2025-6543, carries a CVSS score of 9.2 out of a maximum of 10.0.

It has been described as a case of memory overflow that could result in unintended control flow and denial-of-service. However, successful exploitation requires the appliance to be configured as a Gateway (VPN virtual server, ICA Proxy, CVPN, RDP Proxy) or AAA virtual server.

The shortcoming impacts the below versions -

"Secure Private Access on-prem or Secure Private Access Hybrid deployments using NetScaler instances are also affected by the vulnerabilities," Citrix said.

"Customers need to upgrade these NetScaler instances to the recommended NetScaler builds to address the vulnerabilities."

The company did not reveal how the flaw is being exploited in real-world attacks, but said "exploits of CVE-2025-6543 on unmitigated appliances have been observed."

The disclosure comes shortly after Citrix patched another critical-rated security flaw in NetScaler ADC (CVE-2025-5777, CVSS score: 9.3) that could be exploited by threat actors to gain access to susceptible appliances.