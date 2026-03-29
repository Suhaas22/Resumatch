import re

KNOWN_SKILLS = [

    # ── PROGRAMMING ───────────────────────────────────────
    "python", "java", "c", "c++", "c#", "go", "golang", "rust",
    "javascript", "typescript", "kotlin", "swift", "ruby", "php",
    "scala", "r", "matlab", "dart",

    # ── WEB ───────────────────────────────────────────────
    "html", "css", "react", "angular", "vue", "nodejs", "express",
    "django", "flask", "spring boot", "nextjs", "bootstrap",
    "tailwind", "jquery",

    # ── DATABASES ─────────────────────────────────────────
    "mysql", "postgresql", "mongodb", "sqlite", "oracle", "redis",
    "cassandra", "firebase", "dynamodb", "neo4j",

    # ── AI / ML ───────────────────────────────────────────
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "numpy", "pandas",
    "opencv", "keras", "xgboost", "data science", "statistics",

    # ── DEVOPS ────────────────────────────────────────────
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
    "terraform", "ansible", "ci/cd", "linux", "nginx",

    # ── MOBILE ────────────────────────────────────────────
    "android", "ios", "react native", "flutter",

    # ── TOOLS ─────────────────────────────────────────────
    "git", "github", "gitlab", "jira", "figma", "postman",
    "power bi", "tableau", "excel", "ms office", "word", "powerpoint",

    # ── SECURITY ──────────────────────────────────────────
    "cybersecurity", "ethical hacking", "network security",
    "penetration testing", "siem", "firewall", "vapt",

    # ── FINANCE & ACCOUNTING ──────────────────────────────
    "financial analysis", "financial reporting", "budgeting",
    "forecasting", "auditing", "bookkeeping", "taxation", "tally",
    "quickbooks", "sap", "accounts payable", "accounts receivable",
    "balance sheet", "profit and loss", "gst", "tds", "ifrs",
    "gaap", "cost accounting", "investment analysis",
    "portfolio management", "equity research", "mutual funds",
    "stock market", "derivatives", "payroll",

    # ── HR ────────────────────────────────────────────────
    "recruitment", "talent acquisition", "onboarding",
    "employee relations", "performance management", "hris",
    "learning and development", "compensation",
    "hr policies", "workforce planning", "succession planning",
    "grievance handling", "exit interviews", "hr analytics",
    "organizational development", "employee engagement",

    # ── SALES & BUSINESS DEVELOPMENT ──────────────────────
    "lead generation", "cold calling", "crm", "salesforce",
    "client acquisition", "b2b", "b2c", "revenue growth",
    "market research", "sales strategy", "pipeline management",
    "account management", "upselling", "cross-selling",
    "business development", "partnership management",

    # ── MARKETING & PUBLIC RELATIONS ──────────────────────
    "digital marketing", "seo", "sem", "google ads", "meta ads",
    "content marketing", "email marketing", "social media marketing",
    "brand management", "market analysis", "media relations",
    "press release", "crisis communication", "event management",
    "public relations", "copywriting", "influencer marketing",
    "campaign management", "google analytics",

    # ── DIGITAL MEDIA ─────────────────────────────────────
    "video editing", "premiere pro", "after effects", "final cut pro",
    "youtube", "instagram", "content creation", "podcast",
    "motion graphics", "davinci resolve", "graphic design",
    "photoshop", "illustrator", "canva", "indesign",
    "photography", "videography", "color grading",

    # ── DESIGN & ARTS ─────────────────────────────────────
    "ui design", "ux design", "user research", "wireframing",
    "prototyping", "adobe xd", "sketch", "typography",
    "branding", "visual design", "3d modeling", "autocad",
    "solidworks", "3ds max", "blender", "animation",
    "illustration", "art direction", "creative direction",

    # ── HEALTHCARE ────────────────────────────────────────
    "patient care", "clinical", "nursing", "diagnosis",
    "medical records", "ehr", "emr", "pharmacy", "surgery",
    "first aid", "cpr", "triage", "radiology", "pathology",
    "physiotherapy", "pediatrics", "cardiology", "oncology",
    "pharmacology", "medical coding", "hipaa", "telemedicine",
    "health informatics", "icd", "cpt coding",

    # ── BANKING ───────────────────────────────────────────
    "kyc", "aml", "loan processing", "credit analysis",
    "retail banking", "core banking", "trade finance",
    "treasury", "basel", "nbfc", "microfinance",
    "bancassurance", "wealth management", "swift",
    "financial products", "npa management",

    # ── LEGAL / ADVOCATE ──────────────────────────────────
    "litigation", "legal research", "contract drafting",
    "client counseling", "case management", "court proceedings",
    "ipc", "crpc", "civil procedure", "criminal law",
    "corporate law", "intellectual property", "arbitration",
    "due diligence", "legal compliance", "bar council",
    "llb", "judiciary", "affidavit", "legal drafting",
    "labour law", "family law", "property law",

    # ── ENGINEERING ───────────────────────────────────────
    "autocad", "catia", "ansys", "lean manufacturing",
    "six sigma", "iso", "cad", "cam", "mechanical design",
    "civil engineering", "structural analysis",
    "electrical engineering", "plc", "scada",
    "embedded systems", "hvac", "piping", "welding",
    "procurement", "solidworks",

    # ── CONSTRUCTION ──────────────────────────────────────
    "site management", "blueprint reading", "estimation",
    "quantity surveying", "project scheduling", "ms project",
    "primavera", "contract management", "bim", "revit",
    "civil works", "rcc", "steel structures", "safety management",
    "hse", "tendering", "subcontractor management",

    # ── AVIATION ──────────────────────────────────────────
    "dgca", "atc", "notam", "icao", "iata", "airworthiness",
    "aircraft maintenance", "avionics", "logbook", "cockpit",
    "flight operations", "ground handling", "load planning",
    "crew resource management", "safety management system",
    "line maintenance", "base maintenance", "aoc",
    "flight dispatch", "meteorology", "navigation",

    # ── AGRICULTURE ───────────────────────────────────────
    "crop management", "soil science", "irrigation",
    "fertilizer", "pesticide", "horticulture", "agronomy",
    "farm management", "drip irrigation", "hydroponics",
    "greenhouse", "crop yield", "soil ph", "organic farming",
    "seed technology", "plant pathology", "livestock",
    "poultry", "aquaculture", "agricultural machinery",
    "remote sensing", "gis",

    # ── APPAREL & FASHION ─────────────────────────────────
    "fashion design", "textile", "garment", "merchandising",
    "trend forecasting", "fabric", "pattern making", "lectra",
    "gerber", "gsm", "knitting", "weaving", "dyeing",
    "quality inspection", "sourcing", "production planning",
    "retail merchandising", "visual merchandising",
    "fashion styling", "cad pattern", "tech pack",
    # ── APPAREL & FASHION (extended) ──────────────────────
    "embroidery", "zari", "chikankari", "handloom", "saree",
    "ethnic wear", "readymade garments", "export", "buying house",
    "woven fabric", "yarn", "spinning", "printing", "screen printing",
    "apparel export", "sampling", "fit approval", "pp sample",
    "bulk production", "costing", "trim", "accessory",

    # ── FITNESS ───────────────────────────────────────────
    "personal training", "workout planning", "nutrition",
    "strength training", "cardio", "yoga", "pilates",
    "group fitness", "client assessment", "body composition",
    "sports coaching", "rehabilitation", "crossfit",
    "weight management", "certified personal trainer",
    "cpt", "ace", "nasm", "wellness coaching",

    # ── CHEF & HOSPITALITY ────────────────────────────────
    "food preparation", "menu planning", "kitchen management",
    "culinary", "food safety", "haccp",
    "pastry", "baking", "grilling", "sauteing", "plating",
    "supplier management", "fssai", "hygiene standards",
    "catering", "banquet", "hospitality",
    "restaurant management", "barista", "sommelier",

    # ── TEACHER & EDUCATION ───────────────────────────────
    "lesson planning", "curriculum development",
    "classroom management", "student assessment",
    "e-learning", "lms", "instructional design",
    "special education", "montessori", "cbse", "icse",
    "teaching", "tutoring", "academic counseling",
    "school administration", "pedagogy", "smart board",

    # ── CONSULTANT ────────────────────────────────────────
    "business analysis", "process improvement",
    "stakeholder management", "strategy consulting",
    "change management", "gap analysis", "feasibility study",
    "business transformation", "erp implementation",
    "it consulting", "management consulting",

    # ── BPO & CUSTOMER SERVICE ────────────────────────────
    "customer support", "call center", "voice process",
    "non-voice process", "chat support", "email support",
    "kpi", "sla", "csat", "nps", "helpdesk", "zendesk",
    "freshdesk", "ticketing system", "escalation management",
    "data entry", "back office", "bpo operations",

    # ── AUTOMOBILE ────────────────────────────────────────
    "vehicle maintenance", "engine diagnostics", "auto repair",
    "spare parts", "transmission", "brake system",
    "electrical systems", "ac service", "wheel alignment",
    "tire fitting", "oil change", "warranty claims",
    "service advisor", "workshop management", "obd",
    "automobile engineering", "ev", "hybrid vehicles",

]


def extract_skills(text):
    text = text.lower()
    found_skills = []

    for skill in KNOWN_SKILLS:
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text):
            found_skills.append(skill)

    return list(set(found_skills))
