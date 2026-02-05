# SAFE TFA Matrix

**A structured threat intelligence framework for technology-facilitated abuse.**

🔗 **Live site:** [tfa.notastandard.org](https://tfa.notastandard.org)

The SAFE TFA Matrix applies the methodology of frameworks like [MITRE ATT&CK](https://attack.mitre.org/) to map, categorise, and describe the techniques used in technology-facilitated abuse (TFA). It provides a shared language for practitioners, researchers, technologists, and policymakers working to understand and counter tech-enabled coercive control, surveillance, and harassment in the context of domestic and family violence.

## What's in the matrix

- **7 tactics** representing stages of technology-facilitated abuse
- **74 techniques** with detailed descriptions, real-world indicators, mitigations, and detection guidance
- **849 STIX objects** in a machine-readable threat intelligence bundle ([STIX 2.1](https://oasis-open.github.io/cti-documentation/stix/intro.html))
- **210 recognition signals**, **242 safety actions**, and **43 safety warnings** embedded across the framework

## Dual-view design

The matrix serves two audiences through a toggle-based dual-view system:

- **Public view** (default): Written for victim-survivors and frontline practitioners. Uses plain language, recognition signals ("You might notice..."), and actionable safety steps. Every technique page includes helpline numbers and safety warnings where relevant.
- **Technical view**: Written for security professionals, researchers, and analysts. Uses structured threat intelligence language — indicators, mitigations, detections, STIX mappings.

Both views draw from the same underlying STIX data. The public view is not a simplification — it's a purpose-built layer designed with victim safety as the primary constraint.

## Safety features

This site is built for people who may be in danger. Safety features include:

- **Quick Exit button** and **Escape key** binding — immediately navigates away from the site
- **Browser safety banner** on first visit with guidance on safe browsing
- **Helpline numbers** (1800RESPECT, Lifeline, 000) on every technique page
- **Online safety guide** with advice on private browsing, clearing history, and device security
- Content warnings where techniques describe particularly distressing patterns

## Data & STIX bundle

The complete framework is available as a STIX 2.1 bundle at [`tfa-attack.json`](tfa-attack.json). This can be consumed by any STIX-compatible threat intelligence platform.

The bundle includes custom STIX extensions for public-facing content:

- `x_public_title` — plain-language technique names
- `x_public_description` — victim-oriented descriptions
- `x_recognition_signals` — observable indicators in everyday language
- `x_safety_actions` — concrete protective steps
- `x_safety_warning` — content warnings for sensitive techniques

## Built with

The site structure is based on the [MITRE ATT&CK website](https://github.com/mitre-attack/attack-website) architecture, adapted for the TFA domain. Key technologies:

- Static HTML generated from STIX data
- Bootstrap 5 for responsive layout
- Vanilla JavaScript for dual-view toggle, Quick Exit, and safety banner
- GitHub Pages for hosting

## Licence

The **SAFE TFA Matrix data** (STIX bundle, technique descriptions, public content) is licensed under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/).

You are free to share and adapt the data for non-commercial purposes with attribution. Commercial licensing is available — contact us for details.

The **website code** (HTML templates, JavaScript, CSS) is based on MITRE ATT&CK's open-source architecture and retains its original licence terms.

## Contributing

We welcome contributions from DFV practitioners, security researchers, technologists, and policy professionals. Areas where contributions are particularly valuable:

- **New techniques or sub-techniques** — emerging TFA patterns not yet in the matrix
- **Mitigations and detections** — platform-specific or technical countermeasures
- **Public content review** — tone, accuracy, and safety of victim-facing language
- **Translations** — making the framework accessible in languages other than English

Please open an issue to discuss proposed changes before submitting a pull request.

## About

The SAFE TFA Matrix is developed by [Not A Standard](https://notastandard.org), a security and intelligence consultancy that applies threat intelligence methodologies to interpersonal harm. SAFE treats technology-facilitated abuse as an intelligence problem — because that's what it is.

## Contact

- **Website:** [notastandard.org](https://notastandard.org)
- **Email:** safe@notastandard.org
- **Commercial licensing & partnerships:** safe@notastandard.org

---

*If you or someone you know is experiencing domestic or family violence, contact [1800RESPECT](https://www.1800respect.org.au/) (1800 737 732) or in an emergency call 000.*
