# -*- coding: utf-8 -*-

extensions = [
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages'
]
templates_path = ['_templates']
source_suffix = ['.rst']
master_doc = 'index'
project = u'存储使用手册'
copyright = u'2020, liangtianyou'
author = u'梁天友'
version = u'2020.09'
release = u''
language = 'zh_cn'
exclude_patterns = []
pygments_style = 'sphinx'
html_theme = "sphinx_rtd_theme"
html_static_path = ['_static']
html_sidebars = {
    '**': [
        'relations.html',  # needs 'show_related': True theme option to display
        'searchbox.html',
    ]
}
htmlhelp_basename = 'sphinxdoc'
latex_elements = {
}
latex_documents = [
    (master_doc, 'sphinx.tex', u'存储使用手册',
     u'liangtianyou', 'manual'),
]
man_pages = [
    (master_doc, 'sphinx', u'存储使用手册',
     [author], 1)
]
texinfo_documents = [
    (master_doc, 'sphinx', u'存储使用手册',
     author, 'sphinx', 'One line description of project.',
     'Miscellaneous'),
]
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']
