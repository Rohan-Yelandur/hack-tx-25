Why Supabase?
  - Free tier with 1GB storage
  - Built-in authentication
  - PostgreSQL database + file storage in one
  - Simple REST API
  - Fast setup (15-20 minutes)

  Implementation Plan:

  A. Storage Setup:
  // Store videos in Supabase Storage bucket
  // Store metadata in PostgreSQL table

  Database Table: `videos`
  - id (uuid)
  - prompt (text)
  - video_url (text)
  - manim_code (text)
  - created_at (timestamp)
  - user_id (uuid, optional for auth)
  - likes (integer, for community engagement)

  B. Flow:
  1. User generates video → Backend saves to Supabase Storage
  2. Backend stores metadata (prompt, URL, code) in PostgreSQL
  3. Frontend fetches all videos for community page
  4. Check cache before generating new video

  Quick Setup Steps:
  # 1. Install Supabase client
  pip install supabase

  # 2. In backend, add to requirements.txt:
  supabase

  # 3. Create .env variables:
  SUPABASE_URL=your_project_url
  SUPABASE_KEY=your_anon_key

  2. Even Faster Alternative: Cloudinary

  Why Cloudinary?
  - Specializes in media storage
  - Free tier: 25GB storage, 25GB bandwidth/month
  - Video transformations built-in
  - Simpler API than Supabase for just video storage

  Pros:
  - Faster to implement (10 minutes)
  - Auto-generates thumbnails
  - CDN included

  Cons:
  - Need separate database for metadata (could use Supabase's free PostgreSQL)

  3. Caching System Options

  Option A: Simple File-Based Cache (Fastest - 5 minutes)
  # Hash the prompt → check if video exists locally
  # If exists, return cached video
  # If not, generate and save with hashed filename

  import hashlib

  def get_cache_key(prompt):
      return hashlib.md5(prompt.lower().strip().encode()).hexdigest()

  # Check: manim_videos/{hash}.mp4

  Option B: Redis Cache (Recommended for production)
  - Store prompt → video_url mappings
  - Fast lookups
  - Can set expiration times
  - Free tier on Railway/Render

  Option C: Database Cache (Best for hackathon)
  - Use Supabase PostgreSQL
  - Query existing videos by prompt similarity
  - No extra infrastructure needed

  My Recommendation for Hackathon Speed:

  Quickest Path (30-45 minutes total):

  1. Supabase for everything:
    - Storage bucket for videos
    - PostgreSQL for metadata + cache lookups
    - Optional: Auth for user features
  2. Implementation:
    - Backend: Add Supabase upload after video generation
    - Frontend: New "Community" page showing all videos
    - Cache: Query database before generating (check if prompt already exists)

  Alternative Super Fast (20 minutes):

  1. Cloudinary for video storage only
  2. Simple hash-based file cache locally (no database)
  3. Skip community page or show local videos only

  Would you like me to implement the Supabase approach? I can:
  1. Set up the Supabase integration in your backend
  2. Add caching logic to check before generating
  3. Create a basic Community page component in the frontend
  4. Update the backend to save videos to Supabase

  Just let me know if you want to go with Supabase, and I'll get it set up! You'll just need to:
  1. Create a free Supabase account
  2. Create a new project
  3. Give me the project URL and anon key

  Or would you prefer the simpler file-based cache approach first?