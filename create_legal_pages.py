#!/usr/bin/env python3
"""
Create legal, privacy, terms, licensing, and online safety pages.
Also inject browser safety banner and update footers on all pages.
"""

import re
from pathlib import Path

BASE_DIR = Path(__file__).parent

# Page templates
ONLINE_SAFETY_CONTENT = '''
<!DOCTYPE html>
<html lang='en'>

<head>

        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1,shrink-to-fit=no'>
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <link rel='shortcut icon' href='/theme/favicon.ico' type='image/x-icon'>
        <title>Your Safety Online | SAFE TFA Matrix</title>
        <!-- Bootstrap CSS -->
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap.min.css' />
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap-tourist.css' />
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap-select.min.css' />
        <!-- Fontawesome CSS -->
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/fontawesome.min.css"/>
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/brands.min.css"/>
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/solid.min.css"/>
        <link rel="stylesheet" href="/theme/style-user.css"/>

</head>

<body>

    <div class="safety-banner" id="browser-safety-banner">
        <div class="safety-banner-content">
            <strong>Is someone checking your browsing?</strong>
            This website will appear in your browser history. If you're concerned someone may be monitoring your internet use, consider using a trusted friend's device, a library computer, or your browser's private/incognito mode. You can press <strong>Quick Exit</strong> or hit <strong>Escape</strong> at any time to leave this site quickly.
            <a href="/about/online-safety/">Learn more about staying safe online</a>
        </div>
        <button class="safety-banner-close" id="close-safety-banner" aria-label="Dismiss safety notice">&times;</button>
    </div>

    <div class="container-fluid attack-website-wrapper d-flex flex-column h-100">
        <div class="row sticky-top flex-grow-0 flex-shrink-1">
            <!-- header elements -->
            <header class="col px-0">
                    <nav class='navbar navbar-expand-lg navbar-dark position-static'>
        <a class='navbar-brand' href='/'><img src="/theme/images/safe_logo_header.png" class="attack-logo"></a>
        <button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarCollapse'
                aria-controls='navbarCollapse' aria-expanded='false' aria-label='Toggle navigation'>
                <span class='navbar-toggler-icon'></span>
        </button>
        <div class='collapse navbar-collapse' id='navbarCollapse'>
            <ul class='nav nav-tabs ml-auto'>
                        <li class="nav-item">
                            <a href="/matrices/tfa/"  class="nav-link" ><b>Matrix</b></a>
                        </li>
                        <li class="nav-item">
                            <a href="/tactics/tfa/"  class="nav-link" ><b>Tactics</b></a>
                        </li>
                        <li class="nav-item">
                            <a href="/techniques/tfa/"  class="nav-link" ><b>Techniques</b></a>
                        </li>
                        <li class="nav-item">
                            <a href="/about/"  class="nav-link" ><b>About</b></a>
                        </li>
                        <li class="nav-item">
                            <button id="search-button" class="btn search-button">Search <div id="search-icon" class="icon-button search-icon"></div></button>
                        </li>


            </ul>
            <a href="https://doodles.google" id="quick-exit-btn" class="btn ml-3"
               style="background-color: #e65100; color: white; font-weight: bold; padding: 8px 16px; border-radius: 4px;"
               title="Press Escape to quickly leave this site">Quick Exit</a>
        </div>
    </nav>

            </header>
        </div>
        <div class="row flex-grow-0 flex-shrink-1">
            <!-- banner elements -->
            <div class="col px-0">
                <!-- !versions banner! -->
            </div>
        </div>
        <div class="row flex-grow-1 flex-shrink-0">
            <!-- main content elements -->
            <!--start-indexing-for-search-->

    <div class="col pt-4">
        <!--stopindex-->
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/">Home</a></li>
            <li class="breadcrumb-item"><a href="/about/">About</a></li>
            <li class="breadcrumb-item">Your Safety Online</li>
        </ol>

        <div class="container pb-5">
            <!-- Helpline Banner -->
            <div class="helpline-banner">
                <strong>Need support?</strong>
                <a href="tel:1800737732">1800RESPECT (1800 737 732)</a> |
                Emergency: <a href="tel:000">000</a>
            </div>

            <div class="limitations-page">
                <h1>Your Safety Online</h1>

                <h2>Before You Browse</h2>
                <p>If someone is monitoring your phone, computer, or internet activity, visiting this website — or any domestic violence resource — could put you at risk. Please consider:</p>
                <ul>
                    <li><strong>Browser history:</strong> This site will appear in your browsing history. You can delete individual entries, but if the person causing harm regularly checks your history, a gap may also raise suspicion.</li>
                    <li><strong>Incognito/private mode:</strong> Opening a private or incognito window prevents sites from appearing in your history. This doesn't protect against stalkerware or network monitoring, but it helps with casual checking.</li>
                    <li><strong>Use a safer device:</strong> A trusted friend's phone, a work computer, or a library or community centre computer may be safer than a device the person causing harm has had access to.</li>
                    <li><strong>Monitored networks:</strong> If the person causing harm manages your home Wi-Fi or router, they may be able to see which websites you visit. Mobile data or a different Wi-Fi network may be safer.</li>
                    <li><strong>Quick Exit:</strong> The orange Quick Exit button in the top right of every page, or pressing the Escape key, will immediately take you away from this site. It navigates to a neutral page. However, it cannot clear this site from your browser history — you'll need to do that manually if needed.</li>
                </ul>

                <h2>How to Clear Browser History</h2>
                <p>The steps vary by browser. In most cases:</p>
                <ul>
                    <li><strong>Chrome:</strong> Menu (⋮) → History → find the entry → click the three dots next to it → Remove from history</li>
                    <li><strong>Safari:</strong> History menu → Show All History → find the entry → right-click → Delete</li>
                    <li><strong>Firefox:</strong> Menu (☰) → History → find the entry → right-click → Delete Page</li>
                    <li><strong>Edge:</strong> Menu (⋯) → History → find the entry → click × to remove</li>
                </ul>
                <p>Clearing your entire browser history may be more noticeable than removing individual entries.</p>

                <h2>What This Site Stores on Your Device</h2>
                <p>This site is entirely static — it does not require an account, does not ask for your name or email, and does not track you.</p>
                <p>The only data stored on your device is:</p>
                <ul>
                    <li><strong>View preference:</strong> Whether you last used the Public or Technical view (stored in your browser's localStorage under the key <code>tfa_view_preference</code>)</li>
                    <li><strong>Banner dismissal:</strong> Whether you've dismissed the browser safety banner (stored under <code>tfa_safety_banner_dismissed</code>)</li>
                </ul>
                <p>This data stays on your device. It is never sent to us or anyone else. You can clear it at any time by clearing your browser's site data for this domain.</p>

                <h2>If You Think Your Device Is Monitored</h2>
                <p>If you suspect stalkerware or monitoring software has been installed on your device:</p>
                <ul>
                    <li><strong>Do not remove it immediately.</strong> The person who installed it may receive an alert that it has been removed, which could escalate the situation. Get specialist advice first.</li>
                    <li><strong>Contact 1800RESPECT</strong> (<a href="tel:1800737732">1800 737 732</a>) to talk through your options with a specialist counsellor.</li>
                    <li><strong>Contact the eSafety Commissioner</strong> (<a href="https://www.esafety.gov.au" target="_blank" rel="noopener">esafety.gov.au</a>) — they have specific resources for technology-facilitated abuse and can help with device safety planning.</li>
                    <li><strong>If you are in immediate danger</strong>, call <a href="tel:000">000</a>.</li>
                </ul>

                <h2>Useful Resources</h2>
                <ul>
                    <li><strong>1800RESPECT:</strong> <a href="tel:1800737732">1800 737 732</a> — national DFV and sexual assault helpline (24/7)</li>
                    <li><strong>eSafety Commissioner:</strong> <a href="https://www.esafety.gov.au" target="_blank" rel="noopener">esafety.gov.au</a> — technology safety resources and reporting</li>
                    <li><strong>WESNET Safety Net Australia:</strong> <a href="https://techsafety.org.au" target="_blank" rel="noopener">techsafety.org.au</a> — technology safety guides for DFV</li>
                    <li><strong>Lifeline:</strong> <a href="tel:131114">13 11 14</a> — crisis support (24/7)</li>
                    <li><strong>Emergency:</strong> <a href="tel:000">000</a></li>
                </ul>

            </div>
        </div>
    </div>

            <!--stop-indexing-for-search-->
            <!-- search overlay -->
            <div class="overlay search" id="search-overlay" style="display: none;">
    <div class="overlay-inner">
        <div class="search-header">
            <div class="search-input">
                <input type="text" id="search-input" placeholder="search">
            </div>
            <div class="search-icons">
                <div class="search-parsing-icon spinner-border" style="display: none" id="search-parsing-icon"></div>
                <div class="close-search-icon" id="close-search-icon">&times;</div>
            </div>
        </div>
        <div id="search-body" class="search-body">
            <div class="results" id="search-results"></div>
            <div id="load-more-results" class="load-more-results">
                <button class="btn btn-default" id="load-more-results-button">load more results</button>
            </div>
        </div>
    </div>
</div>

        </div>
        <div class="row flex-grow-0 flex-shrink-1">
            <!-- footer elements -->
            <footer class="col footer">
                <div class="container-fluid">
                    <div class="row row-footer">
                        <div class="col-2 col-sm-2 col-md-2">
                            <div class="footer-center-responsive my-auto">
                                <a href="https://notastandard.org" target="_blank" rel="noopener" aria-label="Not A Standard">
                                    <img src="/theme/images/safe_logo_footer.png" class="mitre-logo-wtrans">
                                </a>
                            </div>
                        </div>
                        <div class="col-2 col-sm-2 footer-responsive-break"></div>
                        <div class="footer-link-group">
                            <div class="row row-footer">
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="/about/" class="footer-link">About</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://notastandard.org" class="footer-link">About SAFE</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://form.jotform.com/260340396646056" class="footer-link" target="_blank">Submit a Pattern</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://github.com/notastandard-org/tfa-matrix" class="footer-link" target="_blank">Contribute</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://www.notastandard.org/contact-8" class="footer-link">Contact</a></u>
                                </div>
                            </div>
                            <div class="row row-footer footer-legal-row">
                                <div class="px-3 col-footer">
                                    <a href="/about/online-safety/" class="footer-link">Your Safety Online</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/privacy/" class="footer-link">Privacy</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/terms/" class="footer-link">Terms</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/licensing/" class="footer-link">Licensing</a>
                                </div>
                            </div>
                            <div class="row">
                                <small class="px-3">
                                    &copy;&nbsp;2026, Not A Standard Pty Ltd. SAFE and TFA Matrix are trademarks of Not A Standard Pty Ltd.
                                </small>
                            </div>
                        </div>
                        <div class="w-100 p-2 footer-responsive-break"></div>
                        <div class="col footer-float-right-responsive-centered">
                            <div>
                                <div>
                                    <a href="https://tfa.notastandard.org" class="btn btn-primary w-100">
                                        tfa.notastandard.org
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    </div>

<!--stopindex-->

</div>
    <!--SCRIPTS-->
    <script src="/theme/scripts/jquery-3.5.1.min.js"></script>
    <script src="/theme/scripts/popper.min.js"></script>
    <script src="/theme/scripts/bootstrap-select.min.js"></script>
    <script src="/theme/scripts/bootstrap.bundle.min.js"></script>
    <script src="/theme/scripts/site.js"></script>
    <script src="/theme/scripts/settings.js"></script>
    <script src="/theme/scripts/search_bundle.js"></script>
    <script src="/theme/scripts/safety-banner.js"></script>
    <script>
        // Quick Exit - Escape key shortcut
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                window.location.href = 'https://doodles.google';
            }
        });
    </script>
</body>
</html>
'''

