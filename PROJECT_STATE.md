# iOS OTA Apps Site — Project State

## Current live site

- GitHub Pages: https://soundtrackminus-hash.github.io/ios-ota-apps-site/
- Repository: `soundtrackminus-hash/ios-ota-apps-site`
- Current verified commit: `79e1df2`
- Current catalog size: 50 apps

## Working rules — do not lose these

1. First restore/check the site without downloading IPA files.
2. Process IPA uploads strictly one file at a time.
3. No background bulk upload/download jobs.
4. Download each IPA only into a temporary scratch folder, upload it to the GitHub release asset, verify by HTTP HEAD/content-length, then delete the temporary IPA immediately.
5. Hard stop before download/upload if free disk space is below 10 GB.
6. Do not keep all IPA files locally under the repo; `downloads/` stays ignored.
7. If a release exists but the asset is stale/missing/wrong size, re-upload that single asset with `--clobber` and verify again.
8. Manifest metadata must come from the real IPA: `CFBundleIdentifier` and `CFBundleShortVersionString` from `Payload/*.app/Info.plist`.
9. Every generated `manifest.plist` must point to the exact GitHub release asset URL for that app.
10. Verify before claiming done:
    - live site returns HTTP 200;
    - live site has 50 app cards or the expected current count;
    - each local manifest bundle id/version matches metadata;
    - each IPA release URL returns HTTP 200;
    - release asset `content-length` matches the expected IPA size;
    - GitHub Pages deployment succeeded.

## Current implementation notes

- `index.html` contains the app catalog, search field, count display, and install buttons.
- `styles.css` contains the visual design and mobile layout.
- App manifests live under `apps/<slug>/manifest.plist`.
- Local metadata files such as `apps_metadata.json`, `drive_files.json`, and `drive_files_all.json` are intentionally ignored by git.
- IPA files are stored in GitHub Releases, not in the repository.

## Last verified behavior

- GitHub Pages deployment for commit `79e1df2` completed successfully.
- Live site showed 50 cards.
- Search field was present on the live site.
- Sample live manifests opened successfully for `vk`, `avito`, `do-vershiny`, and `most-wanted`.
- All 50 release IPA assets were verified by HTTP HEAD with matching content length before the final UI update.
