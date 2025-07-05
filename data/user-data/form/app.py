"""
Resume Information Collection Web Form

This web application provides a form interface for collecting user resume information
and generating JSON and Markdown files for IT professionals or other industries.
"""

from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file
import os
import json
import time
from datetime import datetime
import uuid
import tempfile
from pathlib import Path

# Import custom filters
from filters import nl2br

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'ai_artisan_resume_builder_key'  # For session management
app.config['SESSION_TYPE'] = 'filesystem'

# Register custom filters
app.jinja_env.filters['nl2br'] = nl2br

# Define the base paths
BASE_DIR = Path(__file__).resolve().parent.parent
JSON_DIR = BASE_DIR / "profiles" / "json"
MD_DIR = BASE_DIR / "profiles" / "md"

# Ensure the output directories exist
JSON_DIR.mkdir(parents=True, exist_ok=True)
MD_DIR.mkdir(parents=True, exist_ok=True)

@app.route('/')
def index():
    """Render the home page."""
    return render_template('index.html')

@app.route('/form/personal', methods=['GET', 'POST'])
def personal_info():
    """Handle personal information form."""
    if request.method == 'POST':
        session['personal_info'] = {
            "full_name": request.form['full_name'],
            "professional_title": request.form['professional_title'],
            "phone": request.form['phone'],
            "email": request.form['email'],
            "location": {
                "city": request.form['city'],
                "state": request.form['state'],
                "country": request.form['country']
            }
        }
        return redirect(url_for('online_presence'))
    
    # Pre-fill form if data exists in session
    personal_data = session.get('personal_info', {})
    return render_template('personal_info.html', data=personal_data)

@app.route('/form/online-presence', methods=['GET', 'POST'])
def online_presence():
    """Handle online presence form."""
    if request.method == 'POST':
        online_presence = {
            "linkedin": request.form['linkedin'],
            "portfolio": request.form['portfolio'],
            "github": request.form['github']
        }
        
        # Process additional profiles
        additional_profiles = []
        platform_names = request.form.getlist('platform_name')
        platform_urls = request.form.getlist('platform_url')
        
        for i in range(len(platform_names)):
            if platform_names[i] and platform_urls[i]:
                additional_profiles.append({
                    "platform": platform_names[i],
                    "url": platform_urls[i]
                })
        
        if additional_profiles:
            online_presence["additional_profiles"] = additional_profiles
        
        session['online_presence'] = online_presence
        return redirect(url_for('professional_summary'))
    
    # Pre-fill form if data exists in session
    online_data = session.get('online_presence', {})
    return render_template('online_presence.html', data=online_data)

@app.route('/form/professional-summary', methods=['GET', 'POST'])
def professional_summary():
    """Handle professional summary form."""
    if request.method == 'POST':
        session['professional_summary'] = {
            "career_objective": request.form['career_objective'],
            "summary": request.form['summary'],
            "key_achievements": request.form['key_achievements']
        }
        return redirect(url_for('skills'))
    
    # Pre-fill form if data exists in session
    summary_data = session.get('professional_summary', {})
    return render_template('professional_summary.html', data=summary_data)

@app.route('/form/skills', methods=['GET', 'POST'])
def skills():
    """Handle skills form."""
    skill_categories = [
        ("Programming Languages", "languages"),
        ("Frameworks", "frameworks"),
        ("Tools", "tools"),
        ("Cloud Platforms", "cloud_platforms"),
        ("Databases", "databases"),
        ("Libraries", "libraries"),
        ("Other Technical Skills", "technical_skills")
    ]
    
    if request.method == 'POST':
        skills_data = {}
        
        for display_name, key in skill_categories:
            skill_names = request.form.getlist(f'{key}_name')
            skill_proficiencies = request.form.getlist(f'{key}_proficiency')
            
            skills_data[key] = []
            for i in range(len(skill_names)):
                if skill_names[i]:
                    skill_item = {"name": skill_names[i]}
                    if skill_proficiencies[i]:
                        skill_item["proficiency"] = skill_proficiencies[i]
                    skills_data[key].append(skill_item)
        
        session['skills'] = skills_data
        return redirect(url_for('education'))
    
    # Pre-fill form if data exists in session
    skills_data = session.get('skills', {})
    return render_template('skills.html', categories=skill_categories, data=skills_data)

