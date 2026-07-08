# 🎬 4090 Starter Batch — Both Lanes (run this tonight)

You chose **ads now + a compounding brand**. This is your production kit for both.
Everything here is copy-paste ready. Nothing is a promise — but nothing is vague either.

---

# PART 0 — Set up the machine (one evening, ~45 min)

1. **Install ComfyUI Desktop** (Windows, easiest for your 4090): download from comfy.org. It bundles Python + a one-click updater.
2. **Install ComfyUI-Manager** (it's built into Desktop; otherwise `git clone` it into `custom_nodes`). This is how you install every model/node with one click from now on.
3. **Download models** (via Manager → Model Manager, or the ComfyUI model folders):
   - **Image:** `Flux.1-schnell` (fast, 4-step) to start; add `Flux.1-dev` later for max quality. Grab the matching `t5xxl_fp16`, `clip_l`, and `ae.safetensors` VAE.
   - **Video:** `LTX-Video` (LTXV) — the fastest text/image→video model that fits a 4090 comfortably. (Add `Wan2.1` later when you want higher quality and can wait longer per clip.)
   - **Talking avatar (optional for spokesperson ads):** `LivePortrait` or `SadTalker` node pack via Manager.
   - **Voice:** install `Coqui TTS` (XTTS-v2) OR use `RVC` — either gives you unlimited voiceovers in any voice/language, free.
   - **Upscale:** `Real-ESRGAN` / `Upscayl` for crisp final export.
4. **Do ONE full dry run tonight:** Flux image → LTX 5-sec clip → add a voiceover → export a vertical (1080×1920) MP4. That single finished clip is your first portfolio piece. Don't skip this — a finished clip is worth more than a week of reading.

> All of these are the current #1-ranked tools in the app's **Make AI images & videos** arena — open GrandGitMaster → Tools → that arena for live links.

---

# PART A — ADS NOW (cash flow this week)

## A1. Three ready-to-shoot sample ads
Make these for **real brands you don't work for yet** — they become your portfolio/reel. Each has a hook, script, the exact prompts, and captions.

### Sample 1 — Skincare serum (e-commerce)
- **Hook (first 2s, on-screen + VO):** "I stopped buying $80 serums. Here's why."
- **Script (20s VO):**
  1. "This little bottle does what three of my old products couldn't."
  2. "Vitamin C, hyaluronic acid, zero greasy feel."
  3. "Two weeks in — brighter, tighter, done."
  4. "Link's right here. Your future skin says thanks."
- **Flux image prompt:** `photorealistic product photography of a minimalist glass serum dropper bottle on a wet marble surface, soft morning window light, water droplets, shallow depth of field, clean beige background, luxury skincare aesthetic, 9:16 vertical, ultra detailed, commercial photography`
- **LTX video prompt (image→video):** `slow cinematic push-in on the serum bottle, gentle light shimmer on glass, a single water droplet slides down, subtle rack focus, smooth premium motion`
- **Voice:** warm female, calm-confident (Coqui XTTS preset).
- **Caption:** `The $80-serum era is over ✨ #skincare #glowup #skintok`

### Sample 2 — Local gym (local business)
- **Hook:** "Everyone at this gym was a beginner once."
- **Script (18s VO):**
  1. "No mirrors full of pros judging you."
  2. "Just clean equipment, real coaches, and people who get it."
  3. "First week's free. Walk in intimidated, walk out addicted."
  4. "[Gym name], [neighborhood]. Come see."
- **Flux image prompt:** `cinematic wide shot of a modern boutique gym interior at golden hour, empty rack of dumbbells in foreground, warm rim lighting, motivational atmosphere, no people, moody contrast, 9:16 vertical, photoreal`
- **LTX video prompt:** `slow dolly through the gym, dust motes in golden light, gentle camera drift, cinematic, inspirational tone`
- **Caption:** `Your week 1 starts scarier than your week 52 💪 #gym #fitnessjourney`

### Sample 3 — Coffee / supplement brand (e-commerce)
- **Hook:** "POV: your 3pm crash never happens again."
- **Script (15s VO):**
  1. "Clean caffeine, no jitters, no crash."
  2. "One scoop, cold water, done in ten seconds."
  3. "Tastes like a treat, works like a switch."
  4. "Grab a bag — link below."
- **Flux image prompt:** `top-down flat lay of a matte-black supplement pouch beside a frosted glass of iced coffee, ice cubes, condensation, scattered coffee beans, bright airy studio light, pastel background, 9:16 vertical, commercial product photography`
- **LTX video prompt:** `iced coffee swirls as it's poured, condensation drips, product pouch gently rotates, crisp bright commercial motion`
- **Caption:** `3pm crash? Never met her ☕ #cleanenergy #coffeetok`

## A2. Land the first client (do this the same night you finish a sample)
**Instagram/TikTok DM (to small brands running ads):**
```
Hey [brand]! Love what you're doing with [product]. I make short AI video ads
for brands like yours — here are 3 samples I made: [link]. I can do 3 custom
ones for your top product for $75, delivered in 48h. Want me to make one free
sample with YOUR product so you can see it first?
```
*(The free-sample offer closes deals — your cost is ~$0, so it's all upside.)*

**Fiverr gig title:** `I will create a scroll-stopping AI UGC video ad for your product`
**Fiverr packages:** Basic $25 (1 video) · Standard $60 (3 videos) · Premium $150 (5 videos + captions + hooks).

**Cold email (e-com brands):**
```
Subject: quick AI ad for [brand]?

Hi [name] — I made a 15-second video ad concept for [product] (took me an hour,
cost me nothing to produce). Mind if I send it over? If you like it, I do 3 for
$75; if not, no worries — it's yours to keep.
```

## A3. Pricing & the retainer (the sure-shot part)
| Offer | Price | Why |
|---|---|---|
| Starter pack | 3 videos / $75 | Easy yes, gets the first testimonial |
| Standard | 5 videos / $150 | Once you have 1–2 reviews |
| **Retainer** | **12 videos / mo / $300** | **The goal — predictable monthly income** |
Convert every happy one-off buyer into a retainer: *"Want me to just handle 3 fresh ads a week so you never run dry? $300/mo."*

---

# PART B — THE BRAND (the compounding asset)

## B1. Your niche (recommended): "Cinematic Discipline"
A **faceless motivation/self-improvement** account: cinematic AI visuals + short punchy voiceover about discipline, focus, "level up." Why this niche:
- **Broad, hungry audience** → fast follower growth.
- **Trivially batchable** on a 4090 (image → 5s clip → text overlay → VO).
- **Three stacked income paths:** creator ad revenue → sponsorships (supplement/fitness/app brands — the *same* type you make ads for) → selling your own product back (a $9 discipline guide, or your ad service).

*(If motivation feels crowded, the same machine runs an **AI-character fashion/aesthetic** account or a **"satisfying AI worlds"** account — say the word and I'll swap the batch.)*

## B2. First 7 posts (scripts — post one a day)
Each: 5–8s cinematic clip + this line as VO + on-screen text.
1. "Discipline is just remembering what you actually want."
2. "Nobody is coming to save you. That's the good news."
3. "You don't need more time. You need fewer excuses."
4. "The version of you that you want is built at 6am, not 6pm."
5. "Comfort is the most expensive thing you'll ever buy."
6. "Motivation gets you started. Systems keep you alive."
7. "One year from now you'll wish you started today. So start today."

## B3. The visual style (one reusable Flux prompt template)
```
cinematic [SCENE] , lone figure silhouette, dramatic god-rays, volumetric fog,
deep shadows, teal-and-orange color grade, film grain, anamorphic lens flare,
epic and moody, motivational poster aesthetic, 9:16 vertical, ultra detailed
```
Swap `[SCENE]` per post: `a runner cresting a foggy hill at dawn` · `a boxer alone in an empty gym` · `a climber on a mountain ridge` · `a desk with one lamp on at 5am` · `a swimmer in an empty lane` · `a city rooftop at sunrise` · `a figure walking into a storm`.
**Video prompt (LTX):** `slow cinematic push-in, drifting fog, subtle light flicker, dust in the air, epic slow motion`.

## B4. Cadence & monetization ladder
- **Post 1–2×/day, every day.** Consistency > perfection. Batch a week's clips in one 4090 session.
- **0 → 1k followers:** just post. Reply to every comment. Watch which lines pop, make more of those.
- **1k → 10k:** add a link-in-bio (your $9 guide, made with the phone-pack prompts). First sponsor DMs start.
- **10k+:** pitch sponsorships to the fitness/app/supplement brands you already make ads for — now you sell them *reach*, not just production.

---

# Your rhythm (both lanes, ~1–2 hrs/day)
- **Morning (30 min):** batch 5–7 brand clips on the 4090, schedule them.
- **Midday (30 min):** send 10 client DMs / respond to leads, deliver any orders.
- **Evening (as needed):** produce paid orders (fast — your pipeline's already built).

## What I produce for you on demand (just ask)
- More ad scripts + prompts for any product a client sends.
- Fresh brand scripts + scene prompts whenever you want a new batch.
- Your DMs, pitches, pricing tweaks, and sponsor outreach.
- A new niche/character batch if you want to test another account.

**Send me:** (1) the first product/brand you want a custom ad for, or (2) a "give me the next 7 brand scripts," and I'll turn it around immediately.

---
*Honest footer: no income promised. This is a real, high-ceiling plan for your hardware; results depend on you shipping clips and sending pitches. Cost to try = your time + electricity.*
