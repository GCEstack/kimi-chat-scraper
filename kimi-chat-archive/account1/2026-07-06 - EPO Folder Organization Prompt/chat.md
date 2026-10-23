# EPO Folder Organization Prompt

- Created: 2026-07-03T02:41:33Z
- Updated: 2026-07-06T11:52:14Z

---

## 🧑 You

I NEED A KIMI CODE PROMPT INSTRUVCTIOJNSD TO FUNDF AND ORGANIXE ALL MY EEPO FOLDERS THAT ARE CROWDSOURCE AND COMMAND CENTER TO CREATE A READ

---

## 🤖 Kimi

I want to make sure I understand your request correctly. It looks like you need help organizing folders related to "EPO" (which I believe refers to the European Patent Office) that are part of a crowdsourced project and command center setup, and you want to create a README file for documentation.However, I need some clarification to help you effectively:What do you mean by "Kimi Code Prompt Instructions"? Are you looking for:A system prompt/instruction set for me (Kimi) to help you organize files?A code script or automation workflow?Documentation templates?What are "EPO folders"? Are these:Patent application folders?Project folders for a specific EPO-related crowdsourcing initiative?Data folders from the EPO Open Patent Services?What is the "Command Center"? Is this:A specific software platform?A dashboard you're building?A folder structure for managing operations?What do you need in the README? For example:Folder structure documentation?Workflow instructions?Data handling guidelines?Could you clarify these points? Once I understand your setup, I can help you create the proper organization structure and documentation.                                               ALL FOLDERS SUB FOLDERS ETC FILES

---

## 🧑 You

I understand you need to organize all folders, subfolders, and files for your EPO (European Patent Office) crowdsourced project. Let me search for current information about EPO data structures and crowdsourcing platforms to help create a comprehensive organization system. Search EPO European Patent Office crowdsourcing data folder structure 2026 EPO Open Patent Services API data organization patent data crowdsourcing project folder management  27 results    I understand you need a comprehensive folder organization system and README for your EPO (European Patent Office) crowdsourced project. Based on the EPO Open Patent Services (OPS) structure and patent data management best practices, I'll create a complete system for you.Here's your Kimi Prompt Instructions and Folder Organization System:📋 KIMI CODE PROMPT INSTRUCTIONSplain   Copy ROLE: You are a Patent Data Organization Specialist for EPO Crowdsourcing Projects.

TASK: Organize all EPO-related folders, subfolders, and files into a structured Command Center system.

CONTEXT: 
- Working with EPO Open Patent Services (OPS) API data
- Crowdsourced patent analysis project
- Multiple data types: bibliographic, full-text, legal status, images, classifications
- Need centralized README documentation

RULES:
1. Use consistent naming conventions (YYYYMMDD_Prefix_Description)
2. Separate raw data from processed data
3. Maintain API quota tracking logs
4. Version control all scripts and configurations
5. Document all data sources with timestamps
6. Keep backup archives separate from active work
7. Use ISO 8601 date formats (YYYY-MM-DD)
8. Tag files with technology field keywords (CPC/IPC classes)

