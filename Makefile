PYTHON_SCRIPTS = \
	ci/gitlab-ci/check-style.py \
	$(NULL)	

all:
	flake8 $(PYTHON_SCRIPTS)
