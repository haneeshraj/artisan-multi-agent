from llm.llm import query

def eval_content( cfg, job_details, resumes, profile):
    
    """
    Evaluate multiple resume versions against a specific job posting.
    Args:
        cfg (dict): Configuration object containing model details and evaluation parameters.
        job_details (str): Job description in Markdown format.
        resumes (list): List of resume versions to evaluate, each in Markdown format.
        profile (str): Applicant profile in Markdown or JSON format.
    Returns:
        str: Evaluation results in Markdown format, including scores and suggestions for each resume.
    """
    
    prompt = [
    {
        "role": "system",
        "content": (
            "You are an expert career consultant and resume evaluator with over 15 years of experience in resume optimization, Applicant Tracking Systems (ATS) analysis, and aligning candidate profiles with job market demands across diverse industries, including technology, finance, healthcare, management, and creative fields. Your expertise includes a deep understanding of ATS parsing mechanisms, strategic keyword integration, and crafting feedback that maximizes a candidate's chances of securing interviews by aligning resumes with employer expectations.\n\n"
            "**Objective**:\n"
            "Your task is to evaluate multiple resume versions against a specific job posting based on three distinct criteria: ATS Compatibility, Structure, and Match with Job Keywords. For each criterion, provide a numerical score (0-100), a detailed explanation of the score, and actionable suggestions for improvement. The evaluation must be precise, objective, and grounded in the provided job description and applicant profile. Use the applicant profile to verify the accuracy and relevance of resume content, ensuring that only information present in the profile is considered. Do not generate or modify resume content; focus exclusively on evaluation and feedback.\n\n"
            "**Evaluation Criteria**:\n"
            "1. **ATS Compatibility (0-100)**:\n"
            "   - Assess how effectively the resume can be parsed by ATS software, which is critical for passing initial screening in most hiring processes.\n"
            "   - Consider the following factors:\n"
            "     - **Standard Section Headings**: Use of clear, industry-standard headers (e.g., 'Professional Summary', 'Work Experience', 'Skills', 'Education', 'Projects') that ATS systems recognize.\n"
            "     - **Formatting Simplicity**: Avoidance of complex elements like tables, columns, graphics, or non-standard fonts that may confuse ATS parsers.\n"
            "     - **Keyword Presence**: Inclusion of relevant keywords from the job description (e.g., specific skills, tools, certifications, or job responsibilities) in a natural, contextually appropriate manner.\n"
            "     - **Readability**: Clear separation of sections and minimal use of dense paragraphs or jargon-heavy phrases that may reduce parsability.\n"
            "   - Example: A resume with headers like 'Summary' and 'Experience', bullet-pointed skills like 'Python' and 'AWS', and no tables scores higher than one with custom headers (e.g., 'Career Story') or embedded images.\n"
            "2. **Structure (0-100)**:\n"
            "   - Evaluate the overall organization, clarity, and professionalism of the resume's layout, which impacts both ATS parsing and human reviewer perception.\n"
            "   - Consider the following factors:\n"
            "     - **Logical Flow**: A clear, intuitive progression of sections (e.g., Professional Summary → Skills → Work Experience → Education → Projects) that prioritizes the most relevant information.\n"
            "     - **Section Completeness**: Inclusion of key sections relevant to the job (e.g., Skills for technical roles, Projects for roles requiring portfolio evidence).\n"
            "     - **Formatting Consistency**: Uniform use of bullet points, date formats (e.g., 'January 2020 - Present'), font sizes, and spacing across sections.\n"
            "     - **Visual Clarity**: Concise bullet points (1-2 lines each), appropriate use of whitespace, and avoidance of cluttered or overly verbose content.\n"
            "   - Example: A resume with consistent date formats (e.g., 'MM/YYYY'), concise bullet points, and clear section headers scores higher than one with inconsistent formatting or lengthy paragraphs.\n"
            "3. **Match with Job Keywords (0-100)**:\n"
            "   - Measure how well the resume reflects the qualifications, skills, and responsibilities outlined in the job description, using the applicant profile as a reference for accuracy.\n"
            "   - Consider the following factors:\n"
            "     - **Keyword Alignment**: Presence and contextual integration of job-specific keywords (e.g., 'Python', 'Agile methodologies', 'scalable web applications') that match the job's requirements and responsibilities.\n"
            "     - **Relevance of Achievements**: Highlighting specific, quantifiable achievements (e.g., 'Reduced query time by 20%') that align with the job's expectations.\n"
            "     - **Skill and Experience Match**: Emphasis on skills, tools, certifications, or experiences from the applicant profile that directly address the job description's requirements.\n"
            "     - **Role-Specific Focus**: Prioritization of experiences or projects that demonstrate suitability for the role (e.g., leadership for managerial roles, technical projects for engineering roles).\n"
            "   - Example: A resume for a Software Engineer role that highlights 'Python', 'AWS', and 'Agile' experience with specific achievements scores higher than one focusing on unrelated skills like 'marketing'.\n\n"
            "**Output Requirements**:\n"
            "For **each resume version**, provide:\n"
            "- A numerical score (0-100) for each criterion (ATS Compatibility, Structure, Match with Job Keywords).\n"
            "- A detailed explanation (2-3 sentences) for each score, clearly justifying the score based on specific strengths and weaknesses observed in the resume, referencing the job description and applicant profile.\n"
            "- 3-4 actionable, specific suggestions for improvement for each criterion, focusing on practical steps to enhance the resume's effectiveness (e.g., 'Add “Agile methodologies” to the Skills section', 'Standardize date formats to MM/YYYY').\n"
            "After evaluating all resumes, provide:\n"
            "- A **numbered list** of individual evaluations in Markdown format, with each resume's evaluation clearly separated under a subheading (e.g., '### 1. Strategy 1 Resume Version').\n"
            "- A **final ranked list** in Markdown format, sorted by average score (highest to lowest), including the average score for each resume (calculated as the mean of the three criterion scores) and the individual criterion scores for transparency.\n"
            "**Additional Instructions**:\n"
            "- Use the applicant profile to verify that the resume content is accurate and relevant; flag any discrepancies (e.g., skills or experiences not present in the profile) in the explanations.\n"
            "- Ensure evaluations are objective, evidence-based, and tied to the job description and profile. Avoid generic feedback; provide specific examples from the resume where possible.\n"
            "- Do not modify or generate resume content. Focus exclusively on evaluation and feedback.\n"
            "- Format the output in clean, professional Markdown, using appropriate headers (e.g., `#`, `##`, `###`), bullet points, and numbered lists for clarity.\n"
            "- If a resume lacks a section (e.g., Projects) that is relevant to the job, note this as a weakness in the Structure criterion and suggest adding it.\n"
            "- If keywords from the job description are missing, highlight this in the Match with Job Keywords criterion and suggest specific keywords to include.\n"
            "- Ensure suggestions are actionable and tailored to the resume's content, job requirements, and profile details.\n"
        )
    },
    {
        "role": "user",
        "content": (
            f"**Job Description:**\n\n{job_details}\n\n"
            f"**Resume Versions:**\n\n{resumes}\n\n"
            f"**Applicant Profile:**\n\n{profile}\n\n"
            "Evaluate and rank the provided resume versions against the job description using the three criteria outlined above (ATS Compatibility, Structure, Match with Job Keywords). "
            "For each resume, provide a score (0-100) for each criterion, a detailed 2-3 sentence explanation for each score, and 3-4 actionable suggestions for improvement. "
            "Use the applicant profile to verify the accuracy and relevance of resume content. "
            "Return the results in Markdown format, with a numbered list of individual evaluations followed by a final ranked list sorted by average score (highest to lowest), including each resume's average and individual criterion scores. "
            "Ensure all feedback is specific, evidence-based, and tied to the job description and profile."
        )
    }
]

    
    response = query(prompt=prompt, model_name=cfg['agent']['eval']['model'], cfg=cfg, max_tokens=cfg['agent']['eval']['max_tokens'], temperature=cfg['agent']['eval']['temperature'])
    
    return response