PRIVACY_CONTENT = '''
<!DOCTYPE html>
<html lang='en'>

<head>

        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1,shrink-to-fit=no'>
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <link rel='shortcut icon' href='/theme/favicon.ico' type='image/x-icon'>
        <title>Privacy Statement | SAFE TFA Matrix</title>
        <!-- Bootstrap CSS -->
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap.min.css' />
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap-tourist.css' />
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap-select.min.css' />
        <!-- Fontawesome CSS -->
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/fontawesome.min.css"/>
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/brands.min.css"/>
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/solid.min.css"/>
        <link rel="stylesheet" href="/theme/style-user.css"/>

</head>

<body>

    <div class="safety-banner" id="browser-safety-banner">
        <div class="safety-banner-content">
            <strong>Is someone checking your browsing?</strong>
            This website will appear in your browser history. If you're concerned someone may be monitoring your internet use, consider using a trusted friend's device, a library computer, or your browser's private/incognito mode. You can press <strong>Quick Exit</strong> or hit <strong>Escape</strong> at any time to leave this site quickly.
            <a href="/about/online-safety/">Learn more about staying safe online</a>
        </div>
        <button class="safety-banner-close" id="close-safety-banner" aria-label="Dismiss safety notice">&times;</button>
    </div>

    <div class="container-fluid attack-website-wrapper d-flex flex-column h-100">
        <div class="row sticky-top flex-grow-0 flex-shrink-1">
            <!-- header elements -->
            <header class="col px-0">
                    <nav class='navbar navbar-expand-lg navbar-dark position-static'>
        <a class='navbar-brand' href='/'><img src="/theme/images/safe_logo_header.png" class="attack-logo"></a>
        <button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarCollapse'
                aria-controls='navbarCollapse' aria-expanded='false' aria-label='Toggle navigation'>
                <span class='navbar-toggler-icon'></span>
        </button>
        <div class='collapse navbar-collapse' id='navbarCollapse'>
            <ul class='nav nav-tabs ml-auto'>
                        <li class="nav-item">
                            <a href="/matrices/tfa/"  class="nav-link" ><b>Matrix</b></a>
                        </li>
                        <li class="nav-item">
                            <a href="/tactics/tfa/"  class="nav-link" ><b>Tactics</b></a>
                        </li>
                        <li class="nav-item">
                            <a href="/techniques/tfa/"  class="nav-link" ><b>Techniques</b></a>
                        </li>
                        <li class="nav-item">
                            <a href="/about/"  class="nav-link" ><b>About</b></a>
                        </li>
                        <li class="nav-item">
                            <button id="search-button" class="btn search-button">Search <div id="search-icon" class="icon-button search-icon"></div></button>
                        </li>


            </ul>
            <a href="https://doodles.google" id="quick-exit-btn" class="btn ml-3"
               style="background-color: #e65100; color: white; font-weight: bold; padding: 8px 16px; border-radius: 4px;"
               title="Press Escape to quickly leave this site">Quick Exit</a>
        </div>
    </nav>

            </header>
        </div>
        <div class="row flex-grow-0 flex-shrink-1">
            <!-- banner elements -->
            <div class="col px-0">
                <!-- !versions banner! -->
            </div>
        </div>
        <div class="row flex-grow-1 flex-shrink-0">
            <!-- main content elements -->
            <!--start-indexing-for-search-->

    <div class="col pt-4">
        <!--stopindex-->
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/">Home</a></li>
            <li class="breadcrumb-item"><a href="/about/">About</a></li>
            <li class="breadcrumb-item">Privacy</li>
        </ol>

        <div class="container pb-5">
            <div class="limitations-page">
                <h1>Privacy Statement</h1>
                <p><strong>Effective date:</strong> February 2026<br>
                <strong>Last updated:</strong> February 2026</p>

                <h2>Overview</h2>
                <p>The TFA Matrix (tfa.notastandard.org) is operated by Not A Standard Pty Ltd. We take your privacy seriously — particularly given the sensitive nature of the subject matter on this site.</p>
                <p><strong>The short version:</strong> We don't collect your personal information. This site doesn't use accounts, analytics, tracking cookies, or contact forms. The only data stored is on your own device, under your control.</p>

                <h2>What We Collect</h2>
                <p><strong>Nothing.</strong> This website is a static site hosted on GitHub Pages. We do not:</p>
                <ul>
                    <li>Collect your name, email address, or any personal information</li>
                    <li>Use analytics or tracking tools (no Google Analytics, no Meta Pixel, no equivalent)</li>
                    <li>Use cookies</li>
                    <li>Store any data on our servers</li>
                    <li>Track which pages you visit</li>
                    <li>Log your IP address (though our hosting provider GitHub may — see below)</li>
                </ul>

                <h2>What's Stored on Your Device</h2>
                <p>This site uses your browser's localStorage to save two preferences:</p>
                <ul>
                    <li><code>tfa_view_preference</code> — whether you prefer the Public or Technical view</li>
                    <li><code>tfa_safety_banner_dismissed</code> — whether you've dismissed the browser safety banner</li>
                </ul>
                <p>This data is stored locally on your device only. It is never transmitted to us. You can clear it at any time through your browser settings.</p>

                <h2>Hosting Provider</h2>
                <p>This site is hosted on GitHub Pages, a service provided by GitHub, Inc. GitHub may collect technical information such as IP addresses in server logs as part of operating the hosting service. This is governed by <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" target="_blank" rel="noopener">GitHub's privacy statement</a>.</p>
                <p>We do not have access to GitHub's server logs.</p>

                <h2>External Links</h2>
                <p>This site contains links to external services and resources, including:</p>
                <ul>
                    <li><strong>1800RESPECT</strong> (1800respect.org.au)</li>
                    <li><strong>eSafety Commissioner</strong> (esafety.gov.au)</li>
                    <li><strong>JotForm</strong> (for the "Submit a Pattern" form)</li>
                    <li><strong>GitHub</strong> (for the source code repository)</li>
                    <li><strong>Not A Standard</strong> (notastandard.org)</li>
                </ul>
                <p>These external sites have their own privacy policies. We encourage you to review them. In particular, the "Submit a Pattern" form is hosted by JotForm and is subject to JotForm's privacy policy.</p>

                <h2>Children's Privacy</h2>
                <p>This site does not knowingly collect any information from children or any other person. No information is collected.</p>

                <h2>Your Rights</h2>
                <p>Under the Australian Privacy Act 1988, you have rights regarding your personal information. Since we do not collect personal information through this site, these rights are not directly engaged by your use of this website.</p>
                <p>If you have submitted information through the "Submit a Pattern" form (hosted by JotForm) and wish to have it amended or deleted, contact us at the details below.</p>

                <h2>Contact</h2>
                <p>If you have questions about this privacy statement:</p>
                <ul>
                    <li><strong>Website:</strong> <a href="https://notastandard.org" target="_blank" rel="noopener">notastandard.org</a></li>
                </ul>

                <h2>Changes to This Statement</h2>
                <p>We may update this privacy statement from time to time. The "Last updated" date at the top of this page will be revised accordingly.</p>

            </div>
        </div>
    </div>

            <!--stop-indexing-for-search-->
            <!-- search overlay -->
            <div class="overlay search" id="search-overlay" style="display: none;">
    <div class="overlay-inner">
        <div class="search-header">
            <div class="search-input">
                <input type="text" id="search-input" placeholder="search">
            </div>
            <div class="search-icons">
                <div class="search-parsing-icon spinner-border" style="display: none" id="search-parsing-icon"></div>
                <div class="close-search-icon" id="close-search-icon">&times;</div>
            </div>
        </div>
        <div id="search-body" class="search-body">
            <div class="results" id="search-results"></div>
            <div id="load-more-results" class="load-more-results">
                <button class="btn btn-default" id="load-more-results-button">load more results</button>
            </div>
        </div>
    </div>
</div>

        </div>
        <div class="row flex-grow-0 flex-shrink-1">
            <!-- footer elements -->
            <footer class="col footer">
                <div class="container-fluid">
                    <div class="row row-footer">
                        <div class="col-2 col-sm-2 col-md-2">
                            <div class="footer-center-responsive my-auto">
                                <a href="https://notastandard.org" target="_blank" rel="noopener" aria-label="Not A Standard">
                                    <img src="/theme/images/safe_logo_footer.png" class="mitre-logo-wtrans">
                                </a>
                            </div>
                        </div>
                        <div class="col-2 col-sm-2 footer-responsive-break"></div>
                        <div class="footer-link-group">
                            <div class="row row-footer">
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="/about/" class="footer-link">About</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://notastandard.org" class="footer-link">About SAFE</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://form.jotform.com/260340396646056" class="footer-link" target="_blank">Submit a Pattern</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://github.com/notastandard-org/tfa-matrix" class="footer-link" target="_blank">Contribute</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://www.notastandard.org/contact-8" class="footer-link">Contact</a></u>
                                </div>
                            </div>
                            <div class="row row-footer footer-legal-row">
                                <div class="px-3 col-footer">
                                    <a href="/about/online-safety/" class="footer-link">Your Safety Online</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/privacy/" class="footer-link">Privacy</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/terms/" class="footer-link">Terms</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/licensing/" class="footer-link">Licensing</a>
                                </div>
                            </div>
                            <div class="row">
                                <small class="px-3">
                                    &copy;&nbsp;2026, Not A Standard Pty Ltd. SAFE and TFA Matrix are trademarks of Not A Standard Pty Ltd.
                                </small>
                            </div>
                        </div>
                        <div class="w-100 p-2 footer-responsive-break"></div>
                        <div class="col footer-float-right-responsive-centered">
                            <div>
                                <div>
                                    <a href="https://tfa.notastandard.org" class="btn btn-primary w-100">
                                        tfa.notastandard.org
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    </div>

<!--stopindex-->

</div>
    <!--SCRIPTS-->
    <script src="/theme/scripts/jquery-3.5.1.min.js"></script>
    <script src="/theme/scripts/popper.min.js"></script>
    <script src="/theme/scripts/bootstrap-select.min.js"></script>
    <script src="/theme/scripts/bootstrap.bundle.min.js"></script>
    <script src="/theme/scripts/site.js"></script>
    <script src="/theme/scripts/settings.js"></script>
    <script src="/theme/scripts/search_bundle.js"></script>
    <script src="/theme/scripts/safety-banner.js"></script>
    <script>
        // Quick Exit - Escape key shortcut
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                window.location.href = 'https://doodles.google';
            }
        });
    </script>
</body>
</html>
'''

