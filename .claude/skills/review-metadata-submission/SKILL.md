---
name: review-metadata-submission
description: Review a new Hakai metadata record in unpublished/hakai against the Hakai Best Practices Checklist. Use when the user asks to review, check or QA a submission, giving a record name or file prefix (e.g. "johnstone_straight_ph__ctd_and_60b8a").
---

# Review a Hakai metadata submission

Each submission is four files with the same prefix in `unpublished/hakai/`: `.yaml` (the root file), `.xml`, `.cff`, `.erddap`. The `.yaml` is the source of truth. Published records live in `hakai/`.

Review ONE record at a time. The user gives the file prefix. Read the `.yaml` fully, then apply the checks below.

Report every item as **PASS**, **FAIL**, **WARNING** or **MANUAL CHECK**, each with a suggested fix where there is one. Group the report by checklist section. End with a short list of the fixes the user needs to make. Do not edit the record files unless asked. Fixes are made in the metadata entry form, since the files are generated from it.

Checklist source: https://github.com/HakaiInstitute/hakai-metadata-entry-form/blob/main/firebase-functions/functions/dataset-name.md

## Facts to establish first

- **Resource type:** `metadata.scope`. If absent, treat as `dataset` (the export omits the default). Other values: `collection`, `document`, `service`.
- **Theme (Oceanographic / Biological / Other):** this form field is NOT exported. Infer it from EOV keywords (`identification.keywords.eov`), title, abstract and keywords, and state the inferred theme in the report so the user can correct it.
- **Public or not:** follow each Primary Resource link (see Data and Documentation). Data is public only if reachable without a login and not just via the Data Access Request Form.
- **Has DOI:** `identification.identifier` holds a `https://doi.org/...` value.

## Start

- **Earlier versions (WARNING if found):** compare the title against the published records in `hakai/*.yaml` (`identification.title.en`). Search only for similar-looking titles. Flag possible older versions and closely related records (same topic, location or instrument), and name them. Never FAIL on this; the user decides.
- **No version info in title (FAIL):** words like "v2", "version", "revised". Year ranges such as "(2020-2025)" are date coverage, not versions, so they pass.
- **Region in title (FAIL):** the title must name a geographic region.
- **French title matches English (WARNING):** compare numbers, years and place names in `title.fr` and `title.en`. A discrepancy usually means the English title changed and the translation did not (e.g. "2025" vs "2050").
- **EOV keywords match the measured variables (WARNING):** list the variables named in the title and abstract and compare them with `identification.keywords.eov.en`. For each variable with no matching EOV, suggest one. EOV values seen in published records include `oxygen`, `inorganicCarbon`, `nutrients`, `subSurfaceTemperature`, `seaSurfaceTemperature`, `subSurfaceSalinity`, `seaSurfaceSalinity`, `particulateMatter`, `dissolvedOrganicCarbon`, `subSurfaceCurrents`, `seaSurfaceHeight`, and biological ones such as `fishAbundanceAndDistribution`. `other` alone does not count as a match. Use sub-surface vs sea-surface according to the measurement depth. Treat the suggestions as prompts for review, not certainties. It is NOT confirmed which EOV covers pH (do not assume `inorganicCarbon`); when pH or another variable has no clear EOV, ask the user instead of suggesting one.
- **Place-name spelling (WARNING, for review):** flag misspelled place names, e.g. "Johnstone Straight" should be "Johnstone Strait".

## Resource identification

- **Hakai Program (FAIL if empty):** `identification.project` must contain at least one program.
- **Publication date and DOI:**
  - Resource type `dataset` requires a DOI. Missing identifier: FAIL, "needs DOI drafted".
  - Other resource types (e.g. `collection`) do not require a DOI.
  - `identification.dates.publication` is required when the record has a DOI. It should be the date the data were made public. If there is no DOI, a missing publication date is not a failure (report as not yet required). If the data are already public per the link check, a publication date is needed, so flag it.
  - A publication date should only be set when the record is being published.
- **DOI steps after review (draft, update via form, edit on DataCite Fabrica, Draft to Findable):** skip. Do not report these.

### Abstract

- **Word count over 500 (WARNING):** count words in `abstract.en`.
- **How, when, what, where, why (WARNING for each weak or missing element):** brief mentions are enough; elaborate detail is not required. Name which elements are weak.
- **Abbreviations (WARNING):** acronyms for platforms or projects must be expanded at first mention. Do NOT flag instruments (e.g. SeapHOx2), standard terms (pH, CTD) or common organizations (WWF).