OUTPUT FORMAT: 
- Hierarchical folder tree
- README.md with full documentation
- File naming conventions
- Data management protocols 🗂️ COMPLETE FOLDER STRUCTUREplain   Copy EPO_CROWDSOURCE_COMMAND_CENTER/
│
├── 📁 00_ADMIN/
│   ├── 📁 00a_Project_Charter/
│   │   ├── project_scope.md
│   │   ├── team_roles.md
│   │   └── stakeholder_map.md
│   │
│   ├── 📁 00b_Meetings/
│   │   ├── YYYY-MM-DD_meeting_type_agenda.md
│   │   └── YYYY-MM-DD_meeting_type_minutes.md
│   │
│   ├── 📁 00c_Legal_Ethical/
│   │   ├── data_protection_gdpr.md
│   │   ├── terms_of_use_epo.md
│   │   └── contributor_agreements.md
│   │
│   └── 📁 00d_Reporting/
│       ├── weekly_status_reports/
│       ├── monthly_metrics/
│       └── quarterly_reviews/
│
├── 📁 01_DATA_SOURCES/
│   ├── 📁 01a_EPO_OPS_API/
│   │   ├── 📁 configs/
│   │   │   ├── ops_credentials.env (SECURED)
│   │   │   ├── api_endpoints.json
│   │   │   └── rate_limits.yaml
│   │   │
│   │   ├── 📁 raw_downloads/
│   │   │   ├── 📁 bibliographic/
│   │   │   ├── 📁 full_text/
│   │   │   ├── 📁 legal_status/
│   │   │   ├── 📁 family_data/
│   │   │   ├── 📁 images_tiff/
│   │   │   └── 📁 classifications/
│   │   │
│   │   ├── 📁 processed/
│   │   │   ├── 📁 xml_parsed/
│   │   │   ├── 📁 json_converted/
│   │   │   └── 📁 csv_extracted/
│   │   │
│   │   └── 📁 quota_tracking/
│   │       ├── weekly_usage_logs/
│   │       └── monthly_quota_reports/
│   │
│   ├── 📁 01b_Espacenet/
│   │   ├── search_queries/
│   │   └── export_data/
│   │
│   ├── 📁 01c_PATSTAT/
│   │   ├── database_schema/
│   │   └── sql_queries/
│   │
│   └── 📁 01d_External_Sources/
│       ├── uspto_data/
│       ├── wipo_data/
│       └── google_patents/
│
├── 📁 02_CROWDSOURCE/
│   ├── 📁 02a_Contributor_Onboarding/
│   │   ├── training_materials/
│   │   ├── style_guides/
│   │   └── quality_standards/
│   │
│   ├── 📁 02b_Active_Tasks/
│   │   ├── 📁 pending/
│   │   ├── 📁 in_progress/
│   │   └── 📁 completed/
│   │
│   ├── 📁 02c_Validation/
│   │   ├── 📁 peer_review/
│   │   ├── 📁 expert_review/
│   │   └── 📁 quality_assurance/
│   │
│   └── 📁 02d_Contributor_Profiles/
│       ├── skill_matrix.csv
│       ├── contribution_logs/
│       └── performance_metrics/
│
├── 📁 03_PATENT_DATA/
│   ├── 📁 03a_By_Technology_Field/
│   │   ├── 📁 CPC_Sections/
│   │   │   ├── A_Human_Necessities/
│   │   │   ├── B_Performing_Operations/
│   │   │   ├── C_Chemistry_Metallurgy/
│   │   │   ├── D_Textiles_Paper/
│   │   │   ├── E_Fixed_Constructions/
│   │   │   ├── F_Mechanical_Engineering/
│   │   │   ├── G_Physics/
│   │   │   ├── H_Electricity/
│   │   │   └── Y_General_Tagging/
│   │   │
│   │   └── 📁 IPC_Classes/
│   │
│   ├── 📁 03b_By_Geography/
│   │   ├── EP_European/
│   │   ├── US_United_States/
│   │   ├── WO_PCT/
│   │   ├── CN_China/
│   │   ├── JP_Japan/
│   │   └── KR_Korea/
│   │
│   ├── 📁 03c_By_Status/
│   │   ├── pending_applications/
│   │   ├── granted_patents/
│   │   ├── expired_lapsed/
│   │   └── withdrawn_refused/
│   │
│   └── 📁 03d_By_Date/
│       ├── YYYY/
│       │   └── MM/
│       └── YYYY_quarterly/
│
├── 📁 04_ANALYSIS/
│   ├── 📁 04a_Prior_Art/
│   │   ├── search_reports/
│   │   └── novelty_assessments/
│   │
│   ├── 📁 04b_Landscape_Studies/
│   │   ├── technology_trends/
│   │   ├── competitor_intelligence/
│   │   └── whitespace_analysis/
│   │
│   ├── 📁 04c_Valuation/
│   │   ├── patent_scores/
│   │   └── portfolio_rankings/
│   │
│   └── 📁 04d_Citations/
│       ├── backward_citations/
│       └── forward_citations/
│
├── 📁 05_COMMAND_CENTER/
│   ├── 📁 05a_Dashboards/
│   │   ├── project_overview.html
│   │   ├── data_quality_dashboard.html
│   │   └── contributor_activity.html
│   │
│   ├── 📁 05b_Scripts/
│   │   ├── 📁 python/
│   │   │   ├── ops_api_client.py
│   │   │   ├── data_parser.py
│   │   │   └── batch_processor.py
│   │   │
│   │   ├── 📁 sql/
│   │   │   ├── data_extraction_queries/
│   │   │   └── reporting_queries/
│   │   │
│   │   └── 📁 bash/
│   │       ├── automation_scripts/
│   │       └── cron_jobs/
│   │
│   ├── 📁 05c_Workflows/
│   │   ├── data_ingestion_pipeline.md
│   │   ├── quality_control_checklist.md
│   │   └── escalation_procedures.md
│   │
│   └── 📁 05d_Alerts/
│       ├── api_quota_alerts/
│       ├── data_quality_flags/
│       └── deadline_reminders/
│
├── 📁 06_DOCUMENTATION/
│   ├── 📁 06a_API_Documentation/
│   │   ├── ops_reference_guide.md
│   │   ├── cql_query_cheatsheet.md
│   │   └── xml_schema_docs/
│   │
│   ├── 📁 06b_Standards/
│   │   ├── naming_conventions.md
│   │   ├── metadata_standards.md
│   │   └── file_formats.md
│   │
│   ├── 📁 06c_Guides/
│   │   ├── contributor_handbook.md
│   │   ├── data_entry_guide.md
│   │   └── troubleshooting.md
│   │
│   └── 📁 06c_Change_Logs/
│       ├── version_history.md
│       └── migration_logs/
│
├── 📁 07_OUTPUTS/
│   ├── 📁 07a_Reports/
│   │   ├── 📁 weekly/
│   │   ├── 📁 monthly/
│   │   └── 📁 ad_hoc/
│   │
│   ├── 📁 07b_Deliverables/
│   │   ├── client_deliverables/
│   │   └── internal_deliverables/
│   │
│   ├── 📁 07c_Publications/
│   │   ├── white_papers/
│   │   ├── blog_posts/
│   │   └── conference_presentations/
│   │
│   └── 📁 07d_Exports/
│       ├── csv_exports/
│       ├── json_exports/
│       └── pdf_reports/
│
├── 📁 08_ARCHIVE/
│   ├── 📁 08a_Completed_Projects/
│   │   └── YYYY-MM-DD_project_name/
│   │
│   ├── 📁 08b_Obsolete_Data/
│   │   └── YYYY-MM-DD_retired_dataset/
│   │
│   └── 📁 08c_Backups/
│       ├── daily_snapshots/
│       ├── weekly_backups/
│       └── monthly_archives/
│
├── 📁 99_TEMPLATES/
│   ├── folder_template_standard.md
│   ├── file_naming_template.md
│   ├── report_template.md
│   └── task_assignment_template.md
│
└── 📄 README.md (MASTER DOCUMENTATION) 📄 README.md CONTENTMarkdown  Fullscreen  Download  Fit  Code Preview  # EPO CROWDSOURCE COMMAND CENTER
**European Patent Office Crowdsourced Data Analysis Project**

