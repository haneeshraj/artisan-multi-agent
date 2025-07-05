"""
Resume Information Collection Form

This script provides a command-line interface for collecting user resume information
and generating JSON and Markdown files for IT professionals or other industries.
"""

import os
import json
import time
from datetime import datetime

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"{title:^60}")
    print("=" * 60 + "\n")

def get_input(prompt, required=True, multiline=False):
    """Get user input with validation for required fields."""
    while True:
        if multiline:
            print(f"{prompt} (Enter multiple lines, type 'DONE' on a new line when finished):")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == 'DONE':
                    break
                lines.append(line)
            value = "\n".join(lines)
        else:
            value = input(f"{prompt}: ").strip()
        
        if required and not value:
            print("⚠️ This field is required. Please try again.")
            continue
        return value

def get_yes_no_input(prompt):
    """Get a yes/no response from the user."""
    while True:
        response = input(f"{prompt} (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("⚠️ Please enter 'y' for Yes or 'n' for No.")

def collect_personal_info():
    """Collect personal information."""
    print_header("PERSONAL INFORMATION")
    
    personal_info = {
        "full_name": get_input("Full Name"),
        "professional_title": get_input("Professional Title"),
        "phone": get_input("Phone Number"),
        "email": get_input("Email"),
        "location": {
            "city": get_input("City"),
            "state": get_input("State/Province"),
            "country": get_input("Country")
        }
    }
    
    return personal_info

def collect_online_presence():
    """Collect online presence information."""
    print_header("ONLINE PRESENCE")
    
    online_presence = {
        "linkedin": get_input("LinkedIn Profile URL", required=False),
        "portfolio": get_input("Portfolio Website", required=False),
        "github": get_input("GitHub Profile", required=False)
    }
    
    # Ask for additional social/professional profiles
    additional_profiles = []
    while True:
        platform = get_input("Additional Platform Name (or leave blank to continue)", required=False)
        if not platform:
            break
        url = get_input(f"{platform} URL")
        additional_profiles.append({"platform": platform, "url": url})
    
    if additional_profiles:
        online_presence["additional_profiles"] = additional_profiles
    
    return online_presence

def collect_professional_summary():
    """Collect professional summary information."""
    print_header("PROFESSIONAL SUMMARY")
    
    professional_summary = {
        "career_objective": get_input("Career Objective", multiline=True),
        "summary": get_input("Professional Summary (2-3 sentences about your career goals and how you plan to contribute)", multiline=True),
        "key_achievements": get_input("Key Achievements (2-3 lines summarizing your key achievements)", multiline=True)
    }
    
    return professional_summary

def collect_skills():
    """Collect skills information."""
    print_header("SKILLS & EXPERTISE")
    
    skills = {
        "technical_skills": [],
        "languages": [],
        "frameworks": [],
        "tools": [],
        "cloud_platforms": [],
        "databases": [],
        "libraries": []
    }
    
    categories = [
        ("Programming Languages", "languages"),
        ("Frameworks", "frameworks"),
        ("Tools", "tools"),
        ("Cloud Platforms", "cloud_platforms"),
        ("Databases", "databases"),
        ("Libraries", "libraries"),
        ("Other Technical Skills", "technical_skills")
    ]
    
    for display_name, key in categories:
        print(f"\n{display_name}:")
        print("Enter skills one by one. Leave blank when done.")
        
        items = []
        while True:
            item = get_input(f"- Add {display_name[:-1] if display_name.endswith('s') else display_name}", required=False)
            if not item:
                break
            
            # Optionally collect proficiency level
            if get_yes_no_input(f"Would you like to specify proficiency level for '{item}'?"):
                proficiency = get_input("Proficiency (e.g., Beginner, Intermediate, Advanced, Expert)")
                items.append({"name": item, "proficiency": proficiency})
            else:
                items.append({"name": item})
        
        if items:
            skills[key] = items
    
    return skills

def collect_education():
    """Collect education information."""
    print_header("EDUCATION")
    
    education = []
    
    while True:
        print("\nEnter education details (leave degree blank when done):")
        degree = get_input("Degree/Certificate", required=False)
        if not degree:
            break
        
        education_entry = {
            "degree": degree,
            "institution": get_input("Institution"),
            "location": get_input("Location"),
            "graduation_date": get_input("Graduation Date (Month Year)"),
            "gpa": get_input("GPA (optional)", required=False),
            "highlights": []
        }
        
        # Collect achievements or highlights
        print("Enter academic achievements or highlights (leave blank when done):")
        while True:
            highlight = get_input("- Achievement/Highlight", required=False)
            if not highlight:
                break
            education_entry["highlights"].append(highlight)
        
        education.append(education_entry)
    
    return education

def collect_projects():
    """Collect projects information."""
    print_header("PROJECTS")
    
    projects = []
    
    while True:
        print("\nEnter project details (leave project name blank when done):")
        name = get_input("Project Name", required=False)
        if not name:
            break
        
        project = {
            "name": name,
            "description": get_input("Project Description", multiline=True),
            "technologies": get_input("Technologies Used").split(", "),
            "url": get_input("Project URL (optional)", required=False),
            "start_date": get_input("Start Date (Month Year)"),
            "end_date": get_input("End Date (Month Year or 'Present')"),
            "highlights": []
        }
        
        # Collect key highlights
        print("Enter key highlights or achievements for this project:")
        while True:
            highlight = get_input("- Highlight", required=False)
            if not highlight:
                break
            project["highlights"].append(highlight)
        
        projects.append(project)
    
    return projects

def collect_professional_experience():
    """Collect professional experience information."""
    print_header("PROFESSIONAL EXPERIENCE")
    
    experience = []
    
    while True:
        print("\nEnter professional experience details (leave position blank when done):")
        position = get_input("Position/Title", required=False)
        if not position:
            break
        
        exp = {
            "position": position,
            "company": get_input("Company"),
            "location": get_input("Location"),
            "start_date": get_input("Start Date (Month Year)"),
            "end_date": get_input("End Date (Month Year or 'Present')"),
            "responsibilities": []
        }
        
        # Collect responsibilities and achievements
        print("Enter responsibilities and achievements (use action verbs, quantify impact):")
        while True:
            resp = get_input("- Responsibility/Achievement", required=False)
            if not resp:
                break
            exp["responsibilities"].append(resp)
        
        experience.append(exp)
    
    return experience

def collect_additional_info():
    """Collect additional information."""
    print_header("ADDITIONAL INFORMATION")
    
    additional_info = {}
    
    if get_yes_no_input("Would you like to add certifications?"):
        certs = []
        while True:
            cert_name = get_input("Certification Name", required=False)
            if not cert_name:
                break
            cert = {
                "name": cert_name,
                "issuer": get_input("Issuing Organization"),
                "date": get_input("Date Earned (Month Year)"),
                "expires": get_input("Expiration Date (Month Year or 'No Expiration')")
            }
            certs.append(cert)
        
        if certs:
            additional_info["certifications"] = certs
    
    if get_yes_no_input("Would you like to add languages spoken?"):
        languages = []
        while True:
            lang = get_input("Language", required=False)
            if not lang:
                break
            proficiency = get_input("Proficiency (e.g., Native, Fluent, Intermediate, Basic)")
            languages.append({"language": lang, "proficiency": proficiency})
        
        if languages:
            additional_info["languages"] = languages
    
    # For non-IT professionals
    is_it_professional = get_yes_no_input("Is this resume for an IT professional?")
    if not is_it_professional:
        additional_info["industry"] = get_input("Specify the industry this resume is for")
    
    # Any other additional information
    if get_yes_no_input("Would you like to add any other information?"):
        additional_info["other"] = get_input("Additional Information", multiline=True)
    
    return additional_info

def generate_resume_files(data):
    """Generate JSON and Markdown files."""
    # Create sanitized filename from the user's name and timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_name = data["personal_info"]["full_name"].lower().replace(" ", "_")
    base_filename = f"{sanitized_name}_{timestamp}"
    
    # Define file paths
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "profiles", "json", f"{base_filename}.json")
    md_path = os.path.join(base_dir, "profiles", "md", f"{base_filename}.md")
    
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

