# Translation Pipeline Framework

## Purpose
Explain the role of the translation pipeline in supporting multilingual glossary entries, teaching materials, and cross-language conceptual scaffolding.

## Directory Structure
- i18n/schema.yaml
- i18n/en/
- i18n/zh/
- (future languages)
- lookup indexes (e.g., index-en-zh.yaml)

## How to Add a New Term
1. Create a YAML file in the source language directory.
2. Follow schema.yaml.
3. Add scaffolding fields (anchor, pronunciation) as needed.
4. Add the corresponding file in the target language directory.
5. Update the lookup index.

## How to Add a New Language
1. Create a new directory under i18n/.
2. Add language code (ISO).
3. Create initial example entries.
4. Create a new lookup index (e.g., index-en-de.yaml).

## Scaffolding Fields
- anchor: cultural or conceptual analogy
- pronunciation: phonetic support
- notes: conceptual unpacking
- context: usage domain

## Cross-Linking
Explain how related_terms supports conceptual navigation across languages.

## Automation Hooks (Future)
- glossary generation
- bilingual teaching sheets
- pronunciation tables
- topic-sorted indexes
- cross-language search

## Governance Notes
- small bursts
- schema-first
- contributor-friendly
- multilingual sovereignty
