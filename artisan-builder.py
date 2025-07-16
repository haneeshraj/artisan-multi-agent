
import argparse
import yaml
import os
import re

from llm.llm import query
from llm.agent.content_gen import generate_resume_content
from llm.agent.eval import eval_content

def load_config():
    """
    Load configuration from config.yaml file.
    
    Returns:
        dict: Configuration settings.
    """
    config_path = 'config.yaml'
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file '{config_path}' not found.")
    
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    
    return config

def parse_arguments():

    default_config = load_config()

    # Initialize argument parser with default values from config

    content_gen_model = default_config.get('agent', {}).get('content-gen', {}).get('model', {})
    content_gen_iter = default_config.get('agent', {}).get('content-gen', {}).get('iter', {})

    eval_model = default_config.get('agent', {}).get('eval',  {}).get('model', {})
    code_gen_model = default_config.get('agent', {}).get('code-gen',  {}).get('model', {})

    output_format = default_config.get('output', {}).get('format', {})


    print(f"Using content generation model: {content_gen_model}")

    parser = argparse.ArgumentParser(description="Resume Builder")
    parser.add_argument('--url', type=str, required=True, help='URL to scrape data from')

    parser.add_argument("--verbose-strategies", default=True, action="store_true", help="Generate detailed resume tailoring strategies with reasoning and keyword highlights."
)
    parser.add_argument('--profile', type=str, required=True, help='User profile for resume generation')
    parser.add_argument('--content-gen-model', type=str, default=content_gen_model, help='Model to use for content generation')
    parser.add_argument('--evaluation-model', type=str, default=eval_model, help='Model to use for resume evaluation')
    parser.add_argument('--code-gen-model', type=str, default=code_gen_model, help='Model to use for code generation')
    parser.add_argument('--output-format', type=str, choices=['pdf', 'docx'], default=output_format, help='Output format for the resume')
    parser.add_argument('--content-iter', type=int, default=content_gen_iter, help='Number of iterations for content generation')

    return parser.parse_args()

def validate_arguments(args):
    """
    Validate the command line arguments.
    
    Args:
        args (argparse.Namespace): Parsed command line arguments.
        
    Raises:
        ValueError: If any argument is invalid.
    """
    if not args.url.startswith('http'):
        raise ValueError("Invalid URL provided. It should start with 'http' or 'https'.")
    
    link_regex  = r'^https?://(?:www\.)?[^\s/$.?#].[^\s]*$'

    if not re.match(link_regex, args.url):
        raise ValueError("Invalid URL format. Please provide a valid URL. It should start with 'http' or 'https' and be a valid web address.\n Example: https://example.com")

    # store data/profle-data/profiles in var of the profile path
    # check if profile path is an existing file
    
    profile_dir = os.path.join('data', 'profile-data', 'profiles')
    profile_path = os.path.join(profile_dir, args.profile)

     # Check in the appropriate subdirectory based on file extension
    if args.profile.endswith('.json'):
        profile_path = os.path.join(profile_dir, 'json', args.profile)
    elif args.profile.endswith('.md'):
        profile_path = os.path.join(profile_dir, 'md', args.profile)
    else:
        raise ValueError("Profile file must be a JSON or Markdown file. Please provide a valid profile name ending with '.json' or '.md'.")

    if not os.path.exists(profile_path):
        raise ValueError(f"Profile file '{args.profile}' does not exist in {profile_path}. Please provide a valid profile name.")
    
    if args.output_format not in ['pdf', 'docx']:
        raise ValueError("Invalid output format. Supported formats are 'pdf' and 'docx'.")
    
    if not isinstance(args.content_iter, int) or args.content_iter <= 0:
        raise ValueError("Content iteration must be a positive integer.")
    
    if not args.content_gen_model:
        raise ValueError("Content generation model must be specified.")
    
    if not args.evaluation_model:
        raise ValueError("Evaluation model must be specified.")
    
    if not args.code_gen_model:
        raise ValueError("Code generation model must be specified.")
    
    if not args.url:
        raise ValueError("URL must be provided for scraping data.")
    
    if not args.profile:
        raise ValueError("User profile must be provided for resume generation.")
    
    print("All arguments are valid.")


