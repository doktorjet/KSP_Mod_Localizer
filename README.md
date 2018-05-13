# KSP AutoLoc 0.3

This script is meant to replace boring manual text replacement tasks for implementing localization to non-localized-yet part mods in KSP 1.3+

Beware, it does not use KSP API for clean node processing, so it may produce errors.

Beware, it definitely WILL produce errors if you have:
1) Any .cfg files with MORE THAN ONE PART in them.
2) More than one single agency in /Agencies/Agents.cfg

Also it will NOT localize ModuleManager patches, GUI commands or science definitions - you should do them manually.

# How to use:
Drag your mod folder onto the autoloc.py (Windows) or supply path to that folder as command line parameter.
Answer questions asked by script.

That's all.

P.S. Don't blame me for ugly code, it's my first effort in programming after 15 years pause.
