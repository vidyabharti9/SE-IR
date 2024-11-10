import requests
from url_project1 import remove_punc, remove_html_tags

def count_freq(text):
    text = remove_html_tags(text)  
    text = text.lower()  
    text = remove_punc(text)  
    freq = {}
    words = text.split()
    fivegrams = []
    for i in range(len(words)-4):
        fivegram = words[i] + " " + words[i+1] + " " + words[i+2] + " " + words[i+3] + " " + words[i+4]
        fivegrams.append(fivegram)
    for i in fivegrams:
        if i in freq:
            freq[i] += 1
        else:
            freq[i] = 1
    return freq

def hashcode(word):
    p = 53
    m = (2 ** 64)
    value = 0
    for i in range(len(word)):
        value = (value + (ord(word[i]) * (p ** i)))
    return format(value%m, '064b')

def simhashcode(text, freq):
    code = [0] * 64  
    for fivegram in freq:
        hashcode_code = hashcode(fivegram)
        weight = freq[fivegram]
        for i in range(64):
            bit = hashcode_code[i]
            if bit == '1':
                code[i] += weight
            else:
                code[i] -= weight
    simhash = ''
    for x in code:
        if x > 0:
            simhash += '1'
        else:
            simhash += '0'
    return simhash

def compare(sim1, sim2):
    value = 0
    for i in range(len(sim1)):
        if sim1[i] == sim2[i]:
            value += 1
    return value

def main():
    url1 = input("Enter first URL: ")
    url2 = input("Enter Second URL: ")
    response1 = requests.get(url1)
    response2 = requests.get(url2)
    html_content1 = response1.text
    html_content2 = response2.text
    fivegram_1 = count_freq(html_content1)
    fivegram_2 = count_freq(html_content2)
    sim1 = simhashcode(html_content1, fivegram_1)
    sim2 = simhashcode(html_content2, fivegram_2)
    common_bits = compare(sim1, sim2)
    print("Total Number of common bits: ", common_bits)
    print("Percentage same: " ,(common_bits*100)/64)
if __name__ == "__main__":
    main()