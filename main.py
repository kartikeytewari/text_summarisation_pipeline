import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest

nlp=spacy.load('en_core_web_sm')

def print_summary(raw_text, summary_text):
    print(summary_text)

    print("length of original text = " + str(len(raw_text)))
    print("length of summary text = " + str(len(summary_text)))

# define the text to summarise
raw_text="""
Passwords have long been the de facto method for authenticating services on the web from as long as we can remember. People keep handy small passwords, that they can remember. But passwords, are inherently unsafe. Let’s say you have an 8 digit long alphanumeric password with small alphabets, for your web services.
Each place can either have 26 distinct alphabets or 10 numbers making the alphabet size of 36. So, the total possible passwords of 8 digits would be pow(36,8). That would be around 2.82e12 possible passwords. A possible brute force method with a generic system that “guesses” 1e8 passwords per second would take a little over 7.5 hours to break into. Most people won’t have a longer or more complex password than that because they tend to forget it. Add to such attacks a sophisticated dictionary attack and a generic password would not hold a minute against such password generators. This is what makes traditional passwords systems insecure.
A possible method to mitigate this problem would be to use fingerprints and other biometrics for uniquely determining user identity. This approach also has two major flaws. They are:
Storing raw images of fingerprint in a database is simply a stupid idea. Even if the database is encrypted by a good encryption method, it is still too big of a risk. It can potentially be stolen, by malicious agents and can be used in worst of ways. To mitigate this problem we will require a function that maps the fingerprints to there unique values in a one-to-one map. It should also be a cryptographic function. So that it is easy to generate the key value of a fingerprint from the image in a fairly efficient manner, while regenerating the image from the key pair an impractical feat from the standpoint of computation time required to “guess” the image.
The next problem that fingerprint authentication should manage would be to search fingerprints among a large database in an efficient manner. Standard, approaches that I have discovered are not efficient for this task. Brute Force approach takes O(n) time complexity making it unscalable. A better approach than that would be to use, Binary Trees (search time of (logn)) or Hash Map (search time of O(1)). But both of the above DS has a large constant of time complexity and they do not scale precisely because of this reason above certain thresholds.
Keeping in mind the above failures of password methods, and the caveats of fingerprint-based methods I propose an entirely different approach, that solves all the problems. We can use a cryptographic templating function that gets the scanned image of fingerprint as an input and gives the output as a single key-value that maps the fingerprint to it. There are ridges and minutiae in the fingerprint, and there unique position within the fingerprint boundary can certainly be leveraged for making this function. Since, the number of minutiae and ridges in generally well below 200, a cryptographic templating function with O(pow(n,3)) Time complexity, where n is the number of ridges in a fingerprint would suffice.
Searching the data size for a huge dataset of fingerprints would still be an issue. This can be mitigated by using Wavelet Tree as the means to search fingerprints. Creation of the database takes time complexity of O(nlogn). Searching would require just O(logn) time, and the constant of complexity does not increase considerably with the size of the database, making it more efficient than binary trees or hash maps. This makes the process of construction and searching of the database for the key-value of a fingerprint very fast. A simple implementation of the above scheme is available here, and I plan to add better functionality to it.
"""

# tokenise the text
doc=nlp(raw_text)

# generate tokens
tokens=[]
for token in doc:
    tokens.append(token.text)

# generate word list to filtered out
extra_word=list(STOP_WORDS) + list(punctuation) + list("\n")

# generate word frequency
word_freq={}
for word in doc:
    word_key=word.text.lower()
    if word_key not in extra_word:
        if word_key not in word_freq.keys():
            word_freq[word_key]=1
        else:
            word_freq[word_key]+=1


# make normalised frequency
max_freq=max(word_freq.values())
for word in word_freq.keys():
    word_freq[word]/=max_freq

# generate list of sentence_token
sentence_token=[]
for i in doc.sents:
    sentence_token.append(i)

# generate sentence_token_score
sentence_token_score={}
for i in sentence_token:
    for j in i:
        lower_word=j.text.lower()
        if lower_word not in extra_word:
            if i in sentence_token_score.keys():
                sentence_token_score[i]+=word_freq[lower_word]
            else:
                sentence_token_score[i]=word_freq[lower_word]

select_length=int(len(sentence_token)*0.3)
summary_1=nlargest(select_length, sentence_token_score, key=sentence_token_score.get)

summary_2=[]
for i in summary_1:
    summary_2.append(i.text)

summary_3 = " ".join((summary_2))
print_summary(raw_text, summary_3)