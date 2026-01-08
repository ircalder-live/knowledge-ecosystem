# Contributing to the i18n/l10n System

## Purpose
This guide explains how to add or translate glossary terms using the multilingual architecture in the knowledge-ecosystem.

## Prerequisites
- Basic familiarity with YAML
- Ability to type in the target language (IME setup recommended)
- Understanding of schema.yaml

## Directory Structure
- i18n/schema.yaml
- i18n/en/
- i18n/zh/
- i18n/index-en-zh.yaml
- (future languages)

## Adding a New Term (English Source)
1. Create a new file in i18n/en/ using the canonical ID as the filename.
2. Follow the fields in schema.yaml.
3. Add scaffolding fields (anchor, pronunciation) as needed.
4. Add the corresponding file in the target language directory.
5. Update the lookup index.

## Translating an Existing Term
1. Locate the ID in the lookup index.
2. Create the corresponding file in the target language directory.
3. Include pronunciation and cultural anchors where appropriate.
4. Update the lookup index.

## Adding a New Language
1. Create a new directory under i18n/ using the ISO language code.
2. Add initial example entries.
3. Create a new lookup index (e.g., index-en-de.yaml).
4. Follow the same workflow as en/zh.

## Scaffolding Guidelines
- Use cultural anchors to support conceptual understanding.
- Include pronunciation for languages where it aids learning.
- Keep definitions concise and aligned with schema.yaml.

## Governance Notes
- Small, atomic commits
- Schema-first workflow
- Contributor-friendly structure
- Multilingual sovereignty
