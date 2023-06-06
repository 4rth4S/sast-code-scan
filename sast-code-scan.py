import requests
import re
import subprocess
import sys
import os

def get_issue_comment(Issue_URL,TOKEN):
    try:       
        token = TOKEN
        headers = {'Accept': 'application/vnd.github.v3+json',
                    'Authorization': 'Bearer '+str(token),
                    'X-GitHub-Api-Version': '2022-11-28'}

        owner = re.findall(r"github\.com\/([A-z0-9]+?)\/",Issue_URL)
        repo = re.findall(r"github\.com\/[A-z0-9]+?\/([A-z0-9]+?)\/",Issue_URL)
        commentID = re.findall(r"\-([0-9]+)",Issue_URL)
        
        r = requests.get("https://api.github.com/repos/"+owner[0]+"/"+repo[0]+"/issues/comments/"+commentID[0]+"",headers=headers, timeout=5)
        response=r.json()
        script_to_analize=response['body']
        # Download issue-comment (with the script to check) and write into file
        try:
            with open("script-to-scan.txt", "w", encoding="utf-8") as f:
                f.write(script_to_analize)
            script_to_scan = "script-to-scan.txt"
        except Exception as e:
            print(str(e))
            return None
        return script_to_scan
    except Exception as e:
        print(str(e))
        return None


def get_code_type(script_to_scan):
    try:
        with open(script_to_scan, "r") as f:
            script_to_analize = f.read()                
            # Parse summary to determinate if the script will be .sh or .py later 
            summary = re.findall(r"\<summary\>(.*)\<\/summary\>", script_to_analize)
            
            # Parse script from file and delete GH tags
            script_parsed = re.sub(r"(\<details\>\n\<summary\>.*\<\/summary>\n\n```\n)","",script_to_analize).replace("```\n</details>","")
        # Write the parsed script to file for checking with SAST tool later
        with open(script_to_scan, "w") as f:
            f.write(script_parsed)                 
        # Check if Py or Sh
        if summary[0].split(".")[-1] == "py":
            print("We will run BANDIT on "+str(summary[:]))
            # Run Bandit scan on Python script
            try:
                scan_output_filename = subprocess.run(['bandit', script_to_scan], stdout=subprocess.PIPE).stdout.decode('utf-8')
                with open("bandit_output.txt", "w") as f:
                    f.write(scan_output_filename)
                scan_output = "bandit_output.txt"                                 
                return scan_output
            except Exception as e:
                print(str(e))            
        elif summary[0].split(".")[-1] == "sh":
            try:
                print("We will run SHELLCHECK on "+str(summary[:]))
                # Run ShellCheck scan on shell script
                subprocess.run(['apt-get', 'install', 'shellcheck', '-y'], check=True)
                scan_output_filename = subprocess.run(['shellcheck', script_to_scan], stdout=subprocess.PIPE).stdout.decode('utf-8')
                with open("shellcheck_output.txt", "w") as f:
                    f.write(scan_output_filename)                
                scan_output = "shellcheck_output.txt"
                return scan_output
            except Exception as e:
                print(str(e))            
        else:
            print("Unsupported file format.")
            sys.exit(1)
        return None
    except Exception as e:
        print(str(e))


def post_comment(Issue_URL, scan_output, TOKEN):
    try:
        token = TOKEN
        headers = {'Accept': 'application/vnd.github.v3+json',
                'Authorization': 'Bearer '+str(token),
                'X-GitHub-Api-Version': '2022-11-28'}
        owner = re.findall(r"github\.com\/([A-z0-9]+?)\/",Issue_URL)
        repo = re.findall(r"github\.com\/[A-z0-9]+?\/([A-z0-9]+?)\/",Issue_URL)
        issue_number = re.findall(r"issues\/([0-9]+?)",Issue_URL)
        
        with open(scan_output, "r") as f:
            scan_results = f.read()
        
        # Create the request payload
        comment_questions = "## Manual Review Checks\n- [ ] Define manual checks:\n     - [ ] Series of questions that people who work in support should ask themselves\n       - [ ] It has an undefined loop? (the iterations are under control?)\n       - [ ] It has an Evil Regex? (exploitable regex patterns)\n       - [ ] It has hardcoded values into the script? (sensitive data is hardcoded?)\n       - [ ] It has suspicious behaviors?\n         - [ ] It opens sockets or establishes network connections?\n         - [ ] It has some connection with external org domains?\n         - [ ] It takes some user untrusted input from somewhere?"
        comment_body = "## Scan Report :bulb: \n\n\n \n"+scan_results+" \n\n  "+comment_questions+""
        
        payload = {
            'body': comment_body
            }
        # Send the POST request to create the comment
        url="https://api.github.com/repos/"+owner[0]+"/"+repo[0]+"/issues/"+issue_number[0]+"/comments"
        response = requests.post(url=url, headers=headers, json=payload, timeout=5)
        print('w00tw00t --> Script Scanned ;) ')
        return None
    except Exception as e:
        print(str(e))

def main(Issue_URL, TOKEN):
    try:
        script_to_scan = get_issue_comment(Issue_URL, TOKEN) # Writes the comment into a file for parsing
        scan_output = get_code_type(script_to_scan)
        post_comment(Issue_URL,scan_output, TOKEN)
        os.remove(script_to_scan)
        os.remove(scan_output)
    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    Issue_URL = str(sys.argv[1])
    TOKEN = str(sys.argv[2])
    main(Issue_URL, TOKEN)
