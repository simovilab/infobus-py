# Cairo Library Setup on macOS

## The Problem

When running `infobus` commands that use the signage module, you may encounter an error like:

```
OSError: no library called "cairo" was found
cannot load library 'libcairo.2.dylib'
```

This happens because Python's `cairocffi` library cannot find the Cairo graphics library installed by Homebrew, even though it's installed on your system.

## Why This Happens

On macOS, Homebrew installs libraries to `/opt/homebrew/lib` (on Apple Silicon) or `/usr/local/lib` (on Intel Macs), which are not in the default dynamic library search path that Python uses.

## Solution

You have several options to fix this:

### Option 1: Use the Wrapper Script (Recommended for Development)

Use the provided `run_infobus.sh` script which sets the library path automatically:

```bash
./run_infobus.sh --help
./run_infobus.sh signage --help
```

### Option 2: Set Environment Variable Per Command

Prefix each command with the library path:

```bash
DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:/opt/homebrew/opt/cairo/lib:/opt/homebrew/opt/libffi/lib uv run infobus --help
```

### Option 3: Add to Shell Profile (Permanent Solution)

Add this to your `~/.zshrc` (or `~/.bashrc` if using bash):

```bash
# Cairo library path for Python packages
export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:/opt/homebrew/opt/cairo/lib:/opt/homebrew/opt/libffi/lib${DYLD_FALLBACK_LIBRARY_PATH:+:$DYLD_FALLBACK_LIBRARY_PATH}"
```

Then reload your shell:

```bash
source ~/.zshrc
```

### Option 4: Create an Alias

Add this alias to your `~/.zshrc`:

```bash
alias infobus='DYLD_FALLBACK_LIBRARY_PATH=/opt/homebrew/lib:/opt/homebrew/opt/cairo/lib:/opt/homebrew/opt/libffi/lib uv run infobus'
```

## Verifying the Setup

After applying any of the solutions above, test with:

```bash
uv run infobus signage --help
```

You should see the signage help menu without any errors.

## For Production Deployment

For production environments, consider:

1. Using a virtual environment with properly configured library paths
2. Building a standalone executable with PyInstaller that bundles Cairo
3. Using Docker containers with Cairo pre-installed

## Additional Notes

- This issue is specific to macOS and Homebrew installations
- On Linux, Cairo is typically installed in standard system paths (`/usr/lib`)
- The `DYLD_FALLBACK_LIBRARY_PATH` variable is macOS-specific; Linux uses `LD_LIBRARY_PATH`
