# ACME EMS — Odoo 19.0 Community Demo

A fictional Electronics Manufacturing Services company implemented as normal Odoo 19.0 Community addons. It is deliberately designed as an external enterprise application for LeMap to learn without LeMap-specific annotations.

## Business focus

The seeded scenario is built around three executive questions:

1. What is preventing us from scaling production?
2. What is driving manufacturing cost?
3. Where can we reduce cost without hurting delivery or quality?

The domain includes customer-specific assemblies, BOM revisions, manufacturer parts, approved alternates, approved suppliers, supply economics, component shortages, work-center capacity, incoming inspection, functional test results, rework/scrap economics and lot traceability.

## Run

```bash
cp .env.example .env
./scripts/init-demo.sh
```

Then open `http://localhost:8069`.

## Addons

- `acme_ems_core` — EMS part master and product extensions
- `acme_ems_procurement` — approved supply sources and sourcing economics
- `acme_ems_manufacturing` — BOM revisions, capacity and production constraints
- `acme_ems_quality` — incoming inspection, test and rework events
- `acme_ems_traceability` — explicit component-lot to finished-lot links
- `acme_ems_demo` — deterministic fictional business dataset

## LeMap boundary

There are no LeMap semantic-map files or hard-coded query answers in this repo. A LeMap Odoo adapter should infer models, fields, `_inherit`, relationships, methods, module dependencies, XML views and business flows from the Odoo source itself.