TERMS_CONTENT = '''
<!DOCTYPE html>
<html lang='en'>

<head>

        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1,shrink-to-fit=no'>
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <link rel='shortcut icon' href='/theme/favicon.ico' type='image/x-icon'>
        <title>Terms of Use | SAFE TFA Matrix</title>
        <!-- Bootstrap CSS -->
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap.min.css' />
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap-tourist.css' />
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap-select.min.css' />
        <!-- Fontawesome CSS -->
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/fontawesome.min.css"/>
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/brands.min.css"/>
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/solid.min.css"/>
        <link rel="stylesheet" href="/theme/style-user.css"/>

</head>

<body>

    <div class="safety-banner" id="browser-safety-banner">
        <div class="safety-banner-content">
            <strong>Is someone checking your browsing?</strong>
            This website will appear in your browser history. If you're concerned someone may be monitoring your internet use, consider using a trusted friend's device, a library computer, or your browser's private/incognito mode. You can press <strong>Quick Exit</strong> or hit <strong>Escape</strong> at any time to leave this site quickly.
            <a href="/about/online-safety/">Learn more about staying safe online</a>
        </div>
        <button class="safety-banner-close" id="close-safety-banner" aria-label="Dismiss safety notice">&times;</button>
    </div>

    <div class="container-fluid attack-website-wrapper d-flex flex-column h-100">
        <div class="row sticky-top flex-grow-0 flex-shrink-1">
            <!-- header elements -->
            <header class="col px-0">
                    <nav class='navbar navbar-expand-lg navbar-dark position-static'>
        <a class='navbar-brand' href='/'><img src="/theme/images/safe_logo_header.png" class="attack-logo"></a>
        <button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarCollapse'
                aria-controls='navbarCollapse' aria-expanded='false' aria-label='Toggle navigation'>
                <span class='navbar-toggler-icon'></span>
        </button>
        <div class='collapse navbar-collapse' id='navbarCollapse'>
            <ul class='nav nav-tabs ml-auto'>
                        <li class="nav-item">
                            <a href="/matrices/tfa/"  class="nav-link" ><b>Matrix</b></a>
                        </li>
                        <li class="nav-item">
                            <a href="/tactics/tfa/"  class="nav-link" ><b>Tactics</b></a>
                        </li>
                        <li class="nav-item">
                            <a href="/techniques/tfa/"  class="nav-link" ><b>Techniques</b></a>
                        </li>
                        <li class="nav-item">
                            <a href="/about/"  class="nav-link" ><b>About</b></a>
                        </li>
                        <li class="nav-item">
                            <button id="search-button" class="btn search-button">Search <div id="search-icon" class="icon-button search-icon"></div></button>
                        </li>


            </ul>
            <a href="https://doodles.google" id="quick-exit-btn" class="btn ml-3"
               style="background-color: #e65100; color: white; font-weight: bold; padding: 8px 16px; border-radius: 4px;"
               title="Press Escape to quickly leave this site">Quick Exit</a>
        </div>
    </nav>

            </header>
        </div>
        <div class="row flex-grow-0 flex-shrink-1">
            <!-- banner elements -->
            <div class="col px-0">
                <!-- !versions banner! -->
            </div>
        </div>
        <div class="row flex-grow-1 flex-shrink-0">
            <!-- main content elements -->
            <!--start-indexing-for-search-->

    <div class="col pt-4">
        <!--stopindex-->
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/">Home</a></li>
            <li class="breadcrumb-item"><a href="/about/">About</a></li>
            <li class="breadcrumb-item">Terms of Use</li>
        </ol>

        <div class="container pb-5">
            <div class="limitations-page">
                <h1>Terms of Use</h1>
                <p><strong>Effective date:</strong> February 2026<br>
                <strong>Last updated:</strong> February 2026</p>

                <h2>Agreement</h2>
                <p>By accessing and using the TFA Matrix (tfa.notastandard.org), you agree to these Terms of Use. If you do not agree, please do not use this site.</p>

                <h2>About This Resource</h2>
                <p>The TFA Matrix is a structured knowledge base of technology-facilitated abuse techniques, maintained by Not A Standard Pty Ltd. It is provided as a public resource for education, protection, research, and policy development.</p>
                <p><strong>This site does not provide personal advice.</strong> The information on this site is general in nature and is not a substitute for professional legal, psychological, forensic, technical, or safety advice. Every situation involving domestic and family violence is different. Please see our full <a href="/about/limitations/">Limitations, Methodology &amp; Responsible Use</a> statement.</p>

                <h2>Permitted Use</h2>
                <p>You may use this site and its content for:</p>
                <ul>
                    <li><strong>Personal safety:</strong> Understanding technology-facilitated abuse and identifying potential indicators in your own situation</li>
                    <li><strong>Professional practice:</strong> Informing domestic violence case work, law enforcement investigation, legal practice, counselling, and related professional activities</li>
                    <li><strong>Research:</strong> Academic and policy research into technology-facilitated abuse, domestic violence, or related fields</li>
                    <li><strong>Education:</strong> Teaching, training, and professional development</li>
                    <li><strong>Policy development:</strong> Informing legislation, regulation, and organisational policy</li>
                    <li><strong>Tool development:</strong> Building tools, services, or resources that protect people from technology-facilitated abuse, subject to the licensing terms below</li>
                </ul>

                <h2>Prohibited Use</h2>
                <p>You must not use this site or its content to:</p>
                <ul>
                    <li>Develop, refine, or implement techniques for perpetrating abuse, surveillance, harassment, coercive control, or any form of interpersonal harm</li>
                    <li>Identify or exploit vulnerabilities in a victim's protective measures</li>
                    <li>Develop tools, products, or services that enable abuse, stalking, surveillance, or control of another person</li>
                    <li>Circumvent detection indicators described in this framework</li>
                    <li>Misrepresent the framework's conclusions, methodology, or scope</li>
                    <li>Present technique descriptions as instructional or how-to guides</li>
                </ul>
                <p>Not A Standard reserves the right to take action, including pursuing legal remedies, against any individual or organisation that uses this framework to facilitate harm.</p>

                <h2>No Warranty</h2>
                <p>This site and its content are provided "as is" and "as available" without warranty of any kind, express or implied. Not A Standard does not warrant that:</p>
                <ul>
                    <li>The content is complete, accurate, or current</li>
                    <li>The framework covers all possible technology-facilitated abuse techniques</li>
                    <li>Any protective action described on this site will be effective or safe in any specific situation</li>
                    <li>The site will be available without interruption or error</li>
                </ul>

                <h2>Limitation of Liability</h2>
                <p>To the maximum extent permitted by Australian law, Not A Standard, its directors, employees, and contributors shall not be liable for any direct, indirect, incidental, consequential, or special damages arising from:</p>
                <ul>
                    <li>Your use of or reliance on information provided on this site</li>
                    <li>Any action taken or not taken based on information on this site</li>
                    <li>Any inability to access the site</li>
                    <li>Any errors or omissions in the content</li>
                </ul>
                <p>This limitation applies regardless of the legal theory on which the claim is based.</p>

                <h2>Intellectual Property</h2>

                <h3>Our Content</h3>
                <p>The text, structure, methodology, and presentation of the TFA Matrix are &copy; 2026 Not A Standard Pty Ltd. SAFE and TFA Matrix are trademarks of Not A Standard Pty Ltd.</p>

                <h3>STIX Data</h3>
                <p>The TFA Matrix dataset (<code>tfa-attack.json</code>) is released under the <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)</a>. You are free to share and adapt the data for non-commercial purposes, provided you give appropriate credit and distribute any derivative works under the same licence. For commercial licensing enquiries, contact Not A Standard.</p>

                <h3>MITRE ATT&amp;CK</h3>
                <p>MITRE ATT&amp;CK&reg; is a registered trademark of The MITRE Corporation. The TFA Matrix uses the ATT&amp;CK knowledge representation methodology for interoperability and is not affiliated with, endorsed by, or a product of The MITRE Corporation. The ATT&amp;CK website framework code used for this site is used under the Apache 2.0 License.</p>

                <h3>Contributing</h3>
                <p>By submitting a pull request, issue, or pattern submission to the TFA Matrix, you grant Not A Standard Pty Ltd a perpetual, worldwide, royalty-free licence to use, modify, and distribute your contribution as part of the TFA Matrix under the terms stated here.</p>

                <h2>Third-Party Links</h2>
                <p>This site contains links to third-party websites and services. Not A Standard is not responsible for the content, privacy practices, or availability of these external sites.</p>

                <h2>Governing Law</h2>
                <p>These Terms of Use are governed by the laws of Australia. Any disputes arising from or relating to the use of this site shall be subject to the jurisdiction of the courts of Australia.</p>

                <h2>Changes to These Terms</h2>
                <p>We may update these Terms of Use from time to time. The "Last updated" date at the top of this page will be revised accordingly. Continued use of the site after changes constitutes acceptance of the revised terms.</p>

                <h2>Contact</h2>
                <p>If you have questions about these Terms of Use:</p>
                <ul>
                    <li><strong>Website:</strong> <a href="https://notastandard.org" target="_blank" rel="noopener">notastandard.org</a></li>
                </ul>

            </div>
        </div>
    </div>

            <!--stop-indexing-for-search-->
            <!-- search overlay -->
            <div class="overlay search" id="search-overlay" style="display: none;">
    <div class="overlay-inner">
        <div class="search-header">
            <div class="search-input">
                <input type="text" id="search-input" placeholder="search">
            </div>
            <div class="search-icons">
                <div class="search-parsing-icon spinner-border" style="display: none" id="search-parsing-icon"></div>
                <div class="close-search-icon" id="close-search-icon">&times;</div>
            </div>
        </div>
        <div id="search-body" class="search-body">
            <div class="results" id="search-results"></div>
            <div id="load-more-results" class="load-more-results">
                <button class="btn btn-default" id="load-more-results-button">load more results</button>
            </div>
        </div>
    </div>
</div>

        </div>
        <div class="row flex-grow-0 flex-shrink-1">
            <!-- footer elements -->
            <footer class="col footer">
                <div class="container-fluid">
                    <div class="row row-footer">
                        <div class="col-2 col-sm-2 col-md-2">
                            <div class="footer-center-responsive my-auto">
                                <a href="https://notastandard.org" target="_blank" rel="noopener" aria-label="Not A Standard">
                                    <img src="/theme/images/safe_logo_footer.png" class="mitre-logo-wtrans">
                                </a>
                            </div>
                        </div>
                        <div class="col-2 col-sm-2 footer-responsive-break"></div>
                        <div class="footer-link-group">
                            <div class="row row-footer">
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="/about/" class="footer-link">About</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://notastandard.org" class="footer-link">About SAFE</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://form.jotform.com/260340396646056" class="footer-link" target="_blank">Submit a Pattern</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://github.com/notastandard-org/tfa-matrix" class="footer-link" target="_blank">Contribute</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://www.notastandard.org/contact-8" class="footer-link">Contact</a></u>
                                </div>
                            </div>
                            <div class="row row-footer footer-legal-row">
                                <div class="px-3 col-footer">
                                    <a href="/about/online-safety/" class="footer-link">Your Safety Online</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/privacy/" class="footer-link">Privacy</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/terms/" class="footer-link">Terms</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/licensing/" class="footer-link">Licensing</a>
                                </div>
                            </div>
                            <div class="row">
                                <small class="px-3">
                                    &copy;&nbsp;2026, Not A Standard Pty Ltd. SAFE and TFA Matrix are trademarks of Not A Standard Pty Ltd.
                                </small>
                            </div>
                        </div>
                        <div class="w-100 p-2 footer-responsive-break"></div>
                        <div class="col footer-float-right-responsive-centered">
                            <div>
                                <div>
                                    <a href="https://tfa.notastandard.org" class="btn btn-primary w-100">
                                        tfa.notastandard.org
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    </div>

<!--stopindex-->

</div>
    <!--SCRIPTS-->
    <script src="/theme/scripts/jquery-3.5.1.min.js"></script>
    <script src="/theme/scripts/popper.min.js"></script>
    <script src="/theme/scripts/bootstrap-select.min.js"></script>
    <script src="/theme/scripts/bootstrap.bundle.min.js"></script>
    <script src="/theme/scripts/site.js"></script>
    <script src="/theme/scripts/settings.js"></script>
    <script src="/theme/scripts/search_bundle.js"></script>
    <script src="/theme/scripts/safety-banner.js"></script>
    <script>
        // Quick Exit - Escape key shortcut
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                window.location.href = 'https://doodles.google';
            }
        });
    </script>
</body>
</html>
'''

