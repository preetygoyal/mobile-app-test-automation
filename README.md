# Mobile App Test Automation (Appium + Python)

[![Mobile App Test Automation](https://github.com/preetygoyal/mobile-app-test-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/preetygoyal/mobile-app-test-automation/actions/workflows/ci.yml)

Appium + Python/pytest test suite for a real Android app, using the
**Page Object Model**, targeting Sauce Labs' public demo app
[`my-demo-app-rn`](https://github.com/saucelabs/my-demo-app-rn) — a
React Native shopping app purpose-built for mobile test automation practice
(login, product catalog, item details, cart).

## Why this app

Unlike a generic sample APK, `my-demo-app-rn` ships with real validation
logic, real error copy, a locked-out-account scenario, and sortable product
listings — enough surface area to demonstrate realistic mobile QA scenarios
rather than trivial "tap a button" tests. All locators and test credentials
in this project come directly from the app's own published source, not
guessed from the UI.

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
│   ├── base_screen.py          # Shared find/wait helpers, Android text-extraction workaround
│   ├── login_screen.py         # Username/password fields, validation errors
│   ├── menu_screen.py          # Drawer menu: login/logout navigation
│   ├── catalog_screen.py       # Product list, sort button
│   ├── sort_modal.py           # Name/price ascending & descending sort options
│   ├── item_details_screen.py  # Product detail, quantity counter, add-to-cart
│   └── cart_screen.py          # Cart contents, remove item, proceed to checkout
├── tests/
│   ├── conftest.py             # Appium session fixture + per-test app-state reset
│   ├── test_data.py            # Real credentials/error strings from the app's own source
│   ├── test_login.py           # Valid/invalid/locked-out login, validation, logout
│   ├── test_catalog.py         # Product listing, sorting, navigation to item details
│   └── test_cart.py            # Add to cart, quantity counter, remove item, checkout gate
├── .github/workflows/ci.yml
└── requirements.txt
```

## What's covered

- **Login** — valid credentials, no-match credentials, a locked-out account, missing username, missing password, and logout (16 scenarios total across the suite).
- **Catalog** — product list loads, sort by name/price, opening an item's details.
- **Cart** — empty-cart state, adding an item, adjusting quantity, the checkout button appearing once the cart is non-empty, and removing an item back to empty.

Every test starts from a known state via `reset_app_state` in `conftest.py`,
which long-presses the app's header logo — the same in-app reset gesture the
app's own official test suite uses, rather than reinstalling the APK between
tests.

## Running locally

You'll need Appium and Android SDK tooling set up locally (an emulator or a
real device attached over ADB):

```bash
pip install -r requirements.txt
npm install -g appium
appium driver install uiautomator2

# Download the demo app once
mkdir -p app
curl -L -o app/MyDemoAppRN.apk \
  https://github.com/saucelabs/my-demo-app-rn/releases/latest/download/MyDemoAppRN.apk

# In one terminal
appium

# In another terminal, with an emulator/device already running
pytest tests -m mobile -v
```

## CI/CD

`.github/workflows/ci.yml` runs on every push/PR to `main`, using
[`reactivecircus/android-emulator-runner`](https://github.com/ReactiveCircus/android-emulator-runner)
on a `macos-latest` runner (required for hardware-accelerated emulation) to:

1. Install Python deps, Appium, and the UiAutomator2 driver.
2. Download the public demo APK from its GitHub release.
3. Boot a real Android emulator, start Appium, and run the full pytest suite against it.
4. Upload the HTML test report and Appium server log as workflow artifacts.

**Honest note on verification:** Appium + a full Android emulator can't run
inside this project's development sandbox (no Android SDK/emulator support
there), so this suite was verified for correct syntax, imports, and test
collection locally, but the actual emulator run is exercised by the GitHub
Actions workflow itself rather than pre-verified end-to-end before pushing.
Android emulator boot times in CI can also be slow (several minutes) —
this is normal for this kind of pipeline, not a sign of something broken.

**CI note (runner choice):** the emulator repeatedly failed to boot in time
on `macos-latest` runners, on both `x86_64` and native `arm64-v8a` system
images. Checking the android-emulator-runner project's own current docs
clarified why: they now explicitly recommend **Ubuntu runners with KVM
enabled** over macOS runners for hardware-accelerated emulation -- 2-3x
faster and more reliable. The workflow now runs on `ubuntu-latest`, enables
KVM via udev rules, and follows the project's documented two-step AVD
snapshot pattern (generate once, cache, reuse) to keep boot times low.

**CI note (APK download):** the demo app's "latest" download alias
(`.../releases/latest/download/MyDemoAppRN.apk`) returns a 404 for this
release -- the real asset on the v1.3.0 release is named
`Android-MyDemoAppRN.1.3.0.build-244.apk`. Without `curl -f`, a 404 doesn't
fail the build; curl just saves the tiny HTML error page in place of the
APK, and Appium then fails to install it -- which looked like every single
test erroring instantly. The workflow now points at the exact versioned
asset URL and uses `curl -fL` so any future link breakage fails the build
immediately with a clear error instead of silently downloading garbage.

**CI note (Android version mismatch):** the emulator is created with
`api-level: 30`, which boots as **Android 11**, but the Appium driver
fixture (`tests/conftest.py`) defaulted to requesting `platform_version
"13"` when no override was supplied. Appium correctly reported this as
`Unable to find an active device or emulator with OS 13` -- the emulator
itself was healthy, the requested OS version just didn't match what was
actually running. The workflow now exports `PLATFORM_VERSION=11` before
the test run so the two stay in sync.

## License

MIT — see [LICENSE](LICENSE).
