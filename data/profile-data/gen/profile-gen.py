import os
import json
import uuid
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'resume_profile_builder_secret_key'

# Ensure directories exist
def ensure_directories():
    profiles_json_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                   "profiles", "json")
    profiles_md_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                                 "profiles", "md")
    
    os.makedirs(profiles_json_dir, exist_ok=True)
    os.makedirs(profiles_md_dir, exist_ok=True)
    
    return profiles_json_dir, profiles_md_dir

# Convert JSON to Markdown
def convert_to_markdown(data):
    md_content = f"# {data['personal_info']['first_name']} {data['personal_info']['last_name']}\n\n"
    
    # Personal Information
    md_content += "## Personal Information\n\n"
    md_content += f"- **Email:** {data['personal_info']['email']}\n"
    md_content += f"- **Phone:** {data['personal_info']['phone']}\n"
    md_content += f"- **Location:** {data['personal_info']['location']}\n"
    md_content += f"- **LinkedIn:** {data['personal_info']['linkedin']}\n"
    md_content += f"- **GitHub:** {data['personal_info']['github']}\n"
    md_content += f"- **Role:** {data['personal_info']['role']}\n\n"
    
    # Summary
    md_content += "## Summary\n\n"
    md_content += f"{data['personal_info']['summary']}\n\n"
    
    # Education
    md_content += "## Education\n\n"
    for edu in data['education']:
        md_content += f"### {edu['institute']}\n"
        md_content += f"**{edu['field']}**  \n"
        md_content += f"{edu['start_date']} - {edu['graduation_date']}  \n\n"
    
    # Skills
    md_content += "## Skills\n\n"
    skill_categories = {}
    for skill in data['skills']:
        category = skill['category']
        if category not in skill_categories:
            skill_categories[category] = []
        skill_categories[category].append(f"{skill['name']} ({skill['proficiency']})")
    
    for category, skills in skill_categories.items():
        md_content += f"### {category}\n"
        for skill in skills:
            md_content += f"- {skill}\n"
        md_content += "\n"
    
    # Experience
    if data['experience'] and len(data['experience']) > 0:
        md_content += "## Experience\n\n"
        for exp in data['experience']:
            md_content += f"### {exp['position']} | {exp['company']}\n"
            md_content += f"**{exp['start_date']} - {exp['end_date']}** | {exp['location']}\n\n"
            for resp in exp['responsibilities'].split('\n'):
                if resp.strip():
                    md_content += f"- {resp.strip()}\n"
            md_content += "\n"
    
    # Projects
    md_content += "## Projects\n\n"
    for proj in data['projects']:
        md_content += f"### {proj['name']}\n"
        md_content += f"**{proj['start_date']} - {proj['end_date']}**\n\n"
        for detail in proj['description'].split('\n'):
            if detail.strip():
                md_content += f"- {detail.strip()}\n"
        if proj['link']:
            md_content += f"\n[Project Link]({proj['link']})\n"
        md_content += "\n"
    
    # Certifications
    if data['certifications'] and len(data['certifications']) > 0:
        md_content += "## Certifications\n\n"
        for cert in data['certifications']:
            md_content += f"- **{cert['name']}** - {cert['company']}\n"
        md_content += "\n"
    
    # Important Information
    md_content += "## Additional Information\n\n"
    md_content += f"- **Industry:** {data['important_info']['industry']}\n"
    md_content += f"- **Target Role:** {data['important_info']['role']}\n"
    
    return md_content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Collect form data
            data = {
                "personal_info": {
                    "first_name": request.form['first_name'],
                    "last_name": request.form['last_name'],
                    "email": request.form['email'],
                    "phone": request.form['phone'],
                    "location": request.form['location'],
                    "linkedin": request.form['linkedin'],
                    "github": request.form['github'],
                    "role": request.form['role'],
                    "summary": request.form['summary']
                },
                "certifications": [],
                "education": [],
                "skills": [],
                "experience": [],
                "projects": [],
                "important_info": {
                    "industry": request.form['industry'],
                    "role": request.form['target_role']
                }
            }
            
            # Process certifications (dynamic fields)
            cert_count = int(request.form['cert_count'])
            for i in range(cert_count):
                if f'cert_name_{i}' in request.form and request.form[f'cert_name_{i}']:
                    data["certifications"].append({
                        "name": request.form[f'cert_name_{i}'],
                        "company": request.form[f'cert_company_{i}']
                    })
            
            # Process education (dynamic fields)
            edu_count = int(request.form['edu_count'])
            for i in range(edu_count):
                if f'edu_field_{i}' in request.form and request.form[f'edu_field_{i}']:
                    data["education"].append({
                        "field": request.form[f'edu_field_{i}'],
                        "institute": request.form[f'edu_institute_{i}'],
                        "start_date": request.form[f'edu_start_{i}'],
                        "graduation_date": request.form[f'edu_end_{i}']
                    })
            
            # Process skills (dynamic fields)
            skill_count = int(request.form['skill_count'])
            for i in range(skill_count):
                if f'skill_name_{i}' in request.form and request.form[f'skill_name_{i}']:
                    data["skills"].append({
                        "category": request.form[f'skill_category_{i}'],
                        "name": request.form[f'skill_name_{i}'],
                        "proficiency": request.form[f'skill_proficiency_{i}']
                    })
            
            # Process experience (dynamic fields)
            exp_count = int(request.form['exp_count'])
            for i in range(exp_count):
                if f'exp_position_{i}' in request.form and request.form[f'exp_position_{i}']:
                    data["experience"].append({
                        "position": request.form[f'exp_position_{i}'],
                        "company": request.form[f'exp_company_{i}'],
                        "responsibilities": request.form[f'exp_responsibilities_{i}'],
                        "location": request.form[f'exp_location_{i}'],
                        "start_date": request.form[f'exp_start_{i}'],
                        "end_date": request.form[f'exp_end_{i}'],
                        "link": request.form[f'exp_link_{i}'] if f'exp_link_{i}' in request.form else ""
                    })
            
            # Process projects (dynamic fields)
            proj_count = int(request.form['proj_count'])
            for i in range(proj_count):
                if f'proj_name_{i}' in request.form and request.form[f'proj_name_{i}']:
                    data["projects"].append({
                        "name": request.form[f'proj_name_{i}'],
                        "description": request.form[f'proj_description_{i}'],
                        "start_date": request.form[f'proj_start_{i}'],
                        "end_date": request.form[f'proj_end_{i}'],
                        "link": request.form[f'proj_link_{i}'] if f'proj_link_{i}' in request.form else ""
                    })
            
            # Generate file names with timestamp and name
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_name_base = f"{data['personal_info']['first_name'].lower()}_{data['personal_info']['last_name'].lower()}_{timestamp}"
            
            # Save as JSON
            profiles_json_dir, profiles_md_dir = ensure_directories()
            json_path = os.path.join(profiles_json_dir, f"{file_name_base}.json")
            with open(json_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            # Convert to Markdown and save
            md_content = convert_to_markdown(data)
            md_path = os.path.join(profiles_md_dir, f"{file_name_base}.md")
            with open(md_path, 'w') as f:
                f.write(md_content)
            
            flash(f"Profile saved successfully! JSON: {json_path}, Markdown: {md_path}", "success")
            return redirect(url_for('index'))
            
        except Exception as e:
            flash(f"Error saving profile: {str(e)}", "error")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
