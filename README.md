meta-phosh
==========

This repository contains config shared between different projects related to
[Phosh][].

You need to copy the scripts you intend to run in CI into your repo's `.gitlab-ci/`.

We also track issues that affect multiple components in this repo.

gitlab-ci jobs
--------------

Shared gitlab-ci jobs are in [ci/phosh-common-jobs.yml][]. The scripts needed
for those jobs are expected in the `.gitlab-ci` folder in each project. We copy
them there so they can be easily executed in a working copy as well. You can
use `release-helpers/update-ci` to update them.

[Phosh]: https://phosh.mobi/
[ci/phosh-common-jobs.yml]: ./ci/phosh-common-jobs.yml
