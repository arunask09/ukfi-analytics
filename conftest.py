from hypothesis import settings

# CI: same inputs every run, so a red build always reproduces.
settings.register_profile("ci", derandomize=True)
