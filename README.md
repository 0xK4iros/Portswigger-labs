# Portswigger-labs

> A structured collection of scripts and write-ups developed while working through the PortSwigger Web Security Academy.

---

## Index

### Authentication Vulnerabilities

| Lab | Level | Write-up |
|-----|-------|----------|
| [username_enumeration_basic](/Authentication%20vulnerabilities/01%20username_enumeration_basic/README.md) | Apprentice | Username enumeration via response anomalies followed by password brute-forcing |
| [username_enumeration_subtle](/Authentication%20vulnerabilities/02%20username_enumeration_subtle.py/README.md) | Practitioner | Username enumeration via subtly different responses (Bypassing dynamic length with Regex) |
| [username_enumeration_timebased](/Authentication%20vulnerabilities/03%20username_enumeration_timebased/README.md) | Practitioner | Timing-based username enumeration (IP rotation via X-Forwarded-For and hashing delay analysis) |

### SQL Injection

| Lab | Level | Write-up |
|-----|-------|----------|
| [Blind SQLi — Conditional Responses](/SQL%20Injections/01%20Conditional_responses/README.md) | Practitioner | Boolean-based blind SQLi with binary search optimization |
| [Blind SQLi — Conditional Errors](/SQL%20Injections/02%20Conditional_errors/README.md) | Practitioner | Error-based blind SQLi using `CASE`/division-by-zero, extracted via HTTP status oracle (500) |

---

*Labs are added progressively as they are completed.*