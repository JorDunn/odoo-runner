# odoo-runner

odoo-runner is a command-line tool. It tests Odoo modules in a disposable
Docker environment. It can also start a demo server or an interactive shell.

odoo-runner does not install Odoo on your computer. It runs Odoo inside
Docker containers. odoo-runner removes the containers after each run.

## Requirements

Install these tools before you use odoo-runner:

- Docker. Docker must run on your computer.
- uv. Get uv from <https://docs.astral.sh/uv/>.

odoo-runner needs no other software. It uses only the Python standard
library.

## Install

1. Clone this repository.
2. Make the `odoo-runner` file executable:

   ```sh
   chmod +x odoo-runner
   ```

3. Run the tool directly:

   ```sh
   ./odoo-runner --help
   ```

   The first line of the file tells `uv` to fetch Python 3.13+ and run the
   script. You do not need a virtual environment.

Optional: put `odoo-runner` on your `PATH` so you can call it from any
directory.

## Quick start

Run this command from a directory that holds one module or many modules:

```sh
odoo-runner --odoo 19.0
```

odoo-runner finds the modules, installs them in a temporary database, and
runs their tests. The exit code shows the result: `0` means every test
passed.

## Usage examples

### Test mode (default)

Test a single module directory:

```sh
odoo-runner --dir path/to/my_module --odoo 19.0
```

Test many modules in an addons directory:

```sh
odoo-runner --dir path/to/addons --odoo 19.0
```

Test only some modules:

```sh
odoo-runner --dir path/to/addons --modules module_a,module_b --odoo 19.0
```

By default, odoo-runner tests only the module(s) you asked for. It does
this even though Odoo installs `base` (and other core modules) as
dependencies first. Without this default, Odoo would also run its own
built-in `base` and `web` test suites on every first-time run.

Filter further, for example to one test class:

```sh
odoo-runner --dir path/to/my_module --odoo 19.0 --test-tags /my_module:TestMyClass
```

Pass `--test-tags` to widen scope, for example to include the core suites
too:

```sh
odoo-runner --dir path/to/my_module --odoo 19.0 --test-tags /my_module,/base
```

### Upgrade test

Run the install-and-test cycle, then run it again with `-u` on the same
database. Use this to check that your module upgrades cleanly:

```sh
odoo-runner --dir path/to/my_module --odoo 19.0 --upgrade-test
```

### Demo mode

Start a live Odoo server with your module installed:

```sh
odoo-runner --dir path/to/my_module --odoo 19.0 --demo
```

odoo-runner prints the URL, the login, and the port when the server is
ready. Press `Ctrl-C` to stop the server. odoo-runner removes the
containers when the server stops.

Keep demo data between runs:

```sh
odoo-runner --dir path/to/my_module --odoo 19.0 --demo --persist
```

Wipe kept demo data and start clean:

```sh
odoo-runner --dir path/to/my_module --odoo 19.0 --demo --persist --fresh
```

### Shell mode

Open an interactive Odoo shell against your module:

```sh
odoo-runner --dir path/to/my_module --odoo 19.0 --shell
```

odoo-runner installs the module first if the database does not exist yet.
Then it opens the shell prompt in your terminal.

### Browser-enabled tests

Some tests need a browser, for example `HttpCase` tests and tours. Add
`--browser` to build an image with Google Chrome:

```sh
odoo-runner --dir path/to/my_module --odoo 19.0 --browser
```

The first run with `--browser` builds a new image. This takes longer than a
normal run. Later runs reuse the built image.

### Requirements file

If your module needs extra Python packages, add a `requirements.txt` file
next to the module (or in the addons directory you pass to `--dir`).
odoo-runner finds this file and builds a custom image with the packages
installed. You do not need a flag for this. Use `--requirements FILE` only
to point odoo-runner at a file in a different location.

### Odoo server options

Write `--` after the odoo-runner options. odoo-runner sends all the
arguments after `--` to the Odoo server in the container. You can use
`--` in test mode, demo mode, and shell mode.

Examples:

```sh
# Show debug log lines for one Python module. You can give
# --log-handler more than one time.
odoo-runner --dir path/to/my_module --odoo 19.0 -- --log-handler=odoo.orm:DEBUG

# Show each SQL query in demo mode.
odoo-runner --dir path/to/my_module --odoo 19.0 --demo -- --log-sql

# Increase the time limits for long operations.
odoo-runner --dir path/to/my_module --odoo 19.0 --demo -- --limit-time-cpu=600 --limit-time-real=1200
```

#### Option precedence

odoo-runner puts your options at the end of the Odoo command. When one
option occurs two times, Odoo uses the last value. Your value thus
replaces the odoo-runner default. For example, in test mode
`-- --log-level=debug` replaces the default `--log-level=test`.

Some options collect values, for example `--log-handler`. These options
do not replace each other. You can give them more than one time.

In shell mode, odoo-runner sends your options only to the shell process.
odoo-runner does not send your options to the first installation step.

#### Blocked options

Some Odoo options are necessary for correct odoo-runner operation.
odoo-runner does not accept these options after `--`. It stops with exit
code `2` and shows the cause.

| Blocked option | Correct procedure |
| --- | --- |
| `--dev` | Do not use. odoo-runner is not a development server. |
| `-d`, `--database` | Do not use. odoo-runner sets the database name. |
| `-i`, `--init` | Use the `--modules` flag. |
| `-u`, `--update` | Use the `--upgrade-test` flag. |
| `--test-enable` | Do not use. odoo-runner starts the tests. |
| `--test-tags` | Use the odoo-runner `--test-tags` flag. |
| `--stop-after-init`, `--no-http` | Do not use. odoo-runner sets these options. |
| `-p`, `--http-port`, `--xmlrpc-port` | Use the `--port` flag. |

