from collections import OrderedDict


SUBREDDIT_INFO = [
    ('Gifs', ['behindthegifs', 'bettereveryloop', 'brokengifs', 'Cinemagraphs', 'combinedgifs', 'educationalgifs', 'gif', 'gifextra', 'gifrecipes', 'gifs', 'gifsound', 'gifsthatkeepongiving', 'highqualitygifs', 'loadingicon', 'mechanical_gifs', 'michaelbaygifs', 'noisygifs', 'perfectloops', 'retiredgif', 'slygifs', 'splitdepthgifs', 'WastedGifs', 'wholesomegifs']),
    ('People', ['asianpeoplegifs', 'blackpeoplegifs', 'scriptedasiangifs', 'whitepeoplegifs']),
    ('Reaction', ['reactiongifs', 'shittyreactiongifs']),
    ('Science', ['chemicalreactiongifs', 'cogsci', 'everythingscience', 'geology', 'medicine', 'physicsgifs', 'Science']),
    ('Nature', ['babyelephantgifs', 'earthporn', 'hardcoreaww', 'heavyseas', 'hitmanimals', 'natureisfuckinglit', 'weathergifs']),
    ('Images', ['dogpictures', 'ExpectationVSReality', 'FifthWorldPics', 'foundpaper', 'images', 'itookapicture', 'miniworlds', 'misleadingthumbnails', 'nocontextpics', 'Pareidolia', 'perfecttiming', 'PhotoshopBattles', 'pic', 'pics', 'TheWayWeWere']),
    ('Interesting', ['beamazed', 'damnthatsinteresting', 'interestingasfuck', 'mildlyinteresting', 'reallifeshinies']),
    ('Images/Gifs of Women (SFW)', ['bois', 'fitandnatural', 'gentlemanboners', 'GentlemanBonersGifs', 'girlsmirin', 'goddesses', 'hardbodies', 'prettygirls', 'shorthairedhotties', 'skinnywithabs', 'thinspo', 'wrestlewiththeplot']),
    ('Asian', ['asiancuties', 'asiangirlsbeingcute']),
    ('Photoshop', ['colorization', 'ColorizedHistory', 'HybridAnimals', 'PhotoshopBattles', 'reallifedoodles']),
    ('Redditors/Selfies', ['amiugly', 'prettygirlsuglyfaces', 'rateme', 'roastme', 'uglyduckling']),
    ('Wallpapers', ['Offensive_Wallpapers', 'wallpaper', 'wallpapers']),
    ('Videos', ['artisanvideos', 'DeepIntoYouTube', 'killthecameraman', 'nottimanderic', 'praisethecameraman', 'videos', 'youtubehaiku']),
    ('General', ['accounting', 'applyingtocollege', 'architecture', 'awesome', 'blacksmith', 'bulletjournal', 'casualconversation', 'changemyview', 'college', 'CoolGuides', 'cosplay', 'crazyideas', 'crochet', 'crossstitch', 'cubers', 'digitalnomad', 'Disney', 'DiWHY', 'DIY', 'DoesAnybodyElse', 'dumpsterdiving', 'EDC', 'education', 'educationalgifs', 'entertainment', 'everymanshouldknow', 'fantheories', 'FastWorkers', 'Foodforthought', 'geek', 'GetStudying', 'gunpla', 'howto', 'howtonotgiveafuck', 'ifyoulikeblank', 'knitting', 'lawschool', 'LearnUselessTalents', 'lectures', 'lifehacks', 'LifeProTips', 'modelmakers', 'obscuremedia', 'preppers', 'ProtectAndServe', 'quotes', 'rainmeter', 'redneckengineering', 'RTLSDR', 'sewing', 'ShowerThoughts', 'simpleliving', 'somethingimade', 'teachers', 'tinyhouses', 'tipofmytongue', 'TrueReddit', 'UnethicalLifeProTips', 'urbanplanning', 'vandwellers', 'watchandlearn', 'woodworking', 'WorldBuilding', 'YouShouldKnow']),
    ('Advice/assistance', ['advice', 'bestoflegaladvice', 'legaladvice', 'raisedbynarcissists', 'relationship_advice']),
    ('AMA', ['AMA', 'casualiama', 'de_Iama', 'ExplainlikeIAmA', 'IAmA']),
    ('Games', ['AskOuija', 'boardgames', 'chess', 'jrpg', 'lego', 'poker', 'rpg', 'scenesfromahat', 'whowouldwin', 'wouldyourather']),
    ('Question/Answer', ['amiugly', 'answers', 'AskReddit', 'NoStupidQuestions', 'samplesize', 'tooafraidtoask', 'whatisthisthing', 'whatsthisbug', 'whatsthisplant']),
    ('Ask______', ['AskOuija', 'AskScienceFiction', 'ShittyAskScience', 'TrueAskReddit']),
    ('Occupation', ['askculinary', 'askengineers', 'askhistorians', 'askphilosophy', 'AskSocialScience']),
    ('Sex/Gender', ['askgaybros', 'askmen', 'askredditafterdark', 'asktransgender', 'askwomen']),
    ('Stories', ['confession', 'confessions', 'fatpeoplestories', 'self', 'tifu']),
    ('Customer Service', ['idontworkherelady', 'KitchenConfidential', 'starbucks', 'talesfromcallcenters', 'talesfromretail', 'talesfromtechsupport', 'talesfromthecustomer', 'TalesFromTheFrontDesk', 'talesfromthepharmacy', 'TalesFromThePizzaGuy', 'talesfromthesquadcar', 'TalesFromYourServer', 'techsupportmacgyver']),
    ('Revenge', ['pettyrevenge', 'prorevenge']),
    ('Scary/Weird', ['Glitch_in_the_Matrix', 'LetsNotMeet', 'nosleep', 'shortscarystories', 'thetruthishere', 'UnresolvedMysteries', 'UnsolvedMysteries']),
    ('Support', ['Anxiety', 'depression', 'foreveralone', 'offmychest', 'socialanxiety', 'SuicideWatch', 'trueoffmychest']),
    ('Facts', ['todayilearned', 'wikipedia']),
    ('Questions', ['IWantToLearn', 'OutOfTheLoop']),
    ('Explain Like...', ['explainlikeIAmA', 'ExplainLikeImCalvin', 'ExplainLikeImFive']),
    ('Anthropology', ['anthropology']),
    ('Art', ['animation', 'Art', 'artfundamentals', 'ArtPorn', 'breadstapledtotrees', 'drawing', 'graffiti', 'heavymind', 'illustration', 'learnart', 'pixelart', 'redditgetsdrawn', 'retrofuturism', 'sketchdaily', 'specart', 'streetart', 'wimmelbilder']),
    ('Painting', ['minipainting', 'painting']),
    ('Computer Science/Engineering', ['askengineers', 'cscareerquestions', 'engineering', 'EngineeringStudents', 'gamedev', 'ubuntu']),
    ('Coding', ['artificial', 'coding', 'compsci', 'cpp', 'dailyprogrammer', 'howtohack', 'java', 'javascript', 'learnprogramming', 'machinelearning', 'python']),
    ('Python', ['learnpython', 'python']),
    ('Economics', ['BasicIncome', 'business', 'Economics', 'entrepreneur', 'marketing']),
    ('Business', ['business', 'smallbusiness']),
    ('Stocks', ['stockmarket', 'stocks', 'wallstreetbets']),
    ('Environment', ['environment', 'zerowaste']),
    ('History', ['100yearsago', 'AskHistorians', 'badhistory', 'ColorizedHistory', 'history', 'historynetwork']),
    ('Historical Images', ['castles', 'historymemes', 'HistoryPorn', 'PropagandaPosters', 'TheWayWeWere']),
    ('Language', ['french', 'languagelearning', 'learnjapanese', 'linguistics']),
    ('Law', ['law']),
    ('Math', ['math', 'theydidthemath']),
    ('Medicine', ['medicalschool']),
    ('Psychology', ['JordanPeterson', 'psychology']),
    ('Astronomy', ['astronomy', 'astrophotography', 'nasa', 'SpacePorn', 'spacex']),
    ('Biology', ['Awwducational', 'biology']),
    ('Chemistry', ['chemicalreactiongifs', 'chemistry']),
    ('Physics', ['physics']),
    ('Anime/Manga', ['anime', 'anime_irl', 'animegifs', 'animemes', 'animesuggest', 'animewallpaper', 'awwnime', 'manga', 'TsundereSharks']),
    ('Individual Anime/manga', ['berserk', 'BokuNoHeroAcademia', 'dbz', 'DDLC', 'hunterxhunter', 'naruto', 'onepiece', 'onepunchman', 'pokemon', 'ShingekiNoKyojin', 'tokyoghoul', 'yugioh']),
    ('Books/Writing', ['Books', 'booksuggestions', 'boottoobig', 'freeEbooks', 'hfy', 'lifeofnorman', 'literature', 'lovecraft', 'poetry', 'screenwriting', 'suggestmeabook', 'writing', 'WritingPrompts']),
    ('Comics', ['bertstrips', 'comicbooks', 'comics', 'defenders', 'marvel', 'marvelstudios', 'polandball', 'webcomics']),
    ('Individual books/stories/comics', ['arrow', 'batman', 'calvinandhobbes', 'DCComics', 'deadpool', 'explainlikeimcalvin', 'harrypotter', 'KingkillerChronicle', 'spiderman', 'unexpectedhogwarts', 'xkcd']),
    ('Game of Thrones', ['asoiaf', 'freefolk', 'gameofthrones']),
    ('Lord of the Rings', ['lotr', 'lotrmemes', 'tolkeinfans']),
    ('Celebrities', ['celebhub', 'celebs']),
    ('Female', ['alexandradaddario', 'alisonbrie', 'EmilyRatajkowski', 'EmmaWatson', 'jenniferlawrence', 'jessicanigri', 'kateupton']),
    ('Male', ['crewscrew', 'donaldglover', 'elonmusk', 'joerogan', 'keanubeingawesome', 'onetruegod']),
    ('Cosplay', ['cosplay', 'cosplaygirls']),
    ('Dungeons and Dragons', ['criticalrole', 'DMAcademy', 'DnD', 'DnDBehindTheScreen', 'DnDGreentext', 'dndnext', 'dungeonsanddragons']),
    ('Magic', ['magicTCG', 'modernmagic']),
    ('Genres', ['classicalmusic', 'cyberpunk', 'gamemusic', 'indieheads', 'jazz', 'outrun', 'trap', 'vaporwave', 'zombies']),
    ('Fantasy', ['fantasy']),
    ('For other sci-fi subreddits, see here!', ['asksciencefiction', 'empiredidnothingwrong', 'prequelmemes', 'sciencefiction', 'scifi', 'SequelMemes', 'startrek', 'starwars']),
    ('Internet/Apps', ['bannedfromclubpenguin', 'bestofworldstar', 'creepyPMs', 'discordapp', 'facepalm', 'google', 'KenM', 'savedyouaclick', 'snaplenses', 'tronix', 'web_design', 'wikipedia']),
    ('4chan', ['4chan', 'Classic4chan', 'greentext']),
    ('Facebook', ['facebookwins', 'facepalm', 'indianpeoplefacebook', 'insanepeoplefacebook', 'oldpeoplefacebook', 'terriblefacebookmemes']),
    ('Internet Dating', ['OkCupid', 'Tinder']),
    ('Internet Politics', ['KotakuInAction', 'shitcosmosays', 'wikileaks']),
    ('Live Streaming', ['livestreamfail', 'twitch']),
    ('Podcasts', ['podcasts', 'serialpodcast']),
    ('Tumblr', ['tumblr', 'tumblrinaction']),
    ('Twitter', ['blackpeopletwitter', 'latinopeopletwitter', 'scottishpeopletwitter', 'WhitePeopleTwitter', 'wholesomebpt']),
    ('YouTube', ['youtube', 'YoutubeHaiku']),
    ('Individual YouTubers/Companies', ['CGPGrey', 'cynicalbrit', 'defranco', 'gamegrumps', 'h3h3productions', 'Idubbbz', 'jontron', 'loltyler1', 'pewdiepiesubmissions', 'pyrocynical', 'RedLetterMedia', 'SovietWomble', 'videogamedunkey', 'yogscast']),
    ('Roosterteeth', ['cowchop', 'funhaus', 'roosterteeth', 'rwby']),
    ('Movies', ['bollywoodrealism', 'cinematography', 'continuityporn', 'documentaries', 'fullmoviesonvimeo', 'fullmoviesonyoutube', 'ghibli', 'moviedetails', 'movies', 'moviesinthemaking', 'shittymoviedetails', 'truefilm']),
    ('Individual Movies/Series', ['harrypotter', 'lotr', 'lotrmemes', 'otmemes', 'starwars']),
    ('Comic movies', ['batman', 'DC_Cinematic', 'intothesoulstone', 'marvelstudios', 'thanosdidnothingwrong']),
    ('Music', ['ableton', 'drums', 'edmproduction', 'FL_Studio', 'fakealbumcovers', 'futurebeats', 'guitar', 'guitarlessons', 'listentothis', 'mashups', 'music', 'musictheory', 'piano', 'spotify', 'vinyl', 'WeAreTheMusicMakers']),
    ('Artists', ['beatles', 'brockhampton', 'deathgrips', 'donaldglover', 'eminem', 'frankocean', 'gorillaz', 'kanye', 'KendrickLamar', 'pinkfloyd', 'radiohead']),
    ('Electronic', ['dubstep', 'EDM', 'edmproduction', 'electronicmusic']),
    ('Hip Hop', ['hiphopheads', 'hiphopimages']),
    ('Metal', ['Metal', 'Metalcore']),
    ('Pop', ['funkopop', 'kpop', 'popheads', 'spop']),
    ('Instruments', ['bass', 'drums', 'guitar', 'piano']),
    ('Sports subreddits!', ['bicycling', 'cricket', 'discgolf', 'fishing', 'golf', 'rugbyunion', 'running', 'sailing', 'skiing', 'sports', 'sportsarefun', 'tennis']),
    ('American Football', ['CFB', 'fantasyfootball', 'nfl', 'nflstreams']),
    ('American Football Teams', ['eagles', 'greenbaypackers', 'minnesotavikings', 'patriots']),
    ('Baseball', ['baseball', 'fantasybaseball', 'mlb']),
    ('Basketball', ['collegebasketball', 'nba', 'nbastreams']),
    ('Teams', ['bostonceltics', 'lakers', 'torontoraptors', 'warriors']),
    ('Boards', ['longboarding', 'skateboarding', 'snowboarding']),
    ('Cars', ['formula1', 'Nascar']),
    ('Fighting', ['boxing', 'MMA', 'MMAStreams', 'squaredcircle', 'theocho', 'ufc', 'wwe']),
    ('Hockey', ['hockey', 'leafs', 'nhl', 'nhlstreams']),
    ('Olympics', ['apocalympics2016', 'olympics']),
    ('Soccer', ['Bundesliga', 'fantasypl', 'futbol', 'MLS', 'soccer', 'soccerstreams', 'worldcup']),
    ('Soccer Teams', ['chelseafc', 'gunners', 'LiverpoolFC', 'reddevils']),
    ('TV', ['cordcutters', 'japanesegameshows', 'marvelstudios', 'offlinetv', 'shield', 'Television', 'tvdetails']),
    ('Individual Shows', ['30rock', 'AmericanHorrorStory', 'arresteddevelopment', 'BetterCallSaul', 'bigbrother', 'blackmirror', 'BreakingBad', 'brooklynninenine', 'community', 'DunderMifflin', 'FilthyFrank', 'firefly', 'FlashTV', 'GameOfThrones', 'HIMYM', 'houseofcards', 'howyoudoin', 'lifeisstrange', 'MakingaMurderer', 'mrrobot', 'orangeisthenewblack', 'PandR', 'riverdale', 'rupaulsdragrace', 'scrubs', 'Sherlock', 'siliconvalleyhbo', 'StarTrek', 'strangerthings', 'supernatural', 'survivor', 'thegrandtour', 'thewalkingdead', 'topgear', 'trailerparkboys', 'TrueDetective', 'twinpeaks', 'westworld']),
    ('Animated', ['AdventureTime', 'ArcherFX', 'BobsBurgers', 'BoJackHorseman', 'familyguy', 'futurama', 'gravityfalls', 'kingofthehill', 'mylittlepony', 'naruto', 'onepunchman', 'Pokemon', 'rickandmorty', 'southpark', 'spongebob', 'stevenuniverse', 'TheLastAirbender', 'TheSimpsons']),
    ('Dragon Ball Z', ['dbz', 'DBZDokkanBattle', 'dragonballfighterz']),
    ('Doctor Who', ['doctorwho', 'gallifrey']),
    ('It\'s Always Sunny in Philadelphia', ['IASIP', 'the_dennis']),
    ('Seinfeld', ['redditwritesseinfeld', 'seinfeld', 'seinfeldgifs']),
    ('Netflix Related', ['bestofnetflix', 'Netflix', 'NetflixBestOf']),
    ('Aquariums', ['aquariums', 'plantedtank']),
    ('Arts/Writing', ['alternativeart', 'art', 'artporn', 'coloringcorruptions', 'crafts', 'DisneyVacation', 'Drawing', 'glitch_art', 'illustration', 'restofthefuckingowl', 'sketchdaily']),
    ('Writing', ['calligraphy', 'fountainpens', 'handwriting', 'screenwriting', 'twosentencehorror', 'Writing', 'writingprompts']),
    ('Automotive', ['AutoDetailing', 'autos', 'awesomecarmods', 'carporn', 'cars', 'cartalk', 'justrolledintotheshop', 'motorcycles', 'projectcar', 'roadcam', 'Shitty_Car_Mods', 'tiresaretheenemy']),
    ('Car companies', ['bmw', 'jeep', 'subaru', 'teslamotors']),
    ('Design', ['assholedesign', 'ATBGE', 'CrappyDesign', 'design', 'designporn', 'dontdeadopeninside', 'graphic_design', 'InteriorDesign', 'keming', 'logodesign', 'tombstoning', 'web_design']),
    ('Fake it til you make it', ['actlikeyoubelong', 'irlsmurfing']),
    ('Combat', ['army', 'combatfootage', 'military', 'militarygfys', 'MilitaryPorn', 'warshipporn']),
    ('Guns', ['airsoft', 'ar15', 'ccw', 'firearms', 'gundeals', 'gunporn', 'guns']),
    ('Job finding', ['cscareerquestions', 'forhire', 'Jobs', 'workonline']),
    ('Outdoors', ['backpacking', 'camping', 'campinggear', 'gardening', 'homestead', 'MTB', 'outdoors', 'survival', 'urbanexploration', 'wildernessbackpacking']),
    ('Hiking', ['campingandhiking', 'hiking', 'ultralight']),
    ('Photography/Film', ['analog', 'astrophotography', 'Filmmakers', 'itookapicture', 'photocritique', 'photography']),
    ('Planes', ['aviation', 'flying']),
    ('Tech Related', ['compsci', 'engineering', 'graphic_design', 'itsaunixsystem', 'mechanicalkeyboards', 'multicopter', 'plex', 'programmerhumor', 'programminghorror', 'reverseengineering', 'sysadmin', 'webdev']),
    ('PC Building', ['buildapc', 'buildapcforme', 'buildapcsales']),
    ('Tech Support', ['iiiiiiitttttttttttt', 'softwaregore', 'talesfromtechsupport', 'techsupport', 'techsupportgore']),
    ('Tools', ['knifeclub', 'knives', 'lockpicking', 'specializedtools', 'watches']),
    ('Travel', ['japantravel', 'solotravel', 'travel']),
    ('Gender', ['malelifestyle', 'malelivingspace', 'TheGirlSurvivalGuide']),
    ('Home', ['battlestations', 'homeautomation', 'homeimprovement', 'homelab', 'hometheater']),
    ('Communities', ['ADHD', 'aliensamongus', 'bipolar', 'introvert', 'neverbrokeabone', 'polyamory', 'teachers', 'teenagers', 'totallynotrobots']),
    ('Body/Diet', ['beards', 'swoleacceptance', 'tall', 'vegan']),
    ('LGBT', ['actuallesbians', 'ainbow', 'askgaybros', 'bisexual', 'gay', 'gay_irl', 'gaybros', 'gaymers', 'lgbt']),
    ('Transgender', ['asktransgender', 'transgender']),
    ('Parenting', ['babybumps', 'daddit', 'parenting']),
    ('Alcohol', ['bourbon', 'cocktails', 'drunk', 'scotch', 'stopdrinking', 'whiskey', 'wine']),
    ('Beer', ['beer', 'beerporn', 'homebrewing', 'showerbeer']),
    ('Marijuana', ['cannabis', 'eldertrees', 'leaves', 'marijuana', 'microgrowery', 'see', 'trees', 'weed', 'weedstocks']),
    ('Other drugs', ['dmt', 'drugs', 'electronic_cigarette', 'LSD', 'Nootropics', 'shrooms', 'stonerengineering', 'stopsmoking', 'Vaping', 'vaporents']),
    ('Exercise/Health', ['GetMotivated', 'health', 'Medicine', 'ZenHabits']),
    ('Mental', ['LucidDreaming', 'meditation', 'mentalhealth', 'Psychonaut']),
    ('Physical', ['Fitness', 'xxfitness']),
    ('Diet', ['fasting', 'fitmeals', 'HealthyFood', 'intermittentfasting', 'leangains', 'nutrition', 'paleo', 'vegetarian']),
    ('Keto', ['keto', 'ketogains', 'ketorecipes']),
    ('Exercise', ['backpacking', 'bicycling', 'bjj', 'climbing', 'crossfit', 'skateboarding', 'skiing', 'yoga']),
    ('Lifting/Weights', ['bodybuilding', 'powerlifting', 'WeightRoom']),
    ('Running', ['c25k', 'running']),
    ('Weight/Body Shape Control', ['bodyweightfitness', 'flexibility', 'gainit', 'loseit', 'swoleacceptance']),
    ('Progress Pictures', ['brogress', 'progresspics']),
    ('Body Image', ['AsianBeauty', 'beards', 'makeupaddiction', 'piercing', 'RedditLaqueristas', 'SkincareAddiction', 'wicked_edge']),
    ('Hair', ['curlyhair', 'FancyFollicles', 'malehairadvice']),
    ('Tattoos', ['badtattoos', 'tattoo', 'tattoos']),
    ('Fashion', ['fashion', 'FashionReps', 'femalefashionadvice', 'frugalmalefashion', 'malefashion', 'malefashionadvice', 'streetwear', 'supremeclothing', 'thriftstorehauls']),
    ('Shoes', ['goodyearwelt', 'repsneakers', 'sneakers']),
    ('Food', ['eatsandwiches', 'food', 'foodhacks', 'FoodPorn', 'forbiddensnacks', 'mealtimevideos', 'nutrition', 'seriouseats', 'shittyfoodporn', 'WeWantPlates']),
    ('Cooking', ['askculinary', 'baking', 'breadit', 'castiron', 'cooking', 'cookingforbeginners', 'instantpot', 'mealprepsunday', 'slowcooking', 'smoking']),
    ('Diets', ['1200isplenty', 'budgetfood', 'Cheap_Meals', 'EatCheapAndHealthy', 'fasting', 'fitmeals', 'HealthyFood', 'intermittentfasting', 'ketorecipes', 'vegan', 'veganrecipes']),
    ('Drinks (non-alcoholic)', ['coffee', 'tea']),
    ('Recipes', ['gifrecipes', 'recipes', 'veganrecipes']),
    ('Specific food', ['bbq', 'grilledcheese', 'pizza', 'ramen', 'sushi']),
    ('Money', ['antimlm', 'apphookup', 'beermoney', 'churning', 'economy', 'Entrepreneur', 'finance', 'financialindependence', 'flipping', 'Iota', 'PersonalFinance', 'realestate', 'ripple', 'startups', 'stellar']),
    ('Betting/Investing/Stocks', ['investing', 'millionairemakers', 'wallstreetbets', 'weedstocks']),
    ('Budget', ['budgetfood', 'cheap_meals', 'EatCheapAndHealthy', 'frugal', 'Frugal_Jerk', 'frugalmalefashion', 'povertyfinance']),
    ('Consumerism', ['Anticonsumption', 'BuyItForLife', 'crappyoffbrands', 'sbubby', 'shouldibuythisgame', 'shutupandtakemymoney', 'Wellworn']),
    ('CryptoCurrency', ['Bitcoin', 'btc', 'cardano', 'CryptoCurrency', 'dogecoin', 'ethereum', 'ethtrade', 'garlicoin', 'litecoin', 'Vechain']),
    ('Religion/Beliefs', ['Buddhism', 'occult', 'Psychonaut', 'Stoicism']),
    ('Atheism', ['atheism', 'trueatheism']),
    ('Christianity', ['Catholicism', 'Christianity', 'dankchristianmemes', 'exmormon']),
    ('Philosophy', ['askphilosophy', 'philosophy']),
    ('Relationships/Sex', ['socialengineering', 'socialskills', 'weddingplanning']),
    ('Family', ['childfree', 'daddit', 'incest', 'justnofamily', 'justnomil', 'Parenting', 'raisedbynarcissists']),
    ('Relationships', ['dating_advice', 'relationship_advice', 'relationships']),
    ('Online Relationships', ['dirtyr4r', 'longdistance', 'OKCupid', 'r4r', 'Tinder']),
    ('Sex', ['deadbedrooms', 'nofap', 'polyamory', 'seduction', 'sex']),
    ('Self-Improvement', ['DecidingToBeBetter', 'getdisciplined', 'GetMotivated', 'GetStudying', 'happy', 'happycrowds', 'humansbeingbros', 'iwantout', 'mademesmile', 'productivity', 'QuotesPorn', 'selfimprovement', 'sportsarefun']),
    ('Technology', ['technology']),
    ('More tech related subreddits, from the sidebar of /r/technology, can be found here.', ['aboringdystopia', 'buildapc', 'cableporn', 'compsci', 'crackwatch', 'design', 'engineering', 'EngineeringPorn', 'futurology', 'gamedev', 'hacking', 'imaginarytechnology', 'infographics', 'internetisbeautiful', 'jailbreak', 'netsec', 'networking', 'onions', 'opensource', 'pcmasterrace', 'php', 'piracy', 'privacy', 'simulated', 'talesfromtechsupport', 'tech', 'technology', 'torrents', 'unixporn', 'virtualreality']),
    ('3D Printing', ['3Dprinting', 'functionalprint']),
    ('Business Tech', ['amd', 'firefox', 'nasa', 'nintendo', 'nvidia', 'photoshop', 'spacex']),
    ('Android products', ['Android', 'AndroidApps', 'AndroidDev', 'AndroidGaming', 'AndroidThemes', 'oneplus']),
    ('Apple Products', ['apple', 'applewatch', 'ipad', 'iphone', 'mac']),
    ('Gadgets', ['amazonecho', 'arduino', 'blender', 'electronics', 'gadgets', 'gopro', 'raspberry_pi', 'RetroPie', 'trackers']),
    ('Hardware', ['hardware', 'hardwareswap']),
    ('Kodi', ['Addons4Kodi', 'kodi']),
    ('Google Products', ['chromecast', 'google', 'googlehome', 'googlepixel']),
    ('Linux', ['archlinux', 'linux', 'linux4noobs', 'linux_gaming', 'linuxmasterrace']),
    ('Microsoft Products', ['excel', 'microsoft', 'surface', 'windows', 'Windows10']),
    ('Data', ['DataHoarder', 'dataisbeautiful']),
    ('Digital Currency', ['Bitcoin', 'bitcoinmarkets', 'btc', 'CryptoCurrency', 'cryptomarkets', 'dogecoin', 'ethereum', 'ethtrader', 'litecoin', 'monero', 'neo']),
    ('Programming', ['excel', 'java', 'javascript', 'learnprogramming', 'learnpython', 'programming', 'python', 'unity3d']),
    ('Sound', ['audioengineering', 'audiophile', 'headphones']),
    ('General Humor', ['accidentalcomedy', 'ChildrenFallingOver', 'ComedyCemetery', 'comedyheaven', 'comedyhomicide', 'comedynecromancy', 'contagiouslaughter', 'dadreflexes', 'funny', 'funnyandsad', 'humor', 'kenm', 'kidsarefuckingstupid', 'notkenm', 'politicalhumor', 'prematurecelebration', 'ProgrammerHumor', 'standupcomedy']),
    ('Jokes', ['3amjokes', 'antijokes', 'dadjokes', 'darkjokes', 'meanjokes', 'punny', 'puns', 'standupshots', 'WordAvalanches']),
    ('Memes/Rage comics', ['copypasta', 'Demotivational', 'emojipasta', 'lolcats', 'supershibe']),
    ('Memes and Rage Comics', ['starterpacks', 'TrollXChromosomes', 'trollychromosome']),
    ('Memes', ['absoluteunits', 'AdviceAnimals', 'animemes', 'bidenbro', 'BikiniBottomTwitter', 'bonehurtingjuice', 'bossfight', 'dank_meme', 'dankchristianmemes', 'dankmemes', 'deepfriedmemes', 'delightfullychubby', 'equelmemes', 'garlicbreadmemes', 'gocommitdie', 'historymemes', 'ilikthebred', 'kappa', 'lotrmemes', 'madlads', 'meme', 'memeeconomy', 'memes', 'Memes_Of_The_Dank', 'namflashbacks', 'offensivememes', 'otmemes', 'Overwatch_Memes', 'prequelmemes', 'raimememes', 'rarepuppers', 'see', 'SequelMemes', 'smoobypost', 'suddenlygay', 'surrealmemes', 'terriblefacebookmemes', 'trebuchetmemes', 'trippinthroughtime', 'wholesomegreentext', 'wholesomememes']),
    ('____irl', ['2meirl4meirl', 'absolutelynotme_irl', 'absolutelynotmeirl', 'anime_irl', 'me_irl', 'meirl', 'meow_irl', 'TooMeIrlForMeIrl', 'woof_irl']),
    ('Rage Comics', ['fffffffuuuuuuuuuuuu', 'iiiiiiitttttttttttt']),
    ('Animals', ['AnimalPorn', 'AnimalsBeingBros', 'AnimalsBeingDerps', 'AnimalsBeingJerks', 'animalsthatlovemagic', 'animaltextgifs', 'BeforeNAfterAdoption', 'bigboye', 'brushybrushy', 'curledfeetsies', 'Floof', 'hitmanimals', 'HybridAnimals', 'likeus', 'mlem', 'properanimalnames', 'shittyanimalfacts', 'sneks', 'spiderbro', 'stoppedworking', 'TsundereSharks', 'whatsthisbug', 'zoomies']),
    ('Birds', ['birbs', 'birdsbeingdicks', 'birdswitharms', 'emuwarflashbacks', 'partyparrot', 'superbowl']),
    ('Mammals', ['babyelephantgifs', 'foxes', 'goatparkour', 'happycowgifs', 'rabbits', 'sloths', 'trashpandas']),
    ('Cats', ['babybigcatgifs', 'bigcatgifs', 'blackcats', 'catgifs', 'catloaf', 'catpictures', 'catpranks', 'cats', 'catsareassholes', 'catsareliquid', 'catsisuottatfo', 'catslaps', 'catsstandingup', 'CatSubs', 'cattaps', 'holdmycatnip', 'jellybeantoes', 'meow_irl', 'startledcats', 'stuffoncats', 'supermodelcats', 'teefies', 'thecatdimension', 'thisismylifemeow', 'tuckedinkitties']),
    ('Dogs', ['barkour', 'blop', 'dogberg', 'dogpictures', 'dogs', 'dogswithjobs', 'dogtraining', 'masterreturns', 'petthedamndog', 'puppies', 'puppysmiles', 'WhatsWrongWithYourDog', 'woof_irl']),
    ('Breeds', ['babycorgis', 'corgi', 'goldenretrievers', 'incorgnito', 'Pitbulls']),
    ('Conspiracy', ['conspiracy', 'conspiratard', 'empiredidnothingwrong', 'karmaconspiracy', 'scp', 'skeptic', 'UFOs']),
    ('Cringe', ['4PanelCringe', 'accidentalracism', 'amibeingdetained', 'blunderyears', 'corporatefacepalm', 'cringe', 'cringepics', 'engrish', 'facepalm', 'fatlogic', 'fellowkids', 'instant_regret', 'instantbarbarians', 'lewronggeneration', 'masterhacker', 'publicfreakout', 'sadcringe', 'technicallythetruth', 'watchpeopledieinside', 'wokekids']),
    ('Called out', ['atetheonion', 'badfaketexts', 'beholdthemasterrace', 'boneappletea', 'delusionalartists', 'delusionalcraigslist', 'dontfundme', 'dontyouknowwhoiam', 'facepalm', 'facingtheirparenting', 'goodfaketexts', 'iamatotalpieceofshit', 'ihadastroke', 'ihavesex', 'lostredditors', 'murderedbywords', 'NobodyAsked', 'nothingeverhappens', 'oopsdidntmeanto', 'phonesarebad', 'quityourbullshit', 'suicidebywords', 'suspiciousquotes', 'thathappened', 'topmindsofreddit', 'untrustworthypoptarts', 'vaxxhappened', 'woooosh', 'wowthanksimcured']),
    ('"Neckbeard"', ['ChoosingBeggars', 'creepyasterisks', 'gatekeeping', 'humblebrag', 'iamverybadass', 'iamverysmart', 'inceltears', 'justneckbeardthings', 'mallninjashit', 'neckbeardnests', 'neckbeardrpg', 'nicegirls', 'niceguys', 'nothowdrugswork', 'whiteknighting']),
    ('Cute', ['animalsbeingbros', 'animalsbeingjerks', 'aww', 'Awwducational', 'awww', 'babycorgis', 'blep', 'cats', 'corgi', 'dogs', 'eyebeach', 'thisismylifenow', 'tippytaps']),
    ('Disgusting/Angering/Scary/Weird (Note: Potentially NSFL)', ['awwwtf', 'DeepIntoYouTube', 'fifthworldproblems', 'maybemaybemaybe', 'oddlyterrifying', 'streetfights', 'thatlookedexpensive', 'wellthatsucks', 'Whatthefuckgetitoffme', 'wtfgaragesale', 'wtfstockphotos', 'yesyesyesno', 'yesyesyesyesno']),
    ('Angering', ['Bad_Cop_No_Donut', 'casualchildabuse', 'crappydesign', 'fuckthesepeople', 'gifsthatendtoosoon', 'mildlyinfuriating', 'peoplebeingjerks', 'rage']),
    ('Edgy', ['imgoingtohellforthis', 'toosoon']),
    ('Judgy', ['13or30', 'awfuleverything', 'awfuleyebrows', 'ghettoglamourshots', 'hittablefaces', 'peopleofwalmart', 'punchablefaces', 'trashy']),
    ('Scary (potentially NSFL)', ['Glitch_in_the_Matrix', 'horror', 'lastimages', 'morbidreality', 'nononono', 'nosleep', 'Paranormal', 'peoplefuckingdying', 'serialkillers', 'shortscarystories', 'whatcouldgowrong', 'WhyWereTheyFilming', 'WinStupidPrizes']),
    ('Creepy', ['creepy', 'creepypasta', 'creepysigns', 'megalophobia']),
    ('Imaginary', ['imaginarycharacters', 'imaginarylandscapes', 'ImaginaryLeviathans', 'imaginarymaps', 'ImaginaryMindscapes', 'ImaginaryMonsters', 'SympatheticMonsters']),
    ('Water is scary', ['submechanophobia', 'thalassophobia', 'TheDepthsBelow']),
    ('Free Stuff', ['coupons', 'dealsreddit', 'efreebies', 'freebies', 'freeEbooks', 'freegamefindings', 'freegamesonsteam', 'fullmoviesonvimeo', 'fullmoviesonyoutube', 'googleplaydeals', 'megalinks', 'opendirectories', 'Random_Acts_Of_Pizza', 'randomactsofgaming']),
    ('For Men', ['askmen', 'bigdickproblems', 'everymanshouldknow', 'frugalmalefashion', 'malefashion', 'MaleFashionAdvice', 'malehairadvice', 'malelifestyle', 'malelivingspace', 'MensRights', 'mgtow', 'trollychromosome']),
    ('For Women', ['abrathatfits', 'askwomen', 'badwomensanatomy', 'femalefashionadvice', 'LadyBoners', 'TheGirlSurvivalGuide', 'TrollXChromosomes', 'TwoXChromosomes', 'xxfitness']),
    ('Geography', ['MapPorn', 'polandball', 'vexillology']),
    ('Africa', ['SouthAfrica']),
    ('Europe', ['austria', 'belgium', 'denmark', 'europe', 'ireland', 'italy', 'norge', 'polska', 'romania', 'scotland', 'suomi', 'thenetherlands']),
    ('France', ['france', 'french']),
    ('Germany', ['de', 'german', 'germany']),
    ('Russia', ['ANormalDayInRussia', 'youseecomrade']),
    ('Sweden', ['Allsvenskan', 'intresseklubben', 'spop', 'svenskpolitik', 'SWARJE', 'sweden', 'swedishproblems']),
    ('United Kingdom', ['britishproblems', 'casualuk', 'london', 'ukpolitics', 'unitedkingdom']),
    ('Canada', ['calgary', 'canada', 'canadapolitics', 'toronto', 'vancouver']),
    ('Mexico', ['mexico']),
    ('USA: United States of America', ['atlanta', 'boston', 'chicago', 'michigan', 'minnesota', 'MURICA', 'newjersey', 'nyc', 'philadelphia', 'portland', 'washingtondc']),
    ('California', ['bayarea', 'california', 'disneyland', 'losangeles', 'sandiego', 'sanfrancisco']),
    ('Colorado', ['colorado', 'denver']),
    ('Florida', ['floridaman', 'waltdisneyworld']),
    ('Texas', ['austin', 'dallas', 'houston', 'texas']),
    ('Washington', ['seattle', 'SeattleWA']),
    ('Oceania', ['australia', 'melbourne', 'newzealand', 'sydney']),
    ('Asia', ['china', 'hongkong', 'india', 'Philippines', 'singapore']),
    ('Japan', ['japan', 'japanpics', 'japantravel']),
    ('Korea', ['korea', 'kpop', 'pyongyang']),
    ('South America', ['argentina', 'brasil']),
    ('Meta', ['againsthatesubreddits', 'beetlejuicing', 'Enhancement', 'evenwithcontext', 'modnews', 'MuseumOfReddit', 'nocontext', 'OutOfTheLoop', 'redditinreddit', 'SecretSanta', 'theoryofreddit', 'threadkillers', 'tldr']),
    ('Administrative', ['announcements', 'beta', 'blog']),
    ('Apps', ['alienblue', 'apolloapp', 'baconit', 'baconreader', 'redditmobile', 'redditsync', 'relayforreddit']),
    ('Circlejerks', ['Circlejerk', 'DiWHY', 'frugal_jerk']),
    ('Drama', ['drama', 'hobbydrama', 'SubredditDrama']),
    ('Negative', ['jesuschristreddit', 'karmaconspiracy', 'karmacourt', 'ShitAmericansSay', 'ShitRedditSays', 'titlegore', 'undelete']),
    ('Positive', ['bestoflegaladvice', 'BestOfReports', 'DepthHub']),
    ('Subreddits', ['findareddit', 'newreddits', 'ofcoursethatsathing', 'subredditoftheday', 'wowthissubexists']),
    ('Subreddit Simulator', ['subredditsimmeta', 'subredditsimulator']),
    ('Looking for something', ['TipOfMyPenis', 'TipOfMyTongue']),
    ('Mind blowing', ['asmr', 'frisson', 'glitchinthematrix', 'VaporwaveAesthetics', 'woahdude']),
    ('Plants/Fungi', ['bonsai', 'marijuanaenthusiasts', 'mycology', 'succulents', 'TreesSuckingOnThings']),
    ('Violent Nature', ['Natureisbrutal', 'natureismetal', 'naturewasmetal']),
    ('Weather', ['tropicalweather', 'weathergifs']),
    ('News', ['energy', 'floridaman', 'gamernews', 'news', 'nottheonion', 'offbeat', 'syriancivilwar', 'truecrime', 'UpliftingNews', 'worldnews']),
    ('Fake News', ['AteTheOnion', 'TheOnion']),
    ('Politics', ['anarchism', 'communism', 'completeanarchy', 'conservative', 'geopolitics', 'Libertarian', 'neutralpolitics', 'politicaldiscussion', 'politicalhumor', 'Politics', 'socialism', 'ukpolitics', 'worldpolitics']),
    ('Capitalism', ['anarcho_capitalism', 'latestagecapitalism']),
    ('Gender Politics', ['feminism', 'MensRights']),
    ('Left', ['bidenbro', 'bluemidterm2018', 'democrats', 'esist', 'fuckthealtright', 'keep_track', 'liberal', 'political_revolution', 'SandersForPresident', 'thanksobama', 'The_Mueller']),
    ('Anti-Trump', ['enoughtrumpspam', 'impeach_trump', 'MarchAgainstTrump', 'TinyTrumps', 'TrumpCriticizesTrump', 'trumpgret']),
    ('Nostalgia/Time', ['forwardsfromgrandma', 'nostalgia', 'oldphotosinreallife', 'OldSchoolCool', 'TheWayWeWere', 'vinyl']),
    ('Parodies', ['AccidentalRenaissance', 'bollywoodrealism', 'coaxedintoasnafu', 'fakehistoryporn', 'firstworldanarchists', 'hailcorporate', 'im14andthisisdeep', 'irleastereggs', 'maliciouscompliance', 'montageparodies', 'OSHA', 'outside', 'unexpectedthuglife', 'wheredidthesodago', 'youdontsurf']),
    ('SFWPorn Network', ['sfwpornnetwork', 'AbandonedPorn', 'adporn', 'adrenalineporn', 'animalporn', 'ArchitecturePorn', 'artefactporn', 'ArtPorn', 'cabinporn', 'carporn', 'CityPorn', 'DesignPorn', 'destructionporn', 'EarthPorn', 'ExposurePorn', 'FoodPorn', 'futureporn', 'gunporn', 'HistoryPorn', 'houseporn', 'humanporn', 'illusionporn', 'InfrastructurePorn', 'JusticePorn', 'machineporn', 'macroporn', 'MapPorn', 'microporn', 'militaryporn', 'mineralporn', 'movieposterporn', 'penmanshipporn', 'powerwashingporn', 'productporn', 'QuotesPorn', 'RoomPorn', 'shockwaveporn', 'skyporn', 'SpacePorn', 'ThingsCutInHalfPorn', 'VillagePorn', 'waterporn']),
    ('Shitty', ['crappydesign', 'shitpost', 'Shitty_Car_Mods', 'shittyadvice', 'shittyanimalfacts', 'shittyaskscience', 'shittyfoodporn', 'shittykickstarters', 'ShittyLifeProTips', 'shittymoviedetails', 'shittyreactiongifs', 'shittyrobots']),
    ('Unexpected', ['blackmagicfuckery', 'misleadingthumbnails', 'slygifs', 'unexpected', 'unexpectedhogwarts', 'unexpectedjihad', 'UnexpectedMulaney', 'UnexpectedThugLife']),
    ('Visually Appealing', ['AbandonedPorn', 'AccidentalWesAnderson', 'AmateurRoomPorn', 'breathinginformation', 'Cinemagraphs', 'CityPorn', 'cozyplaces', 'DesignPorn', 'desirepath', 'eyebleach', 'handwriting', 'humansbeingbros', 'ImaginaryLandscapes', 'minimalism', 'mostbeautiful', 'nevertellmetheodds', 'nonononoyes', 'OddlySatisfying', 'penmanshipporn', 'perfectfit', 'perfectloops', 'powerwashingporn', 'raining', 'RoomPorn', 'slygifs', 'thatpeelingfeeling', 'tiltshift', 'typography', 'unstirredpaint']),
    ('Hold My ____', ['holdmybeaker', 'holdmybeer', 'holdmycatnip', 'holdmycosmo', 'holdmyfeedingtube', 'holdmyfries', 'holdmyjuicebox', 'holdmyredbull']),
    ('Weird Feelings/Categorize Later', ['2healthbars', 'AskReddit', 'BestOfStreamingVideo', 'bitchimabus', 'bizarrebuildings', 'boop', 'CatastrophicFailure', 'collapse', 'confusing_perspective', 'dashcamgifs', 'dontputyourdickinthat', 'drunkorakid', 'evilbuildings', 'ExpandDong', 'fifthworldpics', 'fiftyfifty', 'firstworldproblems', 'FullScorpion', 'greendawn', 'hadtohurt', 'halloween', 'happycryingdads', 'hmmm', 'hmmmgifs', 'idiotsfightingthings', 'idiotsincars', 'inclusiveor', 'instantkarma', 'instantregret', 'Justfuckmyshitup', 'justiceserved', 'kurzgesagt', 'lostgeneration', 'MandelaEffect', 'mildlypenis', 'MildlyVandalised', 'mypeopleneedme', 'nextfuckinglevel', 'notinteresting', 'notmyjob', 'okbuddyretard', 'onejob', 'ooer', 'pussypassdenied', 'redditdayof', 'slavs_squatting', 'sweatypalms', 'tendies', 'the_pack', 'therewasanattempt', 'thingsforants', 'tworedditorsonecup', 'UNBGBBIIVCHIDCTIICBG', 'unpopularopinion', 'urbanhell', 'wackytictacs', 'watchpeoplesurvive', 'whatcouldgoright', 'whatintarnation', 'whatsinthisthing', 'youseeingthisshit']),
    ('Ex 50k+', ['battlefield3', 'csgobetting', 'historicalwhatif', 'mindcrack', 'punchablefaces', 'twitchplayspokemon']),
]

SUBREDDITS = OrderedDict(SUBREDDIT_INFO)

assert len(SUBREDDIT_INFO) == len(SUBREDDITS)
