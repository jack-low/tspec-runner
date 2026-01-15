@spec: 0.1.0

# Android YouTube: open -> search -> play -> exit
# Backend: appium (UiAutomator2)
#
# NOTE:
# - YouTube は UI が頻繁に変わるので locator は "contains" を多用して頑丈にしてあります
# - まず「YouTube が起動して前面に来る」ことを保証するため appActivity を確定値にしています

```tspec
suite:
  name: "android-youtube-search-play"
  tags: [ui, android, appium, youtube]
  default_timeout_ms: 60000
  fail_fast: true
  artifact_dir: "artifacts"

vars:
  # Appium server
  appium_server: "http://127.0.0.1:4723"

  # device
  device_name: "emulator-5554"
  udid: "emulator-5554"

  # YouTube
  youtube_package: "com.google.android.youtube"
  # adb resolve-activity --brief com.google.android.youtube で判明した入口
  youtube_activity: "com.google.android.youtube.app.honeycomb.Shell$HomeActivity"

  # search query
  query: "OpenAI"

  # ---------- Robust selectors ----------
  # Search button: content-desc が Search/検索 のどちらでも拾う + resource-id に search が含まれるものも拾う
  sel_search_btn: "xpath=//*[@content-desc='Search' or @content-desc='検索' or contains(@resource-id,'search') or contains(@resource-id,'menu_search')]"

  # Search input: 既知ID or contains
  sel_search_input: "xpath=//*[@resource-id='com.google.android.youtube:id/search_edit_text' or contains(@resource-id,'search_edit')]"

  # First result: title系の先頭
  sel_first_result: "xpath=(//*[@resource-id='com.google.android.youtube:id/title' or contains(@resource-id,'title')])[1]"

  # Player area: player を含む resource-id を広く拾う
  sel_player_any: "xpath=//*[contains(@resource-id,'player') or contains(@resource-id,'player_view')]"

cases:
  - id: "YT-001"
    title: "Launch YouTube, search query, play first result, exit"
    steps:
      - do: ui.open_app
        with:
          server_url: "${vars.appium_server}"
          caps:
            platformName: "Android"
            automationName: "UiAutomator2"
            deviceName: "${vars.device_name}"
            udid: "${vars.udid}"

            appPackage: "${vars.youtube_package}"
            appActivity: "${vars.youtube_activity}"

            # 起動待ちを強める（ホームに戻る/遷移が遅い対策）
            appWaitPackage: "com.google.android.youtube"
            appWaitActivity: "com.google.android.youtube.*"
            appWaitDuration: 60000

            newCommandTimeout: 180
            noReset: true
            autoGrantPermissions: true
            adbExecTimeout: 60000
            uiautomator2ServerInstallTimeout: 60000

      # 起動直後の状態を保存（ホーム画面に戻っているか等が一発で分かる）
      - do: ui.screenshot
        with:
          path: "artifacts/after_open.png"

      # 検索アイコン（Search/検索/ID包含に対応）
      - do: ui.wait_for
        with:
          selector: "${vars.sel_search_btn}"
        timeout_ms: 60000

      - do: ui.click
        with:
          selector: "${vars.sel_search_btn}"

      # 検索入力
      - do: ui.wait_for
        with:
          selector: "${vars.sel_search_input}"
        timeout_ms: 60000

      - do: ui.type
        with:
          selector: "${vars.sel_search_input}"
          text: "${vars.query}"

      # 検索実行（多くの場合、同じ検索アイコンが確定操作になる）
      - do: ui.click
        with:
          selector: "${vars.sel_search_btn}"

      # 結果先頭を再生
      - do: ui.wait_for
        with:
          selector: "${vars.sel_first_result}"
        timeout_ms: 60000

      - do: ui.click
        with:
          selector: "${vars.sel_first_result}"

      # プレイヤーが出るまで待つ
      - do: ui.wait_for
        with:
          selector: "${vars.sel_player_any}"
        timeout_ms: 60000

      - do: ui.screenshot
        with:
          path: "artifacts/youtube_playing.png"

      - do: ui.close
        with: {}
```