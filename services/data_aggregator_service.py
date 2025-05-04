from models import db, User, PlatformAccount, SavedContent
from datetime import datetime
import time # For mock delay

class DataAggregatorService:

    def _fetch_youtube_content(self, access_token):
        """Mocks fetching saved YouTube content."""
        print(f"--- MOCK: Calling YouTube API with token: {access_token[:10]}... ---")
        # In a real app, use google-api-python-client to fetch saved/liked videos
        time.sleep(1) # Simulate network delay
        # Return mock data
        return [
            {'id': 'video1', 'title': 'Mock YouTube Video 1', 'url': 'http://youtube.com/watch?v=video1', 'publishedAt': '2023-10-26T10:00:00Z'},
            {'id': 'video2', 'title': 'Mock YouTube Video 2', 'url': 'http://youtube.com/watch?v=video2', 'publishedAt': '2023-10-25T15:30:00Z'}
        ]

    def _fetch_twitter_content(self, access_token):
        """Mocks fetching saved Twitter content (e.g., liked tweets)."""
        print(f"--- MOCK: Calling Twitter (X) API with token: {access_token[:10]}... ---")
         # In a real app, use tweepy or similar
        time.sleep(1) # Simulate network delay
        # Return mock data
        return [
            {'id': 'tweet1', 'text': 'Mock Tweet 1', 'url': 'http://twitter.com/user/status/tweet1', 'created_at': 'Wed Oct 25 20:00:00 +0000 2023'},
            {'id': 'tweet2', 'text': 'Mock Tweet 2', 'url': 'http://twitter.com/user/status/tweet2', 'created_at': 'Wed Oct 25 21:00:00 +0000 2023'}
        ]

    def _fetch_reddit_content(self, access_token):
        """Mocks fetching saved Reddit content."""
        print(f"--- MOCK: Calling Reddit API with token: {access_token[:10]}... ---")
         # In a real app, use PRAW (Python Reddit API Wrapper)
        time.sleep(1) # Simulate network delay
        # Return mock data
        return [
            {'id': 'post1', 'title': 'Mock Reddit Post 1', 'url': 'http://reddit.com/r/subreddit/comments/post1', 'created_utc': 1698345600}, # UTC timestamp
            {'id': 'post2', 'title': 'Mock Reddit Post 2', 'url': 'http://reddit.com/r/subreddit/comments/post2', 'created_utc': 1698349200}
        ]

    def _normalize_content(self, platform, raw_data):
        """Mocks normalizing data from different platforms into a common schema."""
        normalized_list = []
        for item in raw_data:
            normalized_item = {
                'platform': platform,
                'original_id': str(item.get('id')), # Ensure string
                'title': None,
                'url': item.get('url'),
                'description': None,
                'content_type': None,
                'original_published_at': None
            }

            if platform == 'youtube':
                normalized_item['title'] = item.get('title')
                normalized_item['content_type'] = 'video'
                # Parse ISO 8601 string
                try:
                    normalized_item['original_published_at'] = datetime.strptime(item.get('publishedAt'), '%Y-%m-%dT%H:%M:%S%fZ')
                except (ValueError, TypeError):
                    pass # Handle parsing errors
                # YouTube API might need more logic to get full URL or description easily depending on endpoint

            elif platform == 'twitter':
                normalized_item['title'] = item.get('text') # Use text as title
                normalized_item['description'] = item.get('text')
                normalized_item['content_type'] = 'tweet'
                 # Parse Twitter date format: "Wed Oct 25 20:00:00 +0000 2023"
                try:
                     normalized_item['original_published_at'] = datetime.strptime(item.get('created_at'), '%a %b %d %H:%M:%S +0000 %Y')
                except (ValueError, TypeError):
                    pass

            elif platform == 'reddit':
                normalized_item['title'] = item.get('title')
                normalized_item['content_type'] = 'post'
                normalized_item['url'] = item.get('url') # Can be link or permalink
                # Handle timestamp (UTC)
                try:
                    normalized_item['original_published_at'] = datetime.utcfromtimestamp(item.get('created_utc'))
                except (ValueError, TypeError):
                     pass
                # Description might need fetching post content

            normalized_list.append(normalized_item)
        return normalized_list


    def sync_user_platform(self, user_id, platform):
        """Syncs saved content for a specific user and platform."""
        account = PlatformAccount.query.filter_by(user_id=user_id, platform=platform).first()
        if not account:
            print(f"--- SYNC: No {platform} account linked for user {user_id} ---")
            return False # No account linked

        access_token = account.access_token # In real app, handle token refresh if expired

        print(f"--- SYNC: Starting sync for user {user_id}, platform {platform} ---")

        raw_content = []
        if platform == 'youtube':
            raw_content = self._fetch_youtube_content(access_token)
        elif platform == 'twitter':
            raw_content = self._fetch_twitter_content(access_token)
        elif platform == 'reddit':
            raw_content = self._fetch_reddit_content(access_token)
        else:
             print(f"--- SYNC: Unsupported platform {platform} ---")
             return False

        normalized_content = self._normalize_content(platform, raw_content)

        # Save normalized content to the database
        new_items_count = 0
        for item_data in normalized_content:
            # Check if content already exists for this user/platform/original_id
            existing_content = SavedContent.query.filter_by(
                user_id=user_id,
                platform=platform,
                original_id=item_data['original_id']
            ).first()

            if not existing_content:
                # Add new content
                new_content = SavedContent(user_id=user_id, **item_data)
                db.session.add(new_content)
                new_items_count += 1
            else:
                # Optional: Update existing content if needed
                pass # For simplicity, we only add new items in this mock

        db.session.commit()
        print(f"--- SYNC: Finished sync for user {user_id}, platform {platform}. Added {new_items_count} new items. ---")
        return True

    def schedule_full_sync(self):
        """
        Mocks scheduling a full sync for all users/platforms.
        In a real app, this would submit jobs to a background queue.
        """
        print("\n--- SCHEDULER: Mocking full sync scheduler run ---")
        users = User.query.all()
        platforms = ['youtube', 'twitter', 'reddit'] # Define supported platforms

        for user in users:
            linked_platforms = self.get_user_linked_platforms(user.id)
            for platform in platforms:
                if platform in linked_platforms:
                    # In a real app: send this task to Celery/RQ
                    print(f"--- SCHEDULER: Submitting sync job for User {user.id}, Platform {platform} ---")
                    # Example: celery_app.send_task('tasks.sync_platform', args=[user.id, platform])
                    self.sync_user_platform(user.id, platform) # Directly calling for demo

        print("--- SCHEDULER: Mock sync scheduler run finished ---\n")


    def get_user_linked_platforms(self, user_id):
         """Helper to get platforms linked by a user."""
         user = User.query.get(user_id)
         if not user:
             return []
         return [acc.platform for acc in user.platform_accounts]


    def get_user_content(self, user_id, platform=None):
        """Retrieves aggregated content for a user."""
        query = SavedContent.query.filter_by(user_id=user_id).order_by(SavedContent.saved_at.desc())
        if platform:
            query = query.filter_by(platform=platform)
        return query.all()