@app.route('/form/education', methods=['GET', 'POST'])
def education():
    """Handle education form."""
    if request.method == 'POST':
        # Extract education entries from form
        degrees = request.form.getlist('degree')
        institutions = request.form.getlist('institution')
        locations = request.form.getlist('location')
        graduation_dates = request.form.getlist('graduation_date')
        gpas = request.form.getlist('gpa')
        
        # Extract highlights (multi-dimensional array)
        highlights_per_education = request.form.getlist('highlights')
        
        education_data = []
        
        for i in range(len(degrees)):
            if degrees[i]:  # Only process if degree is provided
                edu_entry = {
                    "degree": degrees[i],
                    "institution": institutions[i],
                    "location": locations[i],
                    "graduation_date": graduation_dates[i],
                    "gpa": gpas[i] if gpas[i] else None,
                    "highlights": []
                }
                
                # Process highlights for this education entry
                if i < len(highlights_per_education):
                    highlights = highlights_per_education[i].split('\n')
                    edu_entry["highlights"] = [h for h in highlights if h.strip()]
                
                education_data.append(edu_entry)
        
        session['education'] = education_data
        return redirect(url_for('projects'))
    
    # Pre-fill form if data exists in session
    education_data = session.get('education', [])
    return render_template('education.html', data=education_data)

@app.route('/form/projects', methods=['GET', 'POST'])
def projects():
    """Handle projects form."""
    if request.method == 'POST':
        # Extract project entries from form
        names = request.form.getlist('name')
        descriptions = request.form.getlist('description')
        technologies = request.form.getlist('technologies')
        urls = request.form.getlist('url')
        start_dates = request.form.getlist('start_date')
        end_dates = request.form.getlist('end_date')
        
        # Extract highlights (multi-dimensional array)
        highlights_per_project = request.form.getlist('highlights')
        
        projects_data = []
        
        for i in range(len(names)):
            if names[i]:  # Only process if name is provided
                tech_list = [t.strip() for t in technologies[i].split(',')]
                
                project_entry = {
                    "name": names[i],
                    "description": descriptions[i],
                    "technologies": tech_list,
                    "url": urls[i] if urls[i] else None,
                    "start_date": start_dates[i],
                    "end_date": end_dates[i],
                    "highlights": []
                }
                
                # Process highlights for this project entry
                if i < len(highlights_per_project):
                    highlights = highlights_per_project[i].split('\n')
                    project_entry["highlights"] = [h for h in highlights if h.strip()]
                
                projects_data.append(project_entry)
        
        session['projects'] = projects_data
        return redirect(url_for('experience'))
    
    # Pre-fill form if data exists in session
    projects_data = session.get('projects', [])
    return render_template('projects.html', data=projects_data)

@app.route('/form/experience', methods=['GET', 'POST'])
def experience():
    """Handle professional experience form."""
    if request.method == 'POST':
        # Extract experience entries from form
        positions = request.form.getlist('position')
        companies = request.form.getlist('company')
        locations = request.form.getlist('location')
        start_dates = request.form.getlist('start_date')
        end_dates = request.form.getlist('end_date')
        
        # Extract responsibilities (multi-dimensional array)
        responsibilities_per_job = request.form.getlist('responsibilities')
        
        experience_data = []
        
        for i in range(len(positions)):
            if positions[i]:  # Only process if position is provided
                exp_entry = {
                    "position": positions[i],
                    "company": companies[i],
                    "location": locations[i],
                    "start_date": start_dates[i],
                    "end_date": end_dates[i],
                    "responsibilities": []
                }
                
                # Process responsibilities for this experience entry
                if i < len(responsibilities_per_job):
                    responsibilities = responsibilities_per_job[i].split('\n')
                    exp_entry["responsibilities"] = [r for r in responsibilities if r.strip()]
                
                experience_data.append(exp_entry)
        
        session['professional_experience'] = experience_data
        return redirect(url_for('additional_info'))
    
    # Pre-fill form if data exists in session
    experience_data = session.get('professional_experience', [])
    return render_template('experience.html', data=experience_data)

