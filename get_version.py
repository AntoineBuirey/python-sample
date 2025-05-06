from version.version import Version
import os

tags = [Version.from_string(t) for t in os.listdir(".git/refs/tags")]
tags.sort(reverse=True)

branch = os.popen("git rev-parse --abbrev-ref HEAD").read().strip()
last_commit = os.popen("git rev-parse HEAD").read().strip()

version = tags[0] if tags else Version(0, 0, 0)
version.patch_increment()
version.prerelease = "alpha"
version.metadata = f"{branch}.{last_commit}"
print(version)