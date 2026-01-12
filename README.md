# Pyrefly #2036 example repository

This repository serves as a minimal working example for the issue reported in
[Pyrefly #2036](https://github.com/facebook/pyrefly/issues/2036). It is based on
the [ROTARC/ADAPT](https://github.com/ROTARC/ADAPT) template.

To replicate the issue, follow these steps:

1. Clone the repository.
2. Open the repostitory in Visual Studio Code.

    The rest of these instructions assume you use Visual Studio Code and have
    `uv` installed. The same behavior was found using Python native `venv`. See
    comments below.

## Variation: do not install local package

This showcases the expected behavior of symbol renaming, but no functional
installation to run code/tests in.

3. Uncomment the last two lines to `pyproject.toml` too look like this. This
   prevents the local package from being installed by uv.

      ```toml
      [tool.uv]
      package = false
      ```

4. In the Terminal, run `uv sync` to install a local environment. This should
   **not** install `case-2036==0.1` because of the above change.
5. Reload the window (Command Pallette -> Developer: Reload Window) to force
   Pyrefly to restart.
6. Open `src/my_module.py`. Observe the class `Foo` has the method `bar`.
7. Open `analysis/case.py`.
8. Right click on `bar` in line 4 (`foo.bar()`) and select "Rename symbol".
   Choose a new name (e.g., `baz`).
9. Open `src/my_module.py`. Observe that the mothod name has changed to `baz`.
10.  In the Terminal, run `uv run python analysis/case.py`.
11.  Observe that `my_module` could not be found.

## Variation: install local package using uv

This showcases a functional installation to run code/tests in, but with the
'Rename symbol' functionality broken.

12.  Comment out the last two lines in `pyproject.toml` to look like this. This
    re-enables the local package installation.

      ```toml
      # [tool.uv]
      # package = false
      ```

13.  In the Terminal, run `uv sync`. This should now install `case-2036==0.1`. 
14.  Reload the window (Command Pallette -> Developer: Reload Window) to force
   Pyrefly to restart.
15. Open `analysis/case.py`.
16. Right click on `baz` in line 4 (`foo.baz()`) and select "Rename symbol".
   Choose a new name (e.g., back to `bar`).
17. An error message should appear stating that the element cannot be renamed.
18.  In the Terminal, run `uv run python analysis/case.py`.
19.  Observe that the method runs, printing `"Hello from Foo!"`.


## Comments

- The same behavior can be replicated using Python's native `venv`. Instead of
  using `uv sync`, create a virtual environment with `python -m venv .venv` and
  activate it using `source .venv/bin/activate`. Install the local package using
  `pip install -e .` and uninstall it using `pip uninstall case-2036`. Run the
  script using `python analysis/case.py`. The other steps remain the same.
- Note that without reloading Pyrefly, the behavior does not change
  (immediately?). In other words: it is possible to rename symbols in installed
  packages if Pyrefly was not reloaded after installation. Vice versa, if
  Pyrefly is reloaded after uninstalling a package, renaming symbols in that
  package fails.
- This repository uses the [src
  layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
  This emphasizes that code that is not installed, cannot be run. There are
  workarounds, e.g., by using the flat layout or adding the src directory to the
  Python PATH. However, these solutions are not best practice, are fragile
  (import during development is different from during production), and break
  functionality of tools that expect the package to be installed.
