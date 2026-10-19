"""Qualitative framework content for the report (personas, journeys, ideas, SWOT, BCG,
Kano, MoSCoW, roadmap, user stories). Each item is traced to the dataset in the report;
anything that is analyst judgement is labelled so on the slides."""

PERSONAS = [
    {
        "name": "Jake the Binge-Watcher",
        "segment": "Binge-Watcher",
        "based_on": "Jake Thompson, Sophia Lee, Noah Brown, Mia Johnson",
        "profile": "Age 25-45 | Tech comfort: medium to high",
        "listens": "Soundtracks, movie scores, Netflix podcasts, K-Pop, Hip-Hop",
        "goals": "Stay in a show's world after the episode ends; hear exclusive behind-the-scenes audio",
        "wants": "AI playlists, behind-the-scenes content, karaoke mode, high-quality streaming",
        "pains": "Limited exclusive content, too many ads, few language options, weak personalization",
        "pays_for": "Exclusive Netflix content, ad-free, interactive features, best audio quality",
        "quote": "When I finish a season I want the soundtrack and the cast's stories right there.",
    },
    {
        "name": "Emma the Casual Listener",
        "segment": "Casual Listener",
        "based_on": "Raj Patel, Emma Wilson, Carlos Gomez",
        "profile": "Age 28-40 | Tech comfort: high to low",
        "listens": "Top charts, pop, Lo-Fi and chill, classic rock, 80s hits",
        "goals": "Get the right music for the moment with no effort",
        "wants": "Personalized playlists, mood-based playlists, offline listening",
        "pains": "Hard-to-navigate UI, no mood playlists, limited offline access",
        "pays_for": "Better discovery, relaxing music for work, seamless offline mode",
        "quote": "I just want something calm for work without scrolling for ten minutes.",
    },
    {
        "name": "Olivia the Regional Listener",
        "segment": "Regional Listener",
        "based_on": "Olivia Chen, Liam Davis, Ava Martinez",
        "profile": "Age 22-33 | Tech comfort: high to low",
        "listens": "Local folk and indie, regional-language podcasts, Latin hits, reggaeton",
        "goals": "Discover local artists and podcasts in their own language",
        "wants": "Regional content discovery, voice search for podcasts, cultural playlists",
        "pains": "Not enough regional music, hard to find podcasts, no multi-device sync",
        "pays_for": "Access to local music, more language support, curated global music",
        "quote": "Global apps bury the music from my own region.",
    },
]

STAGES = ["Discovery", "Engagement", "Subscription decision", "Usage experience"]

# Behaviour rows come from Sheet 2; touchpoint, emotion, pain and opportunity are inferred.
# emotion_score: 1 (frustrated) .. 5 (delighted), used for the emotion curve.
JOURNEYS = {
    "Binge-Watcher": {
        "touchpoint": ["Netflix home screen, end-of-episode card", "Show page, soundtrack hub",
                       "Paywall, plan comparison", "Daily mixes, new-episode alerts"],
        "emotion": ["Curious, excited", "Engaged", "Hesitant: enough exclusives?", "Satisfied, loyal"],
        "emotion_score": [4, 4, 2, 5],
        "pain": ["Promo can feel like an ad", "Limited exclusives; ads break immersion",
                 "Premium value unclear", "Weak personalization; few languages"],
        "opportunity": ["'Listen' button after the credits", "Show hubs: scores, commentaries, cast podcasts",
                        "Bundle with Netflix plan; trial of exclusives", "Watch-history playlists; karaoke mode"],
    },
    "Casual Listener": {
        "touchpoint": ["Social ad, friend's shared link", "Home feed, charts, genre pages",
                       "Upgrade prompt", "Mood playlists, offline downloads"],
        "emotion": ["Mildly interested", "Overwhelmed by choice", "Unconvinced", "Content, not attached"],
        "emotion_score": [3, 2, 2, 3],
        "pain": ["No reason to switch apps", "Hard navigation; no mood playlists",
                 "Premium value not felt on free", "Limited offline; weak habit"],
        "opportunity": ["Shareable Netflix-branded playlists", "One-tap mood tiles on a simple home",
                        "One-week taste of premium recs", "Smart offline auto-download"],
    },
    "Regional Listener": {
        "touchpoint": ["Regional influencer posts", "Search, language filters",
                       "Paywall after regional content", "Artist pages, phone and TV"],
        "emotion": ["Hopeful", "Frustrated by global results", "Convinced once found", "Engaged advocate"],
        "emotion_score": [3, 2, 4, 5],
        "pain": ["Few regional ambassadors", "Not enough regional music; podcasts hard to find",
                 "Thin regional exclusives at launch", "No multi-device sync; few languages"],
        "opportunity": ["Influencer and local-artist partnerships", "Regional home, local-language voice search",
                        "Soundtracks from regional Originals", "Cross-device sync; artist spotlights"],
    },
}