def preview_data(data):
    """Display a preview of the collected data."""
    clear_screen()
    print_header("RESUME DATA PREVIEW")
    
    # Personal info
    print("📋 PERSONAL INFORMATION:")
    print(f"Name: {data['personal_info']['full_name']}")
    print(f"Title: {data['personal_info']['professional_title']}")
    print(f"Contact: {data['personal_info']['email']} | {data['personal_info']['phone']}")
    print(f"Location: {data['personal_info']['location']['city']}, {data['personal_info']['location']['state']}, {data['personal_info']['location']['country']}")
    
    # Online presence
    print("\n🌐 ONLINE PRESENCE:")
    for platform, url in data['online_presence'].items():
        if platform != 'additional_profiles':
            if url:
                print(f"{platform.capitalize()}: {url}")
    
    if 'additional_profiles' in data['online_presence']:
        for profile in data['online_presence']['additional_profiles']:
            print(f"{profile['platform']}: {profile['url']}")
    
    # Professional summary
    print("\n📝 PROFESSIONAL SUMMARY:")
    print(f"Career Objective: {data['professional_summary']['career_objective'][:100]}...")
    print(f"Summary: {data['professional_summary']['summary'][:100]}...")
    
    # Skills summary
    print("\n🛠️ SKILLS (sample):")
    for category, skills in data['skills'].items():
        if skills:
            print(f"{category.replace('_', ' ').title()}: {len(skills)} entries")
    
    # Education summary
    print(f"\n🎓 EDUCATION: {len(data['education'])} entries")
    
    # Professional experience summary
    print(f"\n💼 PROFESSIONAL EXPERIENCE: {len(data['professional_experience'])} entries")
    
    # Projects summary
    print(f"\n🚀 PROJECTS: {len(data['projects'])} entries")
    
    # Additional info
    if data['additional_info']:
        print("\n➕ ADDITIONAL INFORMATION:")
        for key in data['additional_info'].keys():
            print(f"- {key.replace('_', ' ').title()}")
    
    print("\n" + "=" * 60)