## Spatial

- **Depth or height positive (FAIL, suggest corrected value):** `spatial.vertical_positive`. Depth below the surface means `depthPositive`. Elevation or height above a datum (DEM, LiDAR, terrain) means `heightPositive`. Decide from title, abstract and keywords. If the evidence is ambiguous, WARNING for review and no suggested value. Only applies when `spatial.vertical` is present.
- **Description for Biological records (FAIL if missing):** a text `spatial.description` is required only when the inferred theme is Biological. For other themes a polygon or bbox is enough.
- **Polygon closure (WARNING):** `spatial.polygon` is `lon,lat` pairs. The first pair must equal the last pair.

## Contact

- **ROR (FAIL if missing):** every organization block should have a ROR.
- **ORCID (FAIL):** any individual whose organization is Hakai Institute needs an ORCID. Individuals from other organizations are not flagged. Check the ORCID is linked as a full `https://orcid.org/...` URL.
- **Publisher (FAIL):** Hakai Institute with role `publisher` and email `data@hakai.org`.
- **Data owner (WARNING):** if a Hakai-affiliated individual has the `owner` role, Hakai Institute (the organization) should be the owner instead. Suggest removing `owner` from the individual and adding a Hakai Institute owner entry if none exists. If the owner is from outside Hakai, an individual or an organization is fine.
- **Email on custodian / point of contact (FAIL):** a Metadata Custodian or Point of Contact needs an email. When the contact is an individual, the email belongs on the individual block. A personal email (tied to a named person) sitting on the organization block is a FAIL, with the suggestion to move it to the individual block. A shared address such as `data@hakai.org` on an organization block is fine.
- **Point of contact:** a record with no `pointOfContact` role is not a failure. Do not flag it.
- **Tula Foundation funder (FAIL if missing):** if the resource is (partly) generated by Hakai researchers, `Tula Foundation` (ROR `https://ror.org/0029jxk29`) must be included with the `funder` role.

## Data and Documentation

- **Relation types (WARNING):** each entry in `identification.associated_resources` needs an `association_type` that fits what the resource is. An empty list is fine.
- **Primary Resource:** the first entry in `distribution[]` is a Primary Resource. There can be several.
- **Link checks (for each Primary Resource, by fetching the URL):**
  - Link works (FAIL if broken).
  - Login wall (WARNING): data behind a login are not public.
  - Points to a specific dataset or data package, not a generic platform or web page (FAIL). Generic means a user cannot retrieve data from the page and must keep searching (e.g. waterproperties.ca). Acceptable hosts: a general, domain-specific or institutional repository (e.g. GitHub, Google Drive).
  - Data Access Request Form: URLs starting with `https://hecate.hakai.org/auth/access-request.php`. If this is the only data link, the data are not public. The URL must end with `?ref=<DOI>`. With no DOI (e.g. a `collection`), it must end with `?ref=` followed by the catalogue URL `https://catalogue.hakai.org/dataset/ca-cioos_<metadata.identifier>`.
- **Package contents (readme, changelog, data dictionary, protocols; archive folder; files open and not corrupt; no executables):** report as MANUAL CHECK. Do not try to open the package yet.

## Other checks

- **Provisional status (WARNING):** if `identification.progress_code` is `tentative`, `metadata.use_constraints.limitations.en` should say it is a provisional data set. If it does not, suggest adding that.
- **"(Provisional)" in title (WARNING):** if `progress_code` is `tentative` and `title.en` lacks "(Provisional)", suggest appending it to the end of the title (the convention in published records, e.g. "... Estuary (Provisional)"), and the same in the French title.
- **Dates of collection:** a missing `temporal_end` is fine for ongoing or `tentative` records. If `progress_code` is `completed`, STRONGLY RECOMMEND both `temporal_begin` and `temporal_end` (report as WARNING).
- **File consistency (FAIL on discrepancy):** the `.xml`, `.cff` and `.erddap` files are generated from the `.yaml` and should agree with it. Compare title, abstract, DOI or identifier, dates, contacts, keywords, bounding box or polygon and licence. Any difference is a FAIL; name the field and the files that differ.

## Not checked

Instrument descriptions, `platform`, and the DOI Draft-to-Findable workflow are deliberately out of scope.

## Report format

1. Record title, file prefix, resource type, inferred theme and whether the data are public.
2. Results by section, one line per item: status, short reason, suggested fix.
3. Summary count of FAIL / WARNING / MANUAL CHECK, then a numbered list of required fixes.
