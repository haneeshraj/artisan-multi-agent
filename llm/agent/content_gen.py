from llm.llm import query

def generate_resume_content(strategy, cfg, job_details, profile): 
    """
    Generate resume content in Markdown format based on the provided strategy, job description, and applicant profile.
    Args:
        strategy (str): The resume-tailoring strategy to apply.
        model (str): The model to use for content generation.
        cfg (object): Configuration object containing job details and applicant profile.
    Returns:
        str: Generated resume content in Markdown format.
    """
    
    prompt =[
    {
        "role": "system",
        "content": (
        "You are an expert resume writer and career strategist with over a decade of experience in crafting tailored, high-impact resumes for diverse industries and roles, including technical, managerial, and creative positions.\n"
        "Your expertise includes deep knowledge of Applicant Tracking Systems (ATS), job-specific keyword optimization, and aligning candidate profiles with employer expectations to maximize interview opportunities.\n"
        "Your task is to generate resume content in Markdown format that aligns with a specific resume-tailoring strategy, a provided job description, and the applicant's profile.\n"
        "Incorporate important keywords and phrases from the job description to enhance ATS compatibility and relevance, ensuring they are naturally integrated into the content.\n"
        "The resume content should highlight the applicant's qualifications, experience, and skills, emphasizing the given strategy while remaining concise, professional, and ATS-compatible.\n"
        "Include sections such as Professional Summary, Skills, Work Experience, Education, and Projects (if applicable), ensuring all content is tailored to the job description and strategy.\n"
        "Use bullet points for clarity and ensure consistent Markdown formatting with clear section headers.\n"
        "Draw specific, relevant details (e.g., experience, projects, skills) from the applicant's profile, but do not invent or add information not provided.\n"
        "Avoid overly generic phrases (e.g., 'team player' without context) and focus on specific, quantifiable achievements and skills that align with the strategy and job requirements.\n"
        "Do not include placeholder text (e.g., 'Your Name') or personal details not provided in the profile.\n"
        "Return only the resume content in Markdown format, with no additional explanations or context."
        )
    },
    {
        "role": "user",
        "content": (
        f"**Job Description:**\n\n{job_details}\n\n"
        f"**Applicant Profile:**\n\n{profile}\n\n"
        f"**Resume-Tailoring Strategy:**\n\n{strategy}\n\n"
        f"Generate resume content in Markdown format tailored to the provided job description and applicant profile, emphasizing the given strategy. Incorporate important keywords from the job description to enhance ATS compatibility and relevance. Ensure the content is ATS-compatible, professional, and structured with clear sections."
        )
    }
    ]
    
    response = response = query(
    model_name=cfg['agent']['content-gen']['model'],
    prompt=prompt,
    temperature=cfg['agent']['content-gen']['temperature'],
    max_tokens=cfg['agent']['content-gen']['max_tokens'],
    cfg=cfg
)
    
    return response

