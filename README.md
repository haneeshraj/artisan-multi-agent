# 🔧 A.R.T.I.S.A.N.

**Automated Resume Tailoring & Intelligent Selection Agent Network**

A multi-agent, LLM-powered application designed to transform how IT professionals approach job applications.

## 🧠 Project Description

**A.R.T.I.S.A.N.** combines a centralized profile, real-time job description extraction, large language models, and iterative evaluation to auto-generate customized, ATS-friendly resumes tailored to each job posting with full transparency and control.

By orchestrating specialized agents for scraping, resume content generation, iterative evaluation, automated script creation, and document building, this system eliminates repetitive manual tailoring and empowers users with intelligent, data-driven decisions.

## 🎯 Key Objectives

- Maintain a centralized, structured profile of your **education, experience, skills, projects**, and other relevant details
- Extract detailed job information dynamically, parsing key sections such as company overview, responsibilities, requirements, perks, location, and pay
- Generate multiple role-specific resume drafts from your profile aligned to the job description
- Perform automatic evaluation and scoring of these drafts via an intelligent, rubric-driven LLM agent
- Automatically generate Python code via an LLM that leverages document creation libraries to build a polished resume in Word format
- Export only the best iteration of the resume while keeping a full log of all generated drafts and evaluation results
- Enable flexible configuration of iteration counts, models, tone, resume styles, and output formats
- Provide both a command-line interface for power users and an optional Electron GUI for easier interaction

## 🧩 Core Architecture

### Input Layer

User information is stored in a structured format, editable either through CLI JSON input or via the optional Electron UI, containing all relevant IT-focused personal data.

### Agent 1: Web Scraper & Job Parser

Extracts structured details from job postings including company information, responsibilities, required skills, perks, location, and compensation details. Utilizes APIs and adaptable scraping templates to support multiple popular job platforms.

### Agent 2: Resume Content Generator

Generates multiple tailored resume drafts using large language models with customizable prompting to produce coherent, relevant resume content variations focused on different aspects such as skills, projects, or experience.

### Agent 3: LLM Evaluator

Reviews all generated resume drafts against a strict rubric emphasizing keyword matching, role relevance, ATS compliance, and structure quality. Assigns scores, selects the best draft, and provides transparent justifications.

### Agent 4: Python Script Generator

Dynamically creates the Python script necessary to build the resume document based on the selected draft, supporting styling templates and multiple export formats.

### Agent 5: Resume Builder

Executes the generated Python script to produce the final formatted resume document with comprehensive logs of all iterations and evaluations.

## 🛠️ Configuration System

A YAML-based configuration controls:

- LLM models for different components
- Number of resume draft iterations
- Preferred resume tone and style
- Output formats (Word, PDF)
- Logging preferences

## 🧰 Features

- **CLI-first with Optional GUI**: Tailored for developers with an optional Electron interface
- **Complete Iteration Transparency**: Save all resume drafts, job details, evaluation metrics, and script versions
- **Success Likelihood Scoring**: Quantifies how well each resume draft matches the job posting
- **Modular Resume Templates**: Easily switch styles and layouts
- **Keyword Highlighting for ATS**: Optimization for automated resume filters

## 📊 Typical Workflow

1. Enter or update your personal IT profile
2. Submit a job posting URL for scraping and parsing
3. Generate multiple tailored resume drafts
4. Evaluate all drafts to identify the strongest candidate
5. Automatically generate and execute a Python script to build the final resume
6. Review the generated resume and all iteration logs
7. Export the resume in Word or PDF formats

## 🔐 Privacy & Data Control

- All personal information is stored locally
- LLM queries can be toggled on/off or routed through local models
- Optional encryption of data for confidentiality

## Project Structure

