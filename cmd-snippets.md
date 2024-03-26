**DISCLAIMER :
**	CELERY SNIPPETS are meant to be run inside "netflix_clone_backend/"

CELERY SNIPPETS:
py -m celery -A netflix_clone_backend worker -l info
py -m celery -A netflix_clone_backend beat -l info
