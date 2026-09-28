# Content migration

- `content\projects\magazine-system.md` ← `page1.html`: all prose, lists, timeline and media references retained.
- `content\projects\quadruped-robot.md` ← `page2.html`: all prose, lists, timeline and media references retained.
- `content\projects\mql-project.md` ← `page3.html`: all prose, lists, timeline and media references retained.
- `content\projects\gyroid-structures.md` ← `page4.html`: all prose, lists, timeline and media references retained.
- `content\projects\arduino-drone.md` ← `page5.html`: all prose, lists, timeline and media references retained.

The old HTML is archived in `archive/original-site/`. The initial migration preserved technical statements without independently verifying them. Gyroid was subsequently rewritten using the owner's final report; its figures and values are attributed to that report. No new raw-data analysis was performed.

## Original content to review

- Magazine: rewritten from the Spring 2025 thesis, with BT-owned tasks separated from shared responsibilities. Unsupported pilot-deployment and blanket qualification claims were removed. See `docs/MAGAZINE-EDITORIAL-NOTES.md` for attribution and source discrepancies.

- MQL: the Challenge paragraph describes a quadruped robot. It has been preserved to avoid silently changing the author’s content.
- MQL: the completion date and simulation/finalisation timeline are inconsistent.
- Gyroid: rewritten from the final report dated 1 January 2026. The inconsistent old timeline was removed and the completed study, measured results and exploratory predictions are now distinguished. See `docs/GYROID-EDITORIAL-NOTES.md` for source pages and unresolved report inconsistencies.
- Some gallery captions in MQL and Quadruped appear copied from other projects.
- Missing media were restored from the owner's public GitHub repository (42 files, existing local files preserved). `docs/missing-media.json` lists any remaining unresolved references after each build.
- The original standalone contact page used example contact details. The replacement uses the real contact information from the original homepage.
