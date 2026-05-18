gameplot will be a place to record the video games you are playing. it will allow you to review and tag these games. it will allow you to write reviews of these games and hotlink these reviews out-of-context in a publicaly accessible way. 

ultimately: gameplot is the next step above organizing the games you play in an excel spreadsheet.

# pillars (aka the manifesto)

* your data is:
    * easily transferrable -- download as CSV should always be available
    * never sold -- the product is the subscription, not the user
    * densely presented -- we show the user as many pieces of their media as we can, and give them tools for bulk editing
* the team must be:
    * transparent in identity -- the internet is collectively put off by there being no face to the passportdex team
    * transparent in workflow -- develop in the open, strategize in the open -- the moat is not the code: the moat is having the gall to publish a website without a stylesheet in 2026. and being consistent about providing a good service.
        * this document is, too, part of this pillar
    * avoidant of AI tooling -- the gaming community is incredibly off-put by AI generated assets and flaky software
    * dogfooders
* the site must:
    * load incredibly quickly
    * present the least friction possible for reviewing a game or marking it as played
    * degrade gracefully in low network conditions
        * originally I liked the idea of degrading without JS too, but this is not realistic for the widgets in the mvp below. so we split the difference and publish the API.
* the subscription must:
    * pay for the platform
        * this dictates many of the other design decisions -- i.e. asset storage is expensive, so we cannot directly host high quality image assets. 
    * be cheap -- the service is only cool if lots of people are writing high quality game reviews
    * be optional -- the service should provide real value even if you're on a free account -- not just try to upsell the user
    * give kickbacks -- we shouldn't charge users that are pulling in a lot of traffic to the site
        * affiliate links are cool for this. signups that occur due to a linked review should decrease that linked user's monthly subscription. users that write reviews that consistently drive signups should be gifted the subscription outright. 


# mvp (aka when am I gonna post this on Show HN?)

### widgets that will be used across the site
* the spreadsheet
    * shows the logged in user's tagged media in compact rows
    * should allow the user to sort any column by single/double/triple clicking on the column to cycle through sort modes
        * should default to "playthrough end date" 
    * contains metadata columns relevant to the user:
        * external metadata -- title, brief description, release date, platform, maybe iconography -- linked to the game's page directly
        * start/end date for a playthrough -- no end date for an active playthrough
            * along with buttons to start, finish, cut short, or resume a particular playthrough
        * view your review/make a review
* the rich text editor
    * should be flexible enough to both edit a user's bio and create a review
    * should allow for a cumulative total filesize per-review, including embedded images
    * should regularly autosave a user's edits via a slug unique to that particular editor's context
* the rich text renderer
    * for rendering out user bios and reviews
* the game finder
    * a flexible search box widget that hits a dedicated endpoint for game searching
    * will eventually support a wider variety 
### the API
* unauthenticated
    * get user
    * get playthroughs by user
    * get game
    * get playthroughs by game
    * get review
    * get reviews by game
    * get reviews by user
    * fuzzyfind game
* authenticated (CUD = Create/Update/Delete)
    * CUD playthroughs for logged in user
    * CUD review for logged in user
    * "thumbs up" other reviews
    * UD logged in user themselves
    * CUD draft slugs for the rich text editor
    * submit request to add game to DB
    * submit request to deduplicate games from DB
### the page layout
* the homepage
    * spreadsheet widget immediately at the top, reduced in size to only show a few rows
    * "what's new" block: site updates, recently added games, recently reviewed games
* the "request a game" page
    * accepts a game title and a link to a webpage that is associated with said game
    * will operate on a set of whitelisted URLs that are displayed to the user -- sites for which we've developed connectors to scrape a banner image or a basic decsription
* the admin page
    * shows the review queue for games that users have requested to add
        * shows controls to reject a request, approve a request, or merge a game as a new platform for an existing game
    * shows the review queue for games that users have requested to merge
        * with controls to reject or approve a merge
    * admin-authenticated users should also have CRUD permissions on the game pages themselves to fix any issues that arise
    * and there ought to be a "reported content" queue too, huh? for reviews and for
* the game page
    * shows the information stored about the game at the top, including known platforms with backlinks and scraped descriptions with attribution
    * shows an aggregation of review stats -- number of reviews, game ranking by activity, etc
    * shows a list of reviews sorted by date (nonconfigurably), along with a single selected "top supportive" and "top critical" review
        * each review should allow permalinking and should link back to the author's page
* the user page
    * shows a user's join date, rich text bio, and a read-only rendering of their compact spreadsheet
    * shows a date-ordered readout of reviews the user has written, with backlinks to the game's page

# after the mvp
* user-applied tags on games (as a substitute for having various lists of games ala goodreads)
* top-N view of user-applied tags above
* filtering for subsets of your games on the spreadsheet
* the whole subscription service -- see featureset below, none of these overlap with the mvp


# footnotes
* it's difficult to design a subscription that is both optional and compelling.
    * three categories of features that are good fits for the subscription: high liability features, high cost features, brand-divorcing features
        * high cost: HQ asset storage for screenshots, longer length reviews, more customization on a user's page
        * high liability: auto-library import from Steam/itch/epic, skipping the review process for adding a game to the DB and reflecting it in a user's spreadsheet immediately
        * brand-divorcing: link a review or a user's spreadsheet directly in a way that looks classy and strips the rest of the page away