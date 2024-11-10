import requests
def remove_html_tags(text):
    while True:
        script1 = text.find("<script")
        script2 = text.find("</script>")
        if script1 == -1 or script2 == -1:
            break
        text = text[:script1] + text[script2 + len("</script>"):]
    while True:
        style1 = text.find("<style")
        style2 = text.find("</style>")
        if style1 == -1 or style2 == -1:
            break
        text = text[:style1] + text[style2 + len("</style>"):]

    while "&#" in text:
        start_index = text.find("&#")
        end_index = text.find(";", start_index)
        if start_index != -1 and end_index != -1:
            text = text[:start_index] + text[end_index + 1:]
        else:
            break
    inside_tag = False
    result = ""
    for i in text:
        if i == "<":
            inside_tag = True
        elif i == ">":
            inside_tag = False
        elif not inside_tag:
            result += i
    return result

def remove_punc(text):
    punctuation = '''!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~'''
    content = ""
    for i in text:
        if i not in punctuation:
            content += i
    return content
def scrap(html_content):
    title_index = html_content.find("<title>")
    start_index = title_index + len("<title>")
    end_index = html_content.find("</title>")
    title = html_content[start_index:end_index]
    body = remove_html_tags(html_content)
    body = remove_punc(body)

    links = []
    start_i = 0
    for i in range(html_content.count("href=\"")):
        start_i = html_content.find("href=\"", start_i)
        if start_i == -1:
            break
        start_i += len("href=\"")
        end_i = html_content.find("\"", start_i)
        link = html_content[start_i:end_i]
        if link.startswith("https://"):
            links.append(link)
        start_i = end_i + 1
    return title, body, links

def main():
    url = input("Enter the URL: ")
    response = requests.get(url)
    html_content = response.text
    title, body, links = scrap(html_content)
    print("Title:", title)
    print("\nPage Body:", body)
    print("\nLinks found on the webpage:")
    for link in links:
        print(link)

if __name__ == "__main__":
    main()