## GitHub Actions

This repository is also a composite GitHub Action. Use it to run your
module tests in CI. The GitHub Ubuntu runners include Docker, so the
action works without extra setup.

### Test on each push and pull request

Add this workflow to your module repository:

```yaml
name: tests

on:
  push:
    branches: ["18.0", "19.0", "testing"]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: JorDunn/odoo-runner@v1
        with:
          odoo-version: "19.0"
```

The job fails when a test fails, because the action passes the
odoo-runner exit code through.

### Test against more than one Odoo version

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        odoo: ["18", "19"]
    steps:
      - uses: actions/checkout@v4
      - uses: JorDunn/odoo-runner@v1
        with:
          odoo-version: ${{ matrix.odoo }}
```

### Gate a release on the tests

Run the tests first when you push a release tag. The release job starts
only after the test job passes:

```yaml
name: release

on:
  push:
    tags: ["*.*.*.*.*"]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: JorDunn/odoo-runner@v1
        with:
          odoo-version: "19.0"
          upgrade-test: "true"

  release:
    needs: test
    runs-on: ubuntu-latest
    steps:
      # Your release steps go here. They run only when the tests pass.
      - uses: actions/checkout@v4
```

### Action inputs

| Input | CLI flag | Default |
| --- | --- | --- |
| `odoo-version` | `--odoo` | `.env` value, else `latest` |
| `dir` | `--dir` | `.` (the repository root) |
| `modules` | `--modules` | Auto-discovery |
| `test-tags` | `--test-tags` | Scoped to the target modules |
| `requirements` | `--requirements` | Auto-detection |
| `browser` | `--browser` | `"false"` |
| `upgrade-test` | `--upgrade-test` | `"false"` |
| `verbose` | `--verbose` | `"false"` |
| `odoo-args` | Arguments after `--` | (none) |

Set `odoo-args` to send more Odoo server options, for example
`"--log-sql --log-handler=odoo.orm:DEBUG"`. The action divides the
value at each space and sends the parts after `--` to odoo-runner.
Refer to "Odoo server options" above for the blocked options.

Set `browser` and `upgrade-test` to the string `"true"` to enable them.
If your repository holds a `.env` file with `ODOO_RUNNER_ODOO_VERSION`,
you can omit `odoo-version`.

Note: each CI runner starts empty. When your module has a
`requirements.txt`, the action builds the derived image on every run.
This adds one to two minutes.

## Configuration keys

Copy `.env.example` to `.env` inside the directory you pass to `--dir`.
odoo-runner reads this file automatically.

| Key | CLI flag | Purpose |
| --- | --- | --- |
| `ODOO_RUNNER_ODOO_VERSION` | `--odoo VER` | Odoo image tag to use. |
| `ODOO_RUNNER_BROWSER` | `--browser` | Build and use the Chrome-enabled image. |
| `ODOO_RUNNER_PORT` | `--port N` | Fixed port for demo mode. |
| `ODOO_RUNNER_TEST_TAGS` | `--test-tags SPECS` | Test filter passed to Odoo. |

### Precedence order

odoo-runner picks the first value it finds, in this order:

1. A CLI flag (for example `--odoo 19.0`).
2. A process environment variable (for example `export ODOO_RUNNER_ODOO_VERSION=19.0`).
3. A key in the `.env` file inside the `--dir` directory.
4. A built-in default.

If odoo-runner finds no value for `ODOO_RUNNER_ODOO_VERSION` anywhere, it
uses `latest` and prints a warning.

## Exit codes

odoo-runner uses the exit code to report the result. Scripts and CI jobs
can read this code without parsing output text.

| Code | Meaning |
| --- | --- |
| `0` | Every test passed. |
| `1` | A test failed, or the log showed an error. |
| `2` | The command-line input or configuration was invalid. |
| `3` | An infrastructure problem occurred (Docker missing, image pull failed, Postgres did not start). |

## Limitations

- **`--browser` works on amd64 only.** odoo-runner installs the Google
  Chrome `.deb` package for amd64. It refuses to run `--browser` on other
  processor types, for example arm64.
- **odoo-runner mounts your module code read-only.** odoo-runner never
  writes back to your module files. It is not a development server. It
  does not reload code when you edit a file. Restart the run to test a
  change. odoo-runner also does not accept the Odoo `--dev` option
  after `--`.
- **`HttpCase` tests skip without `--browser`.** Odoo skips
  `HttpCase`-based tests when no browser is present. odoo-runner warns you
  when it detects skipped tests. Add `--browser` to run them.
- **Demo data is temporary by default.** odoo-runner deletes the database
  and filestore when the demo server stops, unless you add `--persist`.

## Cleanup

odoo-runner removes its containers and network when a run ends, even after
`Ctrl-C` or a `kill` signal. Named volumes created with `--persist` stay on
disk until you run the same command with `--fresh`, or remove them by
hand.

Every resource odoo-runner creates carries the Docker label
`odoo-runner=1`. Use this label to find or remove leftover resources, for
example after a crash:

```sh
docker ps -a --filter label=odoo-runner=1
docker network ls --filter label=odoo-runner=1
docker rm -f $(docker ps -aq --filter label=odoo-runner=1)
docker network rm $(docker network ls -q --filter label=odoo-runner=1)
```