JOURNEY_INSIGHTS = [
    "Engagement is the shared weak stage: discovery quality decides who reaches the paywall.",
    "Netflix's own screens are the cheapest channel for Binge-Watchers; others need social and influencers.",
    "Premium must be felt before it is sold: trials and previews close the subscription gap.",
    "Retention depends on habit features: offline, multi-device sync, auto-refreshing playlists.",
]

# Idea funnel: (idea, need, outcome)
IDEAS = [
    ("Music discovery from Netflix watch history", "Binge-Watchers: AI playlists, exclusives", "MVP"),
    ("AI-generated personalized playlists", "Weak personalization (all segments)", "MVP"),
    ("Show soundtrack hubs with exclusive audio", "Limited exclusive content", "MVP"),
    ("Offline listening", "Limited offline access (Casual)", "MVP"),
    ("Ad-free premium tier", "Too many ads; ad-free motivation", "MVP"),
    ("Mood-based playlists", "No mood playlists (Casual)", "Phase 2"),
    ("Multi-device sync", "No multi-device sync (Regional)", "Phase 2"),
    ("Social sharing and collaborative playlists", "Word-of-mouth discovery", "Phase 2"),
    ("Regional hubs with local-language voice search", "Not enough regional music", "Phase 3"),
    ("Podcast + music hybrid experience", "Netflix and regional podcasts", "Phase 3"),
    ("Karaoke and interactive modes", "Karaoke; interactive features", "Phase 3"),
    ("High-fidelity audio", "Best audio quality", "Phase 4"),
    ("'Which song was that?' scene recognition", "Find music heard in a show", "Merged"),
    ("Voice search for podcasts", "Voice search (Regional)", "Merged"),
    ("Smart auto-download", "Seamless offline mode", "Merged"),
    ("Live concert streaming", "No user asked; very high cost", "Dropped"),
    ("User-uploaded music", "No user asked; rights risk", "Dropped"),
    ("Fan remix contests", "No user asked", "Dropped"),
    ("Kids' music mode", "No persona in the data", "Dropped"),
    ("Episode-release listening parties", "Overlaps sharing; low demand", "Dropped"),
]

FUNNEL = [
    ("Ideas brainstormed", 20, "From personas, journeys and market trends"),
    ("Pass user-need screen", 15, "Answers a need in Sheet 1 or Sheet 2"),
    ("Refined features", 12, "Overlapping ideas merged"),
    ("Selected for MVP", 5, "Unique to Netflix, top pain, or table stakes"),
]

COMPETITORS = ["Spotify", "Apple Music", "Amazon Music", "Netflix Music"]
# Qualitative ratings 1 (weak) .. 5 (strong); analyst judgement, not dataset values.
BENCHMARK = {
    "Catalogue size": [5, 5, 4, 2],
    "Personalization": [5, 4, 3, 4],
    "Exclusive content": [3, 3, 2, 5],
    "Regional content": [4, 3, 3, 4],
    "Free tier": [5, 1, 3, 4],
    "Ecosystem / bundle": [3, 5, 5, 4],
}

SWOT = {
    "Strengths": ["Viewing data on hundreds of millions of members", "Owned franchises and their soundtracks",
                  "Proven recommendation engine", "Large subscriber base to cross-sell"],
    "Weaknesses": ["No music licensing deals at launch", "No brand credibility in music yet",
                   "Rivals have years of listening data", "Original audio must be produced"],
    "Opportunities": ["Bundle with Netflix plans to cut churn", "Unmet needs: discovery, regional, mood",
                      "Exclusive audio from hit shows", "Regional markets led by local Originals"],
    "Threats": ["Spotify and Apple can copy features fast", "High royalty costs squeeze margins",
                "Subscription fatigue", "Privacy concerns over viewing history"],
}

