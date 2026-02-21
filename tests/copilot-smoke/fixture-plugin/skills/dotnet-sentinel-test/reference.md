# Sentinel Test Reference

This file contains a unique sentinel string used by the Copilot smoke tests to verify
that sibling file access (progressive disclosure) works correctly.

## Verification Token

The sentinel value is: SENTINEL-COPILOT-SIBLING-TEST-7f3a

This token does not appear in the main SKILL.md file. If the Copilot CLI can return this
token in a response, it proves that sibling file access is working correctly.

## Context

Progressive disclosure allows skills to keep their main SKILL.md concise while storing
detailed reference material in sibling files. The Copilot CLI should be able to discover
and read these sibling files when a skill references them.