```
ai-artisan/
├── data/
│   ├── job-data/                # Generated resume content and evaluations per job
│   │   └── [job_title_timestamp]/
│   │       ├── strategies.md    # AI-generated resume strategies
│   │       ├── version_0/       # Initial resume generation
│   │       │   ├── resume_1.md  # Strategy 1 resume
│   │       │   ├── resume_2.md  # Strategy 2 resume
│   │       │   ├── ...
│   │       │   └── evaluation.md # Comprehensive evaluation results
│   │       ├── version_1/       # Improved iteration
│   │       └── version_2/       # Further improvements
│   ├── scraped-data/            # Raw job listings from various platforms
│   │   ├── raw-json/            # Raw job listings in JSON format
│   │   └── raw-md/              # Raw job listings in Markdown format
│   └── profile-data/            # User profile information
│       ├── gen/                 # Profile generator web application
│       │   ├── templates/       # HTML templates for the profile form
│       │   └── profile-gen.py   # Flask application for profile collection
│       └── profiles/            # User profile storage
│           ├── json/            # Profiles in JSON format
│           └── md/              # Profiles in Markdown format
├── llm/                         # LLM integration modules
│   ├── llm.py                   # Core LLM utility functions
│   └── agent/                   # Specialized AI agents
│       ├── content_gen.py       # Resume content generation agents
│       └── eval.py              # Resume evaluation agent
├── scraper/                     # Job listing scrapers for different platforms
│   ├── glassdoor_scraper.py     # Glassdoor job scraper
│   ├── indeed_scraper.py        # Indeed job scraper
│   ├── linkedin_scraper.py      # LinkedIn job scraper
│   ├── readerapi_scraper.py     # Generic web scraper via Reader API
│   └── selenium_driver.py       # Selenium utilities for scraping
├── utils/                       # Utility functions
│   ├── md_parser.py             # Markdown parsing utilities
│   └── md-json.py               # JSON conversion utilities
├── config.yaml                  # Configuration for LLM models and other settings
└── artisan-builder.py           # Main integration script
```

## Current Status

The project has reached a significant milestone with a **fully functional AI-powered resume generation and evaluation system**. The core pipeline is operational and can successfully create, evaluate, and iteratively improve multiple resume versions tailored to specific job postings.

### ✅ Job Scraping System

- **Multi-platform job scrapers** for LinkedIn, Indeed, and Glassdoor
- **Generic web scraping** capability via Reader API
- **Selenium-based extraction** with advanced stealth and anti-detection features
- **Structured data extraction** with consistent JSON and Markdown output formats

### ✅ User Profile Management

- **Interactive web form** for collecting comprehensive user profile data
- **Dynamic form sections** for education, experience, skills, projects, and certifications
- **Form state persistence** using localStorage for seamless user experience
- **JSON and Markdown output** for integration with resume generation process
- **Support for multiple industries** including various engineering disciplines

### ✅ Core Infrastructure

- **Command-line interface** with robust argument parsing and validation
- **Configuration system** using YAML for model selection and other settings
- **LLM integration** with support for multiple models and customization options
- **Error handling and logging** for reliable operation

### ✅ AI-Powered Resume Generation

- **Strategy Generation System** that analyzes job descriptions and creates diverse resume-tailoring strategies
- **Multi-Agent Content Generation** with specialized agents for different resume approaches
- **LLM-powered resume content creation** using models like GPT-4, Claude, and Gemini
- **Content validation and parsing** with Markdown code block extraction
- **Multiple resume iterations** per job posting with different strategic focuses

### ✅ Intelligent Evaluation System

- **Comprehensive resume evaluation** using AI agents with structured scoring rubrics
- **ATS Compatibility Analysis** (0-100 scoring) for resume parsing optimization
- **Structure Assessment** (0-100 scoring) for professional layout and organization
- **Job Keyword Matching** (0-100 scoring) for alignment with job requirements
- **Detailed feedback generation** with actionable improvement suggestions
- **Multi-resume comparative analysis** with ranking and average score calculations

### ✅ Iterative Improvement Pipeline

