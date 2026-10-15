---
name: review-metadata-submission
description: Review a new Hakai metadata record in unpublished/hakai against the Hakai Best Practices Checklist. Use when the user asks to review, check or QA a submission, giving a record name or file prefix (e.g. "johnstone_straight_ph__ctd_and_60b8a").
---

# Review a Hakai metadata submission

Each submission is four files with the same prefix in `unpublished/hakai/`: `.yaml` (the root file), `.xml`, `.cff`, `.erddap`. The `.yaml` is the source of truth. Published records live in `hakai/`.

Review ONE record at a time. The user gives the file prefix. Read the `.yaml` fully, then apply the checks below.

Report every item as **PASS**, **FAIL**, **WARNING**, **MANUAL CHECK** or **CONSIDERATION** (an optional point for the reviewer to weigh, not a problem to fix), each with a suggested fix where there is one. Group the report by checklist section. End with a short list of the fixes the user needs to make. Do not edit the record files unless asked. Fixes are made in the metadata entry form, since the files are generated from it.

Checklist source: https://github.com/HakaiInstitute/hakai-metadata-entry-form/blob/main/firebase-functions/functions/dataset-name.md

## Facts to establish first

- **Resource type:** `metadata.scope`. If absent, treat as `dataset` (the export omits the default). Other values: `collection`, `document`, `service`.
- **Public or not:** follow each Primary Resource link (see Data and Documentation). Data is public only if reachable without a login and not just via the Data Access Request Form.
- **Has DOI:** `identification.identifier` holds a `https://doi.org/...` value.

## Start