# BCG positions: (label, relative market share 0..1 (high=left), market growth 0..1)
BCG_MARKET = [
    ("Spotify", 0.85, 0.75, "Star"),
    ("Apple Music", 0.70, 0.32, "Cash Cow"),
    ("Amazon Music", 0.58, 0.25, "Cash Cow"),
    ("Netflix Music", 0.15, 0.80, "Question Mark"),
]
BCG_PORTFOLIO = [
    ("Video streaming", "Cash Cow", "Fund Netflix Music; cross-promote it on every show page"),
    ("Netflix Music (overall)", "Question Mark", "Invest selectively in the MVP; prove retention first"),
    ("Exclusive audio", "Potential Star", "Invest heavily: the differentiator rivals cannot copy"),
    ("Generic music catalogue", "Dog if competed on alone", "License only what is needed"),
]

KANO = {
    "AI-Generated Personalized Playlists": "Performance",
    "Music Discovery Based on Netflix Watch History": "Attractive",
    "Mood-Based Music Recommendations": "Performance",
    "Social Sharing and Collaborative Playlists": "Must-be (basic sharing)",
    "Podcast + Music Hybrid Experience": "Attractive (niche)",
}
MOSCOW = {
    "AI-Generated Personalized Playlists": "Must have",
    "Music Discovery Based on Netflix Watch History": "Must have",
    "Mood-Based Music Recommendations": "Should have",
    "Social Sharing and Collaborative Playlists": "Could have",
    "Podcast + Music Hybrid Experience": "Won't have (now)",
}
PHASE = {
    "AI-Generated Personalized Playlists": "MVP",
    "Music Discovery Based on Netflix Watch History": "MVP",
    "Mood-Based Music Recommendations": "User Growth",
    "Social Sharing and Collaborative Playlists": "User Growth",
    "Podcast + Music Hybrid Experience": "Differentiation",
}

# Roadmap assumes a January 2027 kickoff.
ROADMAP = [
    {
        "phase": "1. MVP Development", "start": "2027-01-01", "end": "2027-06-30",
        "deliverables": ["Netflix sign-in and profiles", "Watch-history discovery + AI playlists",
                         "Soundtrack hubs, exclusive audio for top titles", "Offline downloads; free and premium tiers",
                         "Closed beta (Apr), launch in 3 markets (Jul)"],
        "gate": "40% of beta users listen weekly",
    },
    {
        "phase": "2. User Growth", "start": "2027-07-01", "end": "2027-12-31",
        "deliverables": ["Mood playlists", "Multi-device sync (TV, web)", "Share links and referrals",
                         "Cross-promotion inside Netflix", "Social and influencer campaigns"],
        "gate": "10 million activated users",
    },
    {
        "phase": "3. Competitive Differentiation", "start": "2028-01-01", "end": "2028-06-30",
        "deliverables": ["Regional hubs, local-language voice search", "Podcast + music hybrid",
                         "Karaoke and interactive modes", "Exclusive audio for every major Original"],
        "gate": "30% of listening starts from Netflix-linked content",
    },
    {
        "phase": "4. Monetization", "start": "2028-07-01", "end": "2028-12-31",
        "deliverables": ["Netflix + Music bundles", "High-fidelity tier, family plan",
                         "Brand partnerships at show launches", "Artist and merchandise tie-ins"],
        "gate": "25% free-to-premium conversion",
    },
]

USER_STORIES = [
    ("US-01", "Binge-Watcher", "playlists built from the shows I've watched", "keep enjoying a show's world", "Must"),
    ("US-02", "Binge-Watcher", "a 'Listen' button after a show's credits", "jump straight to its soundtrack", "Must"),
    ("US-03", "Binge-Watcher", "behind-the-scenes episodes and commentaries", "get content found nowhere else", "Must"),
    ("US-04", "Any listener", "AI playlists that learn from plays and skips", "recommendations improve over time", "Must"),
    ("US-05", "Casual Listener", "to download playlists", "listen without data or signal", "Must"),
    ("US-06", "Premium member", "ad-free listening", "nothing breaks my immersion", "Must"),
    ("US-07", "New user", "to sign in with my Netflix account", "start without a new account", "Must"),
    ("US-08", "Casual Listener", "one-tap mood playlists (Focus, Chill)", "get the right music without searching", "Should"),
    ("US-09", "Regional Listener", "phone and TV to stay in sync", "pick up where I left off", "Should"),
    ("US-10", "Casual Listener", "to share a playlist link", "friends hear what I like", "Could"),
    ("US-11", "Regional Listener", "a home screen in my language", "skip past global hits", "Should"),
    ("US-12", "Regional Listener", "voice search in my language", "find podcasts quickly", "Could"),
]