def scrape_url(url, args):

    try:
        if "linkedin" in url:
            if args.url.startswith("https://www.linkedin.com/jobs/view/"):
                from scraper.linkedin_scraper import scrape_linkedin_job
                return scrape_linkedin_job(args.url)
            else:
                raise ValueError("Invalid LinkedIn job URL. Please provide a valid LinkedIn job URL starting with 'https://www.linkedin.com/jobs/view/'.")
            
        elif "indeed" in url:
            if "indeed.com/viewjob?jk=" in url:
                from scraper.indeed_scraper import scrape_indeed_job
                return scrape_indeed_job(args.url)
            else:
                raise ValueError("Invalid Indeed job URL. Please provide a valid Indeed job URL starting with 'https://www.indeed.com/viewjob?jk='.")
        elif "glassdoor" in url:
            if "/job-listing/" in url:
                from scraper.glassdoor_scraper import scrape_glassdoor_job
                return scrape_glassdoor_job(args.url)
            else:
                raise ValueError("Invalid Glassdoor job URL. Please provide a valid Glassdoor job URL containing '/job-listing/'.")
        elif url not in ["linkedin", "indeed", "glassdoor"]:
            from scraper.readerapi_scraper import scrape_with_readerapi
            return scrape_with_readerapi(args.url)
        else:
            raise ValueError("Unsupported job site. Please provide a valid LinkedIn, Indeed, or Glassdoor job URL.")
    except Exception as e:
        print(f"Error scraping URL: {e}")
        raise 


