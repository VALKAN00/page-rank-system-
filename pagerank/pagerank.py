import os
import random
import re
import sys
import copy

# Damping factor for PageRank calculation
DAMPING = 0.85

# Number of samples for sampling PageRank calculation
SAMPLES = 10000


def main():
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    
    # Crawl through the provided directory to build a corpus of web pages
    corpus = crawl(sys.argv[1])
    
    # Calculate PageRank using both sampling and iteration methods
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            # Find all anchor tags and extract the href attribute
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            # Remove self-references and store the links for each page
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    d = {}
    links = corpus[page]
    num_pages = len(corpus)
    num_links = len(links)

    # If the page has outgoing links
    if links:
        # Assigns probability (1 - damping_factor) / num_pages to each key of the corpus
        for key in corpus:
            d[key] = (1 - damping_factor) / num_pages

        # Assigns probabilities damping_factor / num_links for each key (page) in corpus.
        for key in links:
            d[key] += damping_factor / num_links
    else:
        # If the page has no outgoing links, assign equal probability to all pages
        for key in corpus:
            d[key] = 1.0 / num_pages

    return d


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to the transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize PageRank values for each page
    d = {}.fromkeys(corpus.keys(), 0)
    # Start with a random page
    page = random.choices(list(corpus.keys()))[0]

    # Sample n pages and update PageRank values
    for i in range(1, n):
        # Calculate transition model for the current page
        current_dist = transition_model(corpus, page, damping_factor)
        # Update PageRank values based on the current distribution
        for _page in d:
            d[_page] = (((i - 1) * d[_page]) + current_dist[_page]) / i
        # Choose the next page based on the current distribution
        page = random.choices(list(d.keys()), weights=list(d.values()), k=1)[0]

    return d


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    total_pages = len(corpus)
    # Initialize PageRank values for each page
    distribution = {}.fromkeys(corpus.keys(), 1.0 / total_pages)
    change = True

    # Continue iteration until PageRank values converge
    while change:
        change = False
        old_distribution = copy.deepcopy(distribution)
        # Update PageRank values for each page
        for page in corpus:
            distribution[page] = ((1 - damping_factor)/total_pages) + \
                (damping_factor * get_sum(corpus, distribution, page))
            # Check for convergence
            change = change or abs(
                old_distribution[page] - distribution[page]) > 0.001

    return distribution


def get_sum(corpus, distribution, page):
    """
    Calculate the sum of PageRank values of pages linking to the given page.
    """
    result = 0
    for p in corpus:
        if page in corpus[p]:
            result += distribution[p] / len(corpus[p])
    return result

if __name__ == "__main__":
    main()


#how to run code :
#1-open new terminal or cmd
#2-make sure that you are in project folder
#3-write this command --->  python pagerank.py corpus0
#4-you can try more files if you change corpus0 to corpus1 orcorpus2 in the previous command