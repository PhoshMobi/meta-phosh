PYTHON_SCRIPTS = \
	ci/gitlab-ci/check-style.py \
	release-helpers/announce-string-freeze \
	release-helpers/mk-gitlab-rel.py \
	$(NULL)	

SHELL_SCRIPTS = \
	ci/gitlab-ci/check-consistency \
	ci/gitlab-ci/check-po \
	ci/gitlab-ci/check-meson \
        release-helpers/contributors \
        release-helpers/get-closed-bugs \
        release-helpers/phosh-release.sh \
        release-helpers/prep-rel-branch \
        release-helpers/rel-phosh-component \
        release-helpers/update-ci \
	$(NULL)

YAML = \
	.gitlab-ci.yml \
	ci/phosh-common-jobs.yml \
	$(NULL)

test:
	pytest

all:
	flake8 $(PYTHON_SCRIPTS)
	shellcheck $(SHELL_SCRIPTS)
	yamllint $(YAML)

check-uncrustify:
	uncrustify --check -c ci/gitlab-ci/uncrustify.cfg tests/uncrustify.c