## 🎯 PROJECT OVERVIEW
Centralized repository for managing EPO patent data from crowdsourced contributions, 
API integrations, and analytical workflows.

## 📁 FOLDER STRUCTURE GUIDE

| Folder | Purpose | Access Level |
|--------|---------|-------------|
| 00_ADMIN | Project governance & management | Core Team Only |
| 01_DATA_SOURCES | Raw & processed EPO data | Data Managers |
| 02_CROWDSOURCE | Contributor workflows | All Contributors |
| 03_PATENT_DATA | Organized patent collections | Analysts |
| 04_ANALYSIS | Research & assessment outputs | Analysts |
| 05_COMMAND_CENTER | Dashboards, scripts, automation | Tech Team |
| 06_DOCUMENTATION | Standards, guides, references | All Users |
| 07_OUTPUTS | Reports & deliverables | Stakeholders |
| 08_ARCHIVE | Historical data & backups | Admin Only |
| 99_TEMPLATES | Standardized templates | All Users |

## 🔑 NAMING CONVENTIONS

### Folders
`[NUMBER]_[CATEGORY]_[SpecificName]`

### Files
`[YYYY-MM-DD]_[TYPE]_[Description]_[VERSION].[ext]`

Examples:
- `2026-06-14_OPS_Bibliographic_Download_v1.xml`
- `2026-06-14_Task_PriorArt_Review_EP123456.md`

