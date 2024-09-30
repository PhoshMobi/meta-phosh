PYTHON_SCRIPTS = \
	ci/gitlab-ci/check-style.py \
	release-helpers/announce-string-freeze \
	$(NULL)	

SHELL_SCRIPTS = \
	ci/gitlab-ci/check-po \
	ci/gitlab-ci/check-consistency \
        release-helpers/contributors \
        release-helpers/get-closed-bugs \
        release-helpers/prep-rc \
        release-helpers/update-ci \
	$(NULL)

YAML = \
	.gitlab-ci.yml \
	ci/phosh-common-jobs.yml \
	$(NULL)

all:
	flake8 $(PYTHON_SCRIPTS)
	shellcheck $(SHELL_SCRIPTS)
	yamllint $(YAML)

check-uncrustify:
	uncrustify --check -c ci/gitlab-ci/uncrustify.cfg tests/uncrustify.c
