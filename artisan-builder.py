# scrape data from website based on the given URL
# use the markdown file to extract neccessary data and save it as a json for job details for a more structured format
# use the JSON to generate different resume templates in a mardown format to process it into a word doc in the format of an ATS friendly resume and this is supposed to take the user profile as well
# make the LLM evaluate all the resume and provide feedback on the content, structure, and ATS compatibility
# use LLM to generate code for pydoc, a python library for generating documents as an ATS friendly resume
# Save the final resume as a pdf or a word doc 
# the end

import argparse
import yaml
import os
import re

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

    if  not args.profile.endswith('.json'):
        raise ValueError("Profile file must be a JSON file. Please provide a valid profile name ending with '.json'.")

    if not os.path.exists(profile_path):
        raise ValueError(f"Profile file '{args.profile}' does not exist in {profile_dir}. Please provide a valid profile name.")
        
    
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

        validate_arguments(args)

        print(f"Configuration loaded successfully: {config}")
        print(f"Arguments parsed successfully: {args}")

        # Scrape the URL provided in the arguments
        ( output_file, output_md_file ) = scrape_url(args.url, args)
        print("URL scraping completed successfully.")


        profile_dir = os.path.join('data', 'profile-data', 'profiles')
        profile_path = os.path.join(profile_dir, args.profile)

        







    except Exception as e:
        print(f"Error: {e}")

   
    

if __name__ == "__main__":
    main()
    

    #test command with link 

#     # Example usage:
#     # python artisan-builder.py --url "https://careers.hootsuite.com/job/?gh_jid=6978679" --profile "my-profile.json" --content-gen-model "gpt-4.1-mini" --evaluation-model "claude-3-opus" --code-gen-model "gemini-2.5-pro" --output-format pdf --content-iter 3 