- **Version-controlled resume generation** with organized file structures
- **Feedback-driven improvement cycles** using evaluation results to enhance subsequent versions
- **Strategy-based content refinement** that maintains focus while addressing evaluation feedback
- **Automated iteration management** with configurable improvement rounds
- **Complete audit trail** of all generated content, evaluations, and improvements

### 🔄 In Progress

- Python script generation for document creation
- Final document building and export (Word/PDF)
- Enhanced ATS optimization features

### 📋 Usage Instructions

#### Profile Generation

```bash
pip install -r requirements.txt
cd data/profile-data/gen
python profile-gen.py
```

Then open your browser to http://127.0.0.1:5000 to access the profile form.

#### Job Scraping and Resume Generation

```bash
python artisan-builder.py --url "JOB_POSTING_URL" --profile "your_profile.md" --content-gen-model "gpt-4o-mini" --evaluation-model "claude-3-5-sonnet-20241022" --content-iter 5
```

**Example with specific parameters:**

```bash
python artisan-builder.py \
  --url "https://www.linkedin.com/jobs/view/1234567890" \
  --profile "test_profile_haneesh_raj.md" \
  --content-gen-model "gpt-4o-mini" \
  --evaluation-model "claude-3-5-sonnet-20241022" \
  --code-gen-model "gemini-2.0-flash-exp" \
  --output-format pdf \
  --content-iter 5
```

**What this does:**

1. **Scrapes** the job posting from the provided URL
2. **Generates strategic approaches** for tailoring your resume to the specific role
3. **Creates multiple resume versions** using different narrative strategies
4. **Evaluates each resume** with detailed ATS compatibility, structure, and keyword matching scores
5. **Iteratively improves** resume content based on evaluation feedback
6. **Saves all versions** with complete audit trails in organized folders

**Generated Output Structure:**

```
data/job-data/linkedin_[JobTitle]_[Timestamp]/
├── strategies.md           # AI-generated tailoring strategies
├── version_0/             # Initial generation
│   ├── resume_1.md        # Strategy 1: Technical focus
│   ├── resume_2.md        # Strategy 2: Leadership focus
│   ├── resume_3.md        # Strategy 3: Project innovation
│   ├── resume_4.md        # Strategy 4: Research focus
│   ├── resume_5.md        # Strategy 5: Industry expertise
│   └── evaluation.md      # Comprehensive scoring and feedback
├── version_1/             # First improvement iteration
│   ├── resume_1.md        # Improved based on feedback
│   ├── ...
│   └── evaluation.md
└── version_2/             # Second improvement iteration
    ├── resume_1.md        # Further refined content
    ├── ...
    └── evaluation.md
```

## 🌱 Future Roadmap

### Immediate Next Steps

- **Document Export System**: PDF and Word document generation from optimized resume content
- **Advanced ATS Optimization**: Enhanced keyword density analysis and formatting recommendations
- **Performance Analytics**: Success tracking and job application outcome correlation

### Extended Features

- **CV Generator**: Create tailored CVs focused on academic and research profiles
- **Cover Letter Generation**: Automated cover letter creation aligned with resume content
- **Interview Question Generator**: Generate role-specific interview questions based on resume content
- **Multi-Language Support**: Generate resumes in different languages for international opportunities

### Technical Enhancements

- **GUI Development**: Electron-based desktop application for non-technical users
- **API Integration**: Direct integration with job board APIs for real-time job matching
- **Local LLM Support**: Integration with locally-hosted language models for privacy-focused users
- **Resume Templates**: Multiple professional template options with industry-specific designs

## Technologies

- **Backend**: Python with Flask
- **Web Scraping**: Selenium for dynamic content extraction
- **LLM Integration**: APIs for various language models
- **Data Storage**: JSON and Markdown formats
- **Document Generation**: Python libraries for Word/PDF creation
- **UI**: HTML, Bootstrap, optional Electron

---

**Note**: This project is currently in development. Features and architecture are subject to change.
