# Android / Appium Environment Setup
JP: Android / Appium 環境構築

This file is editable; the manual is in the ` ```tspec ` block.
JP: このファイルは編集可能で、内容は ` ```tspec ` ブロックにあります。

```tspec
manual:
  id: android-env
  title: 'Android/Appium setup / JP: Android + Appium (UiAutomator2) 環境構築 (macOS)'
  tags:
  - android
  - appium
  - setup
  summary: 'EN: Set up Appium + Android SDK/emulator for UI automation.

    JP: Appium + Android SDK/エミュレータを準備して UI 自動化を行う。

    '
  prerequisites:
  - Android SDK / Android Studio
  - Appium Server
  - 'JP: macOS'
  - 'JP: Homebrew (推奨)'
  - 'JP: ネットワーク接続'
  steps:
  - title: '1) Install Appium / JP: 1) Android Studio を入れて SDK を用意'
    body: 'EN: Install Appium and drivers.

      JP: Appium とドライバをインストール。


      npm install -g appium

      appium driver install uiautomator2

      '
  - title: '2) Start Appium Server / JP: 2) 環境変数を設定（zsh）'
    body: 'EN: Start the server and check /status.

      JP: サーバ起動と /status 確認。


      appium --address 127.0.0.1 --port 4723

      curl http://127.0.0.1:4723/status

      '
  - title: '3) Start emulator/device / JP: 3) AVD（エミュレータ）を作って起動'
    body: 'EN: Launch emulator or connect device.

      JP: エミュレータ起動 or 実機接続。

      '
  - title: '4) Run sample / JP: 4) Appium 2/3 をインストール'
    body: 'EN: Run the YouTube smoke sample.

      JP: YouTube smoke サンプルを実行。


      tspec run examples/android_youtube_smoke.tspec.md --backend appium --report
      out/android_youtube_smoke.json

      '
  - title: 'JP: 5) TSpec を実行'
    body: "python 側（クライアント）：\n  pip install -e \".[appium]\"\n\n実行：\n  tspec run examples/android_login.tspec.md\
      \ --backend appium --report out/android.json\n  tspec report out/android.json\
      \ --only-errors --show-steps"
  troubleshooting:
  - title: 'Appium server unreachable / JP: ANDROID_SDK_ROOT が無いと言われる'
    body: 'EN: Ensure appium is running on 127.0.0.1:4723.

      JP: Appium サーバが起動しているか確認。'
  - title: 'JP: adb devices が空'
    body: 'エミュレータを起動していない／実機が未接続。

      emulator -avd <AVD_NAME> または USB デバッグ接続を確認。'
  - title: 'JP: deviceName と実機/エミュレータが一致しない'
    body: "安定させるなら caps に udid を指定：\n  caps:\n    udid: \"emulator-5554\""
  - title: 'JP: UiAutomator2 の instrumentation が 30000ms で起動しない'
    body: "emulator が遅い場合はタイムアウトを延ばす：\n  caps:\n    uiautomator2ServerInstallTimeout:\
      \ 120000\n    uiautomator2ServerLaunchTimeout: 120000"
  - title: 'JP: hidden_api_policy の設定がタイムアウトする'
    body: "端末設定の書き込みが遅い場合は以下を追加：\n  caps:\n    ignoreHiddenApiPolicyError: true\n\
      \    adbExecTimeout: 120000\n    skipDeviceInitialization: true"
  references:
  - 'Android SDK 環境変数: https://developer.android.com/studio/command-line/variables'
```