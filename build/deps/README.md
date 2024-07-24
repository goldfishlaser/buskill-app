This dir holds files needed to verify the authenticity of downloads of dependencies for the BusKill app.

We used to store the dependencies here directly, but that caused this repo to balloon in-size, so we instead moved the actual dependencies to another repo ([buskill-app-deps](https://github.com/BusKill/buskill-app-deps)), separated from the code.

 * https://github.com/BusKill/buskill-app-deps

For more info, see:

 * https://github.com/BusKill/buskill-app/issues/2
 * https://github.com/BusKill/buskill-app/issues/24

Note: all dependencies that are not cryptographically signed by upstream projects will be 3TOFU'd before being added to our repos, at which point we generate a new [SHA256SUMS](https://github.com/BusKill/buskill-app-deps/blob/main/build/deps/SHA256SUMS) checksum file and a signature of the checksum file in [SHA256SUMS.asc](https://github.com/BusKill/buskill-app-deps/blob/main/build/deps/SHA256SUMS.asc). This is the best way to ensure the authenticity of all our dependencies at download-time and at future-build-time.