def main():
    try:
        config = load_config()
        args = parse_arguments()
        cfg = config.copy()

        validate_arguments(args)
        
        cfg['agent']['content-gen']['model'] = args.content_gen_model if args.content_gen_model else cfg['agent']['content-gen']['model']
        cfg['agent']['eval']['model'] = args.evaluation_model if args.evaluation_model else cfg['agent']['eval']['model']
        cfg['agent']['code-gen']['model'] = args.code_gen_model if args.code_gen_model else cfg['agent']['code-gen']['model']
        cfg['output']['format'] = args.output_format if args.output_format else cfg['output']['format']
        cfg['agent']['content-gen']['iter'] = args.content_iter if args.content_iter else cfg['agent']['content-gen']['iter']
        

        print(f"Configuration loaded successfully: {cfg}")

        # Scrape the URL provided in the arguments
        ( output_file, output_md_file ) = scrape_url(args.url, args)
        print("URL scraping completed successfully.")
        
        
        profile_dir = os.path.join('data', 'profile-data', 'profiles')
        if args.profile.endswith('.json'):
            profile_file = os.path.join(profile_dir, 'json', args.profile)
        elif args.profile.endswith('.md'):
            profile_file = os.path.join(profile_dir, 'md', args.profile)
        else:
            raise ValueError("Profile file must be a JSON or Markdown file. Please provide a valid profile name ending with '.json' or '.md'.")
        if not os.path.exists(profile_file):
            raise ValueError(f"Profile file '{args.profile}' does not exist in {profile_dir}. Please provide a valid profile name.")
        print(f"Profile file to be used: {profile_file}")
        
        job_details_md = output_md_file
        
        strategy_prompt = [
        {
            "role": "system",
            "content": (
                "You are a professional career strategist and resume optimizer.\n"
                "Your task is to analyze a job description and generate diverse resume-tailoring strategies that emphasize different aspects of the applicant's background.\n"
                "Each strategy should take a unique angle (e.g., technical strength, leadership, project innovation, etc.).\n"
                "These will later guide an AI in writing multiple resume versions.\n"
                "Adding keywords from the job description is not neccessary, as .\n"
                "Please do not add any additional information, sentences or context beyond the strategies.\n"
                "Each strategy should be concise, focused, and actionable.\n"
                "The strategies should be distinct and cover a wide range of angles to ensure comprehensive coverage of the applicant's qualifications. The strategies should be very descriptive.\n"
                
            )
        },
        {
            "role": "user",
            "content": (
                f"**Job Description:**\n\n{job_details_md}\n\n"
                f"**Profile Information:**\n\n{profile_file}\n\n"
                f"Generate {cfg['agent']['content-gen']['iter']} distinct strategies for tailoring a resume to this job. Return them as a numbered Markdown list. Each strategy should be 1-2 sentences describing the emphasis or narrative angle."
            )
        }
        ]
        
        response = query(model_name=cfg['agent']['content-gen']['model'], cfg=cfg, prompt=strategy_prompt, temperature=cfg['agent']['content-gen']['temperature'], max_tokens=cfg['agent']['content-gen']['max_tokens'])
        
        if response is None or not response.strip():
            raise ValueError("No response received from the LLM. Please check the model and configuration.")
        
        # Write the strategies to a file in the data/job-data/job_title_timestamp/ directory. the job_title_timestamp can be derived from output_md_file without the .md
        job_title = os.path.splitext(os.path.basename(output_md_file))[0]
        job_resumes_dir = os.path.join('data', 'job-data', job_title )
        os.makedirs(job_resumes_dir, exist_ok=True)
        strategies_file = os.path.join(job_resumes_dir, 'strategies.md')
        with open(strategies_file, 'w') as f:
            f.write(response.strip())
            
        
        
        print(f"Strategies written to {strategies_file}")
        
        # Read Strategies from the strategies_file which are numbered 1,2,3,4,5,6, and convert them into a list
        with open(strategies_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Parse numbered strategies properly
        import re
        strategy_pattern = r'^\d+\.\s*(.+?)(?=^\d+\.\s|\Z)'
        strategies = re.findall(strategy_pattern, content, re.MULTILINE | re.DOTALL)
        strategies = [s.strip().replace('\n', ' ') for s in strategies if s.strip()]

        if not strategies:
            raise ValueError("No strategies found in the strategies file. Please check the content generation step.")

        print(f"Strategies loaded: {len(strategies)} strategies found.")
        
        
        improve_rate = cfg['improv-rate']
        
        # If improve rate is not an integer, convert it to an integer
        if not isinstance(improve_rate, int):
            try:
                improve_rate = int(improve_rate)
            except ValueError:
                raise ValueError("Invalid improvement rate. It should be an integer value.")
        
        # generate and eval and regenerate based on feedback on eval based on cfg's improv-rate value
        print(f"Starting iterative resume generation with {improve_rate} improvement iterations...")
        for i in range(improve_rate):
            print(f"\n--- Starting Iteration {i+1}/{improve_rate} ---")
            for j in range(cfg['agent']['content-gen']['iter']):
              if i == 0:
                print(f"Generating resume content with strategy {j+1}/{cfg['agent']['content-gen']['iter']}: {strategies[j][:50]}...")
                resume_content = generate_resume_content(
                    job_details=job_details_md,
                    profile=profile_file,
                    strategy=strategies[j],
                    cfg=cfg
                )
                
                # Convert response to string and handle None values
                if resume_content is None:
                    print(f"Warning: No content generated for strategy {j+1}")
                    resume_content = f"# Resume Generation Failed\n\nNo content was generated for strategy {j+1}."
                else:
                    resume_content = str(resume_content)
                
                # write the response as a file in the job_resumes_dir with the name resume_content_{j+1}.md          
                resume_file = os.path.join(job_resumes_dir, f'version{i}', f'resume_content_{j+1}.md')
                os.makedirs(os.path.dirname(resume_file), exist_ok=True)
                with open(resume_file, 'w', encoding='utf-8') as f:
                    f.write(resume_content.strip())
                print(f"✓ Strategy {j+1} resume saved to {resume_file}")
                    
              else:
                # read the resume content from the previous version and generate new content based on the eval response
                resume_file = os.path.join(job_resumes_dir, f'version{i-1}', f'resume_content_{j+1}.md')
                if not os.path.exists(resume_file):
                    print(f"⚠️  Resume file {resume_file} does not exist. Skipping iteration {i+1}, strategy {j+1}.")
                    continue
                with open(resume_file, 'r', encoding='utf-8') as f:
                    previous_resume_content = f.read().strip()
                print(f"Generating improved resume content for strategy {j+1} based on previous version {i}")
                
                # TODO: Add resume regeneration logic here using eval feedback
                    
            all_resume_content = []
            for j in range(cfg['agent']['content-gen']['iter']):
                resume_file = os.path.join(job_resumes_dir, f'version{i}', f'resume_content_{j+1}.md')
                if os.path.exists(resume_file):
                    with open(resume_file, 'r', encoding='utf-8') as f:
                        all_resume_content.append(f.read().strip())
            
            # Join all the resumes with strategy-specific headers for better evaluation context
            all_resume_content_joined = "\n\n".join([
                f"**Strategy {j+1} Resume Version:**\n\n{content}"
                for j, content in enumerate(all_resume_content)
            ])
            
            eval_response = eval_content(
                cfg=cfg,
                job_details=job_details_md,
                resume=all_resume_content_joined
            )
            
            # write the eval response to a file in the job_resumes_dir inside version{i} with the name eval_response.md
            eval_file = os.path.join(job_resumes_dir, f'version{i}', 'eval_response.md')
            os.makedirs(os.path.dirname(eval_file), exist_ok=True)
            with open(eval_file, 'w', encoding='utf-8') as f:
                f.write(eval_response.strip())
            
            # Log iteration completion with proper scope
            print(f"Iteration {i+1} completed. All {len(all_resume_content)} resume versions generated and evaluated.")
            

            pass

         

    except Exception as e:
        print(f"Error: {e}")

    
    

if __name__ == "__main__":
    main()
    

    #test command with link 

#     # Example usage:
#     # python artisan-builder.py --url "https://careers.hootsuite.com/job/?gh_jid=6978679" --profile "my-profile.json" --content-gen-model "gpt-4.1-mini" --evaluation-model "claude-3-opus" --code-gen-model "gemini-2.5-pro" --output-format pdf --content-iter 3 
