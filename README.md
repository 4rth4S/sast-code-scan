# Sast-Code-Scan Doc

## 📖Configuration of GH

### 📖PAT Token

<aside>
💡  In order to get the script working as Github Action we need to do the following

</aside>

1. Sign in to your GitHub account.
2. Click on your profile picture in the top-right corner of the page and select `Settings` from the dropdown menu.
3. In the left sidebar, click on `Developer settings`
4. In the left sidebar, click on `Personal access tokens` and then `Tokens(classic)`
5. Click on the `Generate new token` button.
6. Provide a meaningful note in the "Note" field to describe the purpose of the token.
7. Under `Select scopes` , choose these specific permissions you want to grant to the token. 
    1. It needs to have the following permissions:
        1. *`codespace:secrets, repo, workflow, write:discussion, write:packages`*
8. Scroll down and click on the "Generate token" button.
9. GitHub will generate a new token for you. 💡**Make sure to copy the token immediately because you won't be able to see it again** 👀
10. Store the token in a secure location like password vault for later use.

### 📖GitHub_Secret

1. Sign in to your GitHub account.
2. Open the repository where you want to add the secret.
3. In the repository, click on the `Settings` tab located near the top-right corner of the page.
4. In the left sidebar, click on `Secrets` and then click on `Actions`
5. Click on the `New repository secret` button.
6. Provide a name for the secret in the `Name` field. Assign `**MY_SECRET_T0K3N**` to it .
7. In the `Secret` field, enter the actual value or sensitive information you want to store as the secret in this case will be the value of your `**GH_PAT_TOKEN**` created in the step before.
8. Click on the `Add secret` button.

---

## 👁️Issue template

To achieve this we need to set a “template” to upload scripts to the issue so it will be checked with the following script development.
💡 please check [this example template](https://github.com/4rth4S/sast-code-scan/blob/main/example/gh_comment_template) 

### 🦖 Important Things

1. The script need to be uploaded into a single comment into an issue.
2. The comment needs to follow this template: 
3. Lets dissect [this template](https://github.com/4rth4S/sast-code-scan/blob/main/example/gh_comment_template) together: 
    1. Between the tags `<summary>` we need to put the name like `custom-integration.py` or `custom-integration.sh` (the script checks `.*py` or `.*sh` between this tags to parse the script so it matters)
    2. Pay attention to **REPLACE_THIS_TEXT_AND_PASTE_YOUR_CODE_HERE** because there you will put all your script code as if you were going to place it in production.    

---
