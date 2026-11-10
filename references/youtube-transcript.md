# Getting a YouTube transcript

Read when a message carries a youtube.com or youtu.be link and the chat needs what the video says. A web fetch of YouTube from a chat gets YouTube's bot wall (title and chapters only). That is not proof there is no transcript. Never tell Charles there is no transcript, and never ask him to paste one, before these steps.

1. **Video id**: the `v=` value, the part after `youtu.be/`, or after `/shorts/` or `/embed/`. Eleven characters.
2. **Already fetched?** Read Chooch333/world-graph `data/transcripts/<id>.md` (GitHub connector). Found: use it. Its frontmatter `transcript_source` says whether captions were auto-made.
3. **Else** query cbrain Supabase `lpeswznkxzeeyiqaewma`: `select id, status, title, full_text from intake_items where kind = 'video' and id = '<id>'`. `full_text` present: use it. `status` `waiting`: it is queued; say so.
4. **Else queue it.** Read Chooch333/yt-relay `queue/<id>.json`. Missing: commit it with exactly `{"url": "<the link>", "source": "charles", "status": "pending", "requested_at": "<now, ISO, Z>"}` (the shape the phone receiver writes). Present: never edit it (WG-234). The PC relay fetches captions from a home address on its next pass while the PC is on, and the transcript lands in step 2's file.
5. **Tell Charles** in one line: queued, the home PC fetches it, and what you will do meanwhile (a talk page or write-up, labelled as not the transcript). "No captions" soon after a video is posted means not yet, never none (EB-154).

Source: step-ins TH-157 and TH-158 (the same miss in two chats); Charles 2026-11-09, "Why does Claude keep telling me there's no transcript." Fixed-set task T4 checks it.