LICENSING_CONTENT = '''
<!DOCTYPE html>
<html lang='en'>

<head>

        <meta charset='utf-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1,shrink-to-fit=no'>
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <link rel='shortcut icon' href='/theme/favicon.ico' type='image/x-icon'>
        <title>Data Licensing & Reuse | SAFE TFA Matrix</title>
        <!-- Bootstrap CSS -->
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap.min.css' />
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap-tourist.css' />
        <link rel='stylesheet' href='/theme/style/vendors/bootstrap-select.min.css' />
        <!-- Fontawesome CSS -->
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/fontawesome.min.css"/>
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/brands.min.css"/>
        <link rel="stylesheet" href="/theme/style/vendors/fontawesome-6.5.1/css/solid.min.css"/>
        <link rel="stylesheet" href="/theme/style-user.css"/>

</head>

<body>

    <div class="safety-banner" id="browser-safety-banner">
        <div class="safety-banner-content">
            <strong>Is someone checking your browsing?</strong>
            This website will appear in your browser history. If you're concerned someone may be monitoring your internet use, consider using a trusted friend's device, a library computer, or your browser's private/incognito mode. You can press <strong>Quick Exit</strong> or hit <strong>Escape</strong> at any time to leave this site quickly.
            <a href="/about/online-safety/">Learn more about staying safe online</a>
        </div>
        <button class="safety-banner-close" id="close-safety-banner" aria-label="Dismiss safety notice">&times;</button>
    </div>

    <div class="container-fluid attack-website-wrapper d-flex flex-column h-100">
        <div class="row sticky-top flex-grow-0 flex-shrink-1">
            <!-- header elements -->
            <header class="col px-0">
                    <nav class='navbar navbar-expand-lg navbar-dark position-static'>
        <a class='navbar-brand' href='/'><img src="/theme/images/safe_logo_header.png" class="attack-logo"></a>
        <button class='navbar-toggler' type='button' data-toggle='collapse' data-target='#navbarCollapse'
                aria-controls='navbarCollapse' aria-expanded='false' aria-label='Toggle navigation'>
                <span class='navbar-toggler-icon'></span>
        </button>
        <div class='collapse navbar-collapse' id='navbarCollapse'>
            <ul class='nav nav-tabs ml-auto'>
                        <li class="nav-item">
                            <a href="/matrices/tfa/"  class="nav-link" ><b>Matrix</b></a>
                        </li>
                        <li class="nav-item">
                            <a href="/tactics/tfa/"  class="nav-link" ><b>Tactics</b></a>
                        </li>
                        <li class="nav-item">
                            <a href="/techniques/tfa/"  class="nav-link" ><b>Techniques</b></a>
                        </li>
                        <li class="nav-item">
                            <a href="/about/"  class="nav-link" ><b>About</b></a>
                        </li>
                        <li class="nav-item">
                            <button id="search-button" class="btn search-button">Search <div id="search-icon" class="icon-button search-icon"></div></button>
                        </li>


            </ul>
            <a href="https://doodles.google" id="quick-exit-btn" class="btn ml-3"
               style="background-color: #e65100; color: white; font-weight: bold; padding: 8px 16px; border-radius: 4px;"
               title="Press Escape to quickly leave this site">Quick Exit</a>
        </div>
    </nav>

            </header>
        </div>
        <div class="row flex-grow-0 flex-shrink-1">
            <!-- banner elements -->
            <div class="col px-0">
                <!-- !versions banner! -->
            </div>
        </div>
        <div class="row flex-grow-1 flex-shrink-0">
            <!-- main content elements -->
            <!--start-indexing-for-search-->

    <div class="col pt-4">
        <!--stopindex-->
        <ol class="breadcrumb">
            <li class="breadcrumb-item"><a href="/">Home</a></li>
            <li class="breadcrumb-item"><a href="/about/">About</a></li>
            <li class="breadcrumb-item">Licensing</li>
        </ol>

        <div class="container pb-5">
            <div class="limitations-page">
                <h1>Data Licensing &amp; Reuse</h1>

                <h2>TFA Matrix STIX Data</h2>
                <p>The TFA Matrix dataset (<code>tfa-attack.json</code>) is released under the <strong><a href="https://creativecommons.org/licenses/by-nc-sa/4.0/" target="_blank" rel="noopener">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License (CC BY-NC-SA 4.0)</a></strong>.</p>

                <p>This means you are free to:</p>
                <ul>
                    <li><strong>Share</strong> — copy and redistribute the data in any medium or format</li>
                    <li><strong>Adapt</strong> — remix, transform, and build upon the data</li>
                </ul>

                <p>Under the following terms:</p>
                <ul>
                    <li><strong>Attribution</strong> — You must give appropriate credit to Not A Standard Pty Ltd, provide a link to the licence, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests Not A Standard endorses you or your use.</li>
                    <li><strong>NonCommercial</strong> — You may not use the material for commercial purposes.</li>
                    <li><strong>ShareAlike</strong> — If you remix, transform, or build upon the material, you must distribute your contributions under the same licence as the original.</li>
                </ul>

                <p>For commercial licensing enquiries, contact Not A Standard.</p>

                <h3>Suggested Citation</h3>
                <blockquote>
                    Not A Standard Pty Ltd. (2026). TFA Matrix: Technology-Facilitated Abuse ATT&amp;CK Framework. Version 1.0. Available at: https://tfa.notastandard.org
                </blockquote>

                <h3>Ethical Use Condition</h3>
                <p>While CC BY-NC-SA 4.0 permits non-commercial sharing and adaptation, use of this data is also subject to our <a href="/about/terms/">Terms of Use</a>, which prohibit using the data to develop tools or techniques that enable abuse. We rely on the good faith of the research and practitioner community to honour this expectation.</p>

                <h2>Website Code</h2>
                <p>The TFA Matrix website is built on a modified version of the MITRE ATT&amp;CK website framework, which is licensed under the Apache License 2.0. Our modifications to the website code are similarly available under Apache 2.0 in our <a href="https://github.com/notastandard-org/tfa-matrix" target="_blank" rel="noopener">GitHub repository</a>.</p>

                <h2>SAFE Methodology</h2>
                <p>The SAFE (Security Abuse Framework for Evidence) methodology, including its analytical framework, classification system, and scoring models, is proprietary to Not A Standard Pty Ltd. Researchers wishing to apply or reference the SAFE methodology should contact us to discuss collaboration.</p>

                <h2>API Access</h2>
                <p>There is currently no public API for the TFA Matrix. The STIX data file can be downloaded directly from the GitHub repository. If you have a use case that would benefit from API access, please get in touch.</p>

                <h2>Contact</h2>
                <p>For licensing queries, research collaboration, or data access requests:</p>
                <ul>
                    <li><strong>Website:</strong> <a href="https://notastandard.org" target="_blank" rel="noopener">notastandard.org</a></li>
                </ul>

            </div>
        </div>
    </div>

            <!--stop-indexing-for-search-->
            <!-- search overlay -->
            <div class="overlay search" id="search-overlay" style="display: none;">
    <div class="overlay-inner">
        <div class="search-header">
            <div class="search-input">
                <input type="text" id="search-input" placeholder="search">
            </div>
            <div class="search-icons">
                <div class="search-parsing-icon spinner-border" style="display: none" id="search-parsing-icon"></div>
                <div class="close-search-icon" id="close-search-icon">&times;</div>
            </div>
        </div>
        <div id="search-body" class="search-body">
            <div class="results" id="search-results"></div>
            <div id="load-more-results" class="load-more-results">
                <button class="btn btn-default" id="load-more-results-button">load more results</button>
            </div>
        </div>
    </div>
</div>

        </div>
        <div class="row flex-grow-0 flex-shrink-1">
            <!-- footer elements -->
            <footer class="col footer">
                <div class="container-fluid">
                    <div class="row row-footer">
                        <div class="col-2 col-sm-2 col-md-2">
                            <div class="footer-center-responsive my-auto">
                                <a href="https://notastandard.org" target="_blank" rel="noopener" aria-label="Not A Standard">
                                    <img src="/theme/images/safe_logo_footer.png" class="mitre-logo-wtrans">
                                </a>
                            </div>
                        </div>
                        <div class="col-2 col-sm-2 footer-responsive-break"></div>
                        <div class="footer-link-group">
                            <div class="row row-footer">
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="/about/" class="footer-link">About</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://notastandard.org" class="footer-link">About SAFE</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://form.jotform.com/260340396646056" class="footer-link" target="_blank">Submit a Pattern</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://github.com/notastandard-org/tfa-matrix" class="footer-link" target="_blank">Contribute</a></u>
                                </div>
                                <div class="px-3 col-footer">
                                    <u class="footer-link"><a href="https://www.notastandard.org/contact-8" class="footer-link">Contact</a></u>
                                </div>
                            </div>
                            <div class="row row-footer footer-legal-row">
                                <div class="px-3 col-footer">
                                    <a href="/about/online-safety/" class="footer-link">Your Safety Online</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/privacy/" class="footer-link">Privacy</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/terms/" class="footer-link">Terms</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/licensing/" class="footer-link">Licensing</a>
                                </div>
                            </div>
                            <div class="row">
                                <small class="px-3">
                                    &copy;&nbsp;2026, Not A Standard Pty Ltd. SAFE and TFA Matrix are trademarks of Not A Standard Pty Ltd.
                                </small>
                            </div>
                        </div>
                        <div class="w-100 p-2 footer-responsive-break"></div>
                        <div class="col footer-float-right-responsive-centered">
                            <div>
                                <div>
                                    <a href="https://tfa.notastandard.org" class="btn btn-primary w-100">
                                        tfa.notastandard.org
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
    </div>

<!--stopindex-->

</div>
    <!--SCRIPTS-->
    <script src="/theme/scripts/jquery-3.5.1.min.js"></script>
    <script src="/theme/scripts/popper.min.js"></script>
    <script src="/theme/scripts/bootstrap-select.min.js"></script>
    <script src="/theme/scripts/bootstrap.bundle.min.js"></script>
    <script src="/theme/scripts/site.js"></script>
    <script src="/theme/scripts/settings.js"></script>
    <script src="/theme/scripts/search_bundle.js"></script>
    <script src="/theme/scripts/safety-banner.js"></script>
    <script>
        // Quick Exit - Escape key shortcut
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                window.location.href = 'https://doodles.google';
            }
        });
    </script>
</body>
</html>
'''