## 🌐 DATA SOURCES

### Primary: EPO Open Patent Services (OPS)
- API Version: 3.2
- Base URL: https://ops.epo.org/3.2/rest-services
- Authentication: OAuth2 (Consumer Key + Secret)
- Quota: 4 GB/week (non-paying) / 2.5 GB/week (fair use)

### Secondary Sources
- Espacenet (search interface)
- PATSTAT (statistical database)
- USPTO, WIPO, Google Patents (cross-referencing)

## 👥 CROWDSOURCE WORKFLOW

1. **Onboarding**: Contributors complete training in 02a
2. **Task Assignment**: Active tasks distributed from 02b
3. **Data Entry**: Input following standards in 06b
4. **Validation**: Peer review in 02c, then expert review
5. **Integration**: Validated data moves to 03_PATENT_DATA
6. **Analysis**: Analysts process in 04_ANALYSIS
7. **Reporting**: Outputs generated in 07_OUTPUTS

## ⚙️ COMMAND CENTER OPERATIONS

### Automation Scripts
- `ops_api_client.py` - EPO API interface
- `data_parser.py` - XML/JSON conversion
- `batch_processor.py` - Bulk data handling

### Monitoring
- API quota usage tracked in 01a/05d
- Data quality flags in 05d
- Contributor activity in 05a

## 🔒 SECURITY & COMPLIANCE

- EPO API credentials stored in `.env` (never commit)
- GDPR compliance for contributor data
- Data retention: 7 years for patent records
- Backup schedule: Daily incremental, weekly full

## 📊 QUALITY STANDARDS

- All data entries require source attribution
- XML validation against EPO schema
- Cross-reference verification mandatory
- Duplicate detection automated

## 🚀 QUICK START

1. Clone repository
2. Copy `99_TEMPLATES` for new work
3. Configure API credentials in `01a/configs/`
4. Review `06a/API_Documentation/`
5. Join active task in `02b/`

## 📞 CONTACT

- Project Lead: [Name]
- Data Manager: [Name]
- Tech Lead: [Name]
- EPO Liaison: [Name]

---
Last Updated: 2026-06-14
Version: 1.0  🔧 FILE NAMING CONVENTION CHEAT SHEETTable  Copy   TypePatternExample API DownloadYYYYMMDD_OPS_[DataType]_[DocNum].xml20260614_OPS_Biblio_EP1000000.xmlTask FileYYYYMMDD_Task_[Type]_[ID].md20260614_Task_PriorArt_001.mdReportYYYYMMDD_Report_[Topic]_[Period].pdf20260614_Report_Landscape_Q2.pdfScript[function]_[module].pyops_api_client.pyConfig[service]_[env].envops_credentials.envBackupYYYYMMDD_Backup_[Type]_[Seq].zip20260614_Backup_Full_001.zip📝 IMPLEMENTATION CHECKLIST[ ] Create all top-level folders (00-99)[ ] Set up .gitignore for sensitive files (credentials, large data)[ ] Configure API credentials in environment variables[ ] Install Python dependencies (epo-ops-client, pandas, xml parsers)[ ] Set up automated quota monitoring[ ] Create contributor onboarding materials[ ] Establish backup automation (cron jobs)[ ] Deploy dashboard templates[ ] Test data pipeline end-to-end[ ] Schedule first team sync in 00bThis system gives you a complete, scalable structure for managing your EPO crowdsourcing project with proper documentation, security, and workflow management. The Command Center (05) serves as your operational hub, while the crowdsourcing section (02) manages all contributor activities.Would you like me to generate specific scripts for any of these folders or create additional templates?                                                       Ask away. Pics work too.                       K2.6 Instant

---