def generate_resume_content_with_eval(eval_response, cfg, job_details, profile, previous_resume_content, strategy):
    """
    Generate improved resume content in Markdown format based on previous resume content, evaluation feedback, and the original strategy.
    
    Args:
        eval_response (str): Evaluation feedback from the previous resume version.
        cfg (dict): Configuration object containing model details and generation parameters.
        job_details (str): Job description in Markdown format.
        profile (str): Applicant profile in Markdown or JSON format.
        previous_resume_content (str): Previous resume content in Markdown format.
        strategy (str): The resume-tailoring strategy used to generate the previous resume.
    
    Returns:
        str: Improved resume content in Markdown format.
    """
    prompt = [
        {
            "role": "system",
            "content": (
                "You are an expert resume writer and career strategist with over 15 years of experience in crafting tailored, high-impact resumes for candidates across diverse industries, including technology, management, finance, healthcare, and creative fields. Your expertise includes deep knowledge of Applicant Tracking Systems (ATS), strategic keyword optimization, and aligning candidate profiles with employer expectations to maximize interview opportunities. You specialize in creating concise, professional resumes that effectively showcase candidates' qualifications, even for those with limited or no major professional experience, by emphasizing relevant skills, projects, and education.\n\n"
                "**Objective**:\n"
                "Your task is to generate improved resume content in Markdown format by refining a previous resume version, taking into account the provided evaluation feedback, the original resume-tailoring strategy, the job description, and the applicant's profile. The previous resume was crafted with a specific strategy that emphasized a particular narrative angle (e.g., technical expertise, leadership capabilities, or innovative project contributions). Your goal is to maintain this strategic focus while addressing the weaknesses identified in the evaluation feedback (e.g., ATS compatibility, structure, or keyword alignment) and enhancing the resume's overall effectiveness. For applicants with limited or no major professional experience, ensure the resume fits a single-page PDF document by prioritizing concise, impactful content and leveraging relevant projects and education. Projects should be described in detail to highlight their relevance and impact.\n\n"
                "**Key Instructions**:\n"
                "- **Incorporate Evaluation Feedback**: Thoroughly analyze the evaluation feedback to identify specific weaknesses (e.g., missing keywords, poor ATS compatibility, unclear structure) and strengths. Address each weakness with targeted improvements while preserving or enhancing the strengths identified in the feedback.\n"
                "- **Maintain the Original Strategy**: The previous resume was generated using the provided strategy. Ensure the improved resume continues to emphasize this strategy's narrative angle (e.g., technical skills, leadership, or project innovation), refining it to better align with the job description and feedback without losing its core focus.\n"
                "- **Fit a Single-Page PDF for Less Experienced Applicants**: If the applicant has limited or no major professional experience (e.g., fewer than 3 years of relevant work history or primarily entry-level roles), ensure the resume content is concise enough to fit on a single page when rendered as a PDF. Prioritize essential sections (Professional Summary, Skills, Education, Projects) and limit Work Experience to key roles or internships. Avoid unnecessary filler content and focus on impactful, relevant details. For more experienced applicants, the resume may extend beyond one page if necessary to fully showcase qualifications.\n"
                "- **Detailed Project Descriptions**: For any projects included in the resume (drawn from the applicant profile), provide detailed, descriptive content that highlights the project's purpose, technologies or tools used, specific contributions, measurable outcomes (e.g., 'Improved efficiency by 15%'), and relevance to the job description. Each project description should be 2-3 sentences long, using action-oriented language and job-specific keywords to demonstrate alignment with the role. For less experienced applicants, projects should be a primary focus to compensate for limited work experience.\n"
                "- **Integrate Job Description Keywords**: Extract critical keywords and phrases from the job description (e.g., specific skills like 'Python', tools like 'AWS', certifications, or responsibilities like 'scalable web applications') and naturally integrate them into the resume content to enhance ATS compatibility and demonstrate alignment with the employer's needs. Avoid keyword stuffing; ensure keywords are contextually relevant and seamlessly woven into sentences or bullet points.\n"
                "- **Leverage Applicant Profile**: Draw specific, relevant details (e.g., work experience, projects, skills, education, certifications) directly from the applicant's profile to craft a tailored resume. Do not invent or add information beyond what is provided in the profile. If the profile indicates limited experience, emphasize transferable skills, academic achievements, or projects to align with the job requirements.\n"
                "- **Ensure ATS Compatibility**: Structure the resume to be easily parsed by ATS software. Use standard, industry-recognized section headers (e.g., 'Professional Summary', 'Skills', 'Work Experience', 'Education', 'Projects'), avoid complex formatting such as tables, columns, graphics, or non-standard fonts, and ensure keywords are clearly presented in lowercase or as they appear in the job description. For example, a Skills section with bullet points like '- Python' or '- Agile methodologies' is more ATS-friendly than a table.\n"
                "- **Maintain Professional and Concise Content**: Craft a professional, concise resume with quantifiable achievements (e.g., 'Developed a web application serving 10,000+ users') and avoid vague or generic phrases (e.g., 'team player' without context). For less experienced applicants, focus on skills, education, and projects to create impactful content within a single page. Each bullet point should be 1-2 lines long and use action-oriented verbs (e.g., 'Developed', 'Optimized', 'Led').\n"
                "- **Use Consistent Markdown Formatting**: Structure the resume with clear Markdown section headers (e.g., `## Professional Summary`), bullet points for readability, and consistent formatting for dates (e.g., '01/2020 - Present'), job titles, and achievements. Ensure proper spacing and alignment for professional presentation in a PDF. For example, use '-' for bullet points and avoid excessive nesting or markdown errors.\n"
                "- **Include Relevant Sections**: Include standard sections such as Professional Summary, Skills, Work Experience, Education, and, if applicable, Projects or Certifications. For less experienced applicants, prioritize Skills, Education, and Projects to showcase potential. Tailor the content of each section to reflect the job description, profile, and strategy, ensuring relevance and impact.\n"
                "- **Avoid Placeholder Text**: Do not include placeholder text (e.g., 'Your Name', 'Your Address') or personal details not provided in the profile. Focus solely on the information provided in the profile to maintain accuracy and professionalism.\n"
                "- **Output Requirements**: Return only the resume content in Markdown format, with no additional explanations, introductions, or context outside the resume itself. Ensure the output is ready to be saved as a `.md` file and rendered as a professional, single-page PDF for less experienced applicants or an appropriately detailed PDF for more experienced candidates.\n"
            )
        },
        {
            "role": "user",
            "content": (
                f"**Job Description:**\n\n{job_details}\n\n"
                f"**Applicant Profile:**\n\n{profile}\n\n"
                f"**Previous Resume Content:**\n\n{previous_resume_content}\n\n"
                f"**Evaluation Feedback:**\n\n{eval_response}\n\n"
                f"**Original Resume-Tailoring Strategy:**\n\n{strategy}\n\n"
                "Generate improved resume content in Markdown format by refining the previous resume based on the evaluation feedback. "
                f"Maintain the focus of the original strategy ({strategy}) while addressing the feedback's identified weaknesses and enhancing strengths. "
                "Incorporate critical keywords from the job description to ensure ATS compatibility and alignment with the employer's requirements. "
                "Use specific details from the applicant's profile to craft a professional, concise, and structured resume with clear sections (e.g., Professional Summary, Skills, Work Experience, Education, Projects). "
                "If the applicant has limited or no major professional experience (e.g., fewer than 3 years of relevant work history or primarily entry-level roles), ensure the resume fits a single-page PDF by prioritizing concise, impactful content and emphasizing skills, education, and detailed project descriptions. "
                "For projects, provide 2-3 sentence descriptions that highlight the project's purpose, technologies used, specific contributions, measurable outcomes, and relevance to the job. "
                "Ensure the resume is ATS-compatible, uses consistent Markdown formatting, and highlights quantifiable achievements relevant to the job and strategy."
            )
        }
    ]
    
    response = query(
        model_name=cfg['agent']['content-gen']['model'],
        prompt=prompt,
        temperature=cfg['agent']['content-gen']['temperature'],
        max_tokens=cfg['agent']['content-gen']['max_tokens'],
        cfg=cfg
    )
    
    return response