from llm.llm import query

def eval_content( cfg, job_details, resume):
    
    """
    Evaluate and rank multiple resume versions based on ATS compatibility, structure, and strength of match with job keywords.
    Args:
        content (list): List of resume versions in Markdown format.
        model (str): The model to use for evaluation.
        cfg (object): Configuration object containing job details and applicant profile.
        job_details (str): Job description in Markdown format.
        resume_versions (str): List of resume versions in Markdown
        format.
    Returns:
        str: Evaluation results in Markdown format, including scores and feedback for each resume.
    """
    prompt = [
    {
        "role": "system",
        "content": (
            "You are an expert career consultant and resume evaluator with deep expertise in Applicant Tracking Systems (ATS), resume optimization, and job-market alignment.\n\n"
            "You will evaluate multiple resume versions against a specific job posting based on **three criteria**:\n\n"
            "1. **ATS Compatibility (0–100)** – Assess whether the resume is parsable by ATS software. Look for:\n"
            "   - Proper use of standard section headings\n"
            "   - Avoidance of tables, columns, or complex formatting\n"
            "   - Presence of relevant keywords from the job posting\n\n"
            "2. **Structure (0–100)** – Evaluate the overall layout and organization of content. Consider:\n"
            "   - Logical flow and visual clarity\n"
            "   - Inclusion and formatting of key sections (Summary, Skills, Work Experience, Education, Projects)\n"
            "   - Consistency in bullet points, dates, and formatting\n\n"
            "3. **Match with Job Keywords (0–100)** – Measure how well the resume reflects the required qualifications. Look for:\n"
            "   - Use of job-specific language\n"
            "   - Highlighting of relevant achievements, tools, or certifications\n"
            "   - Strong alignment with responsibilities and qualifications\n\n"
            "For **each resume**, provide:\n"
            "- A score (0–100) for each criterion\n"
            "- A 1–2 sentence explanation for each score\n"
            "- 2–3 actionable suggestions for improvement\n\n"
            "After evaluating all resumes, return:\n"
            "- A **numbered list** of individual evaluations (in Markdown)\n"
            "- A **final ranked list** sorted by average score (highest to lowest), including average scores\n\n"
            "Do **not** generate or modify resume content. Focus only on evaluation and feedback."
        )
    },
    {
        "role": "user",
        "content": (
            f"**Job Description:**\n\n{job_details}\n\n"
            f"**Resume Versions:**\n\n{resume}\n\n"
            "Evaluate and rank the provided resume versions using the above criteria and instructions. Output the results in **Markdown**."
        )
    }
]
    
    response = query(prompt=prompt, model=cfg['agent']['eval']['model'], cfg=cfg, max_tokens=cfg['agent']['eval']['max_tokens'], temperature=cfg['agent']['eval']['temperature'])
    
    return response