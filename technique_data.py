TECHNIQUE_DATA = {
    # ========================================================================
    # TACTIC 1: Surveillance & Tracking (SAFE-TA-0001)
    # ========================================================================
    
    "SAFE-T-0072": {  # Stalkerware Installation
        "mitigations": [
            ("SAFE-M-0001", "Anti-Stalkerware Scanning", "Deploy anti-stalkerware detection tools to identify monitoring applications. Scan for apps with excessive permissions including location, microphone, camera, and message access."),
            ("SAFE-M-0002", "Device Access Controls", "Implement strong device authentication. Disable installation from unknown sources. Maintain physical control of devices."),
            ("SAFE-M-0003", "Safe Device Acquisition", "Obtain a separate device for sensitive communications if stalkerware is suspected. Removing stalkerware may alert the monitoring party."),
            ("SAFE-M-0004", "Operating System Hardening", "Maintain current OS versions. Security updates frequently patch vulnerabilities exploited by stalkerware."),
            ("SAFE-M-0005", "Forensic Device Audit", "Engage professional forensic analysis to identify monitoring software and preserve evidence."),
        ],
        "detections": [
            ("SAFE-D-0001", "Anomalous Battery Consumption", "Device battery depletes faster than baseline due to continuous background data transmission."),
            ("SAFE-D-0002", "Unexplained Data Usage", "Increased mobile data consumption without corresponding user activity. Monitor per-app data usage for unknown processes."),
            ("SAFE-D-0003", "Device Temperature Anomalies", "Device runs hot during idle periods indicating background process activity."),
            ("SAFE-D-0004", "Information Leakage Indicators", "Adversary demonstrates knowledge of private communications, locations, or activities accessible only through device monitoring."),
            ("SAFE-D-0005", "Unknown Applications or Profiles", "Presence of unrecognised apps, device administrator privileges, or configuration profiles."),
        ],
    },
    
    "SAFE-T-0073": {  # Physical Tracker Planting
        "mitigations": [
            ("SAFE-M-0006", "Bluetooth Tracker Detection", "Use tracker detection applications to scan for nearby Bluetooth tracking devices. Enable platform-native unknown tracker alerts."),
            ("SAFE-M-0007", "Physical Vehicle Inspection", "Conduct systematic inspection of vehicles for GPS tracking devices in common concealment locations."),
            ("SAFE-M-0008", "Belongings Audit", "Inspect bags, clothing, and frequently carried items for concealed tracking devices."),
            ("SAFE-M-0009", "Evidence Preservation Protocol", "If tracker discovered, document location and preserve for evidence before removal. Removal alerts monitoring party."),
        ],
        "detections": [
            ("SAFE-D-0006", "Platform Tracker Alerts", "Device displays alerts for unknown tracking devices travelling with user."),
            ("SAFE-D-0007", "Location Knowledge Indicators", "Adversary references specific locations, routes, or timing not disclosed by target."),
            ("SAFE-D-0008", "Physical Device Discovery", "Small electronic device found attached to vehicle or concealed in belongings."),
            ("SAFE-D-0009", "Audible Tracker Indicators", "Periodic beeping from unknown source in belongings or vehicle."),
        ],
    },
    
    "SAFE-T-0074": {  # Shared Account Surveillance
        "mitigations": [
            ("SAFE-M-0010", "Location Sharing Audit", "Review all location sharing configurations across devices and services. Disable unauthorised sharing."),
            ("SAFE-M-0011", "Account Separation", "Migrate to individual accounts for services previously shared. Use new credentials unknown to adversary."),
            ("SAFE-M-0012", "Carrier Account Review", "Assess family phone plan features that expose location or usage data. Plan migration to individual account."),
        ],
        "detections": [
            ("SAFE-D-0010", "Shared Account Data References", "Adversary references location, purchases, or activities visible through shared account access."),
            ("SAFE-D-0011", "Active Location Sharing Discovery", "Audit reveals location sharing enabled with adversary's account."),
            ("SAFE-D-0012", "Unknown Devices on Shared Accounts", "Unrecognised devices listed in shared account trusted device lists."),
        ],
    },
    
    "SAFE-T-0075": {  # Social Media Monitoring
        "mitigations": [
            ("SAFE-M-0013", "Privacy Configuration Hardening", "Configure maximum privacy settings on all social media platforms. Restrict visibility of posts, connections, and activity."),
            ("SAFE-M-0014", "Connection Audit", "Review all followers and connections for adversary-controlled accounts. Remove suspicious connections."),
            ("SAFE-M-0015", "Information Disclosure Controls", "Avoid posting real-time locations, routines, or future plans. Delay posting until after events conclude."),
            ("SAFE-M-0016", "Tag and Mention Restrictions", "Disable or require approval for tags and mentions to prevent third-party location disclosure."),
        ],
        "detections": [
            ("SAFE-D-0013", "Non-Public Activity Knowledge", "Adversary references social media activity that should not be visible given current privacy settings."),
            ("SAFE-D-0014", "Suspicious Account Patterns", "New follower accounts created recently with minimal activity or connections to adversary's network."),
            ("SAFE-D-0015", "Third-Party Monitoring Reports", "Contacts report adversary has shown them target's social media content or asked about online activity."),
        ],
    },
    
    "SAFE-T-0076": {  # Communication Interception
        "mitigations": [
            ("SAFE-M-0017", "Email Rule Audit", "Check email settings for unauthorised forwarding rules and filters. Remove rules forwarding to unknown addresses."),
            ("SAFE-M-0018", "Linked Device Review", "Review and remove unrecognised devices linked to messaging accounts."),
            ("SAFE-M-0019", "Encrypted Communications", "Use end-to-end encrypted messaging for sensitive communications. Ensure adversary cannot access linked devices."),
            ("SAFE-M-0020", "Voicemail Security", "Change voicemail PIN. Disable remote voicemail access where possible."),
        ],
        "detections": [
            ("SAFE-D-0016", "Read Receipt Anomalies", "Messages marked as read before target has viewed them. Account shows online status during non-use periods."),
            ("SAFE-D-0017", "Unauthorised Forwarding Rules", "Email settings contain forwarding rules to unknown addresses or filters moving messages automatically."),
            ("SAFE-D-0018", "Unknown Linked Devices", "Messaging app settings show unrecognised devices with active sessions."),
            ("SAFE-D-0019", "Communication Content Knowledge", "Adversary quotes or references private message content."),
        ],
    },
    
    "SAFE-T-0077": {  # Smart Home Surveillance
        "mitigations": [
            ("SAFE-M-0021", "Smart Home Account Takeover", "Transfer device ownership to sole-controlled account. Factory reset devices and reconfigure with new credentials."),
            ("SAFE-M-0022", "Recording Device Audit", "Identify all cameras, microphones, and recording-capable devices. Disable or remove devices that cannot be secured."),
            ("SAFE-M-0023", "Voice Assistant Hardening", "Disable remote access features, drop-in capabilities, and voice purchasing. Delete stored recordings."),
        ],
        "detections": [
            ("SAFE-D-0020", "In-Home Activity Knowledge", "Adversary references conversations or activities that occurred inside the home."),
            ("SAFE-D-0021", "Device Behaviour Anomalies", "Cameras activating, indicator lights engaging, or voice assistants responding without user trigger."),
            ("SAFE-D-0022", "Unauthorised Device Access", "Smart home app settings show adversary account retains admin or viewer access."),
        ],
    },
    
    "SAFE-T-0078": {  # Network Traffic Monitoring
        "mitigations": [
            ("SAFE-M-0024", "Router Credential Reset", "Change router admin credentials. Factory reset router if adversary configured it."),
            ("SAFE-M-0025", "Traffic Encryption", "Use VPN to encrypt internet traffic and prevent network-level monitoring."),
            ("SAFE-M-0026", "Network Bypass", "Use mobile data instead of home network for sensitive browsing."),
        ],
        "detections": [
            ("SAFE-D-0023", "Browsing Activity Knowledge", "Adversary references websites visited or searches performed."),
            ("SAFE-D-0024", "Unauthorised Network Controls", "Router contains parental controls, content filtering, or logging not configured by target."),
            ("SAFE-D-0025", "Network Monitoring Tools Present", "Discovery of network monitoring software or devices on home network."),
        ],
    },
    
    "SAFE-T-0079": {  # Calendar/Schedule Surveillance
        "mitigations": [
            ("SAFE-M-0027", "Calendar Sharing Audit", "Review and remove unauthorised calendar sharing permissions across all calendar applications."),
            ("SAFE-M-0028", "Sensitive Appointment Isolation", "Use separate calendar on adversary-unknown account for sensitive appointments."),
            ("SAFE-M-0029", "Medical Portal Security", "Change credentials on health portals. Remove adversary as authorised contact."),
        ],
        "detections": [
            ("SAFE-D-0026", "Appointment Interception", "Adversary appears at calendar events they should not know about."),
            ("SAFE-D-0027", "Schedule Knowledge Indicators", "Adversary references upcoming appointments before disclosure."),
            ("SAFE-D-0028", "Active Calendar Sharing", "Audit reveals adversary retains calendar viewing access."),
        ],
    },
    
    "SAFE-T-0080": {  # Third-Party Monitoring Recruitment
        "mitigations": [
            ("SAFE-M-0030", "Information Compartmentalisation", "Limit sensitive information shared with contacts who maintain relationship with adversary."),
            ("SAFE-M-0031", "Network Trust Assessment", "Identify which contacts may relay information to adversary based on information leakage patterns."),
            ("SAFE-M-0032", "Canary Information Testing", "Share unique details with specific contacts to identify information relay sources."),
        ],
        "detections": [
            ("SAFE-D-0029", "Source-Specific Information Leakage", "Adversary gains knowledge of information shared only with specific individuals."),
            ("SAFE-D-0030", "Unusual Contact Questioning", "Contacts ask unusually specific questions about location, plans, or relationships."),
            ("SAFE-D-0031", "Recruitment Attempt Reports", "Trusted contacts report adversary has requested information about target."),
        ],
    },
    
    "SAFE-T-0081": {  # Fitness/Health Tracker Surveillance
        "mitigations": [
            ("SAFE-M-0033", "Health Account Separation", "Unlink health and fitness accounts from shared or adversary-known accounts. Create new accounts with private credentials."),
            ("SAFE-M-0034", "Fitness App Privacy Settings", "Disable public profiles, activity sharing, and social features on fitness platforms."),
            ("SAFE-M-0035", "Wearable Device Reset", "Factory reset wearable devices and configure with sole-controlled account."),
        ],
        "detections": [
            ("SAFE-D-0032", "Health Data Knowledge", "Adversary references exercise patterns, sleep data, health metrics, or location data from fitness tracking."),
            ("SAFE-D-0033", "Active Health Data Sharing", "Audit reveals fitness or health apps sharing data with adversary's account."),
            ("SAFE-D-0034", "Wearable Account Linkage", "Fitness tracker connected to adversary-controlled account."),
        ],
    },
    
    # ========================================================================
    # TACTIC 2: Account & Access Compromise (SAFE-TA-0002)
    # ========================================================================
    
    "SAFE-T-0082": {  # Credential Theft
        "mitigations": [
            ("SAFE-M-0036", "Password Manager Deployment", "Use password manager with strong master password. Generate unique passwords for all accounts."),
            ("SAFE-M-0037", "Multi-Factor Authentication", "Enable MFA on all accounts using authenticator app on secure device."),
            ("SAFE-M-0038", "Credential Entry Security", "Use privacy screens. Avoid password entry where adversary can observe."),
            ("SAFE-M-0039", "Post-Separation Credential Reset", "Change all passwords after separation, starting with email accounts."),
        ],
        "detections": [
            ("SAFE-D-0035", "Unauthorised Access Alerts", "Login notifications from unrecognised devices or locations."),
            ("SAFE-D-0036", "Account Lockout Events", "Unable to access accounts with previously valid credentials."),
            ("SAFE-D-0037", "Account Content Knowledge", "Adversary demonstrates knowledge of account-specific content."),
        ],
    },
    
    "SAFE-T-0083": {  # Account Takeover
        "mitigations": [
            ("SAFE-M-0040", "Account Documentation", "Document all account details including usernames, associated contacts, and creation dates for recovery purposes."),
            ("SAFE-M-0041", "Recovery Contact Security", "Change recovery email and phone to adversary-unknown contacts."),
            ("SAFE-M-0042", "Platform Recovery Engagement", "Contact platform support for account recovery. Many platforms have DFV-specific recovery processes."),
        ],
        "detections": [
            ("SAFE-D-0038", "Complete Account Lockout", "Unable to access accounts. Password reset attempts fail or redirect to unknown contacts."),
            ("SAFE-D-0039", "Unauthorised Profile Changes", "Contacts report changes to profile content not made by account owner."),
            ("SAFE-D-0040", "Recovery Option Modification", "Account recovery reveals changed backup contacts or security questions."),
        ],
    },
    
    "SAFE-T-0084": {  # Password/Recovery Change
        "mitigations": [
            ("SAFE-M-0043", "Multiple Recovery Methods", "Configure multiple recovery options so compromise of one does not eliminate account access."),
            ("SAFE-M-0044", "Security Question Hardening", "Use fictitious answers to security questions that adversary cannot guess from personal knowledge."),
            ("SAFE-M-0045", "Recovery Email Security", "Secure recovery email account with strong unique credentials and MFA."),
        ],
        "detections": [
            ("SAFE-D-0041", "Unrequested Password Change Notifications", "Receiving confirmation of password or security changes not initiated by account owner."),
            ("SAFE-D-0042", "Recovery Method Change Alerts", "Notifications of backup email, phone, or security question changes."),
        ],
    },
    
    "SAFE-T-0085": {  # Session Hijacking
        "mitigations": [
            ("SAFE-M-0046", "Active Session Monitoring", "Regularly review active sessions on all accounts. Terminate unrecognised sessions."),
            ("SAFE-M-0047", "Session Termination", "Use 'sign out all sessions' feature after credential changes."),
        ],
        "detections": [
            ("SAFE-D-0043", "Unknown Active Sessions", "Session review shows sign-ins from unrecognised devices or locations."),
            ("SAFE-D-0044", "Unauthorised Account Activity", "Settings changed or content accessed without user action. Review platform activity logs."),
        ],
    },
    
    "SAFE-T-0086": {  # Device Lockout
        "mitigations": [
            ("SAFE-M-0048", "Remote Management Removal", "Remove device from adversary's Find My/Find My Device account."),
            ("SAFE-M-0049", "Account Migration", "Migrate device to sole-controlled Apple ID or Google account. Factory reset if required."),
        ],
        "detections": [
            ("SAFE-D-0045", "Remote Lock Activation", "Device displays lock screen or lost mode message without user action."),
            ("SAFE-D-0046", "Remote Wipe Execution", "Device factory resets without user initiation."),
        ],
    },
    
    "SAFE-T-0087": {  # Two-Factor Interception
        "mitigations": [
            ("SAFE-M-0050", "Authenticator App Security", "Use authenticator app on secure device rather than SMS-based 2FA."),
            ("SAFE-M-0051", "SIM Security Controls", "Contact carrier to add SIM lock PIN and port-out protection."),
            ("SAFE-M-0052", "Hardware Security Key", "Use hardware security key for highest-risk accounts."),
        ],
        "detections": [
            ("SAFE-D-0047", "SIM Swap Indicators", "Sudden loss of mobile service may indicate SIM swap attack."),
            ("SAFE-D-0048", "Unrequested 2FA Codes", "Receiving 2FA codes without initiating login attempts."),
        ],
    },
    
    "SAFE-T-0088": {  # Backup/Cloud Access
        "mitigations": [
            ("SAFE-M-0053", "Cloud Account Security", "Change passwords and enable MFA on cloud storage. Review and remove sharing permissions."),
            ("SAFE-M-0054", "Backup Encryption", "Enable encrypted backups where available."),
        ],
        "detections": [
            ("SAFE-D-0049", "Cloud Access Alerts", "Sign-in alerts for cloud services from unfamiliar devices or locations."),
            ("SAFE-D-0050", "Cloud Content Knowledge", "Adversary demonstrates knowledge of cloud-only content."),
        ],
    },
    
    "SAFE-T-0089": {  # Shared Account Weaponization
        "mitigations": [
            ("SAFE-M-0055", "Shared Account Separation", "Systematically separate shared accounts for streaming, utilities, and subscriptions."),
            ("SAFE-M-0056", "Shared Account Documentation", "Document all shared account details before separation."),
        ],
        "detections": [
            ("SAFE-D-0051", "Shared Service Disruption", "Shared services cancelled, passwords changed, or access revoked without discussion."),
            ("SAFE-D-0052", "Weaponized Account Activity", "Adversary uses shared account access to monitor activity or make changes as control mechanism."),
        ],
    },
    
    "SAFE-T-0090": {  # Device Sabotage
        "mitigations": [
            ("SAFE-M-0057", "Data Backup Protocol", "Maintain regular backups to adversary-inaccessible storage."),
            ("SAFE-M-0058", "Physical Device Security", "Maintain physical control of devices. Store evidence in secure cloud storage."),
        ],
        "detections": [
            ("SAFE-D-0053", "Unexplained Data Loss", "Files, photos, or messages disappearing without user action."),
            ("SAFE-D-0054", "Device Damage or Reset", "Devices physically damaged or factory reset during adversary access periods."),
        ],
    },
    
    "SAFE-T-0091": {  # Administrative Access Abuse
        "mitigations": [
            ("SAFE-M-0059", "Administrative Control Removal", "Remove parental control software and MDM profiles. Factory reset if removal not possible."),
            ("SAFE-M-0060", "Family Group Exit", "Leave family sharing groups that grant adversary administrative control."),
        ],
        "detections": [
            ("SAFE-D-0055", "Unexpected Device Restrictions", "Apps blocked, websites inaccessible, or features limited by parental controls not installed by user."),
            ("SAFE-D-0056", "Usage Reports to Adversary", "Screen Time or similar tools sending activity reports to adversary's account."),
        ],
    },
    
    # ========================================================================
    # TACTIC 3: Harassment & Intimidation (SAFE-TA-0003)
    # ========================================================================
    
    "SAFE-T-0092": {  # Direct Threat Messaging
        "mitigations": [
            ("SAFE-M-0061", "Evidence Preservation", "Screenshot and save all threatening messages with timestamps and sender details."),
            ("SAFE-M-0062", "Platform and Law Enforcement Reporting", "Report threats to platform and police. Preserve evidence for legal proceedings."),
            ("SAFE-M-0063", "Communication Boundary Enforcement", "Establish communication boundaries. Block on platforms where no legitimate contact required."),
        ],
        "detections": [
            ("SAFE-D-0057", "Threatening Content Receipt", "Messages containing explicit or implicit threats of harm or adverse consequences."),
            ("SAFE-D-0058", "Escalation Pattern", "Message tone becoming increasingly aggressive or menacing over time."),
        ],
    },
    
    "SAFE-T-0093": {  # Persistent Unwanted Contact
        "mitigations": [
            ("SAFE-M-0064", "Contact Documentation", "Maintain log of all unwanted contact with dates, times, platforms, and content."),
            ("SAFE-M-0065", "Block and Filter Strategy", "Block adversary on all platforms. Configure email filters to archive messages for evidence."),
            ("SAFE-M-0066", "Carrier Harassment Report", "Contact phone carrier to report harassment and implement call blocking."),
        ],
        "detections": [
            ("SAFE-D-0059", "High Volume Contact", "Unreasonable number of contact attempts across channels."),
            ("SAFE-D-0060", "Multi-Platform Contact Pattern", "Simultaneous contact attempts across multiple platforms."),
        ],
    },
    
    "SAFE-T-0094": {  # Contact After Blocking
        "mitigations": [
            ("SAFE-M-0067", "Multi-Platform Block Maintenance", "Maintain blocks across platforms. Enable unknown sender filtering."),
            ("SAFE-M-0068", "Ban Evasion Reporting", "Report new accounts to platforms for ban evasion."),
        ],
        "detections": [
            ("SAFE-D-0061", "New Accounts with Adversary Indicators", "New accounts using familiar language patterns or referencing personal details."),
            ("SAFE-D-0062", "Alternative Channel Contact", "Contact via channels not previously used after blocking on primary platforms."),
        ],
    },
    
    "SAFE-T-0095": {  # Coordinated Harassment Campaign
        "mitigations": [
            ("SAFE-M-0069", "Mass Block and Report", "Block and report all participating accounts. Report coordinated harassment pattern to platform."),
            ("SAFE-M-0070", "Temporary Account Restriction", "Temporarily restrict account access and disable comments during active campaign."),
            ("SAFE-M-0071", "Regulatory Body Report", "Report serious coordinated harassment to eSafety Commissioner or equivalent body."),
        ],
        "detections": [
            ("SAFE-D-0063", "Hostile Interaction Spike", "Rapid increase in negative interactions from multiple accounts."),
            ("SAFE-D-0064", "Coordination Indicators", "Multiple accounts using similar language, talking points, or hashtags."),
        ],
    },
    
    "SAFE-T-0096": {  # Doxxing
        "mitigations": [
            ("SAFE-M-0072", "Personal Information Minimisation", "Audit and remove personal information from public sources. Opt out of data broker sites."),
            ("SAFE-M-0073", "Address and Contact Protection", "Use PO Box for mail. Register domains with privacy protection."),
            ("SAFE-M-0074", "Doxxing Response Protocol", "If doxxed: report to police, request content removal, alert workplace, document everything."),
        ],
        "detections": [
            ("SAFE-D-0065", "Personal Information Published", "Private information appears on public platforms."),
            ("SAFE-D-0066", "Stranger Harassment Based on Published Details", "Contact from unknown individuals referencing doxxed information."),
        ],
    },
    
    "SAFE-T-0097": {  # Swatting
        "mitigations": [
            ("SAFE-M-0075", "Law Enforcement Notification", "Notify local police of false report risk. Request address flagging in dispatch system."),
            ("SAFE-M-0076", "Emergency Response Preparation", "Prepare for calm interaction with emergency services. Brief household members."),
        ],
        "detections": [
            ("SAFE-D-0067", "Unexpected Emergency Response", "Emergency services arrive in response to unrequested call."),
            ("SAFE-D-0068", "False Report Pattern", "Multiple false reports correlating with relationship events."),
        ],
    },
    
    "SAFE-T-0098": {  # Platform Abuse Reporting
        "mitigations": [
            ("SAFE-M-0077", "Content Backup", "Regularly backup social media content using platform export tools."),
            ("SAFE-M-0078", "Appeal Process Utilisation", "Appeal account restrictions with context about weaponised reporting pattern."),
        ],
        "detections": [
            ("SAFE-D-0069", "Unjustified Account Restrictions", "Content removed or account restricted for non-violating posts during conflict periods."),
            ("SAFE-D-0070", "Multiple Report Indicators", "Platform communications indicating multiple reports against account."),
        ],
    },
    
    "SAFE-T-0099": {  # Public Humiliation Posts
        "mitigations": [
            ("SAFE-M-0079", "Content Removal Request", "Report humiliating content to platform. Report to regulatory body for serious content."),
            ("SAFE-M-0080", "Search Result Management", "Request deindexing of harmful content. Create positive content to influence search results."),
        ],
        "detections": [
            ("SAFE-D-0071", "Harmful Content Discovery", "Posts containing embarrassing or private content about target."),
            ("SAFE-D-0072", "Third-Party Content Alerts", "Contacts report encountering harmful content online."),
        ],
    },
    
    "SAFE-T-0100": {  # Impersonation Harassment
        "mitigations": [
            ("SAFE-M-0081", "Impersonation Reporting", "Report fake accounts to platform using impersonation reporting process."),
            ("SAFE-M-0082", "Network Notification", "Inform contacts of fake accounts and request verification through trusted channels."),
        ],
        "detections": [
            ("SAFE-D-0073", "Contact Reports of Impersonation Messages", "Contacts report receiving messages from accounts impersonating target."),
            ("SAFE-D-0074", "Fake Account Discovery", "Profiles using target's name, photos, or information discovered."),
        ],
    },
    
    "SAFE-T-0101": {  # Review/Rating Attacks
        "mitigations": [
            ("SAFE-M-0083", "False Review Dispute", "Flag false reviews for removal. Provide evidence of fraudulent origin."),
            ("SAFE-M-0084", "Review Response Strategy", "Respond professionally to false reviews. Request genuine client reviews to counterbalance."),
        ],
        "detections": [
            ("SAFE-D-0075", "Fraudulent Review Pattern", "Negative reviews from non-genuine accounts correlating with conflict events."),
            ("SAFE-D-0076", "Professional Impact", "Decline in business correlating with review attack."),
        ],
    },
    
    "SAFE-T-0102": {  # Contact Bombing
        "mitigations": [
            ("SAFE-M-0085", "Email Filtering", "Configure email filtering to manage volume. Unsubscribe from spam subscriptions."),
            ("SAFE-M-0086", "Communication Channel Protection", "Consider temporary contact change while maintaining bombarded accounts for evidence."),
        ],
        "detections": [
            ("SAFE-D-0077", "Spam Volume Spike", "Dramatic increase in spam, subscriptions, or marketing messages."),
            ("SAFE-D-0078", "Unrequested Sign-Up Confirmations", "Confirmation emails from services never subscribed to."),
        ],
    },
    
    "SAFE-T-0103": {  # Proxy Harassment via AI
        "mitigations": [
            ("SAFE-M-0087", "AI Content Detection", "Use AI detection tools to identify synthetic content for evidence purposes."),
            ("SAFE-M-0088", "Platform-Level Reporting", "Report automated abuse patterns to platforms rather than responding to individual items."),
        ],
        "detections": [
            ("SAFE-D-0079", "Synthetic Language Patterns", "Messages that are formulaic, vary slightly while making same points, or arrive at unrealistic volumes."),
            ("SAFE-D-0080", "AI-Generated Media Indicators", "Media with artifacts characteristic of synthetic generation."),
        ],
    },
    
    # ========================================================================
    # TACTIC 4: Information Manipulation (SAFE-TA-0004)
    # ========================================================================
    
    "SAFE-T-0104": {  # Message/Evidence Tampering
        "mitigations": [
            ("SAFE-M-0089", "Original Record Preservation", "Preserve original communications using platform export tools with metadata."),
            ("SAFE-M-0090", "Metadata Verification", "Use platform records with headers and metadata rather than screenshots for evidence."),
            ("SAFE-M-0091", "Witness Communication", "Include trusted witness in important communications for corroboration."),
        ],
        "detections": [
            ("SAFE-D-0081", "Evidence Discrepancies", "Adversary-presented records don't match target's records of same communication."),
            ("SAFE-D-0082", "Message Alteration", "Messages deleted or content changed from what target recalls."),
        ],
    },
    
    "SAFE-T-0105": {  # Digital Gaslighting
        "mitigations": [
            ("SAFE-M-0092", "Digital State Documentation", "Screenshot settings and configurations to establish baseline. Log device states to detect changes."),
            ("SAFE-M-0093", "External Verification", "Verify noticed changes with trusted person before doubting own perception."),
            ("SAFE-M-0094", "Version History Monitoring", "Enable and check version history on shared documents to detect manipulation."),
        ],
        "detections": [
            ("SAFE-D-0083", "Unexplained Setting Changes", "Device settings or file locations changed without user action. Check modification timestamps."),
            ("SAFE-D-0084", "Reality Questioning Pattern", "Increasing self-doubt about digital actions aligning with adversary's claims."),
        ],
    },
    
    "SAFE-T-0106": {  # Non-Consensual Intimate Image Distribution (NCII)
        "mitigations": [
            ("SAFE-M-0095", "Regulatory Body Report", "Report NCII to eSafety Commissioner or equivalent body with legal content removal powers."),
            ("SAFE-M-0096", "Hash-Based Prevention Registration", "Register images with StopNCII.org to prevent re-upload on participating platforms."),
            ("SAFE-M-0097", "Law Enforcement Report", "Report to police. NCII is criminal offence in most jurisdictions."),
        ],
        "detections": [
            ("SAFE-D-0085", "Intimate Image Distribution Discovery", "Intimate images found on public platforms or reported by contacts."),
            ("SAFE-D-0086", "Distribution Threats", "Adversary threatens to share intimate images as leverage."),
        ],
    },
    
    "SAFE-T-0107": {  # Deepfake Creation
        "mitigations": [
            ("SAFE-M-0098", "Synthetic Content Reporting", "Report deepfake intimate content to regulatory body and police. Deepfakes treated equivalently to real NCII."),
            ("SAFE-M-0099", "Source Image Restriction", "Restrict access to facial photos on social media to limit deepfake source material."),
        ],
        "detections": [
            ("SAFE-D-0087", "Synthetic Content Discovery", "Intimate content surfaces that depicts events that never occurred. May show AI artifacts on close inspection."),
            ("SAFE-D-0088", "Fabricated Content Threats", "Adversary threatens distribution of content depicting situations that never happened."),
        ],
    },
    
    "SAFE-T-0108": {  # False Narrative Campaigns
        "mitigations": [
            ("SAFE-M-0100", "Counter-Narrative Development", "Develop response strategy with support services. Share truth selectively with key contacts."),
            ("SAFE-M-0101", "False Claim Documentation", "Document each false claim with evidence contradicting it for legal proceedings."),
        ],
        "detections": [
            ("SAFE-D-0089", "Unexplained Relationship Changes", "Contacts becoming distant without clear reason based on adversary communications."),
            ("SAFE-D-0090", "False Information Reports", "Trusted individuals report false information being shared by adversary."),
        ],
    },
    
    "SAFE-T-0109": {  # Context Manipulation
        "mitigations": [
            ("SAFE-M-0102", "Full Context Preservation", "Preserve complete communication threads and surrounding context."),
            ("SAFE-M-0103", "Written Communication Preference", "Conduct important discussions in writing on platforms maintaining complete records."),
        ],
        "detections": [
            ("SAFE-D-0091", "Decontextualised Content Sharing", "Adversary shares real but misleading content stripped of surrounding context."),
            ("SAFE-D-0092", "Partial Truth Accusations", "Third parties confront target about statements that are technically real but misleading without context."),
        ],
    },
    
    "SAFE-T-0110": {  # Sextortion
        "mitigations": [
            ("SAFE-M-0104", "Non-Compliance", "Do not comply with demands. Compliance typically leads to escalating demands."),
            ("SAFE-M-0105", "Specialist Support Engagement", "Contact regulatory body and law enforcement sextortion support resources."),
        ],
        "detections": [
            ("SAFE-D-0093", "Extortion Demands", "Messages demanding money or compliance in exchange for not distributing intimate content."),
            ("SAFE-D-0094", "Demand Escalation", "Increased demands following initial compliance."),
        ],
    },
    
    "SAFE-T-0111": {  # Catfishing/Romance Fraud
        "mitigations": [
            ("SAFE-M-0106", "Identity Verification", "Verify online relationship identity through video calls and reverse image search before trust development."),
            ("SAFE-M-0107", "Financial Boundary Enforcement", "Never send money or financial information to online-only contacts."),
        ],
        "detections": [
            ("SAFE-D-0095", "Verification Avoidance", "Person consistently avoids video calls or in-person meetings. Photos may belong to someone else."),
            ("SAFE-D-0096", "Financial Request Escalation", "Increasingly urgent requests for financial assistance with compelling stories."),
        ],
    },
    
    "SAFE-T-0112": {  # Reputation Destruction SEO
        "mitigations": [
            ("SAFE-M-0108", "Search Result Monitoring", "Set up alerts for own name. Regular self-search to identify harmful content early."),
            ("SAFE-M-0109", "Positive Content Creation", "Create professional content under own name to influence search results."),
            ("SAFE-M-0110", "Legal Content Removal", "Seek legal advice about defamation action or court-ordered content removal."),
        ],
        "detections": [
            ("SAFE-D-0097", "Harmful Search Results", "Name search reveals websites containing false or harmful content designed to rank highly."),
            ("SAFE-D-0098", "Malicious Domain Registrations", "Websites registered using target's name containing harmful content."),
        ],
    },
    
    "SAFE-T-0113": {  # Historical Content Weaponization
        "mitigations": [
            ("SAFE-M-0111", "Historical Content Cleanup", "Review and restrict visibility of old content that could be weaponised."),
            ("SAFE-M-0112", "Context Preparation", "Prepare contextual explanations for known historical content with support team."),
        ],
        "detections": [
            ("SAFE-D-0099", "Old Content Resurfacing", "Historical content shared in new contexts timed to important events."),
            ("SAFE-D-0100", "Content Archiving Activity", "Evidence adversary systematically archiving target's historical content."),
        ],
    },
    
    "SAFE-T-0114": {  # Fake Evidence Creation
        "mitigations": [
            ("SAFE-M-0113", "Digital Forensic Engagement", "Engage forensic specialist to analyse suspected fabricated evidence and provide expert testimony."),
            ("SAFE-M-0114", "Platform Record Requests", "Request official platform records for critical communications. Harder to fabricate than screenshots."),
        ],
        "detections": [
            ("SAFE-D-0101", "Evidence Inconsistent with Records", "Presented evidence doesn't match target's records or memory of events."),
            ("SAFE-D-0102", "Metadata Inconsistencies", "Digital evidence contains impossible timestamps, missing metadata, or editing artifacts."),
        ],
    },
    
    # ========================================================================
    # TACTIC 5: Isolation & Control (SAFE-TA-0005)
    # ========================================================================
    
    "SAFE-T-0115": {  # Communication Interception & Response
        "mitigations": [
            ("SAFE-M-0115", "Secure Communication Channel", "Use separate secure device for sensitive communications with support services."),
            ("SAFE-M-0116", "Message Verification", "Verify directly with contacts if relationships deteriorate unexpectedly."),
        ],
        "detections": [
            ("SAFE-D-0103", "Unauthorised Message Sending", "Contacts report receiving messages from target's accounts not sent by target."),
            ("SAFE-D-0104", "Unexplained Relationship Deterioration", "Support relationships deteriorate without clear cause."),
        ],
    },
    
    "SAFE-T-0116": {  # Contact Blocking/Filtering
        "mitigations": [
            ("SAFE-M-0117", "Contact and Filter Audit", "Periodically check blocked contacts and email filter rules for unauthorised changes."),
            ("SAFE-M-0118", "Alternative Contact Methods", "Maintain backup contact methods for key support people."),
        ],
        "detections": [
            ("SAFE-D-0105", "Missing Inbound Communications", "Contacts report sending messages that were never received."),
            ("SAFE-D-0106", "Unauthorised Blocked Contacts", "Contacts on blocked list that user did not block."),
        ],
    },
    
    "SAFE-T-0117": {  # Social Media Control
        "mitigations": [
            ("SAFE-M-0119", "Autonomy Assertion", "Recognise demands to control social media connections as controlling behaviour. Document demands."),
            ("SAFE-M-0120", "Private Secondary Account", "Maintain separate private account for support connections if needed."),
        ],
        "detections": [
            ("SAFE-D-0107", "Connection Control Demands", "Demands to unfriend specific people, restrict posting, or delete accounts."),
            ("SAFE-D-0108", "Connection Monitoring", "Adversary comments on or confronts about social media connections and interactions."),
        ],
    },
    
    "SAFE-T-0118": {  # Device Time/Access Restrictions
        "mitigations": [
            ("SAFE-M-0121", "Parental Control Removal", "Remove parental controls from adult devices. Factory reset if removal not possible."),
            ("SAFE-M-0122", "Secondary Device Access", "Maintain access to secondary device adversary cannot control."),
        ],
        "detections": [
            ("SAFE-D-0109", "External Device Restrictions", "Device has time limits, app restrictions, or content filters not configured by user."),
            ("SAFE-D-0110", "Resource Access Blocking", "Support websites, apps, or communication tools blocked at device or network level."),
        ],
    },
    
    "SAFE-T-0119": {  # Network Poisoning
        "mitigations": [
            ("SAFE-M-0123", "Support Network Communication", "Proactively inform key contacts about adversary's potential false information campaign."),
            ("SAFE-M-0124", "Professional Support Briefing", "Ensure professionals (therapist, lawyer, caseworker) are aware adversary may contact them."),
        ],
        "detections": [
            ("SAFE-D-0111", "Contact Attitude Changes", "Contacts suddenly withdrawing support or becoming hostile based on adversary communications."),
            ("SAFE-D-0112", "Adversary Contact Reports", "Support people report adversary has contacted them."),
        ],
    },
    
    "SAFE-T-0120": {  # Platform Banning Coordination
        "mitigations": [
            ("SAFE-M-0125", "Ban Appeal with Context", "Appeal bans with context about coordinated reporting campaign."),
            ("SAFE-M-0126", "Support Network Diversification", "Maintain connections across multiple platforms and in-person support."),
        ],
        "detections": [
            ("SAFE-D-0113", "Unexplained Community Removal", "Banned from communities without clear policy violation."),
            ("SAFE-D-0114", "Coordinated Reporting Evidence", "Community administrators report multiple reports received in short timeframe."),
        ],
    },
    
    "SAFE-T-0121": {  # Communication Monitoring Disclosure
        "mitigations": [
            ("SAFE-M-0127", "Monitoring Assumption Planning", "Use separate safe device for sensitive communications if monitoring disclosed."),
            ("SAFE-M-0128", "Monitoring Capability Verification", "Have professional assess actual monitoring capability to calibrate response."),
        ],
        "detections": [
            ("SAFE-D-0115", "Explicit Monitoring Claims", "Adversary states they can monitor communications, either as threat or demonstrated through knowledge."),
            ("SAFE-D-0116", "Self-Censorship Behaviour", "Target stops seeking help or being honest in communications due to monitoring fear."),
        ],
    },
    
    "SAFE-T-0122": {  # Support Resource Blocking
        "mitigations": [
            ("SAFE-M-0129", "Alternative Resource Access", "Memorise key helpline numbers. Use mobile data or public computers to access blocked resources."),
            ("SAFE-M-0130", "Network Blocking Bypass", "Use mobile data, change DNS settings, or use VPN to bypass network-level blocking."),
        ],
        "detections": [
            ("SAFE-D-0117", "Support Website Inaccessibility", "Support resources inaccessible on home network but work on mobile data."),
            ("SAFE-D-0118", "Support Contact Removal", "Helpline numbers or support bookmarks removed from devices without user action."),
        ],
    },
    
    "SAFE-T-0123": {  # Identity Document Control
        "mitigations": [
            ("SAFE-M-0131", "Document Duplication", "Obtain copies of critical identity documents. Store in adversary-inaccessible location."),
            ("SAFE-M-0132", "Government Portal Security", "Secure access to government portals under sole-controlled credentials."),
        ],
        "detections": [
            ("SAFE-D-0119", "Document Access Denial", "Cannot access digital identity documents due to adversary-controlled storage."),
            ("SAFE-D-0120", "Document Relocation", "Digital documents moved, deleted, or password-protected without user action."),
        ],
    },
    
    "SAFE-T-0124": {  # Email/Communication Rerouting
        "mitigations": [
            ("SAFE-M-0133", "Forwarding Rule Audit", "Check email settings for unauthorised forwarding rules and filters."),
            ("SAFE-M-0134", "Call Forwarding Check", "Check phone settings and carrier account for call forwarding configurations."),
        ],
        "detections": [
            ("SAFE-D-0121", "Missing Expected Communications", "Emails, messages, or calls that senders confirm were sent but never received."),
            ("SAFE-D-0122", "Forwarding Discovery", "Audit reveals email forwarding or call forwarding to unknown destinations."),
        ],
    },
    
    # ========================================================================
    # TACTIC 6: Resource & Financial Control (SAFE-TA-0006)
    # ========================================================================
    
    "SAFE-T-0125": {  # Financial Account Lockout
        "mitigations": [
            ("SAFE-M-0135", "Financial Account Security Reset", "Change passwords, enable MFA, remove adversary as authorised user on individual accounts."),
            ("SAFE-M-0136", "Financial Counselling", "Contact financial counsellor experienced in DFV situations for guidance."),
            ("SAFE-M-0137", "Emergency Financial Access", "Maintain separate emergency fund in adversary-unknown account."),
        ],
        "detections": [
            ("SAFE-D-0123", "Financial Account Lockout", "Unable to access financial accounts using previously valid credentials."),
            ("SAFE-D-0124", "Authorised User Removal", "Notification of removal from shared financial accounts."),
        ],
    },
    
    "SAFE-T-0126": {  # Transaction Monitoring
        "mitigations": [
            ("SAFE-M-0138", "Separate Transaction Account", "Open individual account at different institution for sensitive transactions."),
            ("SAFE-M-0139", "Untraceable Payment Methods", "Use cash or prepaid cards for purchases to keep private."),
        ],
        "detections": [
            ("SAFE-D-0125", "Transaction Knowledge", "Adversary references specific purchases, amounts, or merchants from bank transactions."),
            ("SAFE-D-0126", "Unauthorised Alert Configuration", "Transaction alerts configured to adversary's contact information."),
        ],
    },
    
    "SAFE-T-0127": {  # Spending Restrictions
        "mitigations": [
            ("SAFE-M-0140", "Independent Financial Access", "Establish independent financial access: personal account, credit card, superannuation access."),
            ("SAFE-M-0141", "Legal Financial Advice", "Consult lawyer about financial rights and emergency relief options."),
        ],
        "detections": [
            ("SAFE-D-0127", "Unexplained Transaction Declines", "Card declined despite available funds, or daily limits reduced without consent."),
            ("SAFE-D-0128", "Spending Approval Requirements", "Spending limits or approval requirements enabled without user action."),
        ],
    },
    
    "SAFE-T-0128": {  # Unauthorized Transactions
        "mitigations": [
            ("SAFE-M-0142", "Transaction Alert Configuration", "Enable real-time transaction alerts on all financial accounts."),
            ("SAFE-M-0143", "Fraud Reporting", "Report unauthorised transactions to financial institution and police."),
        ],
        "detections": [
            ("SAFE-D-0129", "Unrecognised Transactions", "Transactions appearing on accounts not authorised by account holder."),
            ("SAFE-D-0130", "Balance Discrepancies", "Account balances lower than expected or funds moved without knowledge."),
        ],
    },
    
    "SAFE-T-0129": {  # Coerced Transactions
        "mitigations": [
            ("SAFE-M-0144", "Coerced Debt Legal Advice", "Consult about coerced debt pathways. Debts incurred under duress may be dischargeable."),
            ("SAFE-M-0145", "Coercion Documentation", "Document coercion circumstances for legal proceedings."),
        ],
        "detections": [
            ("SAFE-D-0131", "Financial Coercion", "Threats, intimidation, or manipulation to make transactions or take on debt."),
            ("SAFE-D-0132", "Duress Debt Accumulation", "Increasing debt from pressured financial decisions."),
        ],
    },
    
    "SAFE-T-0130": {  # Crypto/Investment Fraud
        "mitigations": [
            ("SAFE-M-0146", "Investment Verification", "Verify investment opportunities independently through regulatory body resources."),
            ("SAFE-M-0147", "Fraud Reporting", "Report suspected investment fraud to consumer protection and cyber security agencies."),
        ],
        "detections": [
            ("SAFE-D-0133", "Pressure to Invest in Unverified Platforms", "Urged to invest on unfamiliar platforms that cannot be independently verified."),
            ("SAFE-D-0134", "Withdrawal Inability", "Invested funds cannot be withdrawn from platform."),
        ],
    },
    
    "SAFE-T-0131": {  # Benefits/Payments Interception
        "mitigations": [
            ("SAFE-M-0148", "Payment Destination Security", "Ensure all payments directed to sole-controlled account. Update payment details with agencies and employers."),
            ("SAFE-M-0149", "Mail Redirection Check", "Verify no mail redirection configured without knowledge."),
        ],
        "detections": [
            ("SAFE-D-0135", "Missing Expected Payments", "Government benefits, salary, or other payments not arriving in expected accounts."),
            ("SAFE-D-0136", "Payment Detail Changes", "Direct deposit information changed without authorisation."),
        ],
    },
    
    "SAFE-T-0132": {  # Credit/Identity Theft
        "mitigations": [
            ("SAFE-M-0150", "Credit Monitoring", "Set up credit monitoring. Request credit reports from all reporting bodies."),
            ("SAFE-M-0151", "Credit Ban", "Place credit ban to prevent new applications. Available free for DFV victims."),
            ("SAFE-M-0152", "Identity Theft Report", "Report identity theft to national identity support service."),
        ],
        "detections": [
            ("SAFE-D-0137", "Unknown Credit Activity", "Credit report shows accounts or enquiries not initiated by owner."),
            ("SAFE-D-0138", "Unknown Service Bills", "Bills or collection notices for services never subscribed to."),
        ],
    },
    
    "SAFE-T-0133": {  # Smart Home Resource Control
        "mitigations": [
            ("SAFE-M-0153", "Smart Home Account Control", "Transfer all smart home device accounts to sole control. Factory reset and reconfigure."),
            ("SAFE-M-0154", "Manual Override Capability", "Ensure manual overrides available for all smart home-controlled utilities."),
        ],
        "detections": [
            ("SAFE-D-0139", "Remote Utility Control", "Heating, cooling, lighting, or locks changing without user action."),
            ("SAFE-D-0140", "Manipulation-Reflective Utility Bills", "Unusual utility bills resulting from remote environmental manipulation."),
        ],
    },
    
    "SAFE-T-0134": {  # Employment Sabotage
        "mitigations": [
            ("SAFE-M-0155", "Employer Notification", "Inform employer about potential for adversary workplace contact if safe to do so."),
            ("SAFE-M-0156", "Professional Account Security", "Secure professional accounts with strong credentials and MFA."),
        ],
        "detections": [
            ("SAFE-D-0141", "Workplace Interference", "Employer or colleagues report contact from adversary about target."),
            ("SAFE-D-0142", "Application Interference", "Job applications unsuccessful potentially due to adversary contact with prospective employers."),
        ],
    },
    
    "SAFE-T-0135": {  # Subscription/Service Cancellation
        "mitigations": [
            ("SAFE-M-0157", "Individual Account Registration", "Register essential services under own name and billing."),
            ("SAFE-M-0158", "Service Provider DFV Support", "Request DFV support pathway from service providers for expedited account changes."),
        ],
        "detections": [
            ("SAFE-D-0143", "Essential Service Cancellation", "Phone, internet, insurance, or utilities cancelled without knowledge or consent."),
            ("SAFE-D-0144", "Unauthorised Service Changes", "Service plans modified or features removed without notification."),
        ],
    },
    
    # ========================================================================
    # TACTIC 7: Physical Enablement (SAFE-TA-0007)
    # ========================================================================
    
    "SAFE-T-0136": {  # Location-Based Assault
        "mitigations": [
            ("SAFE-M-0159", "Comprehensive Location Security", "Disable all location sharing, remove trackers, secure location-revealing accounts, vary routines."),
            ("SAFE-M-0160", "Safety Planning", "Develop comprehensive safety plan with support service addressing technology-enabled tracking."),
            ("SAFE-M-0161", "Law Enforcement Report", "Report stalking and tracking to police. Apply for intervention order with technology-specific conditions."),
        ],
        "detections": [
            ("SAFE-D-0145", "Location Interception", "Adversary appears at locations not disclosed to them."),
            ("SAFE-D-0146", "Location-Referencing Threats", "Threats that reference specific location or recent movements."),
        ],
    },
    
    "SAFE-T-0137": {  # Safe Location Disclosure
        "mitigations": [
            ("SAFE-M-0162", "Safe Location Digital Hygiene", "Disable location services. Strip metadata from images. Avoid tagging safe location digitally."),
            ("SAFE-M-0163", "Secure Communication from Safe Location", "Use new device and accounts. Only communicate location to those who must know via secure channels."),
        ],
        "detections": [
            ("SAFE-D-0147", "Safe Location Discovery", "Adversary appears near or references safe location. Immediate safety emergency."),
            ("SAFE-D-0148", "Photo Metadata Exposure", "Shared photos contain GPS coordinates revealing safe location."),
        ],
    },
    
    "SAFE-T-0138": {  # Movement Interception
        "mitigations": [
            ("SAFE-M-0164", "Route Variation", "Vary routes, departure times, and transport methods."),
            ("SAFE-M-0165", "Appointment Security", "Keep appointments off monitored calendars. Arrange support person accompaniment."),
        ],
        "detections": [
            ("SAFE-D-0149", "Route Interception", "Adversary appearing along travel route or at destinations."),
            ("SAFE-D-0150", "Travel Knowledge Indicators", "Adversary demonstrates knowledge of travel plans before arrival."),
        ],
    },
    
    "SAFE-T-0139": {  # Smart Lock Manipulation
        "mitigations": [
            ("SAFE-M-0166", "Smart Lock Security Reset", "Change all smart lock credentials. Remove adversary access. Replace with traditional locks if needed."),
            ("SAFE-M-0167", "Lock Replacement Post-Separation", "Change all locks after separation. Most jurisdictions require landlords to do this for DFV situations."),
        ],
        "detections": [
            ("SAFE-D-0151", "Lock Behaviour Anomalies", "Smart locks engaging or disengaging unexpectedly. Access codes no longer working."),
            ("SAFE-D-0152", "Physical Access Control", "Locked inside or outside home due to remote lock manipulation. Safety emergency."),
        ],
    },
    
    "SAFE-T-0140": {  # Vehicle Sabotage
        "mitigations": [
            ("SAFE-M-0168", "Connected Car Account Security", "Change connected car credentials. Remove adversary from vehicle account access."),
            ("SAFE-M-0169", "Vehicle Safety Inspection", "Have mechanic inspect for tracking devices and tampering. Check OBD-II port."),
        ],
        "detections": [
            ("SAFE-D-0153", "Remote Vehicle Control", "Vehicle functions activating without user action — horn, lights, locks, engine."),
            ("SAFE-D-0154", "Connected Car Access Alerts", "Notifications showing adversary's device accessing vehicle features."),
        ],
    },
    
    "SAFE-T-0141": {  # IoT Device Weaponization
        "mitigations": [
            ("SAFE-M-0170", "IoT Device Audit and Reset", "Audit all smart home devices. Factory reset and reconfigure under sole-controlled account."),
            ("SAFE-M-0171", "Network Security", "Change Wi-Fi passwords. Remove adversary access to router admin."),
        ],
        "detections": [
            ("SAFE-D-0155", "Unexplained Device Activation", "Smart home devices activating without user command — alarms, lights, speakers, TV."),
            ("SAFE-D-0156", "Environmental Manipulation", "Temperature or comfort settings changed remotely to create discomfort."),
        ],
    },
    
    "SAFE-T-0142": {  # Medical Device Interference
        "mitigations": [
            ("SAFE-M-0172", "Medical Device Security Review", "Inform healthcare provider of DFV situation. Request security review of connected medical devices."),
            ("SAFE-M-0173", "Health Record Access Control", "Restrict health record access. Change patient portal credentials. Remove adversary as authorised contact."),
        ],
        "detections": [
            ("SAFE-D-0157", "Medical Device Setting Changes", "Connected medical device settings changed without user action. Contact healthcare provider immediately."),
            ("SAFE-D-0158", "Health Data Access Indicators", "Adversary demonstrates knowledge of health information they should not have access to."),
        ],
    },
    
    "SAFE-T-0143": {  # Stalking Coordination
        "mitigations": [
            ("SAFE-M-0174", "Anti-Stalking Strategy", "Develop comprehensive anti-stalking safety plan with police and support service."),
            ("SAFE-M-0175", "Stalking Evidence Documentation", "Maintain detailed stalking log documenting every incident. Use stalking documentation tools."),
        ],
        "detections": [
            ("SAFE-D-0159", "Repeated Unexplained Appearances", "Adversary repeatedly appears at different locations at varied times."),
            ("SAFE-D-0160", "Coordinated Surveillance Evidence", "Evidence adversary involved others in surveillance or uses multiple tracking methods."),
        ],
    },
    
    "SAFE-T-0144": {  # Emergency Service Manipulation
        "mitigations": [
            ("SAFE-M-0176", "Law Enforcement False Report Briefing", "Inform police of false report risk. Request address flagging."),
            ("SAFE-M-0177", "False Report Legal Response", "Report false emergency calls as criminal offences. Gather evidence reports are fabricated."),
        ],
        "detections": [
            ("SAFE-D-0161", "Unrequested Authority Visits", "Authorities arrive based on reports not made by target."),
            ("SAFE-D-0162", "False Report Pattern", "Learning false reports filed against target by adversary or associates."),
        ],
    },
    
    "SAFE-T-0145": {  # Child Custody Tech Abuse
        "mitigations": [
            ("SAFE-M-0178", "Co-Parenting App Boundaries", "Use court-approved co-parenting apps for documented communication."),
            ("SAFE-M-0179", "Children's Device Security", "Audit children's devices for monitoring. Manage parental controls."),
            ("SAFE-M-0180", "Legal Tech Abuse Documentation", "Document technology abuse through custody arrangements for family court."),
        ],
        "detections": [
            ("SAFE-D-0163", "Excessive Location Monitoring", "Adversary checking children's location more than reasonably required."),
            ("SAFE-D-0164", "Co-Parenting App Misuse", "Co-parenting apps used for hostile messages rather than genuine co-parenting."),
            ("SAFE-D-0165", "Children's Device Surveillance", "Monitoring software on children's devices enabling household surveillance."),
        ],
    },
}