@app.route('/form/additional-info', methods=['GET', 'POST'])
def additional_info():
    """Handle additional information form."""
    if request.method == 'POST':
        additional_info = {}
        
        # Certifications
        if 'has_certifications' in request.form:
            cert_names = request.form.getlist('cert_name')
            cert_issuers = request.form.getlist('cert_issuer')
            cert_dates = request.form.getlist('cert_date')
            cert_expires = request.form.getlist('cert_expires')
            
            certs = []
            for i in range(len(cert_names)):
                if cert_names[i]:
                    certs.append({
                        "name": cert_names[i],
                        "issuer": cert_issuers[i],
                        "date": cert_dates[i],
                        "expires": cert_expires[i]
                    })
            
            if certs:
                additional_info["certifications"] = certs
        
        # Languages
        if 'has_languages' in request.form:
            lang_names = request.form.getlist('language')
            lang_proficiencies = request.form.getlist('language_proficiency')
            
            languages = []
            for i in range(len(lang_names)):
                if lang_names[i]:
                    languages.append({
                        "language": lang_names[i],
                        "proficiency": lang_proficiencies[i]
                    })
            
            if languages:
                additional_info["languages"] = languages
        
        # Industry (for non-IT professionals)
        if request.form.get('is_it_professional') == 'no':
            additional_info["industry"] = request.form.get('industry', '')
        
        # Other additional information
        if request.form.get('has_other_info') == 'yes':
            additional_info["other"] = request.form.get('other_info', '')
        
        session['additional_info'] = additional_info
        return redirect(url_for('preview'))
    
    # Pre-fill form if data exists in session
    additional_data = session.get('additional_info', {})
    return render_template('additional_info.html', data=additional_data)

@app.route('/preview', methods=['GET', 'POST'])
def preview():
    """Preview the resume data before final submission."""
    # Collect all resume data from session
    resume_data = {
        "personal_info": session.get('personal_info', {}),
        "online_presence": session.get('online_presence', {}),
        "professional_summary": session.get('professional_summary', {}),
        "skills": session.get('skills', {}),
        "education": session.get('education', []),
        "projects": session.get('projects', []),
        "professional_experience": session.get('professional_experience', []),
        "additional_info": session.get('additional_info', {})
    }
    
    if request.method == 'POST':
        # Add metadata
        resume_data["metadata"] = {
            "generated_at": datetime.now().isoformat(),
            "version": "1.0"
        }
        
        # Generate files
        json_path, md_path = generate_resume_files(resume_data)
        
        # Store paths for the success page
        session['json_path'] = json_path
        session['md_path'] = md_path
        
        # Clear the form data from session
        session['form_completed'] = True
        
        return redirect(url_for('success'))
    
    return render_template('preview.html', data=resume_data)

@app.route('/edit/<section>')
def edit_section(section):
    """Redirect to a specific section for editing."""
    section_routes = {
        'personal_info': 'personal',
        'online_presence': 'online-presence',
        'professional_summary': 'professional-summary',
        'skills': 'skills',
        'education': 'education',
        'projects': 'projects',
        'professional_experience': 'experience',
        'additional_info': 'additional-info'
    }
    
    if section in section_routes:
        return redirect(url_for(section_routes[section]))
    else:
        flash('Invalid section')
        return redirect(url_for('preview'))

@app.route('/success')
def success():
    """Display success page after resume generation."""
    if not session.get('form_completed'):
        return redirect(url_for('index'))
    
    json_path = session.get('json_path', '')
    md_path = session.get('md_path', '')
    
    return render_template('success.html', json_path=json_path, md_path=md_path)

@app.route('/download/<file_type>')
def download(file_type):
    """Download the generated resume file."""
    if file_type == 'json':
        path = session.get('json_path', '')
        if not path or not os.path.exists(path):
            flash('JSON file not found')
            return redirect(url_for('success'))
        return send_file(path, as_attachment=True)
    
    elif file_type == 'md':
        path = session.get('md_path', '')
        if not path or not os.path.exists(path):
            flash('Markdown file not found')
            return redirect(url_for('success'))
        return send_file(path, as_attachment=True)
    
    else:
        flash('Invalid file type')
        return redirect(url_for('success'))

@app.route('/reset')
def reset():
    """Reset the form and start over."""
    # Clear session data
    session.clear()
    return redirect(url_for('index'))

