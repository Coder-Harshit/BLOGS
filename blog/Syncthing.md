---
title: "Hello Syncthing"
date: "2025-08-07"
tags: ['LocalFirst', 'OpenSource', 'SelfHosted', 'Syncthing', 'LinuxLife', 'PrivacyMatters', 'DevTools', 'HackYourSetup']
summary: "Moving from Cloud offered Syncing to Self Hosted Syncing via `Syncthing`"
---
## Goodbye Cloud ? Hello `Syncthing`
Before cloud storage became mainstream, syncing files between devices was pure pain. Remember the time when you share some file named `LastEdit.md`, only for your friend to send back `FinalEdit.md` then `FinalEdit-Real.md` then `FinalEdit-RealFinal.md`.
CHAOS

With the rise of Cloud storage platforms like Google Drive, OneDrive, and Mega, syncing got easier - but still far from perfect. Users would then no longer need to manually do the heavy lifting of syncing one device files with the other. But this came with its own set of trade-offs - limited storage, network latency & questions about the privacy and underlying encryption used. 

Sure building your own cloud sounds cool - until you are knee-deep in hardware specs, config files, and the port forwarding and network confs. 

From years, I wanted to have my very own dedicated physical server setup but that wasn't possible due to hardware limitations and ironically that very limitation lead me to explore alternatives. 
That’s when I stumbled upon the **local-first philosophy** - quite a refreshing shift from cloud dependency to self-hosted, local control. Think of it as apps that work offline-first,  and **put you in charge** of your data by relying on local storage in place of cloud storage. It’s not just more secure and cost-effective (often completely free), but also packs a lot of freedom once set up.

The only catch? Setup time - and even that depends on how polished the tool is.

That's when i found **Syncthing** - an open-source tool that lets you securely sync folders between devices, without relying on any cloud and even removes the limitation of being on the same network.

>To those who build such tools: you have my deepest respect. It’s setups like these that make us feel like our machines truly belong to us!

### 🚀 Curious: Have you tried going local-first?

Whether for syncing, note-taking, or even backups — I'd love to hear how you've replaced cloud dependency with your own setup.
