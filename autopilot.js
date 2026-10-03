/* Auto-Pilot — the money machine layer.
   A Money Move tells you WHAT business to start. An Auto-Pilot blueprint
   hands you (or your AI) the exact thing to RUN so the AI does the work.

   Each blueprint = a real, ready-to-run recipe:
     - the free tool that powers it (a champion from the leaderboard)
     - a complete copy-paste PROMPT that turns Claude/ChatGPT into the worker
     - where to sell the result and a realistic starting price
     - 3 launch steps a total beginner can follow

   No coding. Copy the prompt, paste it into any free AI, collect the output,
   deliver it, get paid. That is the "fully automated way to make money". */
window.AUTOPILOTS = [
  {
    emoji: "🎬", title: "Faceless Video Channel — on Auto-Pilot",
    what: "Have an AI write you a full week of short-form videos every Monday.",
    earn: "$500–5,000/mo (ads + sponsors) once it grows", phone: true,
    tool: { slug: "comfyanonymous/comfyui", name: "ComfyUI (for the visuals)" },
    prompt:
`You are my faceless YouTube/TikTok content engine. My niche is: [SCARY STORIES].
Give me 7 short videos (one per day this week). For EACH video output:
1. A 150-word voiceover script with a 3-second hook that stops the scroll.
2. A title + 5 hashtags built to go viral.
3. A shot list: 6 image prompts I can paste into an AI image tool.
4. The single best moment to use as the thumbnail.
Make them binge-worthy so viewers watch the next one. Number them Day 1–7.`,
    sell: "YouTube Partner + TikTok Creator Fund, then brand sponsors",
    launch: [
      "Copy the prompt, paste into any free AI, swap [SCARY STORIES] for your niche.",
      "Use a free AI voice tool to read each script; make visuals with the tool below.",
      "Post one a day. Repeat the prompt every Monday for a fresh week."
    ]
  },
  {
    emoji: "✍️", title: "Done-For-You Writing Agency — on Auto-Pilot",
    what: "Sell ad copy, emails, and product descriptions the AI writes for you.",
    earn: "$25–100 per order · $1,000+/mo part-time", phone: true,
    tool: { slug: "open-webui/open-webui", name: "Open WebUI (your private ChatGPT)" },
    prompt:
`You are my copywriting studio. A client sells: [DESCRIBE THE PRODUCT].
Produce a ready-to-deliver pack:
1. Five Facebook/Instagram ad variations (hook + body + call-to-action).
2. A 4-email welcome sequence that turns new signups into buyers.
3. Ten product descriptions, each under 60 words, benefit-first.
4. Twenty content ideas for the next month.
Match this brand voice: [FRIENDLY / LUXURY / BOLD]. Make it copy-paste ready.`,
    sell: "Fiverr, Upwork, or DM local businesses. Charge per pack.",
    launch: [
      "Post a gig: 'I'll write your ads & emails, 24h delivery.'",
      "When someone orders, fill the [brackets] and run the prompt.",
      "Deliver the output as a tidy doc. Reuse the prompt forever."
    ]
  },
  {
    emoji: "🤖", title: "Chatbot Shop for Local Businesses — on Auto-Pilot",
    what: "Give every shop a 24/7 AI that answers customers. Charge monthly.",
    earn: "$200–1,000 setup + $50–200/mo per client", phone: true,
    tool: { slug: "open-webui/open-webui", name: "Open WebUI" },
    prompt:
`You are building a customer-service AI for this business: [NAME, TYPE, CITY].
Here are their details: [HOURS, MENU/SERVICES, PRICES, FAQ, PHONE].
Produce:
1. A friendly system prompt that makes an AI answer as this business.
2. The 30 most likely customer questions with perfect answers.
3. A booking/enquiry script that captures name, need, and contact.
4. Three upsell lines the bot can slip in naturally.
Keep the tone warm and on-brand. Output everything ready to paste into a bot.`,
    sell: "Walk into local shops, or DM them. Setup fee + monthly retainer.",
    launch: [
      "Pick a business with no website chat. Get their info.",
      "Run the prompt; drop the result into a free chatbot widget.",
      "Charge to set it up, then monthly to keep it updated."
    ]
  },
  {
    emoji: "🕸️", title: "Lead-List Service — on Auto-Pilot",
    what: "Sell salespeople fresh lists of potential customers, gathered automatically.",
    earn: "$100–500 per list · repeatable weekly", phone: false,
    tool: { slug: "getmaxun/maxun", name: "Maxun (no-code web scraper)" },
    prompt:
`You are my lead-research assistant. My client wants leads matching:
[e.g. dentists in Austin with a website but no online booking].
Produce:
1. A step-by-step plan for where to find these leads from PUBLIC sources.
2. The exact fields to collect (name, site, email, phone, one personal note).
3. A clean spreadsheet template header for the deliverable.
4. A short, personalized outreach email my client can send to each lead.
Only use public info and respect each site's rules. Keep it clean and legal.`,
    sell: "Sell lists to agencies & freelancers; offer a weekly subscription.",
    launch: [
      "Use the no-code scraper below to collect the public info.",
      "Run the prompt to shape it into a sellable list + outreach email.",
      "Deliver as a spreadsheet. Offer 'fresh leads every week' for recurring pay."
    ]
  },
  {
    emoji: "🌐", title: "Websites-for-Shops — on Auto-Pilot",
    what: "Have an AI build a complete small-business website in one paste.",
    earn: "$300–1,500 per site + monthly hosting", phone: false,
    tool: { slug: "vercel/next.js", name: "Next.js (+ free hosting)" },
    prompt:
`You are my web studio. Build a complete one-page website for: [BUSINESS].
Details: [WHAT THEY DO, CITY, PHONE, HOURS, 3 SERVICES, VIBE].
Output a single self-contained HTML file with inline CSS that includes:
hero with headline + call-to-action, services section, about, reviews,
a contact block, and mobile-friendly layout. Modern, clean, fast-loading.
Then give me 5 headline options and a color palette that fits their vibe.`,
    sell: "DM shops with no/old website. Build fee + small monthly upkeep.",
    launch: [
      "Find a business with a weak website. Grab their basics.",
      "Run the prompt; publish the HTML on free hosting in minutes.",
      "Charge for the build, then monthly to keep it live and updated."
    ]
  },
  {
    emoji: "📚", title: "Prompt-Pack & Template Store — on Auto-Pilot",
    what: "Have an AI create a digital product you sell over and over, forever.",
    earn: "$5–50 per sale · fully passive once made", phone: true,
    tool: { slug: "ebookfoundation/free-programming-books", name: "Free learning (to skill up first)" },
    prompt:
`You are my digital-product creator. Make a sellable pack on this topic:
[e.g. "100 viral hooks for real-estate agents"].
Produce:
1. The full pack — 100 polished, ready-to-use items.
2. A catchy product name + a sales description that makes people buy.
3. A 3-tier pricing plan (basic / pro / bundle).
4. Five social posts to promote it.
Format it so I can drop it straight into a PDF and list it for sale today.`,
    sell: "Gumroad, Etsy, or your own page. Make once, sell endlessly.",
    launch: [
      "Pick a hungry audience you understand.",
      "Run the prompt; paste the output into a free doc → export PDF.",
      "List it. Every sale after that is pure profit."
    ]
  },
  {
    emoji: "📅", title: "Social-Media Manager — on Auto-Pilot",
    what: "Sell businesses a whole month of posts an AI plans and writes.",
    earn: "$300–1,500/mo per client", phone: true,
    tool: { slug: "n8n-io/n8n", name: "n8n (to auto-schedule posts)" },
    prompt:
`You are my social-media manager. Client: [BUSINESS + WHAT THEY SELL].
Build a 30-day content calendar. For each day give:
1. The platform + post type (reel, carousel, story, text).
2. A ready-to-post caption with hook, value, and call-to-action.
3. Relevant hashtags and the best posting time.
Mix education, behind-the-scenes, promos, and engagement posts.
Output as a clean day-by-day table I can hand to the client.`,
    sell: "Retainer per business. Use the tool below to auto-schedule everything.",
    launch: [
      "Sign one local business as your first client.",
      "Run the prompt for their month of content.",
      "Auto-schedule with the tool below; bill monthly. Add clients."
    ]
  },
  {
    emoji: "🧾", title: "Bookkeeping-Helper Service — on Auto-Pilot",
    what: "Offer small businesses AI that reads their receipts & sorts their books.",
    earn: "$150–600/mo per client", phone: false,
    tool: { slug: "vas3k/taxhacker", name: "TaxHacker (self-hosted AI receipt reader)" },
    prompt:
`You are my bookkeeping assistant. A client sends messy receipts and invoices.
Given this batch: [PASTE THE EXTRACTED TEXT/AMOUNTS],
produce:
1. A clean table: date, merchant, amount, currency, category, tax.
2. A monthly summary: total spend per category + biggest costs.
3. Three plain-English money-saving observations.
4. A short note flagging anything that looks like a tax deduction.
Keep it accurate and simple enough for a non-accountant to act on.`,
    sell: "Small shops & freelancers who hate paperwork. Monthly retainer.",
    launch: [
      "Set up the self-hosted receipt reader (tool below) for a client.",
      "Each month, feed receipts in and run the prompt on the output.",
      "Deliver a clean summary. Charge monthly. It runs itself."
    ]
  }
];
