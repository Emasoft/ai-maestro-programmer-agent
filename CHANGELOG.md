# Changelog

All notable changes to this project will be documented in this file.
    ## [1.0.24] - 2026-04-10

### Bug Fixes

- Correct governance terminology, version sync, and communication rules    
- Resolve all CPV validation issues    
- Publish.py runs CPV validation remotely + pre-push enforces --strict    
- Ruff F541 — remove extraneous f-prefix in publish.py    
- Remove CPV_PUBLISH_PIPELINE bypass from pre-push hook — CPV --strict always runs    
- Publish.py + pre-push use cpv-remote-validate via uvx    
- Embed complete TOC headings in SKILL.md reference tables (CPV strict)    
- Restore ## Resources section name + embed all H2 headings (CPV strict)    
- Embed exact TOC headings from Contents sections (CPV strict)    
- Replace dead example URLs with example.com + add cliff.toml    

### Documentation

- Reflow markdown line wrapping to ~80 chars + track uv.lock    

### Features

- Add compatible-titles and compatible-clients to agent profile    
- Add communication permissions from title-based graph    
- Add smart publish pipeline + pre-push hook enforcement    

### Ci

- Update validate.yml to use cpv-remote-validate --strict    
- Strict publish.py + release.yml + .serena in .gitignore    
- Add pre-push hook + update publish.py to strict mode with sentinel    
- Pre-push hook uses process ancestry instead of env var    