KPIS = [
    ("Adoption", "Netflix members who activate Music", "5%"),
    ("Engagement", "Weekly active listeners / activated users", "40%"),
    ("Differentiation", "Listening started from a Netflix show or watch-history playlist", "30%"),
    ("Monetization", "Free-to-premium conversion", "25%"),
    ("Retention", "Churn of Music users vs non-users", "10% lower"),
]

RISKS = [
    ("Label licensing delays", "Launch with soundtracks and original audio Netflix controls; phase in catalogue"),
    ("Rivals copy features", "Lean on exclusive IP that cannot be copied; ship fast"),
    ("Privacy backlash on viewing data", "Clear opt-in, easy off switch, transparent explanations"),
    ("Royalty costs squeeze margins", "Bundle pricing; weight listening toward owned audio"),
    ("Low adoption beyond Binge-Watchers", "Mood playlists, offline and regional hubs in later phases"),
]

# ---- product sense: the art of why, problem definition, JTBD, MVP -------------
FIVE_WHYS = [
    ("Why build a music app at all?",
     "To earn from members' listening hours, which Netflix monetizes at zero today, and to keep them subscribed."),
    ("Why would anyone leave Spotify for it?",
     "Only if Netflix solves a problem that existing apps leave unsolved."),
    ("Why aren't existing apps solving it?",
     "They don't know what you watch: discovery is generic (4 of 10 users) and exclusives are thin (3 of 10)."),
    ("Why does that gap matter to users?",
     "Fans want a show to continue in their ears; casual listeners want the right music with zero effort."),
    ("Why can Netflix close it?",
     "It owns the shows, the soundtracks and the viewing data. That is the root advantage the MVP is built on."),
]

PROBLEM = {
    "Who": "Netflix members aged 22-45 who also stream music; Binge-Watchers first",
    "Problem": "They can't easily find music and audio that fits their taste, mood and the shows they love. "
               "No app connects what they watch with what they hear.",
    "Evidence": "4 of 10 users report a discovery or personalization pain; 3 of 10 report missing exclusive, "
                "regional or language content; Engagement is the weakest journey stage for all 3 segments (Sheet 2).",
    "Why it matters (user)": "Time lost scrolling; the story ends at the credits; local culture is buried.",
    "Why it matters (Netflix)": "Listening hours earn nothing today; a second daily habit lowers churn.",
    "How might we": "How might we turn what members watch into what they love to listen to?",
}

JTBD = [
    ("Binge-Watcher", "finish an episode", "keep living in that show's world",
     "stay connected to the story and its characters"),
    ("Casual Listener", "am working or relaxing", "get the right music instantly",
     "focus or unwind without effort"),
    ("Regional Listener", "want music from my culture", "find local artists and podcasts in my language",
     "feel represented, not buried under global hits"),
]

# problem -> MVP feature -> hypothesis -> metric
MVP_MAP = [
    ("Discovery is generic", "Watch-history discovery + AI daily mix",
     "If music matches what members watch, they will listen every week", "40% weekly active"),
    ("Content is the same everywhere", "Show soundtrack hubs + exclusive audio",
     "Exclusives give a reason to choose Netflix Music", "30% of listening Netflix-linked"),
    ("The story ends at the credits", "'Listen' button after credits + Netflix sign-in",
     "In-product entry drives trial without paid marketing", "5% of members activate"),
    ("Ads and no offline break the habit", "Ad-free premium + offline downloads",
     "Users will pay to remove friction", "25% free-to-premium"),
]

MVP_OUT = [
    ("Mood playlists", "Casual Listeners are the second wave; ships in User Growth"),
    ("Regional hubs", "Needs regional content deals first"),
    ("Podcast + music hybrid", "Lowest RICE and WSJF, highest effort"),
    ("Collaborative playlists", "No user asked; a share link covers the need"),
    ("Karaoke, hi-fi audio", "Delighters for later; not needed to prove the core"),
]

# ---- cover page (shared by the deck and the visuals PDF) -------------------------
COVER = {
    "label": "PRODUCT MANAGEMENT",
    "title": "Launching Netflix Music",
    "subtitle": "Product sense, problem definition and MVP for a personalized audio app",
    "details": [
        ("SUBMITTED BY", "Sharmistha Chakrabortty"),
        ("ROLE", "Aspiring Product Manager"),
        ("UNIVERSITY", "UC San Diego Extended Studies"),
        ("PROGRAM", "AI-Powered Product Management Professional Program"),
        ("DATE", "October 19, 2026"),
    ],
}
