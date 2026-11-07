# Online evidence, 2026-11-05

## Official behavioral specification
https://docs.reasonstudios.com/plusre/objekt-modeling-synthesizer

Implementation corrections confirmed in the online manual:
- Coupling On feeds every delay stage into all other stages. X-Over high-pass filters this feedback.
- Object Pitch transposes pitch-dependent processing; Tuning only changes delay lengths. These must not be treated as synonyms.
- Untracked modal stages use C3 as the reference fundamental.
- Mono/Legato allow external audio processing without note triggers.
- Delay and reverb use sends. Reducing a send must preserve previously generated tails.
- Templates leave some controls, including pickup and object decay, unchanged.

This is a behavioral specification, not published source code or measured DSP coefficients.

## Developer and current product
https://www.reasonstudios.com/news/post/synthesize-reality-introducing-objekt-modeling-synthesizer

Reason identifies Peter Jubel as the DSP researcher behind the instrument. No implementation equations were published on this page.

https://www.reasonstudios.com/shop/rack-extension/objekt-modeling-synthesizer/

The page lists version 1.0.3 and a Download trial option. Release notes mention corrected automation for Mid Freq and Mid Freq Gain. User owns Reason 12 only; no trial was activated.

## Local REA evidence and limits
Prior static preload analysis of Companion 3.3.0: ev_71eea96d7ecd63e16c8d1315e534d7bfb67e8fab94e6510a86f8d3ae007a3ced. Scope was preload only, not a full reverse engineering of Companion.
Read-only ASAR string inspection subsequently found Objekt package names including se.propellerheads.Objekt-1.0.0-arm64.zip. Package names establish catalog knowledge, not possession of Objekt DSP. No Objekt package was found in the user's standard RackExtensions directory. No original instrument audio has been captured or compared.
