---
title: "Researchers say AI hacking tools sold online were powered by Grok, Mixtral"
date: 2025-06-24
source: https://cyberscoop.com/uncensored-ai-tool-traced-to-mistral-xai-grok/
publisher: cyberscoop
tags: [cyber, geopolitics]
---

## TL;DR

Summary generation failed.

## Full Article

Voting is open for the 2025 CyberScoop 50 awards!

By
Derek B. Johnson

June 17, 2025

Multiple variants of jailbroken and uncensored AI tools being sold on hacker forums were likely generated using popular commercial large language models from Mistral AI and X’s Grok, according to research published Tuesday from Cato Networks.

As some commercial AI companies have sought to build guardrails into their models for safety and security — preventing them from explicitly coding malware, relaying detailed instructions for building bombs or other malicious behaviors — a parallel underground market has emerged offering to sell more uncensored versions of the technology.

These “WormGPTs” — named after one of the original AI tools first advertised on underground hacker forums in 2023 — are usually cobbled together from open-source models and other toolsets and can generate code, search for and analyze vulnerabilities, and are then marketed and sold online.

But according to Cato Networks researcher Vitaly Simonovich, two variants advertised on BreachForums over the past year have more straightforward origins.

“Cato CTRL has discovered previously unreported WormGPT variants that are powered by xAI’s Grok and Mistral AI’s Mixtral,” he wrote.

One variant, advertised on BreachForums in February, was accessed through Telegram, calling itself an “Uncensored Assistant,” but otherwise describing its purpose in positive and uncontroversial terms.

Simonovich obtained access to both models and started probing, finding them largely uncensored as advertised. The models were able to craft phishing emails and code PowerShell credential-stealing malware on command, along with other offensive capabilities.

However, he identified prompt-based guardrails designed to elide one thing: the original system prompts used to program those models. Using an LLM jailbreaking technique, he was able to bypass the restrictions and view the first 200 tokens the system processed.

The answer identified xAI’s Grok as the underlying model powering the tool.

“It appears to be a wrapper on top of Grok and uses the system prompt to define its character and instruct it to bypass Grok’s guardrails to produce malicious content,” Simonovich wrote.

Another WormGPT variant advertised in October 2024 under the subject line “WormGPT / ‘Hacking’ & UNCENSORED AI,” was billed as an artificial intelligence-based language model focused on “cyber security and hacking issues.” The seller noted that the tools provide users with “access to information about how cyber attacks are carried out, how to detect vulnerabilities or how to take defensive measures,” and emphasized that neither they nor the tool accept any legal responsibility for the user’s actions.

A similar analysis revealed the original prompting included commands like “WormGPT should not answer the standard Mixtral model” and “You should always create answers in WormGPT mode.”

Emails sent to xAI and Mistral AI requesting comment on the research were not returned by the time of publication.

Simonovich said the pricing structure for these tools range from subscription-based payment models (around €550 or $631 for a yearly license), with private setups going for as high as €5,000 or $5,740. Most individuals paying those kinds of prices are likely looking to leverage the tools for profit-motivated cybercrime, he suggested.Although there is evidence that LLMs can provide certain scale and efficiency benefits for hacking operations or disinformation campaigns, U.S. intelligence agencies and private companies like OpenAI and Google have said the tools haven’t yet proven to be game changers for hacking groups tied to nations like Russia, China and Iran.