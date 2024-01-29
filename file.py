import requests
def remove_html_tags(text):
    #assigned inside_tag false to find whether any character is inside the tag or not.
    inside_tag = False
    result = ""

    # iterate over text
    for i in text:

        # if it is <,then we can see that it is opening tag of html so assign itto true.
        if i == "<":
            inside_tag = True

        # if it is >, closing tag so, assign itto false.
        elif i == ">":
            inside_tag = False

        # if it is not inside any tag, then add it to empty string result.
        elif not inside_tag:
            result += i
    
    # these code will align contents into paragraph with proper line break
    result = result.split("\n")
    body = ""
    prev_line = ""
    for line in result:
        if line.strip()=="":
            body += line.strip()
        else:
            body += "\n"+line.strip()
        prev_line = line        
            

    return body

def scrap(html_content):

    #firstly, it is finding <title> index
    title_index = html_content.find("<title>")

    #then, it will add the length, because title name will be after that
    start_index = title_index + len("<title>")

    #now it will find the index of</title>
    end_index = html_content.find("</title>")

    # it will extract the content written b/w start_index and end_index
    title = html_content[start_index:end_index]

    # after title, it will extract page body without HTML tags
    body = remove_html_tags(html_content)

    # Extract links using a for loop
    links = []
    start_i = 0

    # loop will iterate till the number of href=\" appeared
    for i in range(html_content.count("href=\"")):
        
        #in this, it will take index of href, starting from start_i
        #because if we didn't do that, then same link will be printed multiple(no. of href appeared) times.

        start_i = html_content.find("href=\"", start_i)

        #if there is no link after that, then loop will break
        if start_i == -1:
            break

        # adding the length, so that it could achieve link.
        start_i += len("href=\"")

        #it's finding index of end of the link.
        end_i = html_content.find("\"", start_i)

        # now, extracting the link using string slicing
        link = html_content[start_i:end_i]

        #Now,I will add a condn so that the link starts with https should print.

        # Initialize the prefix to check
        prefix = "https://"

        # Check if the link starts with the prefix
        if link[:len(prefix)] == prefix:
        # If it does, append it to the accumulator
            links.append(link)


        # updating the value of start_i, so that it will start again after end of the link.
        start_i = end_i + 1

    # returning title, body and links
    return title, body, links

def main():
    url = input("enter the url:  ")
    response = requests.get(url)
    html_content = response.text
    title, body, links = scrap(html_content)
    print("Title:", title)
    print("\nPage Body:", body)
    print("\nLinks found on the webpage:")
    for link in links:
        print(link)

if __name__== "__main__":
    main()
