# Faith Works — Agent Instructions

**Domain:** `faithworksclearing.com`  
**Site folder:** `E:\All Client Websites\Faith Works`  
**GitHub (source of truth):** `Faith-Works-Outdoor-Services-LLC/faithworksods-website`  
**Pages:** `https://faithworksclearing.com/` (org GitHub Pages)

## Website Audit / GSC

Umbrella: `E:\Website Audit`  
GSC module: `E:\Website Audit\GSC`  
Config: `E:\Website Audit\GSC\sites\faithworksclearing.com.json`

Site config: `E:\Website Audit\sites\faithworksclearing.com.json`

Trigger phrases: GSC audit, Full Website Audit via API / with Playwright, SEO/AEO/GEO/a11y/perf/visibility, submit indexing.

```powershell
node E:\Website Audit\tools\run-visibility-audit.mjs --site faithworksclearing.com --pack full-api
node E:\Website Audit\GSC\tools\audit.mjs --full
node E:\Website Audit\GSC\tools\submit-indexing.mjs --failed
```

Outputs: `website-audit\<date>\`, `gsc-audit\<date>\`, `.website-audit-latest.json` / `.gsc-audit-latest.json`.
