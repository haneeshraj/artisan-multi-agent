from llm.llm import query

def eval_content(cfg, job_details, resumes, profile):
    """
    Evaluate multiple resume versions against a specific job posting.
    Args:
        cfg (dict): Configuration object containing model details and evaluation parameters.
        job_details (str): Job description in Markdown format.
        resumes (str): Concatenated resume versions in Markdown format, separated by headers.
        profile (str): Applicant profile in Markdown or JSON format.
    Returns:
        str: Evaluation results in Markdown format, including scores, suggestions, and a summary by resume.
    """
    prompt = [
        {
            "role": "system",
            "content": (
                "You are an expert career consultant skilled in resume optimization, ATS analysis, and aligning candidate profiles with job requirements across industries like technology and finance. Your task is to evaluate multiple resume versions against a job posting based on three criteria: ATS Compatibility, Structure, and Match with Job Keywords, providing scores, explanations, and actionable feedback without modifying resume content.\n\n"
                "**Evaluation Criteria**:\n"
                "1. **ATS Compatibility (0-100)**:\n"
                "   - Assess ATS parsability, checking:\n"
                "     - Standard headers (e.g., 'Skills', 'Work Experience').\n"
                "     - Simple formatting, avoiding tables or graphics.\n"
                "     - Job description keywords (e.g., 'Python', 'Agile').\n"
                "   - Example: A resume with 'Skills: python, aws' and no tables scores higher than one with images.\n"
                "2. **Structure (0-100)**:\n"
                "   - Evaluate organization, checking:\n"
                "     - Logical section flow (e.g., Summary → Skills → Experience).\n"
                "     - Inclusion of relevant sections (e.g., Projects).\n"
                "     - Consistent formatting (e.g., 'MM/YYYY' dates).\n"
                "   - Example: A resume with consistent dates and clear sections scores higher than one with long paragraphs.\n"
                "3. **Match with Job Keywords (0-100)**:\n"
                "   - Measure alignment with job requirements, verified by the profile, checking:\n"
                "     - Job-specific keywords (e.g., 'machine learning').\n"
                "     - Quantifiable achievements (e.g., 'Improved accuracy by 10%').\n"
                "     - Role-specific skills or experiences.\n"
                "   - Example: A resume with 'TensorFlow' and relevant projects scores higher than one with unrelated skills.\n\n"
                "**Output Requirements**:\n"
                "- For **each resume**, provide:\n"
                "  - Scores (0-100) for ATS Compatibility, Structure, and Match with Job Keywords.\n"
                "  - A 2-sentence explanation per criterion, justifying the score with specific strengths/weaknesses.\n"
                "  - 3 actionable suggestions per criterion (e.g., 'Add “Agile” to Skills').\n"
                "- After evaluations, provide:\n"
                "  - A numbered list of evaluations in Markdown (e.g., '### 1. Resume 1').\n"
                "  - A ranked list sorted by average score (highest to lowest), with average and individual scores.\n"
                "  - A 'Feedback Summary by Resume' section listing each resume, its average score, and a 2-sentence summary (~50 words) of key feedback across all criteria.\n"
                "**Instructions**:\n"
                "- Verify resume content against the profile; flag discrepancies in explanations.\n"
                "- Ensure feedback is specific and tied to the job description/profile.\n"
                "- Use clean Markdown with headers (`#`, `##`, `###`), bullets, and numbered lists.\n"
                "- Note missing sections (e.g., Projects) in Structure and missing keywords in Match with Job Keywords.\n"
                "- Keep output concise to fit within 2000 tokens, prioritizing clarity.\n"
            )
        },
        {
            "role": "user",
            "content": (
                f"**Job Description:**\n\n{job_details}\n\n"
                f"**Resume Versions:**\n\n{resumes}\n\n"
                f"**Applicant Profile:**\n\n{profile}\n\n"
                "Evaluate the resume versions using ATS Compatibility, Structure, and Match with Job Keywords. "
                "For each resume, provide a score (0-100), a 2-sentence explanation, and 3 actionable suggestions per criterion. "
                "Verify content with the profile. "
                "Return Markdown output with a numbered evaluation list, a ranked list by average score, and a 'Feedback Summary by Resume' section with each resume’s average score and a 2-sentence feedback summary."
            )
        }
    ]
    
    response = query(
        prompt=prompt,
        model_name=cfg['agent']['eval']['model'],
        cfg=cfg,
        max_tokens=cfg['agent']['eval']['max_tokens'],
        temperature=cfg['agent']['eval']['temperature']
    )
    
    return response