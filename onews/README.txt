COMPLETELY ORIGINAL NEWS

Takes articles from 'The Conversation'
Uses text from the articles to generate more text with the DeepAI Text API
	The DeepAI Text API is like the OpenAI text generator but it is free and it is not as good
Uses the generated text to populate an article: Title and Body

Most of this is done in the scheduler app, that's where all the code is.

NOTE: 	This project is a work in progress - just started.
	Views and Admin are not set up properly. I intend to finish them off over the weekend
	Also to add images scraped from a google image search using Article.Title_Text.

NOTE: the scheduler and the test program do not work together, before running the test program set SCHEDULER_AUTOSTART = False in settings.py