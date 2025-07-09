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
│   ├── processed-data/          # Normalized and processed data
│   │   ├── json/                # Processed job listings in JSON format
│   │   └── md/                  # Processed job listings in Markdown format
│   ├── scraped-data/            # Raw job listings from various platforms
│   │   ├── raw-json/            # Raw job listings in JSON format
│   │   └── raw-md/              # Raw job listings in Markdown format
│   ├── profile-data/            # User profile information
│       ├── gen/                 # Profile generator web application
│       │   ├── templates/       # HTML templates for the profile form
│       │   └── profile-gen.py   # Flask application for profile collection
│       └── profiles/            # User profile storage
│           ├── json/            # Profiles in JSON format
│           └── md/              # Profiles in Markdown format
├── llm/                         # LLM integration modules
│   ├── llm.py                   # Core LLM utility functions
│   └── content-gen.py           # Resume content generation
├── scraper/                     # Job listing scrapers for different platforms
│   ├── glassdoor_scraper.py     # Glassdoor job scraper
│   ├── indeed_scraper.py        # Indeed job scraper
│   ├── linkedin_scraper.py      # LinkedIn job scraper
│   ├── readerapi_scraper.py     # Generic web scraper via Reader API
│   └── selenium_driver.py       # Selenium utilities for scraping
├── config.yaml                  # Configuration for LLM models and other settings
└── artisan-builder.py           # Main integration script
```

## Current Status

The project is under active development with the following components implemented:

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

### 🔄 In Progress

- Resume content generation using LLMs
- Resume evaluation and scoring system
- Python script generation for document creation
- Final document building and export

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
python artisan-builder.py --url "JOB_POSTING_URL" --profile "your_profile.json" --content-gen-model "gpt-4.1-mini" --evaluation-model "claude-3-opus" --code-gen-model "gemini-2.5-pro" --output-format pdf
```

- Job scraping modules for major platforms
- User profile data collection web form
- Data storage structures

Integration of AI components, evaluation systems, and resume generation are planned for future development.

## 🌱 Future Roadmap

- **CV Generator**: Create tailored CVs focused on academic and research profiles
- **Interview Question Generator**: Generate role-specific interview questions
- **Modular AI agent extensions**: Add-ons for grammar polishing, tone adjustment, and cover letter generation

## Technologies

- **Backend**: Python with Flask
- **Web Scraping**: Selenium for dynamic content extraction
- **LLM Integration**: APIs for various language models
- **Data Storage**: JSON and Markdown formats
- **Document Generation**: Python libraries for Word/PDF creation
- **UI**: HTML, Bootstrap, optional Electron

---

**Note**: This project is currently in development. Features and architecture are subject to change.
