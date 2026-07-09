# Mobile App Test Automation (Appium + Python)

[![Mobile App Test Automation](https://github.com/preetygoyal/mobile-app-test-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/preetygoyal/mobile-app-test-automation/actions/workflows/ci.yml)

Appium + Python/pytest test suite for a real Android app, using the
**Page Object Model**, targeting
[`appium/android-apidemos`](https://github.com/appium/android-apidemos) —
Appium's own official sample app (a fork of Google's Android ApiDemos),
maintained specifically for testing Appium itself.

## Why this app

This project previously targeted Sauce Labs' `my-demo-app-rn`, a React
Native shopping app. It's a good app to *learn* mobile QA against, but it
turned out to be a rough fit for a CI pipeline still being built out: its
custom in-app "reset" gesture didn't reliably return to a known screen
between tests, its product cards required workaround text-extraction logic
that didn't match the driver's own locator strategy, and RN's JS-bundle
cold-start time interacted badly with a resource-constrained, un-cached CI
emulator. Each of those turned into its own multi-run debugging cycle (see
the CI notes below for what that actually looked like).

Switching to `android-apidemos` — a plain native Android app with normal
resource-ids, no login/cart state, and no app-specific reset logic needed —
removes that whole class of problem, at the cost of testing simpler
screens (an alert dialog, a text field) instead of a full shopping flow.
That trade-off was made deliberately to get a reliably green pipeline first;
the app can be swapped back to something more elaborate once the pipeline
itself is solid.

## Tech stack

| Layer | Tools |
|---|---|
| Mobile automation | Appium (UiAutomator2 driver), Appium-Python-Client, Selenium |
| Test framework | pytest, Page Object Model |
| CI/CD | GitHub Actions + `reactivecircus/android-emulator-runner` (boots a real Android emulator in CI) |
| Reporting | pytest-html |

## Project structure

```
.
├── pages/
│   ├── base_screen.py          # Shared find/wait/scroll-into-view helpers
│   ├── home_screen.py          # Root category list (App, Views, ...) and drill-down navigation
│   ├── alert_dialog_screen.py  # App/Alert Dialogs: the OK/Cancel dialog trigger and buttons
│   └── text_fields_screen.py   # Views/TextFields: a plain EditText
├── tests/
│   ├── conftest.py             # Appium session fixture + per-test app relaunch
│   ├── test_navigation.py      # Home screen contents, back-navigation
│   ├── test_alert_dialogs.py   # Opening a dialog, dismissing via OK and via Cancel
│   └── test_text_fields.py     # Typing into and clearing a text field
├── .github/workflows/ci.yml
└── requirements.txt
```

## What's covered

- **Navigation** — the home category list shows its expected top-level entries, and the device back button returns to it from a nested screen.
- **Alert Dialogs** — opening the "OK Cancel dialog with a message" dialog, and dismissing it via both its OK and Cancel buttons.
- **Text Fields** — typing text into a field and reading it back, and clearing a field back to empty.

Every test starts from a known state via `reset_app_state` in
`conftest.py`, which terminates and relaunches the app before each test —
see the CI notes below for why a full relaunch, not a lighter-weight
in-app reset, is what this repo settled on.

## Running locally

You'll need Appium and Android SDK tooling set up locally (an emulator or a
real device attached over ADB):

```bash
pip install -r requirements.txt
npm install -g appium
appium driver install uiautomator2

# Download the demo app once
mkdir -p app
curl -fL -o app/ApiDemos-debug.apk \
  https://github.com/appium/android-apidemos/releases/download/v6.0.10/ApiDemos-debug.apk

# In one terminal
appium

# In another terminal, with an emulator/device already running
pytest tests -m mobile -v
```

## CI/CD

`.github/workflows/ci.yml` runs on every push/PR to `main`, using
[`reactivecircus/android-emulator-runner`](https://github.com/ReactiveCircus/android-emulator-runner)
on an `ubuntu-latest` runner with KVM enabled to:

1. Install Python deps, Appium, and the UiAutomator2 driver.
2. Download the demo APK from its GitHub release.
3. Boot a real Android emulator, start Appium, and run the full pytest suite against it.
4. Upload the HTML test report and Appium server log as workflow artifacts.

**Honest note on verification:** Appium + a full Android emulator can't run
inside this project's development sandbox (no Android SDK/emulator support
there), so this suite is verified for correct syntax, imports, and test
collection locally (`pytest --collect-only`), but the actual emulator run
is exercised by the GitHub Actions workflow itself rather than
pre-verified end-to-end before pushing. Android emulator boot times in CI
can also be slow (several minutes) — this is normal for this kind of
pipeline, not a sign of something broken.

**CI note (runner choice):** the emulator repeatedly failed to boot in time
on `macos-latest` runners, on both `x86_64` and native `arm64-v8a` system
images. Checking the android-emulator-runner project's own current docs
clarified why: they now explicitly recommend **Ubuntu runners with KVM
enabled** over macOS runners for hardware-accelerated emulation -- 2-3x
faster and more reliable. The workflow runs on `ubuntu-latest`, enables
KVM via udev rules, and follows the project's documented two-step AVD
snapshot pattern (generate once, cache, reuse) to keep boot times low.

**CI note (emulator-runner teardown hangs):** a run was observed where
pytest itself finished in about 3 minutes, but the `reactivecircus/
android-emulator-runner` step then sat idle for another ~14 minutes until
the job's overall 20-minute timeout killed the whole run and marked it
"Cancelled" -- burying the real pytest result (which had already printed
"13 failed") behind an unrelated infra hang. The "Run tests on Android
emulator" step now has its own `timeout-minutes: 10`, so a stuck teardown
fails that step directly and quickly instead of silently eating the whole
job's time budget.

**CI note (why this repo moved off `my-demo-app-rn`):** that app's
custom "long-press the header logo to reset" gesture, copied from the
app's own official test suite, turned out to only reliably return to the
Catalog screen on the very first test of a session -- once a test
navigated elsewhere (e.g. to the Cart), the long-press alone did not bring
the app back to a populated Catalog, because (per the official suite's own
`restartApp()` helper) the long-press is meant to run *after* a full
`driver.reset()`, not instead of one. Combined with a separate locator bug
(a page object was matching against a whole concatenated card string —
name + price + rating icons -- instead of just the product name, so its
xpath could never match a real element) and a couple of UI-state checks
using too-short timeouts for this environment's rendering speed, getting
that app fully green took several rounds of "real failure vs. environment
flakiness" triage. `android-apidemos` avoids the whole category: no
custom reset gesture, no multi-field concatenated locators, no
login/cart state to track between tests.

**CI note (Android version mismatch):** the emulator is created with
`api-level: 30`, which boots as **Android 11**, but the Appium driver
fixture (`tests/conftest.py`) defaulted to requesting `platform_version
"13"` when no override was supplied. Appium correctly reported this as
`Unable to find an active device or emulator with OS 13` -- the emulator
itself was healthy, the requested OS version just didn't match what was
actually running. First attempt: `export PLATFORM_VERSION=11` inside the
action's `script:` block -- this did not work, because this action doesn't
necessarily run the whole `script:` block as one continuous shell session,
so an `export` inside it isn't guaranteed to reach the pytest process it
eventually spawns. Fix: set `PLATFORM_VERSION: "11"` as a step-level `env:`
on the "Run tests on Android emulator" step instead, which GitHub Actions
guarantees is present in that step's process environment no matter how the
action runs its script internally.

## License

MIT — see [LICENSE](LICENSE).
