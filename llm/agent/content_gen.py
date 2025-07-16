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

def generate_resume_content_with_eval(eval, cfg, job_details, profile):
    pass