- **Earlier versions (WARNING if a possible older version is found; CONSIDERATION for related or associated works):** compare the title against the published records in `hakai/*.yaml` (`identification.title.en`). Search only for similar-looking titles. Flag possible older versions and closely related records (same topic, location or instrument), and name them. Possible older versions are a WARNING. Related or associated works (same topic, location, instrument or source data, but not an older version) are only a CONSIDERATION, never a warning. A published record that this record already lists in `identification.associated_resources` (matched by DOI or title, e.g. as `HasPart`) is a related work (CONSIDERATION), even if its title is very similar. Never FAIL on this; the user decides. For every record named, give its title and a link to it in the report: the catalogue URL `https://catalogue.hakai.org/dataset/ca-cioos_<metadata.identifier>` (take the identifier from that record's yaml). Do not link to the yaml files. Separate "possible older version" from "related or associated work".
- **No version info in title (FAIL):** words like "v2", "version", "revised". Year ranges such as "(2020-2025)" are date coverage, not versions, so they pass.
- **Title style (WARNING):** the title should not include "Hakai Institute" (it is already the publisher) and should not end with a period. Suggest the corrected title.
- **Region in title (FAIL):** the title must name a geographic region.
- **French title matches English (WARNING):** compare numbers, years and place names in `title.fr` and `title.en`. A discrepancy usually means the English title changed and the translation did not (e.g. "2025" vs "2050").
- **EOV keywords match the measured variables (WARNING):** list the variables named in the title and abstract and compare them with `identification.keywords.eov.en`. For each variable with no matching EOV, suggest one. EOV values seen in published records include `oxygen`, `inorganicCarbon`, `nutrients`, `subSurfaceTemperature`, `seaSurfaceTemperature`, `subSurfaceSalinity`, `seaSurfaceSalinity`, `particulateMatter`, `dissolvedOrganicCarbon`, `subSurfaceCurrents`, `seaSurfaceHeight`, and biological ones such as `fishAbundanceAndDistribution`. `other` alone does not count as a match. Use sub-surface vs sea-surface according to the measurement depth. Treat the suggestions as prompts for review, not certainties. It is NOT confirmed which EOV covers pH (do not assume `inorganicCarbon`); when pH or another variable has no clear EOV, ask the user instead of suggesting one.
- **Keywords are separate (WARNING):** each entry in `identification.keywords.default` (and `taxa`) should be one keyword. An entry with commas or semicolons, such as "ocean acidification, ocean climate, ocean data", should be split into separate keywords. Suggest the split.
- **Place-name spelling (WARNING, for review):** flag misspelled place names, e.g. "Johnstone Straight" should be "Johnstone Strait".

## Resource identification

- **Hakai Program (FAIL if empty):** `identification.project` must contain at least one program.
- **Publication date and DOI:**
  - Resource type `dataset` requires a DOI. Missing identifier: FAIL, "needs DOI drafted". Exception: a record with `progress_code` `tentative` does not need a DOI, so a missing identifier is not a FAIL (report it as not required while provisional).
  - Other resource types (e.g. `collection`) do not require a DOI.
  - `identification.dates.publication` is required when the record has a DOI. It should be the date the data were made public or the date the metadata record was published, whichever came first. If there is no DOI, a missing publication date is not a failure (report as not yet required). If the data are already public per the link check, a publication date is needed, so flag it.
  - A publication date should only be set when the record is being published.
- **DOI format and prefix (WARNING):** the record's own DOI must be written as a full `https://doi.org/10.…` URL (not bare, and not `dx.doi.org`), there must be only one, and it should start with the Hakai prefix `10.21966/`. Suggest the corrected form.
- **Duplicate DOI (FAIL):** the record's own DOI (`identification.identifier`) must not be used by any other record. Compare it with the DOIs in `hakai/*.yaml` and `unpublished/hakai/*.yaml`, ignoring files with the same `metadata.identifier` (the same record can exist in both folders). Name the record(s) that share the DOI, with their catalogue links.
- **DOI steps after review (draft, update via form, edit on DataCite Fabrica, Draft to Findable):** skip. Do not report these. A DOI that does not resolve yet (404 at doi.org) is expected for a submitted record, so do not report it.

### Abstract

- **Word count (PASS at 500 or fewer, WARNING over 500):** count words in `abstract.en` and report the count either way.
- **How, when, what, where, why (WARNING for each weak or missing element):** brief mentions are enough; elaborate detail is not required. Name which elements are weak.
- **Pointers and references in the abstract (WARNING):** the abstract must not contain pointers to other content, such as figures, tables or attachments (e.g. "Figure 1", "see the table below") or other parts of the record (e.g. "see the links section below"). Quote each one and suggest removing it or describing the content in words.
- **Broken sentences (WARNING):** flag sentence fragments, unfinished sentences and sentences that trail off. Quote each one and suggest a fix.
- **Abbreviations (WARNING):** acronyms for platforms or projects must be expanded at first mention. Do NOT flag instruments (e.g. SeapHOx2), standard terms (pH, CTD) or common organizations (WWF).

## Spatial

- **Spatial extent present (FAIL):** the record must have a `spatial.bbox` or `spatial.polygon`.
- **Depth or height positive (FAIL, suggest corrected value):** `spatial.vertical_positive`. Depth below the surface means `depthPositive`. Elevation or height above a datum (DEM, LiDAR, terrain) means `heightPositive`. Airborne work (drone, UAS, aircraft) is `heightPositive` because the vertical extent is the height of the sensor, even when the mapped subject is underwater or nearshore (e.g. drone-derived substrate or eelgrass maps). Decide from title, abstract and keywords. If the evidence is ambiguous, WARNING for review and no suggested value. Only applies when `spatial.vertical` is present.
- **Bounding box matches stated coordinates (WARNING):** if `spatial.description` (or the abstract) gives coordinates, including degrees-minutes-seconds, convert them to decimal degrees (west and south are negative) and compare with `spatial.bbox` / `spatial.polygon`. Flag a difference of more than about 0.001 degrees.
- **Polygon closure (WARNING):** `spatial.polygon` is `lon,lat` pairs. The first pair must equal the last pair.

## Contact

- **ROR (FAIL for Hakai Institute, WARNING for other organizations):** a missing ROR on an organization block named "Hakai Institute" is a FAIL (the correct ROR is `https://ror.org/02pry0c91`). For any other organization it is a WARNING, because some organizations do not have an ROR. Check every organization block, including those under individual contacts.
- **ORCID (WARNING):** any individual whose organization is Hakai Institute needs an ORCID. When it is missing for a Hakai-affiliated person, suggest strongly recommending that they create one (it is free). Individuals from other organizations are not flagged and get no suggestion. Team contacts (e.g. "Hakai Geospatial") are not people, so skip the ORCID check for them. Check the ORCID is linked as a full `https://orcid.org/...` URL.
- **Affiliation matches email (WARNING):** an individual with an `@hakai.org` email must have `Hakai Institute` as their organization, so the ORCID, ROR and owner checks apply. Flag an individual whose organization is empty or different, and suggest Hakai Institute.
- **Look up missing ORCID, ROR and affiliation in other records (adds a fix to the warnings above):** when an individual has no ORCID, or an organization has no ROR, search the other records in `hakai/` and `unpublished/hakai/` for the same person or organization (match names fuzzily: ignore case, middle initials and "Last, First" order). If a match has an ORCID or ROR, quote it and suggest using it. Do the same for an individual with no organization affiliation. If nothing is found, just report the missing item.
- **Publisher (FAIL):** Hakai Institute with role `publisher` and email `data@hakai.org`.
- **Data owner (WARNING):** if a Hakai-affiliated individual has the `owner` role, Hakai Institute (the organization) should be the owner instead. Suggest removing `owner` from the individual and adding a Hakai Institute owner entry if none exists. If the owner is from outside Hakai, an individual or an organization is fine.
- **Email on custodian / point of contact (FAIL):** a Metadata Custodian or Point of Contact needs an email. When the contact is an individual, an email on the individual block is required, and an email on the organization block does not count (even a shared one such as `data@hakai.org`). A missing individual email is a FAIL. If a personal email (tied to a named person) sits on the organization block, suggest moving it to the individual block. A shared address on an organization block is otherwise fine and need not be removed.
- **Point of contact:** a record with no `pointOfContact` role is not a failure. Do not flag it.
- **Tula Foundation funder (FAIL if missing):** if the resource is (partly) generated by Hakai researchers, `Tula Foundation` (ROR `https://ror.org/0029jxk29`) must be included with the `funder` role.

## Data and Documentation

- **Malformed related-work identifiers (WARNING):** a DOI in `associated_resources[].code` must be `https://doi.org/10.…`. Flag forms like `https://10.xxxx/…` (missing `doi.org`) and suggest the corrected URL.
- **Relation types (WARNING):** each entry in `identification.associated_resources` needs an `association_type` that fits what the resource is. An empty list is fine.
- **Primary Resource:** the first entry in `distribution[]` is a Primary Resource. There can be several.
- **Link checks (for each Primary Resource, by fetching the URL):**
  - Link works (FAIL if broken).
  - Login wall (WARNING): data behind a login are not public. A redirect to a sign-in page, or an HTTP 401 or 403 response, counts as a login wall (for Google Drive, a 401 on a file link means it is not shared publicly).
  - Points to a specific dataset or data package, not a generic platform or web page (FAIL). Generic means a user cannot retrieve data from the page and must keep searching (e.g. waterproperties.ca). Acceptable hosts: a general, domain-specific or institutional repository (e.g. GitHub, Google Drive).
  - Data Access Request Form: URLs starting with `https://hecate.hakai.org/auth/access-request.php`, in any distribution entry (not only the first). If this is the only data link, the data are not public. The URL must end with `?ref=<DOI>` (no trailing `#`), where `<DOI>` is the full DOI URL (e.g. `?ref=https://doi.org/10.21966/at9a-1109`). With no DOI (e.g. a `collection`), it must end with `?ref=` followed by the catalogue URL `https://catalogue.hakai.org/dataset/ca-cioos_<metadata.identifier>`.
- **All links work and have titles (FAIL for distribution entries, WARNING for associated resources):** fetch every URL in `distribution[]` and `identification.associated_resources`, not just the Primary Resource. A broken or empty link (including a bare `#`) needs fixing or removing. Every entry needs a name or title.
- **Documents listed as distribution entries (CONSIDERATION):** methods documents, reports and similar supporting documents are better as associated resources (related works) or lineage than as distribution links.
- **Datasets cited in the abstract (CONSIDERATION):** if the abstract (or limitations) names other datasets or records, check that they are listed in `associated_resources`. Look them up in `hakai/*.yaml`, link them with their catalogue URLs, and note any that are still in draft or not published.
- **Primary Resource is a single data file (WARNING):** if a Primary Resource points to one data file (e.g. a Google Drive `/file/d/` link, or a URL ending in .csv/.xlsx/.txt) instead of a data package, suggest linking a package that also holds a data dictionary, readme, changelog and other supporting material.
- **Updates and hosting (CONSIDERATION):** when `progress_code` is `onGoing` or `tentative`, ask whether the data are updated regularly (e.g. annually), and if so suggest a GitHub repository or ERDDAP so the package and its history can be maintained.
- **Provisional and QC'd data together (CONSIDERATION):** if the description, abstract or limitations say the resource mixes provisional and quality-controlled data, suggest separate records for provisional and research-ready data.
- **Package contents (readme, changelog, data dictionary, protocols; archive folder; files open and not corrupt; no executables):** report as MANUAL CHECK. Do not try to open the package yet.

## Other checks

- **Status value (FAIL):** `identification.progress_code` must be one of `onGoing`, `tentative`, `historicalArchive` or `completed`. Any other value, such as `underDevelopment`, is a FAIL. Suggest the most likely valid value from the record (e.g. `completed` if it has a DOI, a publication date and an end of collection; `tentative` if provisional; `onGoing` if collection continues) and ask the user to confirm.
- **Platform (CONSIDERATION):** if the abstract names a platform used for collection (e.g. a UAS or drone, boat, aircraft, buoy, satellite) and the record has no `platform` entry for it, suggest adding one (e.g. "unmanned aerial vehicle" for UAS or drone work).
- **Licence (WARNING):** `metadata.use_constraints.licence.code` should be `CC-BY-4.0`, the Hakai default. Any other licence (e.g. a non-commercial variant) is flagged as a WARNING, with the suggestion to use CC-BY-4.0.
- **Limitations match the data level (WARNING):** if `title.en` says "Research" (research-ready) or the status is `completed`, but `metadata.use_constraints.limitations.en` says the data are preliminary, provisional or not for rigorous analysis, flag the mismatch. Ask whether the limitation is still accurate, and suggest removing or rewording it.
- **Tentative record with a version (WARNING):** if `progress_code` is `tentative` and `identification.edition` is set, flag it. Provisional data should not carry a version, so suggest removing the edition.
- **Version (CONSIDERATION):** if `identification.edition` is missing and the status is not `tentative`, ask for the version (e.g. 1.0) and whether later versions exist.
- **Taxonomic coverage (CONSIDERATION):** if the abstract or keywords name organisms (e.g. kelp, eelgrass, a species) and `identification.keywords.taxa` is missing or does not cover them (including host or prey species named in the abstract), suggest adding taxonomic coverage. Older records may hold taxa in `keywords.eov` (e.g. Zostera marina).
- **Provisional status (WARNING):** if `identification.progress_code` is `tentative`, `metadata.use_constraints.limitations.en` should say it is a provisional data set. If it does not, suggest adding that.
- **"(Provisional)" in title (WARNING):** if `progress_code` is `tentative` and `title.en` lacks "(Provisional)", suggest appending it to the end of the title (the convention in published records, e.g. "... Estuary (Provisional)"), and the same in the French title.
- **"Provisional" title implies Tentative status (WARNING):** if `title.en` includes "Provisional" or "(Provisional)", `identification.progress_code` must be `tentative`. If it is another value (e.g. `completed`, `onGoing`), flag the mismatch and suggest setting the status to `tentative` (the primary suggestion). Only mention removing "(Provisional)" from the title as the alternative if the data are not actually provisional.
- **Collection dates vs abstract (WARNING):** where the abstract states dates of data collection (e.g. mission or deployment dates), compare them with `temporal_begin` and `temporal_end` (and `dates.creation` where relevant). Flag any date in the abstract that falls outside that range, or a range that starts or ends well before or after the abstract's dates. Skip when the abstract gives no dates.
- **Dates of collection:** a missing `temporal_end` is fine for ongoing or `tentative` records. If `progress_code` is `completed`, STRONGLY RECOMMEND both `temporal_begin` and `temporal_end` (report as WARNING).
- **File consistency (FAIL on discrepancy):** the `.xml`, `.cff` and `.erddap` files are generated from the `.yaml` and should agree with it. Compare title, abstract, DOI or identifier, dates, contacts, keywords, bounding box or polygon and licence. Any difference is a FAIL; name the field and the files that differ.

## Not checked

Instrument descriptions and the DOI Draft-to-Findable workflow are deliberately out of scope. (Only the platform suggestion under Other checks applies.)

## Report format

Start with the summary, then elaborate below it.

1. **Header:** record title, file prefix, resource type, and whether the data are public.
2. **Summary (first):** counts of FAIL / WARNING / MANUAL CHECK (CONSIDERATION items are counted separately, not as warnings), then a numbered list of the fixes the user needs to make, one line each, each tagged with its section and status.
3. **Details by section** (Start, Resource identification, Abstract, Spatial, Contact, Data and Documentation, Other checks), one line per item: status, short reason, suggested fix. Within each section, group items by status in this order: FAIL, WARNING, MANUAL CHECK, CONSIDERATION, PASS. Put a status label as a sub-heading or bold lead-in for each group, and omit groups that have no items.
