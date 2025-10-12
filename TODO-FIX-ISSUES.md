# TODO: Fix Issues in App

## 1. Grammar Check Error Message
- **Issue**: Poorly phrased error message "Grammar check failed: Could not understand audio like this it came during the voice chat"
- **Fix**: Update error message in `grammar_services.py` to be more user-friendly: "Speech recognition failed. Please speak clearly and try again."
- **Status**: ✅ Completed

## 2. Reminders Page Header
- **Issue**: Orange color header is awkward and doesn't adapt to the project theme. "+new reminder" button is too close to the heading.
- **Fix**:
  - Change header background from hard-coded orange gradient to theme-adaptive styling using CSS variables.
  - Reposition the "+new reminder" button to the right corner using flexbox layout.
- **Status**: ✅ Completed

## Tasks
- [x] Update `grammar_services.py` error message
- [x] Modify `Reminders.css` for theme-adaptive header background
- [x] Adjust `Reminders.css` for button positioning in header
- [x] Test changes in both light and dark themes
