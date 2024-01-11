PYTHON_SCRIPTS = \
	ci/gitlab-ci/check-style.py \
	$(NULL)	

SHELL_SCRIPTS = \
	ci/gitlab-ci/check-po \
	$(NULL)

all:
	flake8 $(PYTHON_SCRIPTS)
	shellcheck $(SHELL_SCRIPTS)

check-uncrustify:
	uncrustify --check -c ci/gitlab-ci/uncrustify.cfg tests/uncrustify.c
