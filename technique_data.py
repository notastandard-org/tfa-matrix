TECHNIQUE_DATA = {
    # ========================================================================
    # TACTIC 1: Surveillance & Tracking (TFA-TA-0001)
    # ========================================================================
    
    "TFA-T-1001": {  # Stalkerware Installation
        "mitigations": [
            ("TFA-M-1001", "Anti-Stalkerware Scanning", "Deploy anti-stalkerware detection tools to identify monitoring applications. Scan for apps with excessive permissions including location, microphone, camera, and message access."),
            ("TFA-M-1002", "Device Access Controls", "Implement strong device authentication. Disable installation from unknown sources. Maintain physical control of devices."),
            ("TFA-M-1003", "Safe Device Acquisition", "Obtain a separate device for sensitive communications if stalkerware is suspected. Removing stalkerware may alert the monitoring party."),
            ("TFA-M-1004", "Operating System Hardening", "Maintain current OS versions. Security updates frequently patch vulnerabilities exploited by stalkerware."),
            ("TFA-M-1005", "Forensic Device Audit", "Engage professional forensic analysis to identify monitoring software and preserve evidence."),
        ],
        "detections": [
            ("TFA-D-1001", "Anomalous Battery Consumption", "Device battery depletes faster than baseline due to continuous background data transmission."),
            ("TFA-D-1002", "Unexplained Data Usage", "Increased mobile data consumption without corresponding user activity. Monitor per-app data usage for unknown processes."),
            ("TFA-D-1003", "Device Temperature Anomalies", "Device runs hot during idle periods indicating background process activity."),
            ("TFA-D-1004", "Information Leakage Indicators", "Adversary demonstrates knowledge of private communications, locations, or activities accessible only through device monitoring."),
            ("TFA-D-1005", "Unknown Applications or Profiles", "Presence of unrecognised apps, device administrator privileges, or configuration profiles."),
        ],
    },
    
    "TFA-T-1002": {  # Physical Tracker Planting
        "mitigations": [
            ("TFA-M-1006", "Bluetooth Tracker Detection", "Use tracker detection applications to scan for nearby Bluetooth tracking devices. Enable platform-native unknown tracker alerts."),
            ("TFA-M-1007", "Physical Vehicle Inspection", "Conduct systematic inspection of vehicles for GPS tracking devices in common concealment locations."),
            ("TFA-M-1008", "Belongings Audit", "Inspect bags, clothing, and frequently carried items for concealed tracking devices."),
            ("TFA-M-1009", "Evidence Preservation Protocol", "If tracker discovered, document location and preserve for evidence before removal. Removal alerts monitoring party."),
        ],
        "detections": [
            ("TFA-D-1006", "Platform Tracker Alerts", "Device displays alerts for unknown tracking devices travelling with user."),
            ("TFA-D-1007", "Location Knowledge Indicators", "Adversary references specific locations, routes, or timing not disclosed by target."),
            ("TFA-D-1008", "Physical Device Discovery", "Small electronic device found attached to vehicle or concealed in belongings."),
            ("TFA-D-1009", "Audible Tracker Indicators", "Periodic beeping from unknown source in belongings or vehicle."),
        ],
    },
    
    "TFA-T-1003": {  # Shared Account Surveillance
        "mitigations": [
            ("TFA-M-1010", "Location Sharing Audit", "Review all location sharing configurations across devices and services. Disable unauthorised sharing."),
            ("TFA-M-1011", "Account Separation", "Migrate to individual accounts for services previously shared. Use new credentials unknown to adversary."),
            ("TFA-M-1012", "Carrier Account Review", "Assess family phone plan features that expose location or usage data. Plan migration to individual account."),
        ],
        "detections": [
            ("TFA-D-1010", "Shared Account Data References", "Adversary references location, purchases, or activities visible through shared account access."),
            ("TFA-D-1011", "Active Location Sharing Discovery", "Audit reveals location sharing enabled with adversary's account."),
            ("TFA-D-1012", "Unknown Devices on Shared Accounts", "Unrecognised devices listed in shared account trusted device lists."),
        ],
    },
    
    "TFA-T-1004": {  # Social Media Monitoring
        "mitigations": [
            ("TFA-M-1013", "Privacy Configuration Hardening", "Configure maximum privacy settings on all social media platforms. Restrict visibility of posts, connections, and activity."),
            ("TFA-M-1014", "Connection Audit", "Review all followers and connections for adversary-controlled accounts. Remove suspicious connections."),
            ("TFA-M-1015", "Information Disclosure Controls", "Avoid posting real-time locations, routines, or future plans. Delay posting until after events conclude."),
            ("TFA-M-1016", "Tag and Mention Restrictions", "Disable or require approval for tags and mentions to prevent third-party location disclosure."),
        ],
        "detections": [
            ("TFA-D-1013", "Non-Public Activity Knowledge", "Adversary references social media activity that should not be visible given current privacy settings."),
            ("TFA-D-1014", "Suspicious Account Patterns", "New follower accounts created recently with minimal activity or connections to adversary's network."),
            ("TFA-D-1015", "Third-Party Monitoring Reports", "Contacts report adversary has shown them target's social media content or asked about online activity."),
        ],
    },
    
    "TFA-T-1005": {  # Communication Interception
        "mitigations": [
            ("TFA-M-1017", "Email Rule Audit", "Check email settings for unauthorised forwarding rules and filters. Remove rules forwarding to unknown addresses."),
            ("TFA-M-1018", "Linked Device Review", "Review and remove unrecognised devices linked to messaging accounts."),
            ("TFA-M-1019", "Encrypted Communications", "Use end-to-end encrypted messaging for sensitive communications. Ensure adversary cannot access linked devices."),
            ("TFA-M-1020", "Voicemail Security", "Change voicemail PIN. Disable remote voicemail access where possible."),
        ],
        "detections": [
            ("TFA-D-1016", "Read Receipt Anomalies", "Messages marked as read before target has viewed them. Account shows online status during non-use periods."),
            ("TFA-D-1017", "Unauthorised Forwarding Rules", "Email settings contain forwarding rules to unknown addresses or filters moving messages automatically."),
            ("TFA-D-1018", "Unknown Linked Devices", "Messaging app settings show unrecognised devices with active sessions."),
            ("TFA-D-1019", "Communication Content Knowledge", "Adversary quotes or references private message content."),
        ],
    },
    
    "TFA-T-1006": {  # Smart Home Surveillance
        "mitigations": [
            ("TFA-M-1021", "Smart Home Account Takeover", "Transfer device ownership to sole-controlled account. Factory reset devices and reconfigure with new credentials."),
            ("TFA-M-1022", "Recording Device Audit", "Identify all cameras, microphones, and recording-capable devices. Disable or remove devices that cannot be secured."),
            ("TFA-M-1023", "Voice Assistant Hardening", "Disable remote access features, drop-in capabilities, and voice purchasing. Delete stored recordings."),
        ],
        "detections": [
            ("TFA-D-1020", "In-Home Activity Knowledge", "Adversary references conversations or activities that occurred inside the home."),
            ("TFA-D-1021", "Device Behaviour Anomalies", "Cameras activating, indicator lights engaging, or voice assistants responding without user trigger."),
            ("TFA-D-1022", "Unauthorised Device Access", "Smart home app settings show adversary account retains admin or viewer access."),
        ],
    },
    
    "TFA-T-1007": {  # Network Traffic Monitoring
        "mitigations": [
            ("TFA-M-1024", "Router Credential Reset", "Change router admin credentials. Factory reset router if adversary configured it."),
            ("TFA-M-1025", "Traffic Encryption", "Use VPN to encrypt internet traffic and prevent network-level monitoring."),
            ("TFA-M-1026", "Network Bypass", "Use mobile data instead of home network for sensitive browsing."),
        ],
        "detections": [
            ("TFA-D-1023", "Browsing Activity Knowledge", "Adversary references websites visited or searches performed."),
            ("TFA-D-1024", "Unauthorised Network Controls", "Router contains parental controls, content filtering, or logging not configured by target."),
            ("TFA-D-1025", "Network Monitoring Tools Present", "Discovery of network monitoring software or devices on home network."),
        ],
    },
    
    "TFA-T-1008": {  # Calendar/Schedule Surveillance
        "mitigations": [
            ("TFA-M-1027", "Calendar Sharing Audit", "Review and remove unauthorised calendar sharing permissions across all calendar applications."),
            ("TFA-M-1028", "Sensitive Appointment Isolation", "Use separate calendar on adversary-unknown account for sensitive appointments."),
            ("TFA-M-1029", "Medical Portal Security", "Change credentials on health portals. Remove adversary as authorised contact."),
        ],
        "detections": [
            ("TFA-D-1026", "Appointment Interception", "Adversary appears at calendar events they should not know about."),
            ("TFA-D-1027", "Schedule Knowledge Indicators", "Adversary references upcoming appointments before disclosure."),
            ("TFA-D-1028", "Active Calendar Sharing", "Audit reveals adversary retains calendar viewing access."),
        ],
    },
    
    "TFA-T-1009": {  # Third-Party Monitoring Recruitment
        "mitigations": [
            ("TFA-M-1030", "Information Compartmentalisation", "Limit sensitive information shared with contacts who maintain relationship with adversary."),
            ("TFA-M-1031", "Network Trust Assessment", "Identify which contacts may relay information to adversary based on information leakage patterns."),
            ("TFA-M-1032", "Canary Information Testing", "Share unique details with specific contacts to identify information relay sources."),
        ],
        "detections": [
            ("TFA-D-1029", "Source-Specific Information Leakage", "Adversary gains knowledge of information shared only with specific individuals."),
            ("TFA-D-1030", "Unusual Contact Questioning", "Contacts ask unusually specific questions about location, plans, or relationships."),
            ("TFA-D-1031", "Recruitment Attempt Reports", "Trusted contacts report adversary has requested information about target."),
        ],
    },
    
    "TFA-T-1010": {  # Fitness/Health Tracker Surveillance
        "mitigations": [
            ("TFA-M-1033", "Health Account Separation", "Unlink health and fitness accounts from shared or adversary-known accounts. Create new accounts with private credentials."),
            ("TFA-M-1034", "Fitness App Privacy Settings", "Disable public profiles, activity sharing, and social features on fitness platforms."),
            ("TFA-M-1035", "Wearable Device Reset", "Factory reset wearable devices and configure with sole-controlled account."),
        ],
        "detections": [
            ("TFA-D-1032", "Health Data Knowledge", "Adversary references exercise patterns, sleep data, health metrics, or location data from fitness tracking."),
            ("TFA-D-1033", "Active Health Data Sharing", "Audit reveals fitness or health apps sharing data with adversary's account."),
            ("TFA-D-1034", "Wearable Account Linkage", "Fitness tracker connected to adversary-controlled account."),
        ],
    },
    
    # ========================================================================
    # TACTIC 2: Account & Access Compromise (TFA-TA-0002)
    # ========================================================================
    
    "TFA-T-2001": {  # Credential Theft
        "mitigations": [
            ("TFA-M-2001", "Password Manager Deployment", "Use password manager with strong master password. Generate unique passwords for all accounts."),
            ("TFA-M-2002", "Multi-Factor Authentication", "Enable MFA on all accounts using authenticator app on secure device."),
            ("TFA-M-2003", "Credential Entry Security", "Use privacy screens. Avoid password entry where adversary can observe."),
            ("TFA-M-2004", "Post-Separation Credential Reset", "Change all passwords after separation, starting with email accounts."),
        ],
        "detections": [
            ("TFA-D-2001", "Unauthorised Access Alerts", "Login notifications from unrecognised devices or locations."),
            ("TFA-D-2002", "Account Lockout Events", "Unable to access accounts with previously valid credentials."),
            ("TFA-D-2003", "Account Content Knowledge", "Adversary demonstrates knowledge of account-specific content."),
        ],
    },
    
    "TFA-T-2002": {  # Account Takeover
        "mitigations": [
            ("TFA-M-2005", "Account Documentation", "Document all account details including usernames, associated contacts, and creation dates for recovery purposes."),
            ("TFA-M-2006", "Recovery Contact Security", "Change recovery email and phone to adversary-unknown contacts."),
            ("TFA-M-2007", "Platform Recovery Engagement", "Contact platform support for account recovery. Many platforms have DFV-specific recovery processes."),
        ],
        "detections": [
            ("TFA-D-2004", "Complete Account Lockout", "Unable to access accounts. Password reset attempts fail or redirect to unknown contacts."),
            ("TFA-D-2005", "Unauthorised Profile Changes", "Contacts report changes to profile content not made by account owner."),
            ("TFA-D-2006", "Recovery Option Modification", "Account recovery reveals changed backup contacts or security questions."),
        ],
    },
    
    "TFA-T-2003": {  # Password/Recovery Change
        "mitigations": [
            ("TFA-M-2008", "Multiple Recovery Methods", "Configure multiple recovery options so compromise of one does not eliminate account access."),
            ("TFA-M-2009", "Security Question Hardening", "Use fictitious answers to security questions that adversary cannot guess from personal knowledge."),
            ("TFA-M-2010", "Recovery Email Security", "Secure recovery email account with strong unique credentials and MFA."),
        ],
        "detections": [
            ("TFA-D-2007", "Unrequested Password Change Notifications", "Receiving confirmation of password or security changes not initiated by account owner."),
            ("TFA-D-2008", "Recovery Method Change Alerts", "Notifications of backup email, phone, or security question changes."),
        ],
    },
    
    "TFA-T-2004": {  # Session Hijacking
        "mitigations": [
            ("TFA-M-2011", "Active Session Monitoring", "Regularly review active sessions on all accounts. Terminate unrecognised sessions."),
            ("TFA-M-2012", "Session Termination", "Use 'sign out all sessions' feature after credential changes."),
        ],
        "detections": [
            ("TFA-D-2009", "Unknown Active Sessions", "Session review shows sign-ins from unrecognised devices or locations."),
            ("TFA-D-2010", "Unauthorised Account Activity", "Settings changed or content accessed without user action. Review platform activity logs."),
        ],
    },
    
    "TFA-T-2005": {  # Device Lockout
        "mitigations": [
            ("TFA-M-2013", "Remote Management Removal", "Remove device from adversary's Find My/Find My Device account."),
            ("TFA-M-2014", "Account Migration", "Migrate device to sole-controlled Apple ID or Google account. Factory reset if required."),
        ],
        "detections": [
            ("TFA-D-2011", "Remote Lock Activation", "Device displays lock screen or lost mode message without user action."),
            ("TFA-D-2012", "Remote Wipe Execution", "Device factory resets without user initiation."),
        ],
    },
    
    "TFA-T-2006": {  # Two-Factor Interception
        "mitigations": [
            ("TFA-M-2015", "Authenticator App Security", "Use authenticator app on secure device rather than SMS-based 2FA."),
            ("TFA-M-2016", "SIM Security Controls", "Contact carrier to add SIM lock PIN and port-out protection."),
            ("TFA-M-2017", "Hardware Security Key", "Use hardware security key for highest-risk accounts."),
        ],
        "detections": [
            ("TFA-D-2013", "SIM Swap Indicators", "Sudden loss of mobile service may indicate SIM swap attack."),
            ("TFA-D-2014", "Unrequested 2FA Codes", "Receiving 2FA codes without initiating login attempts."),
        ],
    },
    
    "TFA-T-2007": {  # Backup/Cloud Access
        "mitigations": [
            ("TFA-M-2018", "Cloud Account Security", "Change passwords and enable MFA on cloud storage. Review and remove sharing permissions."),
            ("TFA-M-2019", "Backup Encryption", "Enable encrypted backups where available."),
        ],
        "detections": [
            ("TFA-D-2015", "Cloud Access Alerts", "Sign-in alerts for cloud services from unfamiliar devices or locations."),
            ("TFA-D-2016", "Cloud Content Knowledge", "Adversary demonstrates knowledge of cloud-only content."),
        ],
    },
    
    "TFA-T-2008": {  # Shared Account Weaponization
        "mitigations": [
            ("TFA-M-2020", "Shared Account Separation", "Systematically separate shared accounts for streaming, utilities, and subscriptions."),
            ("TFA-M-2021", "Shared Account Documentation", "Document all shared account details before separation."),
        ],
        "detections": [
            ("TFA-D-2017", "Shared Service Disruption", "Shared services cancelled, passwords changed, or access revoked without discussion."),
            ("TFA-D-2018", "Weaponized Account Activity", "Adversary uses shared account access to monitor activity or make changes as control mechanism."),
        ],
    },
    
    "TFA-T-2009": {  # Device Sabotage
        "mitigations": [
            ("TFA-M-2022", "Data Backup Protocol", "Maintain regular backups to adversary-inaccessible storage."),
            ("TFA-M-2023", "Physical Device Security", "Maintain physical control of devices. Store evidence in secure cloud storage."),
        ],
        "detections": [
            ("TFA-D-2019", "Unexplained Data Loss", "Files, photos, or messages disappearing without user action."),
            ("TFA-D-2020", "Device Damage or Reset", "Devices physically damaged or factory reset during adversary access periods."),
        ],
    },
    
    "TFA-T-2010": {  # Administrative Access Abuse
        "mitigations": [
            ("TFA-M-2024", "Administrative Control Removal", "Remove parental control software and MDM profiles. Factory reset if removal not possible."),
            ("TFA-M-2025", "Family Group Exit", "Leave family sharing groups that grant adversary administrative control."),
        ],
        "detections": [
            ("TFA-D-2021", "Unexpected Device Restrictions", "Apps blocked, websites inaccessible, or features limited by parental controls not installed by user."),
            ("TFA-D-2022", "Usage Reports to Adversary", "Screen Time or similar tools sending activity reports to adversary's account."),
        ],
    },
    
    # ========================================================================
    # TACTIC 3: Harassment & Intimidation (TFA-TA-0003)
    # ========================================================================
    
    "TFA-T-3001": {  # Direct Threat Messaging
        "mitigations": [
            ("TFA-M-3001", "Evidence Preservation", "Screenshot and save all threatening messages with timestamps and sender details."),
            ("TFA-M-3002", "Platform and Law Enforcement Reporting", "Report threats to platform and police. Preserve evidence for legal proceedings."),
            ("TFA-M-3003", "Communication Boundary Enforcement", "Establish communication boundaries. Block on platforms where no legitimate contact required."),
        ],
        "detections": [
            ("TFA-D-3001", "Threatening Content Receipt", "Messages containing explicit or implicit threats of harm or adverse consequences."),
            ("TFA-D-3002", "Escalation Pattern", "Message tone becoming increasingly aggressive or menacing over time."),
        ],
    },
    
    "TFA-T-3002": {  # Persistent Unwanted Contact
        "mitigations": [
            ("TFA-M-3004", "Contact Documentation", "Maintain log of all unwanted contact with dates, times, platforms, and content."),
            ("TFA-M-3005", "Block and Filter Strategy", "Block adversary on all platforms. Configure email filters to archive messages for evidence."),
            ("TFA-M-3006", "Carrier Harassment Report", "Contact phone carrier to report harassment and implement call blocking."),
        ],
        "detections": [
            ("TFA-D-3003", "High Volume Contact", "Unreasonable number of contact attempts across channels."),
            ("TFA-D-3004", "Multi-Platform Contact Pattern", "Simultaneous contact attempts across multiple platforms."),
        ],
    },
    
    "TFA-T-3003": {  # Contact After Blocking
        "mitigations": [
            ("TFA-M-3007", "Multi-Platform Block Maintenance", "Maintain blocks across platforms. Enable unknown sender filtering."),
            ("TFA-M-3008", "Ban Evasion Reporting", "Report new accounts to platforms for ban evasion."),
        ],
        "detections": [
            ("TFA-D-3005", "New Accounts with Adversary Indicators", "New accounts using familiar language patterns or referencing personal details."),
            ("TFA-D-3006", "Alternative Channel Contact", "Contact via channels not previously used after blocking on primary platforms."),
        ],
    },
    
    "TFA-T-3004": {  # Coordinated Harassment Campaign
        "mitigations": [
            ("TFA-M-3009", "Mass Block and Report", "Block and report all participating accounts. Report coordinated harassment pattern to platform."),
            ("TFA-M-3010", "Temporary Account Restriction", "Temporarily restrict account access and disable comments during active campaign."),
            ("TFA-M-3011", "Regulatory Body Report", "Report serious coordinated harassment to eSafety Commissioner or equivalent body."),
        ],
        "detections": [
            ("TFA-D-3007", "Hostile Interaction Spike", "Rapid increase in negative interactions from multiple accounts."),
            ("TFA-D-3008", "Coordination Indicators", "Multiple accounts using similar language, talking points, or hashtags."),
        ],
    },
    
    "TFA-T-3005": {  # Doxxing
        "mitigations": [
            ("TFA-M-3012", "Personal Information Minimisation", "Audit and remove personal information from public sources. Opt out of data broker sites."),
            ("TFA-M-3013", "Address and Contact Protection", "Use PO Box for mail. Register domains with privacy protection."),
            ("TFA-M-3014", "Doxxing Response Protocol", "If doxxed: report to police, request content removal, alert workplace, document everything."),
        ],
        "detections": [
            ("TFA-D-3009", "Personal Information Published", "Private information appears on public platforms."),
            ("TFA-D-3010", "Stranger Harassment Based on Published Details", "Contact from unknown individuals referencing doxxed information."),
        ],
    },
    
    "TFA-T-3006": {  # Swatting
        "mitigations": [
            ("TFA-M-3015", "Law Enforcement Notification", "Notify local police of false report risk. Request address flagging in dispatch system."),
            ("TFA-M-3016", "Emergency Response Preparation", "Prepare for calm interaction with emergency services. Brief household members."),
        ],
        "detections": [
            ("TFA-D-3011", "Unexpected Emergency Response", "Emergency services arrive in response to unrequested call."),
            ("TFA-D-3012", "False Report Pattern", "Multiple false reports correlating with relationship events."),
        ],
    },
    
    "TFA-T-3007": {  # Platform Abuse Reporting
        "mitigations": [
            ("TFA-M-3017", "Content Backup", "Regularly backup social media content using platform export tools."),
            ("TFA-M-3018", "Appeal Process Utilisation", "Appeal account restrictions with context about weaponised reporting pattern."),
        ],
        "detections": [
            ("TFA-D-3013", "Unjustified Account Restrictions", "Content removed or account restricted for non-violating posts during conflict periods."),
            ("TFA-D-3014", "Multiple Report Indicators", "Platform communications indicating multiple reports against account."),
        ],
    },
    
    "TFA-T-3008": {  # Public Humiliation Posts
        "mitigations": [
            ("TFA-M-3019", "Content Removal Request", "Report humiliating content to platform. Report to regulatory body for serious content."),
            ("TFA-M-3020", "Search Result Management", "Request deindexing of harmful content. Create positive content to influence search results."),
        ],
        "detections": [
            ("TFA-D-3015", "Harmful Content Discovery", "Posts containing embarrassing or private content about target."),
            ("TFA-D-3016", "Third-Party Content Alerts", "Contacts report encountering harmful content online."),
        ],
    },
    
    "TFA-T-3009": {  # Impersonation Harassment
        "mitigations": [
            ("TFA-M-3021", "Impersonation Reporting", "Report fake accounts to platform using impersonation reporting process."),
            ("TFA-M-3022", "Network Notification", "Inform contacts of fake accounts and request verification through trusted channels."),
        ],
        "detections": [
            ("TFA-D-3017", "Contact Reports of Impersonation Messages", "Contacts report receiving messages from accounts impersonating target."),
            ("TFA-D-3018", "Fake Account Discovery", "Profiles using target's name, photos, or information discovered."),
        ],
    },
    
    "TFA-T-3010": {  # Review/Rating Attacks
        "mitigations": [
            ("TFA-M-3023", "False Review Dispute", "Flag false reviews for removal. Provide evidence of fraudulent origin."),
            ("TFA-M-3024", "Review Response Strategy", "Respond professionally to false reviews. Request genuine client reviews to counterbalance."),
        ],
        "detections": [
            ("TFA-D-3019", "Fraudulent Review Pattern", "Negative reviews from non-genuine accounts correlating with conflict events."),
            ("TFA-D-3020", "Professional Impact", "Decline in business correlating with review attack."),
        ],
    },
    
    "TFA-T-3011": {  # Contact Bombing
        "mitigations": [
            ("TFA-M-3025", "Email Filtering", "Configure email filtering to manage volume. Unsubscribe from spam subscriptions."),
            ("TFA-M-3026", "Communication Channel Protection", "Consider temporary contact change while maintaining bombarded accounts for evidence."),
        ],
        "detections": [
            ("TFA-D-3021", "Spam Volume Spike", "Dramatic increase in spam, subscriptions, or marketing messages."),
            ("TFA-D-3022", "Unrequested Sign-Up Confirmations", "Confirmation emails from services never subscribed to."),
        ],
    },
    
    "TFA-T-3012": {  # Proxy Harassment via AI
        "mitigations": [
            ("TFA-M-3027", "AI Content Detection", "Use AI detection tools to identify synthetic content for evidence purposes."),
            ("TFA-M-3028", "Platform-Level Reporting", "Report automated abuse patterns to platforms rather than responding to individual items."),
        ],
        "detections": [
            ("TFA-D-3023", "Synthetic Language Patterns", "Messages that are formulaic, vary slightly while making same points, or arrive at unrealistic volumes."),
            ("TFA-D-3024", "AI-Generated Media Indicators", "Media with artifacts characteristic of synthetic generation."),
        ],
    },
    
    # ========================================================================
    # TACTIC 4: Information Manipulation (TFA-TA-0004)
    # ========================================================================
    
    "TFA-T-4001": {  # Message/Evidence Tampering
        "mitigations": [
            ("TFA-M-4001", "Original Record Preservation", "Preserve original communications using platform export tools with metadata."),
            ("TFA-M-4002", "Metadata Verification", "Use platform records with headers and metadata rather than screenshots for evidence."),
            ("TFA-M-4003", "Witness Communication", "Include trusted witness in important communications for corroboration."),
        ],
        "detections": [
            ("TFA-D-4001", "Evidence Discrepancies", "Adversary-presented records don't match target's records of same communication."),
            ("TFA-D-4002", "Message Alteration", "Messages deleted or content changed from what target recalls."),
        ],
    },
    
    "TFA-T-4002": {  # Digital Gaslighting
        "mitigations": [
            ("TFA-M-4004", "Digital State Documentation", "Screenshot settings and configurations to establish baseline. Log device states to detect changes."),
            ("TFA-M-4005", "External Verification", "Verify noticed changes with trusted person before doubting own perception."),
            ("TFA-M-4006", "Version History Monitoring", "Enable and check version history on shared documents to detect manipulation."),
        ],
        "detections": [
            ("TFA-D-4003", "Unexplained Setting Changes", "Device settings or file locations changed without user action. Check modification timestamps."),
            ("TFA-D-4004", "Reality Questioning Pattern", "Increasing self-doubt about digital actions aligning with adversary's claims."),
        ],
    },
    
    "TFA-T-4003": {  # Non-Consensual Intimate Image Distribution (NCII)
        "mitigations": [
            ("TFA-M-4007", "Regulatory Body Report", "Report NCII to eSafety Commissioner or equivalent body with legal content removal powers."),
            ("TFA-M-4008", "Hash-Based Prevention Registration", "Register images with StopNCII.org to prevent re-upload on participating platforms."),
            ("TFA-M-4009", "Law Enforcement Report", "Report to police. NCII is criminal offence in most jurisdictions."),
        ],
        "detections": [
            ("TFA-D-4005", "Intimate Image Distribution Discovery", "Intimate images found on public platforms or reported by contacts."),
            ("TFA-D-4006", "Distribution Threats", "Adversary threatens to share intimate images as leverage."),
        ],
    },
    
    "TFA-T-4004": {  # Deepfake Creation
        "mitigations": [
            ("TFA-M-4010", "Synthetic Content Reporting", "Report deepfake intimate content to regulatory body and police. Deepfakes treated equivalently to real NCII."),
            ("TFA-M-4011", "Source Image Restriction", "Restrict access to facial photos on social media to limit deepfake source material."),
        ],
        "detections": [
            ("TFA-D-4007", "Synthetic Content Discovery", "Intimate content surfaces that depicts events that never occurred. May show AI artifacts on close inspection."),
            ("TFA-D-4008", "Fabricated Content Threats", "Adversary threatens distribution of content depicting situations that never happened."),
        ],
    },
    
    "TFA-T-4005": {  # False Narrative Campaigns
        "mitigations": [
            ("TFA-M-4012", "Counter-Narrative Development", "Develop response strategy with support services. Share truth selectively with key contacts."),
            ("TFA-M-4013", "False Claim Documentation", "Document each false claim with evidence contradicting it for legal proceedings."),
        ],
        "detections": [
            ("TFA-D-4009", "Unexplained Relationship Changes", "Contacts becoming distant without clear reason based on adversary communications."),
            ("TFA-D-4010", "False Information Reports", "Trusted individuals report false information being shared by adversary."),
        ],
    },
    
    "TFA-T-4006": {  # Context Manipulation
        "mitigations": [
            ("TFA-M-4014", "Full Context Preservation", "Preserve complete communication threads and surrounding context."),
            ("TFA-M-4015", "Written Communication Preference", "Conduct important discussions in writing on platforms maintaining complete records."),
        ],
        "detections": [
            ("TFA-D-4011", "Decontextualised Content Sharing", "Adversary shares real but misleading content stripped of surrounding context."),
            ("TFA-D-4012", "Partial Truth Accusations", "Third parties confront target about statements that are technically real but misleading without context."),
        ],
    },
    
    "TFA-T-4007": {  # Sextortion
        "mitigations": [
            ("TFA-M-4016", "Non-Compliance", "Do not comply with demands. Compliance typically leads to escalating demands."),
            ("TFA-M-4017", "Specialist Support Engagement", "Contact regulatory body and law enforcement sextortion support resources."),
        ],
        "detections": [
            ("TFA-D-4013", "Extortion Demands", "Messages demanding money or compliance in exchange for not distributing intimate content."),
            ("TFA-D-4014", "Demand Escalation", "Increased demands following initial compliance."),
        ],
    },
    
    "TFA-T-4008": {  # Catfishing/Romance Fraud
        "mitigations": [
            ("TFA-M-4018", "Identity Verification", "Verify online relationship identity through video calls and reverse image search before trust development."),
            ("TFA-M-4019", "Financial Boundary Enforcement", "Never send money or financial information to online-only contacts."),
        ],
        "detections": [
            ("TFA-D-4015", "Verification Avoidance", "Person consistently avoids video calls or in-person meetings. Photos may belong to someone else."),
            ("TFA-D-4016", "Financial Request Escalation", "Increasingly urgent requests for financial assistance with compelling stories."),
        ],
    },
    
    "TFA-T-4009": {  # Reputation Destruction SEO
        "mitigations": [
            ("TFA-M-4020", "Search Result Monitoring", "Set up alerts for own name. Regular self-search to identify harmful content early."),
            ("TFA-M-4021", "Positive Content Creation", "Create professional content under own name to influence search results."),
            ("TFA-M-4022", "Legal Content Removal", "Seek legal advice about defamation action or court-ordered content removal."),
        ],
        "detections": [
            ("TFA-D-4017", "Harmful Search Results", "Name search reveals websites containing false or harmful content designed to rank highly."),
            ("TFA-D-4018", "Malicious Domain Registrations", "Websites registered using target's name containing harmful content."),
        ],
    },
    
    "TFA-T-4010": {  # Historical Content Weaponization
        "mitigations": [
            ("TFA-M-4023", "Historical Content Cleanup", "Review and restrict visibility of old content that could be weaponised."),
            ("TFA-M-4024", "Context Preparation", "Prepare contextual explanations for known historical content with support team."),
        ],
        "detections": [
            ("TFA-D-4019", "Old Content Resurfacing", "Historical content shared in new contexts timed to important events."),
            ("TFA-D-4020", "Content Archiving Activity", "Evidence adversary systematically archiving target's historical content."),
        ],
    },
    
    "TFA-T-4011": {  # Fake Evidence Creation
        "mitigations": [
            ("TFA-M-4025", "Digital Forensic Engagement", "Engage forensic specialist to analyse suspected fabricated evidence and provide expert testimony."),
            ("TFA-M-4026", "Platform Record Requests", "Request official platform records for critical communications. Harder to fabricate than screenshots."),
        ],
        "detections": [
            ("TFA-D-4021", "Evidence Inconsistent with Records", "Presented evidence doesn't match target's records or memory of events."),
            ("TFA-D-4022", "Metadata Inconsistencies", "Digital evidence contains impossible timestamps, missing metadata, or editing artifacts."),
        ],
    },
    
    # ========================================================================
    # TACTIC 5: Isolation & Control (TFA-TA-0005)
    # ========================================================================
    
    "TFA-T-5001": {  # Communication Interception & Response
        "mitigations": [
            ("TFA-M-5001", "Secure Communication Channel", "Use separate secure device for sensitive communications with support services."),
            ("TFA-M-5002", "Message Verification", "Verify directly with contacts if relationships deteriorate unexpectedly."),
        ],
        "detections": [
            ("TFA-D-5001", "Unauthorised Message Sending", "Contacts report receiving messages from target's accounts not sent by target."),
            ("TFA-D-5002", "Unexplained Relationship Deterioration", "Support relationships deteriorate without clear cause."),
        ],
    },
    
    "TFA-T-5002": {  # Contact Blocking/Filtering
        "mitigations": [
            ("TFA-M-5003", "Contact and Filter Audit", "Periodically check blocked contacts and email filter rules for unauthorised changes."),
            ("TFA-M-5004", "Alternative Contact Methods", "Maintain backup contact methods for key support people."),
        ],
        "detections": [
            ("TFA-D-5003", "Missing Inbound Communications", "Contacts report sending messages that were never received."),
            ("TFA-D-5004", "Unauthorised Blocked Contacts", "Contacts on blocked list that user did not block."),
        ],
    },
    
    "TFA-T-5003": {  # Social Media Control
        "mitigations": [
            ("TFA-M-5005", "Autonomy Assertion", "Recognise demands to control social media connections as controlling behaviour. Document demands."),
            ("TFA-M-5006", "Private Secondary Account", "Maintain separate private account for support connections if needed."),
        ],
        "detections": [
            ("TFA-D-5005", "Connection Control Demands", "Demands to unfriend specific people, restrict posting, or delete accounts."),
            ("TFA-D-5006", "Connection Monitoring", "Adversary comments on or confronts about social media connections and interactions."),
        ],
    },
    
    "TFA-T-5004": {  # Device Time/Access Restrictions
        "mitigations": [
            ("TFA-M-5007", "Parental Control Removal", "Remove parental controls from adult devices. Factory reset if removal not possible."),
            ("TFA-M-5008", "Secondary Device Access", "Maintain access to secondary device adversary cannot control."),
        ],
        "detections": [
            ("TFA-D-5007", "External Device Restrictions", "Device has time limits, app restrictions, or content filters not configured by user."),
            ("TFA-D-5008", "Resource Access Blocking", "Support websites, apps, or communication tools blocked at device or network level."),
        ],
    },
    
    "TFA-T-5005": {  # Network Poisoning
        "mitigations": [
            ("TFA-M-5009", "Support Network Communication", "Proactively inform key contacts about adversary's potential false information campaign."),
            ("TFA-M-5010", "Professional Support Briefing", "Ensure professionals (therapist, lawyer, caseworker) are aware adversary may contact them."),
        ],
        "detections": [
            ("TFA-D-5009", "Contact Attitude Changes", "Contacts suddenly withdrawing support or becoming hostile based on adversary communications."),
            ("TFA-D-5010", "Adversary Contact Reports", "Support people report adversary has contacted them."),
        ],
    },
    
    "TFA-T-5006": {  # Platform Banning Coordination
        "mitigations": [
            ("TFA-M-5011", "Ban Appeal with Context", "Appeal bans with context about coordinated reporting campaign."),
            ("TFA-M-5012", "Support Network Diversification", "Maintain connections across multiple platforms and in-person support."),
        ],
        "detections": [
            ("TFA-D-5011", "Unexplained Community Removal", "Banned from communities without clear policy violation."),
            ("TFA-D-5012", "Coordinated Reporting Evidence", "Community administrators report multiple reports received in short timeframe."),
        ],
    },
    
    "TFA-T-5007": {  # Communication Monitoring Disclosure
        "mitigations": [
            ("TFA-M-5013", "Monitoring Assumption Planning", "Use separate safe device for sensitive communications if monitoring disclosed."),
            ("TFA-M-5014", "Monitoring Capability Verification", "Have professional assess actual monitoring capability to calibrate response."),
        ],
        "detections": [
            ("TFA-D-5013", "Explicit Monitoring Claims", "Adversary states they can monitor communications, either as threat or demonstrated through knowledge."),
            ("TFA-D-5014", "Self-Censorship Behaviour", "Target stops seeking help or being honest in communications due to monitoring fear."),
        ],
    },
    
    "TFA-T-5008": {  # Support Resource Blocking
        "mitigations": [
            ("TFA-M-5015", "Alternative Resource Access", "Memorise key helpline numbers. Use mobile data or public computers to access blocked resources."),
            ("TFA-M-5016", "Network Blocking Bypass", "Use mobile data, change DNS settings, or use VPN to bypass network-level blocking."),
        ],
        "detections": [
            ("TFA-D-5015", "Support Website Inaccessibility", "Support resources inaccessible on home network but work on mobile data."),
            ("TFA-D-5016", "Support Contact Removal", "Helpline numbers or support bookmarks removed from devices without user action."),
        ],
    },
    
    "TFA-T-5009": {  # Identity Document Control
        "mitigations": [
            ("TFA-M-5017", "Document Duplication", "Obtain copies of critical identity documents. Store in adversary-inaccessible location."),
            ("TFA-M-5018", "Government Portal Security", "Secure access to government portals under sole-controlled credentials."),
        ],
        "detections": [
            ("TFA-D-5017", "Document Access Denial", "Cannot access digital identity documents due to adversary-controlled storage."),
            ("TFA-D-5018", "Document Relocation", "Digital documents moved, deleted, or password-protected without user action."),
        ],
    },
    
    "TFA-T-5010": {  # Email/Communication Rerouting
        "mitigations": [
            ("TFA-M-5019", "Forwarding Rule Audit", "Check email settings for unauthorised forwarding rules and filters."),
            ("TFA-M-5020", "Call Forwarding Check", "Check phone settings and carrier account for call forwarding configurations."),
        ],
        "detections": [
            ("TFA-D-5019", "Missing Expected Communications", "Emails, messages, or calls that senders confirm were sent but never received."),
            ("TFA-D-5020", "Forwarding Discovery", "Audit reveals email forwarding or call forwarding to unknown destinations."),
        ],
    },
    
    # ========================================================================
    # TACTIC 6: Resource & Financial Control (TFA-TA-0006)
    # ========================================================================
    
    "TFA-T-6001": {  # Financial Account Lockout
        "mitigations": [
            ("TFA-M-6001", "Financial Account Security Reset", "Change passwords, enable MFA, remove adversary as authorised user on individual accounts."),
            ("TFA-M-6002", "Financial Counselling", "Contact financial counsellor experienced in DFV situations for guidance."),
            ("TFA-M-6003", "Emergency Financial Access", "Maintain separate emergency fund in adversary-unknown account."),
        ],
        "detections": [
            ("TFA-D-6001", "Financial Account Lockout", "Unable to access financial accounts using previously valid credentials."),
            ("TFA-D-6002", "Authorised User Removal", "Notification of removal from shared financial accounts."),
        ],
    },
    
    "TFA-T-6002": {  # Transaction Monitoring
        "mitigations": [
            ("TFA-M-6004", "Separate Transaction Account", "Open individual account at different institution for sensitive transactions."),
            ("TFA-M-6005", "Untraceable Payment Methods", "Use cash or prepaid cards for purchases to keep private."),
        ],
        "detections": [
            ("TFA-D-6003", "Transaction Knowledge", "Adversary references specific purchases, amounts, or merchants from bank transactions."),
            ("TFA-D-6004", "Unauthorised Alert Configuration", "Transaction alerts configured to adversary's contact information."),
        ],
    },
    
    "TFA-T-6003": {  # Spending Restrictions
        "mitigations": [
            ("TFA-M-6006", "Independent Financial Access", "Establish independent financial access: personal account, credit card, superannuation access."),
            ("TFA-M-6007", "Legal Financial Advice", "Consult lawyer about financial rights and emergency relief options."),
        ],
        "detections": [
            ("TFA-D-6005", "Unexplained Transaction Declines", "Card declined despite available funds, or daily limits reduced without consent."),
            ("TFA-D-6006", "Spending Approval Requirements", "Spending limits or approval requirements enabled without user action."),
        ],
    },
    
    "TFA-T-6004": {  # Unauthorized Transactions
        "mitigations": [
            ("TFA-M-6008", "Transaction Alert Configuration", "Enable real-time transaction alerts on all financial accounts."),
            ("TFA-M-6009", "Fraud Reporting", "Report unauthorised transactions to financial institution and police."),
        ],
        "detections": [
            ("TFA-D-6007", "Unrecognised Transactions", "Transactions appearing on accounts not authorised by account holder."),
            ("TFA-D-6008", "Balance Discrepancies", "Account balances lower than expected or funds moved without knowledge."),
        ],
    },
    
    "TFA-T-6005": {  # Coerced Transactions
        "mitigations": [
            ("TFA-M-6010", "Coerced Debt Legal Advice", "Consult about coerced debt pathways. Debts incurred under duress may be dischargeable."),
            ("TFA-M-6011", "Coercion Documentation", "Document coercion circumstances for legal proceedings."),
        ],
        "detections": [
            ("TFA-D-6009", "Financial Coercion", "Threats, intimidation, or manipulation to make transactions or take on debt."),
            ("TFA-D-6010", "Duress Debt Accumulation", "Increasing debt from pressured financial decisions."),
        ],
    },
    
    "TFA-T-6006": {  # Crypto/Investment Fraud
        "mitigations": [
            ("TFA-M-6012", "Investment Verification", "Verify investment opportunities independently through regulatory body resources."),
            ("TFA-M-6013", "Fraud Reporting", "Report suspected investment fraud to consumer protection and cyber security agencies."),
        ],
        "detections": [
            ("TFA-D-6011", "Pressure to Invest in Unverified Platforms", "Urged to invest on unfamiliar platforms that cannot be independently verified."),
            ("TFA-D-6012", "Withdrawal Inability", "Invested funds cannot be withdrawn from platform."),
        ],
    },
    
    "TFA-T-6007": {  # Benefits/Payments Interception
        "mitigations": [
            ("TFA-M-6014", "Payment Destination Security", "Ensure all payments directed to sole-controlled account. Update payment details with agencies and employers."),
            ("TFA-M-6015", "Mail Redirection Check", "Verify no mail redirection configured without knowledge."),
        ],
        "detections": [
            ("TFA-D-6013", "Missing Expected Payments", "Government benefits, salary, or other payments not arriving in expected accounts."),
            ("TFA-D-6014", "Payment Detail Changes", "Direct deposit information changed without authorisation."),
        ],
    },
    
    "TFA-T-6008": {  # Credit/Identity Theft
        "mitigations": [
            ("TFA-M-6016", "Credit Monitoring", "Set up credit monitoring. Request credit reports from all reporting bodies."),
            ("TFA-M-6017", "Credit Ban", "Place credit ban to prevent new applications. Available free for DFV victims."),
            ("TFA-M-6018", "Identity Theft Report", "Report identity theft to national identity support service."),
        ],
        "detections": [
            ("TFA-D-6015", "Unknown Credit Activity", "Credit report shows accounts or enquiries not initiated by owner."),
            ("TFA-D-6016", "Unknown Service Bills", "Bills or collection notices for services never subscribed to."),
        ],
    },
    
    "TFA-T-6009": {  # Smart Home Resource Control
        "mitigations": [
            ("TFA-M-6019", "Smart Home Account Control", "Transfer all smart home device accounts to sole control. Factory reset and reconfigure."),
            ("TFA-M-6020", "Manual Override Capability", "Ensure manual overrides available for all smart home-controlled utilities."),
        ],
        "detections": [
            ("TFA-D-6017", "Remote Utility Control", "Heating, cooling, lighting, or locks changing without user action."),
            ("TFA-D-6018", "Manipulation-Reflective Utility Bills", "Unusual utility bills resulting from remote environmental manipulation."),
        ],
    },
    
    "TFA-T-6010": {  # Employment Sabotage
        "mitigations": [
            ("TFA-M-6021", "Employer Notification", "Inform employer about potential for adversary workplace contact if safe to do so."),
            ("TFA-M-6022", "Professional Account Security", "Secure professional accounts with strong credentials and MFA."),
        ],
        "detections": [
            ("TFA-D-6019", "Workplace Interference", "Employer or colleagues report contact from adversary about target."),
            ("TFA-D-6020", "Application Interference", "Job applications unsuccessful potentially due to adversary contact with prospective employers."),
        ],
    },
    
    "TFA-T-6011": {  # Subscription/Service Cancellation
        "mitigations": [
            ("TFA-M-6023", "Individual Account Registration", "Register essential services under own name and billing."),
            ("TFA-M-6024", "Service Provider DFV Support", "Request DFV support pathway from service providers for expedited account changes."),
        ],
        "detections": [
            ("TFA-D-6021", "Essential Service Cancellation", "Phone, internet, insurance, or utilities cancelled without knowledge or consent."),
            ("TFA-D-6022", "Unauthorised Service Changes", "Service plans modified or features removed without notification."),
        ],
    },
    
    # ========================================================================
    # TACTIC 7: Physical Enablement (TFA-TA-0007)
    # ========================================================================
    
    "TFA-T-7001": {  # Location-Based Assault
        "mitigations": [
            ("TFA-M-7001", "Comprehensive Location Security", "Disable all location sharing, remove trackers, secure location-revealing accounts, vary routines."),
            ("TFA-M-7002", "Safety Planning", "Develop comprehensive safety plan with support service addressing technology-enabled tracking."),
            ("TFA-M-7003", "Law Enforcement Report", "Report stalking and tracking to police. Apply for intervention order with technology-specific conditions."),
        ],
        "detections": [
            ("TFA-D-7001", "Location Interception", "Adversary appears at locations not disclosed to them."),
            ("TFA-D-7002", "Location-Referencing Threats", "Threats that reference specific location or recent movements."),
        ],
    },
    
    "TFA-T-7002": {  # Safe Location Disclosure
        "mitigations": [
            ("TFA-M-7004", "Safe Location Digital Hygiene", "Disable location services. Strip metadata from images. Avoid tagging safe location digitally."),
            ("TFA-M-7005", "Secure Communication from Safe Location", "Use new device and accounts. Only communicate location to those who must know via secure channels."),
        ],
        "detections": [
            ("TFA-D-7003", "Safe Location Discovery", "Adversary appears near or references safe location. Immediate safety emergency."),
            ("TFA-D-7004", "Photo Metadata Exposure", "Shared photos contain GPS coordinates revealing safe location."),
        ],
    },
    
    "TFA-T-7003": {  # Movement Interception
        "mitigations": [
            ("TFA-M-7006", "Route Variation", "Vary routes, departure times, and transport methods."),
            ("TFA-M-7007", "Appointment Security", "Keep appointments off monitored calendars. Arrange support person accompaniment."),
        ],
        "detections": [
            ("TFA-D-7005", "Route Interception", "Adversary appearing along travel route or at destinations."),
            ("TFA-D-7006", "Travel Knowledge Indicators", "Adversary demonstrates knowledge of travel plans before arrival."),
        ],
    },
    
    "TFA-T-7004": {  # Smart Lock Manipulation
        "mitigations": [
            ("TFA-M-7008", "Smart Lock Security Reset", "Change all smart lock credentials. Remove adversary access. Replace with traditional locks if needed."),
            ("TFA-M-7009", "Lock Replacement Post-Separation", "Change all locks after separation. Most jurisdictions require landlords to do this for DFV situations."),
        ],
        "detections": [
            ("TFA-D-7007", "Lock Behaviour Anomalies", "Smart locks engaging or disengaging unexpectedly. Access codes no longer working."),
            ("TFA-D-7008", "Physical Access Control", "Locked inside or outside home due to remote lock manipulation. Safety emergency."),
        ],
    },
    
    "TFA-T-7005": {  # Vehicle Sabotage
        "mitigations": [
            ("TFA-M-7010", "Connected Car Account Security", "Change connected car credentials. Remove adversary from vehicle account access."),
            ("TFA-M-7011", "Vehicle Safety Inspection", "Have mechanic inspect for tracking devices and tampering. Check OBD-II port."),
        ],
        "detections": [
            ("TFA-D-7009", "Remote Vehicle Control", "Vehicle functions activating without user action — horn, lights, locks, engine."),
            ("TFA-D-7010", "Connected Car Access Alerts", "Notifications showing adversary's device accessing vehicle features."),
        ],
    },
    
    "TFA-T-7006": {  # IoT Device Weaponization
        "mitigations": [
            ("TFA-M-7012", "IoT Device Audit and Reset", "Audit all smart home devices. Factory reset and reconfigure under sole-controlled account."),
            ("TFA-M-7013", "Network Security", "Change Wi-Fi passwords. Remove adversary access to router admin."),
        ],
        "detections": [
            ("TFA-D-7011", "Unexplained Device Activation", "Smart home devices activating without user command — alarms, lights, speakers, TV."),
            ("TFA-D-7012", "Environmental Manipulation", "Temperature or comfort settings changed remotely to create discomfort."),
        ],
    },
    
    "TFA-T-7007": {  # Medical Device Interference
        "mitigations": [
            ("TFA-M-7014", "Medical Device Security Review", "Inform healthcare provider of DFV situation. Request security review of connected medical devices."),
            ("TFA-M-7015", "Health Record Access Control", "Restrict health record access. Change patient portal credentials. Remove adversary as authorised contact."),
        ],
        "detections": [
            ("TFA-D-7013", "Medical Device Setting Changes", "Connected medical device settings changed without user action. Contact healthcare provider immediately."),
            ("TFA-D-7014", "Health Data Access Indicators", "Adversary demonstrates knowledge of health information they should not have access to."),
        ],
    },
    
    "TFA-T-7008": {  # Stalking Coordination
        "mitigations": [
            ("TFA-M-7016", "Anti-Stalking Strategy", "Develop comprehensive anti-stalking safety plan with police and support service."),
            ("TFA-M-7017", "Stalking Evidence Documentation", "Maintain detailed stalking log documenting every incident. Use stalking documentation tools."),
        ],
        "detections": [
            ("TFA-D-7015", "Repeated Unexplained Appearances", "Adversary repeatedly appears at different locations at varied times."),
            ("TFA-D-7016", "Coordinated Surveillance Evidence", "Evidence adversary involved others in surveillance or uses multiple tracking methods."),
        ],
    },
    
    "TFA-T-7009": {  # Emergency Service Manipulation
        "mitigations": [
            ("TFA-M-7018", "Law Enforcement False Report Briefing", "Inform police of false report risk. Request address flagging."),
            ("TFA-M-7019", "False Report Legal Response", "Report false emergency calls as criminal offences. Gather evidence reports are fabricated."),
        ],
        "detections": [
            ("TFA-D-7017", "Unrequested Authority Visits", "Authorities arrive based on reports not made by target."),
            ("TFA-D-7018", "False Report Pattern", "Learning false reports filed against target by adversary or associates."),
        ],
    },
    
    "TFA-T-7010": {  # Child Custody Tech Abuse
        "mitigations": [
            ("TFA-M-7020", "Co-Parenting App Boundaries", "Use court-approved co-parenting apps for documented communication."),
            ("TFA-M-7021", "Children's Device Security", "Audit children's devices for monitoring. Manage parental controls."),
            ("TFA-M-7022", "Legal Tech Abuse Documentation", "Document technology abuse through custody arrangements for family court."),
        ],
        "detections": [
            ("TFA-D-7019", "Excessive Location Monitoring", "Adversary checking children's location more than reasonably required."),
            ("TFA-D-7020", "Co-Parenting App Misuse", "Co-parenting apps used for hostile messages rather than genuine co-parenting."),
            ("TFA-D-7021", "Children's Device Surveillance", "Monitoring software on children's devices enabling household surveillance."),
        ],
    },
}
