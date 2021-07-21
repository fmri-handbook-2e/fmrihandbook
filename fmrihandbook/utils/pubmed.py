"""
pubmed utils
"""

from Bio import Entrez


def get_pubmed_query_results(query, entrez_email, retmax=50000):
    print('searching for', query)
    Entrez.email = entrez_email
    handle = Entrez.esearch(db='pubmed', term=query, retmax=retmax)
    return Entrez.read(handle)