# Safety banner HTML to inject
SAFETY_BANNER = '''    <div class="safety-banner" id="browser-safety-banner">
        <div class="safety-banner-content">
            <strong>Is someone checking your browsing?</strong>
            This website will appear in your browser history. If you're concerned someone may be monitoring your internet use, consider using a trusted friend's device, a library computer, or your browser's private/incognito mode. You can press <strong>Quick Exit</strong> or hit <strong>Escape</strong> at any time to leave this site quickly.
            <a href="/about/online-safety/">Learn more about staying safe online</a>
        </div>
        <button class="safety-banner-close" id="close-safety-banner" aria-label="Dismiss safety notice">&times;</button>
    </div>

'''

# New footer row with legal links
FOOTER_LEGAL_ROW = '''                            <div class="row row-footer footer-legal-row">
                                <div class="px-3 col-footer">
                                    <a href="/about/online-safety/" class="footer-link">Your Safety Online</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/privacy/" class="footer-link">Privacy</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/terms/" class="footer-link">Terms</a>
                                </div>
                                <div class="px-3 col-footer">
                                    <a href="/about/licensing/" class="footer-link">Licensing</a>
                                </div>
                            </div>
'''

SAFETY_BANNER_SCRIPT = '    <script src="/theme/scripts/safety-banner.js"></script>\n'