def main():
    """Main function to run the resume form."""
    clear_screen()
    print_header("AI ARTISAN - RESUME INFORMATION COLLECTION FORM")
    
    print("""
Welcome to the Resume Information Collection Form!
    
This form will guide you through entering all the necessary information
for generating a comprehensive resume for IT professionals or other industries.

You'll be asked to provide details about:
- Personal information
- Online presence
- Professional summary
- Skills and expertise
- Education history
- Projects
- Professional experience
- Additional information

At the end, you'll be able to preview your information before submission.
    """)
    
    input("Press Enter to begin...")
    
    # Collect all resume information
    resume_data = {
        "personal_info": collect_personal_info(),
        "online_presence": collect_online_presence(),
        "professional_summary": collect_professional_summary(),
        "skills": collect_skills(),
        "education": collect_education(),
        "projects": collect_projects(),
        "professional_experience": collect_professional_experience(),
        "additional_info": collect_additional_info()
    }
    
    # Preview and confirm
    while True:
        preview_data(resume_data)
        
        if get_yes_no_input("\nIs all the information correct?"):
            break
        
        # Allow editing sections
        print("\nWhich section would you like to edit?")
        print("1. Personal Information")
        print("2. Online Presence")
        print("3. Professional Summary")
        print("4. Skills & Expertise")
        print("5. Education")
        print("6. Projects")
        print("7. Professional Experience")
        print("8. Additional Information")
        print("9. Continue with current information")
        
        choice = input("\nEnter your choice (1-9): ")
        if choice == "1":
            resume_data["personal_info"] = collect_personal_info()
        elif choice == "2":
            resume_data["online_presence"] = collect_online_presence()
        elif choice == "3":
            resume_data["professional_summary"] = collect_professional_summary()
        elif choice == "4":
            resume_data["skills"] = collect_skills()
        elif choice == "5":
            resume_data["education"] = collect_education()
        elif choice == "6":
            resume_data["projects"] = collect_projects()
        elif choice == "7":
            resume_data["professional_experience"] = collect_professional_experience()
        elif choice == "8":
            resume_data["additional_info"] = collect_additional_info()
        elif choice == "9":
            break
        else:
            print("Invalid choice. Please try again.")
    
    # Generate files
    clear_screen()
    print_header("GENERATING RESUME FILES")
    print("Processing your information...")
    
    # Add metadata
    resume_data["metadata"] = {
        "generated_at": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    # Generate files
    json_path, md_path = generate_resume_files(resume_data)
    
    # Display success message
    print("\n✅ Resume files have been generated successfully!\n")
    print(f"📄 JSON file saved to: {json_path}")
    print(f"📝 Markdown file saved to: {md_path}")
    print("\nThank you for using the AI Artisan Resume Builder!")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️ Form submission was cancelled. No files were generated.")
    except Exception as e:
        print(f"\n❌ An error occurred: {str(e)}")
        print("Please try again. If the issue persists, contact support.")
