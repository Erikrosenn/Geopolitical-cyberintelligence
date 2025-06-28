---
title: "Microsoft security updates address CrowdStrike crash, kill ‘Blue Screen of Death’"
date: 2025-06-28
source: https://cyberscoop.com/microsoft-security-updates-kernel-restrictions-downtime/
publisher: cyberscoop
tags: [cyber, geopolitics]
---

## TL;DR

CrowdStrike’s Falcon endpoint detection and response was on millions of Windows devices worldwide. The software had direct access to the Windows kernel. Microsoft will be previewing a new endpoint security platform to vendors next month.

## Full Article

Voting is open for the 2025 CyberScoop 50 awards!

By
Derek B. Johnson

June 27, 2025

When a faulty software update from cybersecurity firm CrowdStrike last year caused possibly the largest IT outage in history, Microsoft ended up taking much of the blame.

CrowdStrike’s Falcon endpoint detection and response was on millions of Windows devices worldwide, and like most antivirus products that need broad access to different systems to do their job, the software had direct access to the Windows kernel.

When CrowdStrike’s update crashed, so did millions of Windows-powered systems and devices around the world. A series of security announcements by Microsoft on Thursday are designed to reduce the possibility of future third-party outages and other security threats that can take an organization’s IT out of commission for extended durations.

Among those changes: antivirus software like the kind installed by CrowdStrike and other third-party cybersecurity will no longer have direct access to the Windows kernel. The company will be previewing a new endpoint security platform to vendors next month that requires security updates to go through layers of testing and review before they ship to Windows devices and systems worldwide.

“The new Windows capabilities will allow them to start building their solutions to run outside the Windows kernel,” wrote David Weston, vice president for enterprise and OS security at Microsoft. “This means security products like anti-virus and endpoint protection solutions can run in user mode just as apps do. This change will help security developers provide a high level of reliability and easier recovery resulting in less impact on Windows devices in the event of unexpected issues.”

In a statement that was included in Microsoft’s announcement, Alex Ionescu, CrowdStrike’s chief technology innovation officer, said the company has engaged with customers over the past year that have driven “substantial improvements to the planned capabilities for the Windows endpoint security platform.”

Ionescu said CrowdStrike remains “fully committed to developing a Windows endpoint security platform-ready product and look forward to leveraging these new capabilities as Microsoft releases them.”

While CrowdStrike executives took the blame in front of Congress, the incident only affected an estimated 1% of total Windows operating systems worldwide and was patched within hours, IT outages at some organizations lingered for days. Overall the incident caused substantial embarrassment to executives in Redmond and revived lingering arguments that an overreliance on Microsoft creates a single point of failure for many companies and governments worldwide.

Trey Ford, chief information security officer at BugCrowd, said the changes by Microsoft were long overdue, noting the CrowdStrike outage wasn’t even the first widespread Windows outage created by a faulty antivirus update: in 2010 a faulty McAfee update bricked thousands of Windows XP devices worldwide.

“Administrators, and the teams managing them, will need to work through how the scope of permissions will impact their current deployments – but the effort is more than worth it, these are worthy investments,” Ford told CyberScoop.

Microsoft also announced another change that should bring some solace to anyone who has had their computer or device bricked and witnessed the dreaded “Blue Screen of Death.”

A previous Windows 11 update made fixes to the crash dump collection, reducing the downtime during a crash — or an “unexpected restart experience” as Microsoft calls it — to under two seconds.

Later this summer, a Windows update will replace the infamous blue wall of text displayed on the screen during a crash with “a simplified user interface that pairs with the shortened experience,” while also “preserving the technical information on the screen for when it is needed.”The alterations — along with a new quick recovery mechanism for Windows PCs that can’t properly reboot — is “part of a larger continued effort to reduce disruption in the event of an unexpected restart,” Weston wrote.

Other updates announced by Microsoft include the release of a new e-book focused on building resilience in Windows-based systems, the use of connected cache nodes to better handle bandwidth needs for simultaneous security updates across IT, and an optional autopatch feature that can run security updates without needing to restart.