def create_pages():
    """Create the four new pages."""
    pages = [
        ('about/online-safety', ONLINE_SAFETY_CONTENT),
        ('about/privacy', PRIVACY_CONTENT),
        ('about/terms', TERMS_CONTENT),
        ('about/licensing', LICENSING_CONTENT),
    ]

    for path, content in pages:
        # Create in both root and output
        for base in [BASE_DIR, BASE_DIR / 'output']:
            dir_path = base / path
            dir_path.mkdir(parents=True, exist_ok=True)
            file_path = dir_path / 'index.html'
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Created: {file_path.relative_to(BASE_DIR)}")


def inject_banner_and_footer(filepath):
    """Inject safety banner and footer legal row into an HTML file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    modified = False

    # Skip if already has safety banner
    if 'browser-safety-banner' not in content:
        # Inject banner after <body>
        content = content.replace('<body>\n', '<body>\n\n' + SAFETY_BANNER)
        modified = True

    # Skip if already has footer legal row
    if 'footer-legal-row' not in content:
        # Find the existing footer row with Contact and add new row after it
        # Pattern: the row ending with Contact link, followed by copyright row
        old_pattern = r'(                                <div class="px-3 col-footer">\s*<u class="footer-link"><a href="https://www\.notastandard\.org/contact-8" class="footer-link">Contact</a></u>\s*</div>\s*</div>)'
        new_replacement = r'\1\n' + FOOTER_LEGAL_ROW

        new_content = re.sub(old_pattern, new_replacement, content)
        if new_content != content:
            content = new_content
            modified = True

    # Add safety banner script if not present
    if 'safety-banner.js' not in content:
        # Add before </body>
        content = content.replace('</body>', SAFETY_BANNER_SCRIPT + '</body>')
        modified = True

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def update_all_pages():
    """Update all HTML pages with banner and footer."""
    updated = 0
    for html_file in BASE_DIR.rglob('*.html'):
        # Skip node_modules, etc.
        if 'node_modules' in str(html_file):
            continue
        if inject_banner_and_footer(html_file):
            print(f"  Updated: {html_file.relative_to(BASE_DIR)}")
            updated += 1
    return updated


def main():
    print("Creating legal/safety pages...\n")
    create_pages()

    print("\nInjecting safety banner and footer links into all pages...\n")
    updated = update_all_pages()

    print(f"\nDone! Created 8 new pages, updated {updated} existing pages.")


if __name__ == '__main__':
    main()