def generate_resume_files(data):
    """Generate JSON and Markdown files."""
    # Create sanitized filename from the user's name and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_name = data["personal_info"]["full_name"].lower().replace(" ", "_")
    base_filename = f"{sanitized_name}_{timestamp}"
    
    # Define file paths
    json_path = str(JSON_DIR / f"{base_filename}.json")
    md_path = str(MD_DIR / f"{base_filename}.md")
    
    # Save JSON file
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Generate Markdown content
    md_content = []
    
    # Header
    md_content.append(f"# {data['personal_info']['full_name']}")
    md_content.append(f"## {data['personal_info']['professional_title']}")
    md_content.append("")
    
    # Contact and online presence
    contact_line = [
        f"📍 {data['personal_info']['location']['city']}, {data['personal_info']['location']['state']}, {data['personal_info']['location']['country']}",
        f"📞 {data['personal_info']['phone']}",
        f"📧 {data['personal_info']['email']}"
    ]
    md_content.append(" | ".join(contact_line))
    md_content.append("")
    
    online_line = []
    if data['online_presence'].get('linkedin'):
        online_line.append(f"[LinkedIn]({data['online_presence']['linkedin']})")
    if data['online_presence'].get('github'):
        online_line.append(f"[GitHub]({data['online_presence']['github']})")
    if data['online_presence'].get('portfolio'):
        online_line.append(f"[Portfolio]({data['online_presence']['portfolio']})")
    
    if 'additional_profiles' in data['online_presence']:
        for profile in data['online_presence']['additional_profiles']:
            online_line.append(f"[{profile['platform']}]({profile['url']})")
    
    if online_line:
        md_content.append(" | ".join(online_line))
        md_content.append("")
    
    # Professional Summary
    md_content.append("## Professional Summary")
    md_content.append(data['professional_summary']['summary'])
    md_content.append("")
    md_content.append("### Career Objective")
    md_content.append(data['professional_summary']['career_objective'])
    md_content.append("")
    md_content.append("### Key Achievements")
    md_content.append(data['professional_summary']['key_achievements'])
    md_content.append("")
    
    # Skills
    md_content.append("## Skills & Expertise")
    
    skill_categories = {
        "Programming Languages": "languages",
        "Frameworks": "frameworks",
        "Tools": "tools",
        "Cloud Platforms": "cloud_platforms",
        "Databases": "databases",
        "Libraries": "libraries",
        "Other Technical Skills": "technical_skills"
    }
    
    for display_name, key in skill_categories.items():
        if data['skills'].get(key) and len(data['skills'][key]) > 0:
            md_content.append(f"### {display_name}")
            skills_list = []
            for skill in data['skills'][key]:
                if isinstance(skill, dict):
                    if 'proficiency' in skill:
                        skills_list.append(f"{skill['name']} ({skill['proficiency']})")
                    else:
                        skills_list.append(skill['name'])
                else:
                    skills_list.append(skill)
            md_content.append("- " + "\n- ".join(skills_list))
            md_content.append("")
    
    # Education
    if data['education']:
        md_content.append("## Education")
        for edu in data['education']:
            md_content.append(f"### {edu['degree']}")
            md_content.append(f"**{edu['institution']}** - {edu['location']} ({edu['graduation_date']})")
            if edu.get('gpa'):
                md_content.append(f"GPA: {edu['gpa']}")
            
            if edu['highlights']:
                md_content.append("\n**Highlights:**")
                for highlight in edu['highlights']:
                    md_content.append(f"- {highlight}")
            md_content.append("")
    
    # Professional Experience
    if data['professional_experience']:
        md_content.append("## Professional Experience")
        for exp in data['professional_experience']:
            md_content.append(f"### {exp['position']}")
            md_content.append(f"**{exp['company']}** - {exp['location']} ({exp['start_date']} - {exp['end_date']})")
            
            if exp['responsibilities']:
                md_content.append("")
                for resp in exp['responsibilities']:
                    md_content.append(f"- {resp}")
            md_content.append("")
    
    # Projects
    if data['projects']:
        md_content.append("## Projects")
        for project in data['projects']:
            md_content.append(f"### {project['name']}")
            md_content.append(f"**Duration:** {project['start_date']} - {project['end_date']}")
            if project.get('url'):
                md_content.append(f"**URL:** [{project['url']}]({project['url']})")
            
            md_content.append(f"\n{project['description']}\n")
            
            md_content.append("**Technologies:** " + ", ".join(project['technologies']))
            
            if project['highlights']:
                md_content.append("\n**Key Highlights:**")
                for highlight in project['highlights']:
                    md_content.append(f"- {highlight}")
            md_content.append("")
    
    # Additional Information
    if data['additional_info']:
        md_content.append("## Additional Information")
        
        if 'certifications' in data['additional_info']:
            md_content.append("### Certifications")
            for cert in data['additional_info']['certifications']:
                md_content.append(f"- **{cert['name']}** - {cert['issuer']} ({cert['date']} - {cert['expires']})")
            md_content.append("")
        
        if 'languages' in data['additional_info']:
            md_content.append("### Languages")
            for lang in data['additional_info']['languages']:
                md_content.append(f"- {lang['language']} ({lang['proficiency']})")
            md_content.append("")
        
        if 'industry' in data['additional_info']:
            md_content.append(f"### Industry Focus: {data['additional_info']['industry']}")
            md_content.append("")
        
        if 'other' in data['additional_info']:
            md_content.append("### Other Information")
            md_content.append(data['additional_info']['other'])
    
    # Save the markdown file
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md_content))
    
    return json_path, md_path

if __name__ == '__main__':
    app.run(debug=True)
