/* Money Moves — ready-made playbooks that turn free tools into a business.
   Plain language, no coder-speak. Each one says: what it is, what you can
   earn, whether you need a computer or just your phone, the exact steps,
   and which arenas' crowned tools to use. arenas[] keys match the
   categories in champions.json so we can drop the current champions in. */
window.PLAYBOOKS = [
  {
    emoji: "🎬", title: "Faceless AI Video Channel",
    hook: "Post videos on YouTube & TikTok without ever showing your face or filming anything.",
    earn: "$500–$5,000/mo from ad money + sponsors once it grows",
    phone: true, level: "Easiest",
    steps: [
      "Pick a topic you like — scary stories, motivation, facts, history.",
      "Use an AI voice tool to read your script out loud (sounds human).",
      "Use an AI image/video tool to make the visuals automatically.",
      "Stitch them together, post daily. The algorithm does the selling."
    ],
    arenas: ["ai-media", "llm-tools"],
    freeTry: "No computer? The 'Try in browser' button on each tool runs it online, free."
  },
  {
    emoji: "🖼️", title: "Sell AI Headshots & Profile Pics",
    hook: "People pay $20–40 for pro-looking photos of themselves. AI makes them in minutes.",
    earn: "$20–40 per order · easy $1,000+/mo part-time",
    phone: true, level: "Easiest",
    steps: [
      "Ask the customer for 10 selfies.",
      "Feed them to an AI image tool that makes styled portraits.",
      "Send back 30 polished shots. Charge per pack.",
      "Sell on Fiverr, Instagram, or to LinkedIn folks who need a good photo."
    ],
    arenas: ["ai-media"],
    freeTry: "Runs in the browser — no fancy PC or graphics card needed."
  },
  {
    emoji: "🎙️", title: "Voice-Overs & Audiobook Narration",
    hook: "Clone a voice (or use an AI one) and sell narration for ads, audiobooks, videos.",
    earn: "$50–300 per gig on Fiverr/Upwork",
    phone: true, level: "Easy",
    steps: [
      "Use an AI voice tool to turn any script into clean audio.",
      "Offer 'I'll narrate your video/audiobook' as a gig.",
      "Deliver the audio file. Keep the voice, reuse forever.",
      "Upsell: background music, multiple languages."
    ],
    arenas: ["ai-media"],
    freeTry: "Browser-based voices mean zero hardware needed. Always get permission before cloning a real person's voice."
  },
  {
    emoji: "🎨", title: "AI Art & Thumbnails Studio (ComfyUI)",
    hook: "ComfyUI is the pro AI-art workshop. Sell thumbnails, posters, merch designs, book covers.",
    earn: "$15–150 per design · thumbnails are a goldmine",
    phone: false, level: "Medium",
    steps: [
      "Get ComfyUI (the crowned tool below) running — one-click versions exist.",
      "Learn 2–3 recipes: YouTube thumbnails, product mockups, posters.",
      "Sell to YouTubers and small shops who need eye-catching images fast.",
      "Charge per design or a monthly 'I make all your graphics' deal."
    ],
    arenas: ["ai-media"],
    freeTry: "No powerful PC? Use the browser version first, upgrade later when the money comes in."
  },
  {
    emoji: "🤖", title: "Chatbots for Local Businesses",
    hook: "Every restaurant, clinic, and gym wants an AI that answers customers 24/7. Build it, charge monthly.",
    earn: "$200–1,000 setup + $50–200/mo per client",
    phone: true, level: "Medium",
    steps: [
      "Use an 'AI that works for you' tool to build a helper.",
      "Feed it the business's menu / hours / FAQs.",
      "Put it on their website or WhatsApp.",
      "Charge a monthly fee to keep it running and updated."
    ],
    arenas: ["ai-agents", "llm-tools"],
    freeTry: "Most of these run free on your own machine or a cheap cloud box."
  },
  {
    emoji: "🕸️", title: "Lead Lists & Data Gathering",
    hook: "Businesses pay for lists of potential customers. Tools grab that info from the web automatically.",
    earn: "$100–500 per list · repeatable",
    phone: false, level: "Medium",
    steps: [
      "Use a web-grabbing tool (crowned below) to collect public business info.",
      "Clean it into a neat spreadsheet.",
      "Sell targeted lists to salespeople and agencies.",
      "Offer a monthly 'fresh leads every week' subscription."
    ],
    arenas: ["scraping-data"],
    freeTry: "Only scrape public info and respect each site's rules — keep it clean and legal."
  },
  {
    emoji: "🦾", title: "Automate a Company's Boring Work",
    hook: "Connect a business's apps so repetitive tasks happen by themselves. They pay you to save them hours.",
    earn: "$300–2,000 per automation built",
    phone: false, level: "Medium",
    steps: [
      "Learn n8n (the crowned automation tool below) — it's drag-and-drop.",
      "Find a business drowning in copy-paste work.",
      "Build a flow: new order → invoice → email → spreadsheet, all automatic.",
      "Charge to build it, then a small monthly fee to maintain."
    ],
    arenas: ["automation"],
    freeTry: "n8n runs free on your own computer or a $5/mo cloud box."
  },
  {
    emoji: "🌐", title: "Websites for Local Shops",
    hook: "Tons of small businesses still have no website. Build them one fast with modern free tools.",
    earn: "$300–1,500 per site + hosting fees",
    phone: false, level: "Medium",
    steps: [
      "Use the crowned website tools below to build fast.",
      "Offer a simple 5-page site: home, menu, contact, gallery, reviews.",
      "Charge for the build, then a monthly 'I keep it running' fee.",
      "Reuse your template for the next client — get faster each time."
    ],
    arenas: ["web-dev"],
    freeTry: "Free hosting exists — your only cost is your time."
  },
  {
    emoji: "🧠", title: "Your Own Private ChatGPT (sell access & help)",
    hook: "Run a ChatGPT-style AI on your own machine. Use it to offer writing, coaching, and consulting.",
    earn: "Sell services $25–100/hr · or private AI setups for clients",
    phone: false, level: "Easy",
    steps: [
      "Install a 'your own ChatGPT' tool (crowned below) — private and free.",
      "Use it to write ads, emails, resumes, product copy for clients.",
      "Offer 'done-for-you writing' packages.",
      "Bonus: set it up privately for businesses who don't want to use the cloud."
    ],
    arenas: ["llm-tools"],
    freeTry: "Small versions run even on modest laptops — no $2,000 graphics card required."
  },
  {
    emoji: "🏠", title: "Private Cloud as a Service",
    hook: "Set people up with their own private Netflix/Google Photos so they ditch monthly fees. Charge to build it.",
    earn: "$150–600 setup per person + support fees",
    phone: false, level: "Medium",
    steps: [
      "Learn a self-hosting tool (crowned below) for photos or media.",
      "Set it up for friends/family/small offices on their own box.",
      "Charge for setup and a small 'I keep it running' fee.",
      "Word of mouth spreads fast — everyone hates subscriptions."
    ],
    arenas: ["self-hosted"],
    freeTry: "Runs on cheap hardware — even an old PC or a $35 mini-computer."
  },
  {
    emoji: "🕶️", title: "Ethical Hackerman (bug bounties)",
    hook: "Companies pay real cash to people who find security holes — legally, with permission.",
    earn: "$50–5,000+ per bug found · top hunters make six figures",
    phone: false, level: "Hard",
    steps: [
      "Learn the real security tools (crowned below) the pros use.",
      "Join a bug-bounty site (HackerOne, Bugcrowd) — it's all legal & invited.",
      "Practice on the free training targets first.",
      "Report holes you find, get paid per bug. Never touch anything you're not invited to."
    ],
    arenas: ["security"],
    freeTry: "Only ever test systems you're officially allowed to. That line is what separates a paid pro from a criminal."
  },
  {
    emoji: "📚", title: "Sell Templates, Prompts & Mini-Courses",
    hook: "Package what you learn here into prompt-packs, guides, and courses. Sell the same file forever.",
    earn: "$5–50 per sale · fully passive once made",
    phone: true, level: "Easiest",
    steps: [
      "Master any one Money Move above.",
      "Write it up as a simple guide or a pack of ready prompts.",
      "Sell it on Gumroad, Etsy, or your own page.",
      "Make once, sell endlessly. Learn from the free 'Learn anything' tools below."
    ],
    arenas: ["learning", "llm-tools"],
    freeTry: "All you need is your phone and something you've figured out."
  }
];
