from application import db, Subreddit


# The top 1000 subreddits by subscriber count
SUBREDDITS = [
    'announcements',
    'funny',
    'AskReddit',
    'gaming',
    'pics',
    'science',
    'worldnews',
    'todayilearned',
    'aww',
    'movies',
    'videos',
    'Music',
    'IAmA',
    'gifs',
    'news',
    'EarthPorn',
    'askscience',
    'Showerthoughts',
    'blog',
    'explainlikeimfive',
    'books',
    'Jokes',
    'mildlyinteresting',
    'LifeProTips',
    'DIY',
    'food',
    'television',
    'sports',
    'space',
    'Art',
    'gadgets',
    'nottheonion',
    'photoshopbattles',
    'Documentaries',
    'listentothis',
    'GetMotivated',
    'UpliftingNews',
    'tifu',
    'InternetIsBeautiful',
    'history',
    'Futurology',
    'OldSchoolCool',
    'philosophy',
    'personalfinance',
    'dataisbeautiful',
    'WritingPrompts',
    'nosleep',
    'creepy',
    'TwoXChromosomes',
    'technology',
    'Fitness',
    'AdviceAnimals',
    'WTF',
    'bestof',
    'politics',
    'memes',
    'wholesomememes',
    'interestingasfuck',
    'BlackPeopleTwitter',
    'oddlysatisfying',
    'leagueoflegends',
    'lifehacks',
    'travel',
    'woahdude',
    'pcmasterrace',
    'facepalm',
    'atheism',
    'relationships',
    'me_irl',
    'reactiongifs',
    'nba',
    'dankmemes',
    'Overwatch',
    'PS4',
    'Tinder',
    'NatureIsFuckingLit',
    'AnimalsBeingBros',
    'AnimalsBeingJerks',
    'tattoos',
    'europe',
    'Whatcouldgowrong',
    'malefashionadvice',
    'FoodPorn',
    'programming',
    'Unexpected',
    'gameofthrones',
    'trippinthroughtime',
    'hiphopheads',
    'BikiniBottomTwitter',
    'boardgames',
    'pokemongo',
    'Games',
    'instant_regret',
    'Android',
    'gardening',
    'loseit',
    'dadjokes',
    'mildlyinfuriating',
    'Damnthatsinteresting',
    'CrappyDesign',
    'itookapicture',
    'iphone',
    'PewdiepieSubmissions',
    'photography',
    'pokemon',
    'GifRecipes',
    'relationship_advice',
    'buildapc',
    'soccer',
    'nonononoyes',
    'rarepuppers',
    'Wellthatsucks',
    'slowcooking',
    'BeAmazed',
    'humor',
    'Eyebleach',
    'trees',
    'HistoryPorn',
    'BetterEveryLoop',
    'woodworking',
    'HighQualityGifs',
    'ContagiousLaughter',
    'xboxone',
    'AnimalsBeingDerps',
    'offmychest',
    'keto',
    'OutOfTheLoop',
    'trashy',
    'Roadcam',
    'RoastMe',
    'pcgaming',
    'nfl',
    'drawing',
    'cars',
    'confession',
    'NetflixBestOf',
    'MakeupAddiction',
    'cats',
    'sex',
    'ChildrenFallingOver',
    'raspberry_pi',
    'backpacking',
    'EatCheapAndHealthy',
    'HumansBeingBros',
    'ChoosingBeggars',
    'Cooking',
    'hmmm',
    'MadeMeSmile',
    'comics',
    'NintendoSwitch',
    'frugalmalefashion',
    'blackmagicfuckery',
    'WhitePeopleTwitter',
    'rickandmorty',
    'teenagers',
    'Minecraft',
    'quityourbullshit',
    'insanepeoplefacebook',
    'ArtisanVideos',
    'nevertellmetheodds',
    'recipes',
    'biology',
    'Frugal',
    'cringepics',
    'wheredidthesodago',
    'FortNiteBR',
    'AskMen',
    'StarWars',
    'MurderedByWords',
    'nintendo',
    'Bitcoin',
    '4chan',
    'scifi',
    'DnD',
    'mac',
    'streetwear',
    'MovieDetails',
    'manga',
    'FiftyFifty',
    'Parenting',
    'MealPrepSunday',
    'WatchPeopleDieInside',
    'NoStupidQuestions',
    'wow',
    'hearthstone',
    'whatisthisthing',
    'youseeingthisshit',
    'howto',
    'bodyweightfitness',
    'therewasanattempt',
    'reallifedoodles',
    'iamverysmart',
    'youtubehaiku',
    'DunderMifflin',
    'battlestations',
    'PeopleFuckingDying',
    'assholedesign',
    'anime',
    'YouShouldKnow',
    'apple',
    'holdmybeer',
    'cringe',
    'learnprogramming',
    'AskHistorians',
    'MemeEconomy',
    'thatHappened',
    'SkincareAddiction',
    'PrequelMemes',
    'dogs',
    'educationalgifs',
    'thewalkingdead',
    'natureismetal',
    'electronicmusic',
    'madlads',
    'baseball',
    'DestinyTheGame',
    'Awwducational',
    'AskWomen',
    'KidsAreFuckingStupid',
    'starterpacks',
    'PublicFreakout',
    'entertainment',
    'camping',
    'CollegeBasketball',
    'RoomPorn',
    'CryptoCurrency',
    'niceguys',
    'socialskills',
    'IdiotsInCars',
    'TrollYChromosome',
    'comicbooks',
    'conspiracy',
    'GlobalOffensive',
    'PerfectTiming',
    'fffffffuuuuuuuuuuuu',
    'wallpaper',
    'OopsDidntMeanTo',
    'urbanexploration',
    'oldpeoplefacebook',
    'horror',
    'ATBGE',
    'legaladvice',
    'yesyesyesyesno',
    'ProgrammerHumor',
    'reddit.com',
    'GamePhysics',
    'likeus',
    'nononono',
    'PUBATTLEGROUNDS',
    'shittyfoodporn',
    'savedyouaclick',
    'shittyaskscience',
    'femalefashionadvice',
    'zelda',
    'greentext',
    'UnethicalLifeProTips',
    'math',
    'Outdoors',
    'JapanTravel',
    'AbandonedPorn',
    'JusticeServed',
    'CozyPlaces',
    'iamverybadass',
    'Astronomy',
    'apexlegends',
    'TrollXChromosomes',
    'holdmycosmo',
    'MaliciousCompliance',
    'MMA',
    'foodhacks',
    'writing',
    'The_Donald',
    'dating_advice',
    '2meirl4meirl',
    'hockey',
    'JUSTNOMIL',
    'CatastrophicFailure',
    'changemyview',
    'Physics',
    'worldpolitics',
    'Sneakers',
    'marvelstudios',
    'DeepIntoYouTube',
    'CampingandHiking',
    'progresspics',
    'investing',
    'HistoryMemes',
    'tipofmytongue',
    'DeepFriedMemes',
    'Design',
    'WhyWereTheyFilming',
    'breakingbad',
    'Perfectfit',
    'ProRevenge',
    'hacking',
    'AmItheAsshole',
    'nostalgia',
    'carporn',
    'UnresolvedMysteries',
    'PoliticalHumor',
    'motorcycles',
    'DesignPorn',
    'meirl',
    'confusing_perspective',
    'spaceporn',
    'Bossfight',
    'indieheads',
    'powerwashingporn',
    'hardware',
    'MapPorn',
    'Cinemagraphs',
    'freebies',
    'DiWHY',
    'WeAreTheMusicMakers',
    'fakehistoryporn',
    'HomeImprovement',
    'westworld',
    'dank_meme',
    'crafts',
    'Rainbow6',
    'MachineLearning',
    'ThriftStoreHauls',
    'skyrim',
    'thanosdidnothingwrong',
    'coolguides',
    'GameDeals',
    'running',
    'smashbros',
    'southpark',
    'Economics',
    'dankchristianmemes',
    'ShittyLifeProTips',
    'harrypotter',
    'bodybuilding',
    'ANormalDayInRussia',
    'SweatyPalms',
    'podcasts',
    'OSHA',
    'thisismylifenow',
    'pettyrevenge',
    'WhatsWrongWithYourDog',
    'Justrolledintotheshop',
    'ComedyCemetery',
    'Steam',
    'CasualConversation',
    'whitepeoplegifs',
    'JusticePorn',
    'astrophotography',
    'softwaregore',
    'google',
    'talesfromtechsupport',
    'gatekeeping',
    'UNBGBBIIVCHIDCTIICBG',
    'IdiotsFightingThings',
    'Filmmakers',
    'PoliticalDiscussion',
    'futurama',
    'DoesAnybodyElse',
    'BuyItForLife',
    'CFB',
    'hiking',
    'Fallout',
    'javascript',
    'Health',
    'cursedimages',
    'chemistry',
    'Justfuckmyshitup',
    'freefolk',
    'rpg',
    'boottoobig',
    'ExpectationVsReality',
    'ofcoursethatsathing',
    'financialindependence',
    'Watches',
    'gifsthatkeepongiving',
    'geek',
    'Metal',
    'homestead',
    'Fantasy',
    'justneckbeardthings',
    'blunderyears',
    'environment',
    'AccidentalRenaissance',
    'woooosh',
    'formula1',
    'TooAfraidToAsk',
    'ArtefactPorn',
    'wallstreetbets',
    'BoneAppleTea',
    'FanTheories',
    'creepyPMs',
    'FellowKids',
    'FunnyandSad',
    'tumblr',
    'Graffiti',
    'beta',
    'TalesFromRetail',
    'DotA2',
    'Entrepreneur',
    'solotravel',
    'StartledCats',
    'nasa',
    'redditgetsdrawn',
    'self',
    'Drugs',
    'combinedgifs',
    'LetsNotMeet',
    'PornhubComments',
    'gentlemanboners',
    'entitledparents',
    'Shitty_Car_Mods',
    'KerbalSpaceProgram',
    'Marvel',
    'wallpapers',
    'crappyoffbrands',
    'buildapcsales',
    'techsupport',
    'firstworldanarchists',
    'childfree',
    'shittyrobots',
    'RocketLeague',
    'blackpeoplegifs',
    'compsci',
    'EDM',
    'iamatotalpieceofshit',
    'chemicalreactiongifs',
    'somethingimade',
    'unpopularopinion',
    'asoiaf',
    'holdmyredbull',
    'LearnUselessTalents',
    'Survival',
    'sadcringe',
    'nbastreams',
    'mechanical_gifs',
    'canada',
    'LivestreamFail',
    'evilbuildings',
    'im14andthisisdeep',
    'wiiu',
    'KenM',
    'NotMyJob',
    'PenmanshipPorn',
    'ScottishPeopleTwitter',
    'ExposurePorn',
    'specializedtools',
    'surrealmemes',
    'SubredditDrama',
    'depression',
    'classicalmusic',
    'business',
    'polandball',
    'FloridaMan',
    'confessions',
    'WeWantPlates',
    'dogswithjobs',
    'forbiddensnacks',
    'TumblrInAction',
    'reddeadredemption',
    'IASIP',
    'Twitch',
    'calvinandhobbes',
    'audiophile',
    'instantkarma',
    'psychology',
    'Animemes',
    'MachinePorn',
    'truegaming',
    'thalassophobia',
    'AsianBeauty',
    'IDontWorkHereLady',
    'AskOuija',
    'Nicegirls',
    'indianpeoplefacebook',
    'CrazyIdeas',
    'AnimalTextGifs',
    'antiMLM',
    'Guitar',
    'technicallythetruth',
    'dontdeadopeninside',
    'guns',
    'babyelephantgifs',
    'teslamotors',
    'MostBeautiful',
    'bicycling',
    'disneyvacation',
    'perfectloops',
    'CityPorn',
    '4PanelCringe',
    'offbeat',
    'photocritique',
    'analog',
    'nflstreams',
    'ethereum',
    'lego',
    'TrueReddit',
    'theydidthemath',
    'Zoomies',
    'StoppedWorking',
    'suggestmeabook',
    'IWantToLearn',
    'Prematurecelebration',
    'privacy',
    'woof_irl',
    'nutrition',
    'NoFap',
    'QuotesPorn',
    'FreeEBOOKS',
    'Homebrewing',
    'getdisciplined',
    'PandR',
    '3DS',
    'TheSilphRoad',
    'misleadingthumbnails',
    'holdmyfries',
    'digitalnomad',
    'DadReflexes',
    'CatsStandingUp',
    'Celebs',
    'standupshots',
    'terriblefacebookmemes',
    'AbsoluteUnits',
    'olympics',
    'LateStageCapitalism',
    'holdmyjuicebox',
    'IWantOut',
    'h3h3productions',
    'yesyesyesno',
    'vandwellers',
    'ADHD',
    'aviation',
    'snowboarding',
    'INEEEEDIT',
    'SquaredCircle',
    'fantasyfootball',
    'jailbreak',
    'Simulated',
    'raisedbynarcissists',
    'mealtimevideos',
    'ketorecipes',
    'corgi',
    'rage',
    'bonehurtingjuice',
    'climbing',
    'worldbuilding',
    'ShouldIbuythisgame',
    'cosplaygirls',
    'linux',
    'Poetry',
    'web_design',
    'tippytaps',
    'anime_irl',
    'Screenwriting',
    'Pareidolia',
    'skiing',
    'Piracy',
    'Boxing',
    'SuddenlyGay',
    'MechanicalKeyboards',
    'beer',
    'kpop',
    'HealthyFood',
    'shittyreactiongifs',
    'ActLikeYouBelong',
    'AccidentalRacism',
    'netflix',
    'youdontsurf',
    'delusionalartists',
    'Meditation',
    'malelivingspace',
    'doctorwho',
    'copypasta',
    'EmpireDidNothingWrong',
    'Python',
    'howtonotgiveafuck',
    'Cyberpunk',
    'creepyasterisks',
    'Fishing',
    'minimalism',
    'bestoflegaladvice',
    'circlejerk',
    '2007scape',
    'vagabond',
    'Breath_of_the_Wild',
    'stocks',
    'StrangerThings',
    'jesuschristreddit',
    'vinyl',
    'EngineeringPorn',
    'Glitch_in_the_Matrix',
    'spacex',
    'happy',
    'xxfitness',
    'AMA',
    'totallynotrobots',
    'techsupportgore',
    'absolutelynotme_irl',
    'brooklynninenine',
    'hitmanimals',
    'startups',
    'sysadmin',
    'homeautomation',
    'TheLastAirbender',
    'gamedev',
    'Autos',
    'theocho',
    'webdev',
    'comedyheaven',
    'goddesses',
    'britishproblems',
    'seduction',
    'graphic_design',
    'vegan',
    'TheDepthsBelow',
    'FORTnITE',
    'beermoney',
    'SubredditSimulator',
    'magicTCG',
    'ThingsCutInHalfPorn',
    '2healthbars',
    'CasualUK',
    'MyPeopleNeedMe',
    'australia',
    'Memes_Of_The_Dank',
    'productivity',
    'notinteresting',
    'nocontext',
    'StardewValley',
    'lgbt',
    'Warframe',
    'TheWayWeWere',
    'DecidingToBeBetter',
    'Paranormal',
    'netsec',
    'JoeRogan',
    'ClashRoyale',
    '3Dprinting',
    'ArtPorn',
    'Libertarian',
    'Blackops4',
    'Badfaketexts',
    'AccidentalWesAnderson',
    'findareddit',
    'MURICA',
    'familyguy',
    'ihavesex',
    'beetlejuicing',
    'IsItBullshit',
    'RetroFuturism',
    'suicidebywords',
    'lotr',
    'witcher',
    '1200isplenty',
    'AteTheOnion',
    'rareinsults',
    'thedivision',
    'TrueOffMyChest',
    'outrun',
    'BrandNewSentence',
    'intermittentfasting',
    'civ',
    'patientgamers',
    'sbubby',
    'puns',
    'youtube',
    'MonsterHunter',
    'HadToHurt',
    'PraiseTheCameraMan',
    'trebuchetmemes',
    'shortscarystories',
    'pussypassdenied',
    'cordcutters',
    'TooMeIrlForMeIrl',
    'CombatFootage',
    'NeutralPolitics',
    'AmateurRoomPorn',
    'Instagramreality',
    'wholesomebpt',
    'okbuddyretard',
    'france',
    'cosplay',
    'OnePiece',
    'drunk',
    'BokuNoHeroAcademia',
    'toptalent',
    'TalesFromYourServer',
    'TheSimpsons',
    'noisygifs',
    'Foodforthought',
    'ArchitecturePorn',
    'knitting',
    'fatlogic',
    'NASCAR',
    'edmproduction',
    'engrish',
    'tf2',
    'fo4',
    'raining',
    'PropagandaPosters',
    'hardcoreaww',
    'forwardsfromgrandma',
    'WatchandLearn',
    'holdmyfeedingtube',
    'wikipedia',
    'Baking',
    'fullmoviesonyoutube',
    'btc',
    'VaporwaveAesthetics',
    'whowouldwin',
    'Superbowl',
    'dogpictures',
    'thenetherlands',
    'Kanye',
    'TrumpCriticizesTrump',
    'vexillology',
    'Anxiety',
    'rupaulsdragrace',
    'Coffee',
    'lewronggeneration',
    'pathofexile',
    'nextfuckinglevel',
    'mallninjashit',
    'Advice',
    'MEOW_IRL',
    'SandersForPresident',
    'apolloapp',
    'gainit',
    'lastimages',
    'BoJackHorseman',
    'JonWinsTheThrone',
    'halo',
    'lotrmemes',
    'tennis',
    'behindthegifs',
    'sweden',
    'darksouls3',
    'unitedkingdom',
    'finance',
    'blackmirror',
    'TIHI',
    'PrettyGirls',
    'holdmycatnip',
    'gamernews',
    'LucidDreaming',
    'Cringetopia',
    'fightporn',
    'absolutelynotmeirl',
    'MilitaryPorn',
    'batman',
    'LSD',
    'BeforeNAfterAdoption',
    'destiny2',
    'ImaginaryLandscapes',
    'maybemaybemaybe',
    'brasil',
    'community',
    'cscareerquestions',
    'SequelMemes',
    'UnsentLetters',
    'ffxiv',
    'IncelTears',
    'badwomensanatomy',
    'discordapp',
    'Naruto',
    'medicine',
    'tech',
    'r4r',
    'watchpeoplesurvive',
    'wholesomegifs',
    'HumanPorn',
    'meme',
    'Patriots',
    'starcraft',
    'LadyBoners',
    'DCcomics',
    'engineering',
    'needadvice',
    'gifsthatendtoosoon',
    'AccidentalComedy',
    'jobs',
    'arresteddevelopment',
    'FIFA',
    'headphones',
    'vaxxhappened',
    'roosterteeth',
    'SCP',
    'ArcherFX',
    'Blep',
    'NoMansSkyTheGame',
    'FashionReps',
    'UrbanHell',
    'AntiJokes',
    'StockMarket',
    'forhonor',
    'ihadastroke',
    'darksouls',
    'MensRights',
    'wtfstockphotos',
    'KeanuBeingAwesome',
    'askwomenadvice',
    'Celebhub',
    'AutoDetailing',
    'adventuretime',
    'dbz',
    'birdswitharms',
    'mildlypenis',
    'Amd',
    'creepypasta',
    'MechanicAdvice',
    'Diablo',
    'firstworldproblems',
    'TalesFromTheFrontDesk',
    'ethtrader',
    'Conservative',
    'NHLStreams',
    'GrandTheftAutoV',
    'ImaginaryMonsters',
    'MonsterHunterWorld',
    'yoga',
    'restofthefuckingowl',
    'AskCulinary',
    'ireland',
    'DnDBehindTheScreen',
    'Philippines',
    'cursedcomments',
    'awwwtf',
    'CitiesSkylines',
    '3amjokes',
    'EDC',
    'heroesofthestorm',
    'Sneks',
    'Psychonaut',
    'Guildwars2',
    'fakealbumcovers',
    'litecoin',
    'Moviesinthemaking',
    'india',
    'Competitiveoverwatch',
    'webcomics',
    'Ripple',
    'CatTaps',
    'gif',
    'DnDGreentext',
    'summonerschool',
    'succulents',
    'Aquariums',
    'TopGear',
    'TheMonkeysPaw',
    'keming',
    'gamegrumps',
    'MasterReturns',
    'awfuleverything',
    'DungeonsAndDragons',
    'skateboarding',
    'donthelpjustfilm',
    'facebookwins',
    'smallbusiness',
    'bertstrips',
    'PixelArt',
    'AnthemTheGame',
    'startrek',
    'lostredditors',
    'elderscrollsonline',
    'popping',
    'AnimalCrossing',
    'wowthissubexists',
    'curlyhair',
    'fitmeals',
    'gundeals',
    'wowthanksimcured',
    'dashcamgifs',
    'TalesFromTheCustomer',
    'quotes',
    'asianpeoplegifs',
    'EngineeringStudents',
    'dndnext',
    'battlefield_one',
    'perfectlycutscreams',
    'learnpython',
    'Bad_Cop_No_Donut',
    'ukpolitics',
    'Christianity',
    'ufc',
    'selfimprovement',
    'socialism',
    'golf',
    'Gamingcirclejerk',
    'TrueAskReddit',
    'dontputyourdickinthat',
    'architecture',
    'Frisson',
    'Catloaf',
    'sequence',
    'fo76',
    'Warhammer40k',
    'PartyParrot',
    'languagelearning',
    'povertyfinance',
    'asmr',
    'musictheory',
    'shockwaveporn',
    'CryptoMarkets',
    'HitBoxPorn',
    'gtaonline',
    'Terraria',
    'Military',
    'happycryingdads',
    'techsupportmacgyver',
    'itsaunixsystem',
    'seriouseats',
    'ElderScrolls',
    'realasians',
    'Nootropics',
    'Battlefield',
    'The_Mueller',
    'marketing',
    'StonerEngineering',
    'newzealand',
    'fasting',
    'Idubbbz',
    'brushybrushy',
    'IllegalLifeProTips',
    'badtattoos',
    'homelab',
    'happycowgifs',
    'submechanophobia',
    'BreadStapledToTrees',
    'nyc',
    'classic4chan',
    'Thisismylifemeow',
    'de',
    'Buddhism',
    'stevenuniverse',
    'cableporn',
    'electronic_cigarette',
    'assassinscreed',
    'weightroom',
    'london',
    'beards',
    'TopMindsOfReddit',
    'PUBG',
    'churning',
    'thingsforants',
    'masseffect',
    'marijuanaenthusiasts',
    'StarWarsBattlefront',
    'Breadit',
    'TrueFilm',
    'runescape',
    'YouSeeComrade',
    'coaxedintoasnafu',
    'InteriorDesign',
    'weed',
    'gaybros',
    'college',
    'japan',
    'pyrocynical',
    'funhaus',
    'casualiama',
    'ketogains',
    'Anticonsumption',
    'HailCorporate',
    'warriors',
    'trashpandas',
    'Borderlands',
    'MMAStreams',
    'stopdrinking',
    'WouldYouRather',
    'happycrowds',
    'singapore',
    'MLBStreams',
    'OverwatchUniversity',
    'splatoon',
    'CODZombies',
    'networking',
    'SmashBrosUltimate',
    'answers',
    'KitchenConfidential',
    'teefies',
    'socialanxiety',
    'KarmaCourt',
    'thegrandtour',
    'NBA2k',
    'GamersRiseUp',
    'veganrecipes',
    'unixporn',
    'StreetFights',
    'coloringcorruptions',
    'oddlyterrifying',
    'blessedimages',
    'Windows10',
    'LearnJapanese',
    'HowToHack',
    'IndieGaming',
    'rimjob_steve',
    'disney',
    'ClashOfClans',
    'smoobypost',
    'Monero',
    'TheGirlSurvivalGuide',
]


def insert_subreddits():
    for name in SUBREDDITS:
        db.session.add(Subreddit(name=name))
    db.session.commit()
